'''Copyright 2018 KNet Solutions, India, http://knetsolutions.in

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''

from __future__ import unicode_literals
import sys
import abc
import os
from six import add_metaclass, text_type
import json
import jsonschema
from jsonschema import validate
from shutil import copyfile

from KNet.lib.node import Node
from KNet.lib.router import Router

from KNet.lib.switches import Switch
from KNet.lib.link import NodeLink, SwitchLink, RouterLink
from KNet.lib.networks import Network
from KNet.lib.qos import Qos
import KNet.lib.schema
from KNet.lib.utils import Singleton
import KNet.lib.utils as utils
import KNet.lib.ovs_cmds as ovs
from KNet.lib.logger import logger as log
from KNet.lib.schema import Topology_schema as schema
import KNet.lib.docker_cmds as docker

UI_DATAFILE = "/tmp/data.js"
VERSION = "1.0.5"


@add_metaclass(abc.ABCMeta)
class Topology(Singleton, object):

    def __init__(self):
        self.initialize()

    def initialize(self):
        self.name = None
        self.status = None
        self.controller = None
        self.nodeobjs = []
        self.switchobjs = []
        self.linkobjs = []
        self.networkobjs = []
        self.routerobjs = []
        self.qos = None
        log.debug("Initializing Topology Object")

    def create(self, tdata):
        log.debug("Topology Create called with Data" + str(tdata))
        if self.status:
            res = "Already Topology is running, we cannot create another one"
            log.warn(res)
            return res

        if not self.__validate(tdata):
            log.error("Topology data schmea validation check failed")
            return {"Error": "Invalid Topology Schema Check Data"}

        # create network
        self.name = tdata["Topology"]["name"]
        self.controller = tdata["Topology"]["controller"]["url"]

        # check network object is present in the topology input
        if "networks" in tdata["Topology"]:
            log.debug("Topology Creating Networks")
            for net in tdata["Topology"]["networks"]:
                networkobj = Network(net)
                self.networkobjs.append(networkobj)

        # qos - doesnt require objects. we need to just pass this
        # complete dict to Linkobj.
        if "qos" in tdata["Topology"]:
            self.qos = tdata["Topology"]["qos"]

        # create nodes
        log.debug("Topology Creating Nodes")
        for n in tdata["Topology"]["nodes"]:
            # get the network object for the node
            net = None
            if "network" in n:
                net = self.__getnetwork(n["network"])
            nodeobj = Node(data=n, network=net)
            nodeobj.create()
            self.nodeobjs.append(nodeobj)

        # Create switches
        log.debug("Topology Creating Switches")
        for s in tdata["Topology"]["switches"]:
            # Take details from global openflow json
            if "openflow" not in s:
                s["openflow"] = tdata["Topology"]["openflow"]
            sobj = Switch(data=s, controller=self.controller)
            sobj.create()
            self.switchobjs.append(sobj)

        if "routers" in tdata["Topology"]:
            # create routers
            log.debug("Topology Creating Routers")
            for n in tdata["Topology"]["routers"]:
                routerobj = Router(data=n)
                routerobj.create()
                self.routerobjs.append(routerobj)

        # create links
        log.debug("Topology Creating Links")
        for l in tdata["Topology"]["links"]:
            # creating nodeLinks
            if "nodes" in l:
                lobj = NodeLink(data=l, qos=self.qos)
            elif "routers" in l:
                lobj = RouterLink(data=l, qos=self.qos)
            else:
                # creating Switch Links
                lobj = SwitchLink(data=l)
            lobj.create()
            self.linkobjs.append(lobj)

        # Adding Static Routes in the hosts
        for n in tdata["Topology"]["nodes"]:
            if "static_routes" in n:
                for route in n["static_routes"]:
                    docker.add_static_route(n["name"], route["subnet"],
                                            route["via"])

        # Adding Static Routes in the routers
        if "routers" in tdata["Topology"]:
            for r in tdata["Topology"]["routers"]:
                if "static_routes" in r:
                    for route in r["static_routes"]:
                        docker.add_static_route(r["name"], route["subnet"],
                                                route["via"])

        self.status = "Created"

        log.debug("Topology Creation Completed")

        # Todo - Store Network, Qos in DB??

        # write the topology data for UI
        self.__write_ui_data()
        log.debug("Topology details updated in data.js for UI")

        # return the topology data(for CLI)
        res = utils.format_createtopo({"Name": self.name,
                                       "Status": self.status,
                                       "Controller": self.controller,
                                       "Nodes": self.__getNodeNames(),
                                       "Switches": self.__getSwitchNames(),
                                       "Links": self.__getLinks()})
        log.debug(res)
        return res

    def delete(self):
        if not self.status:
            log.warn("No Topology Exists for delete")
            return "No Topology Exists "

        log.debug("Deleting nodes")
        for n in self.nodeobjs:
            n.delete()
        del self.nodeobjs[:]

        log.debug("Deleting switches")
        for s in self.switchobjs:
            s.delete()
        del self.switchobjs[:]

        log.debug("Deleting Routers")
        for r in self.routerobjs:
            r.delete()
        del self.routerobjs[:]

        log.debug("Deleting Links")
        del self.linkobjs[:]

        log.debug("Deleting Networks")
        del self.networkobjs[:]

        log.debug("Cleaning DB")
        utils.purge_db()
        # reinitializing the instance variable
        self.initialize()
        # resetting the id generator(start from 0)
        utils.reset_id()
        # removing the UI data file
        self.__delete_ui_data()
        res = "****--------- Topology Deleted---------****"
        log.debug(res)
        return res

    def get(self):
        if not self.status:
            log.warn("No Topology Exists")
            return "No Topology Exists "

        topo = utils.format_topo({"Name": self.name,
                                  "Status": self.status,
                                  "Controller": self.controller})
        nodes = utils.format_nodes(self.__getNodeDetails())
        switches = utils.format_switches(self.__getSwitchDetails())
        routers = utils.format_nodes(self.__getRouterDetails())
        links = utils.format_links(utils.link_t.all())
        result = "Topology \n" + str(topo) + "\n"
        result += "Nodes \n" + str(nodes) + "\n"
        result += "Switches \n" + str(switches) + "\n"
        result += "Routers \n" + str(routers) + "\n"
        result += "Links \n" + str(links) + "\n"
        log.debug(result)
        return result

    def deleteNode(self, name):
        obj = self.__getNodebyName(name)
        if obj:
            obj.delete()
            return "Node deleted"
        else:
            return "Node not found"

    def deleteSwitch(self, name):
        obj = self.__getSwitchbyName(name)
        if obj:
            obj.delete()
            return "Switch deleted"
        else:
            return "Switch not found"

    # hack - short way - to be handled by node module
    def adminDownLink(self, ifname):
        ovs.admindown_link(ifname)

    def adminUpLink(self, ifname):
        ovs.adminup_link(ifname)

    def ping(self, src, dst):
        snode = self.__getNodebyName(src)
        dnode = self.__getNodebyName(dst)
        if snode is not None and dnode is not None:
            print "Ping from node " + snode.name + " to " + dnode.name
            print docker.run_ping_in_container(snode.name,
                                               dnode.ip.split('/')[0])
            print "---------------------------------------------------"
        else:
            print "Node not found"

    def pingAll(self):
        for snode in self.nodeobjs:
            for dnode in self.nodeobjs:
                if snode.id != dnode.id:
                    print "Ping from node " + snode.name + " to " + dnode.name
                    print docker.run_ping_in_container(snode.name,
                                                       dnode.ip.split('/')[0])       
                    print "---------------------------------------------------"

    def version(self):
        return VERSION

    def cleanup(self):
        cpath = os.path.dirname(os.path.abspath(__file__)) + "/cleanup.sh"
        cmd = ['sh', cpath]
        return utils.run_cmd(cmd)

    def tcptest(self, srcnode, destnode, connections):
        # Run tcp server in destnode
        docker.run_iperfs_in_container(destnode)

        # Run tcp client in srcnode
        serverip = self.__get_node_ip(destnode)
        docker.run_iperfc_in_container(srcnode, serverip, connections)

        # iperf client process automatically exits, so no need to kill
        # kill iperf server proecess in destnode
        docker.run_pkill_in_container(destnode, "iperf")

    def udptest(self, srcnode, destnode, bandwidth, connections):
        # Run tcp server in destnode
        docker.run_iperf_udps_in_container(destnode)

        # Run tcp client in srcnode
        serverip = self.__get_node_ip(destnode)
        docker.run_iperf_udpc_in_container(srcnode, serverip, bandwidth, connections)

        # iperf client process automatically exits, so no need to kill
        # kill iperf server proecess in destnode
        docker.run_pkill_in_container(destnode, "iperf")


    # private functions
    def __write_ui_data(self):
        topologyData = {}
        nodes = []
        links = []

        for node in self.nodeobjs:
            nodes.append({"id": node.id, "name": node.name, "icon": "host"})
        for switch in self.switchobjs:
            nodes.append({"id": switch.id, "name": switch.name, "icon": "switch"})
        for router in self.routerobjs:
            nodes.append({"id": router.id, "name": router.name, "icon": "router"})           
        for linkobj in self.linkobjs:
            for link in linkobj.links:
                links.append(link)
        topologyData["nodes"] = nodes
        topologyData["links"] = links
        # print topologyData
        with open(UI_DATAFILE, 'w') as outfile:
            hdr = "var topologyData ="
            outfile.write(hdr)
            json.dump(topologyData, outfile)

    def __delete_ui_data(self):
        topologyData = {}
        nodes = []
        links = []
        topologyData["nodes"] = nodes
        topologyData["links"] = links
        with open(UI_DATAFILE, 'w') as outfile:
            hdr = "var topologyData ="
            outfile.write(hdr)
            json.dump(topologyData, outfile)

    def __validate(self, data):
        try:
            validate(data, schema)
        except jsonschema.ValidationError as e:
            log.error("json schema validation error %s", e.message)
            return False
        except jsonschema.SchemaError as e:
            log.error("json schema error %s", e.message)
            return False
        return True

    def __getnetwork(self, netname):
        for net in self.networkobjs:
            if net.name == netname:
                return net
        return None

    def __getqos(self, qosname):
        for qos in self.qosobjs:
            if qos.name == qosname:
                return qos
        return None

    def __getNodebyName(self, nodename):
        for node in self.nodeobjs:
            if node.name == nodename:
                return node
        return None

    def __get_node_ip(self, nodename):
        node = self.__getNodebyName(nodename)
        return node.ip.split('/')[0]

    def __getSwitchbyName(self, swname):
        for sw in self.switchobjs:
            if sw.name == swname:
                return sw
        return None

    # functions for collecting the Data for CLI dsplay

    def __getNodeNames(self):
        return [node.name for node in self.nodeobjs]

    def __getSwitchNames(self):
        return [sw.name for sw in self.switchobjs]

    def __getLinks(self):
        results = []
        for linkobj in self.linkobjs:
            for link in linkobj.links:
                results.append(link["source-name"] + "->" +
                               link["target-name"])
        return results

    def __getNodeDetails(self):
        result = []
        for node in self.nodeobjs:
            result.append({"name": node.name,
                           "status": node.status,
                           "id": node.id,
                           "image": node.img,
                           "ip": node.ip,
                           "mac": node.mac
                           })

        return result

    def __getSwitchDetails(self):
        result = []
        for sw in self.switchobjs:
            result.append({"name": sw.name,
                           "status": sw.status,
                           "id": sw.id,
                           "version": sw.version,
                           "controller": sw.controller
                           })
        return result

    def __getRouterDetails(self):
        result = []
        for router in self.routerobjs:
            result.append({"name": router.name,
                           "status": router.status,
                           "id": router.id,
                           "image": router.img,
                           })
        return result


    def __getLinkDetails(self):
        result = []
        # read from DB. link objects doesnt stores in switch perspective
        links = utils.link_t.all()
        for link in links:
            result.append({"name": sw.name,
                           "status": sw.status,
                           "id": sw.id,
                           "version": sw.version,
                           "controller": sw.controller
                           })
        return result
