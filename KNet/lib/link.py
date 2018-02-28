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
from six import add_metaclass, text_type
import KNet.lib.utils as utils
import KNet.lib.ovs_cmds as ovs
import KNet.lib.tc_cmds as tc
from KNet.lib.logger import logger as log

'''
@add_metaclass(abc.ABCMeta)
class NodeLink(object):
    def __init__(self, data, qos=None):
        # self.network = network
        self.qos = qos
        self.switch = data["switches"][0]
        self.nodes = data["nodes"]
        self.links = []

    def create(self):
        for node in self.nodes:
            # print node
            node_interface = "eth1"
            qos = None
            #mac = None
            #if "mac" in node:
            #    mac = node["mac"]
            #ip = self.network.getip()
            n = utils.get_node_data(node["name"])

            # create a link node to switch
            ovs.create_link(self.switch, node_interface, node["name"],
                            n['ip'], n['mac'])
            # get the tap interface name
            tapif = ovs.get_port_name(node["name"], node_interface)
            # link - source node id
            # sourceid = utils.get_node_data(node["name"])
            sourceid = n["id"]
            # link -target node id
            s = utils.get_switch_data(self.switch)
            targetid = s["id"] 
            # apply the Qos to the interface
            if "qos" in node:
                qos = self.getqos(node["qos"])
                tc.config_qos(tapif, qos)

            # store the link endpoints in array (for UI drawing)
            self.links.append({"source": sourceid, "target": targetid,
                               "source-name": node["name"],
                               "target-name": self.switch})

            # update in DB
            self.docid = utils.link_t.insert({'id': utils.generate_id(),
                                              'source': node["name"],
                                              'target': self.switch,
                                              'source-id': sourceid,
                                              'target-id': targetid,
                                              'if1': node_interface,
                                              'if2': tapif,
                                              'qos': qos,
                                              })

    def getifname(self):
        for node in self.nodes:
            print ovs.get_port_name(node, "eth1")

    def getqos(self, qname):
        for q in self.qos:
            if q["name"] == qname:
                return q
        return None

    def delete(self):
        # what to write?
        pass
'''


@add_metaclass(abc.ABCMeta)
class HostLink(object):
    def __init__(self, data, qos=None):
        # self.network = network
        log.debug("HostLink Object init" + str(data))
        self.qos = qos
        self.switch = data["switches"][0]
        self.hosts = data["hosts"]
        self.links = []

    def __getip(self, interfaces, ifname):
        for interface in interfaces:
            if interface["name"] == ifname:
                return interface["ip"], interface["mac"]
        return None

    def create(self):
        for host in self.hosts:
            log.debug("Creating HostLink" + str(host))
            r = utils.get_host_data(host['name'])
            ip, mac = self.__getip(r['interfaces'], host["interface"])
            log.debug(ip)
            log.debug(mac)
            # create a link node to switch
            ovs.create_link(self.switch, host["interface"], host['name'],
                            ip, mac)

            # get the tap interface name
            tapif = ovs.get_port_name(host["name"], host["interface"])
            # apply the Qos to the interface
            if "qos" in host:
                qos = self.getqos(host["qos"])
                tc.config_qos(tapif, qos)

            sourceid = r["id"]
            # link -target node id
            s = utils.get_switch_data(self.switch)
            targetid = s["id"]

            # get the tap interface name
            #tapif = ovs.get_port_name(host["name"], host["interface"])

            # store the link endpoints in array (for UI drawing)
            self.links.append({"source": sourceid, "target": targetid,
                               "source-name": host["name"],
                               "target-name": self.switch})

            # update in DB
            self.docid = utils.link_t.insert({'id': utils.generate_id(),
                                              'source': host["name"],
                                              'target': self.switch,
                                              'source-id': sourceid,
                                              'target-id': targetid,
                                              'if1': host["interface"],
                                              'if2': tapif,
                                              'qos': None,
                                              })

    def getifname(self):
        for router in self.routers:
            print ovs.get_port_name(router, "eth1")

    def getqos(self, qname):
        for q in self.qos:
            if q["name"] == qname:
                return q
        return None

    def delete(self):
        # what to write?
        pass




@add_metaclass(abc.ABCMeta)
class ServerLink(object):
    def __init__(self, data, qos=None):
        # self.network = network
        log.debug("ServerLink Object init" + str(data))
        self.qos = qos
        self.switch = data["switches"][0]
        self.servers = data["servers"]
        self.links = []

    def __getip(self, interfaces, ifname):
        for interface in interfaces:
            if interface["name"] == ifname:
                return interface["ip"], interface["mac"]
        return None

    def create(self):
        for server in self.servers:
            log.debug("Creating ServerLink" + str(server))
            r = utils.get_server_data(server['name'])

            ip, mac = self.__getip(r['interfaces'], server["interface"])
            log.debug(ip)
            log.debug(mac)
            # create a link node to switch
            ovs.create_link(self.switch, server["interface"], server['name'],
                            ip, mac)
            # get the tap interface name
            tapif = ovs.get_port_name(server["name"], server["interface"])
            # apply the Qos to the interface
            if "qos" in server:
                qos = self.getqos(server["qos"])
                tc.config_qos(tapif, qos)

            sourceid = r["id"]
            # link -target node id
            s = utils.get_switch_data(self.switch)
            targetid = s["id"]

            # get the tap interface name
            tapif = ovs.get_port_name(server["name"], server["interface"])

            # store the link endpoints in array (for UI drawing)
            self.links.append({"source": sourceid, "target": targetid,
                               "source-name": server["name"],
                               "target-name": self.switch})

            # update in DB
            self.docid = utils.link_t.insert({'id': utils.generate_id(),
                                              'source': server["name"],
                                              'target': self.switch,
                                              'source-id': sourceid,
                                              'target-id': targetid,
                                              'if1': server["interface"],
                                              'if2': tapif,
                                              'qos': None,
                                              })

    def getifname(self):
        for server in self.servers:
            print ovs.get_port_name(server, "eth1")

    def getqos(self, qname):
        for q in self.qos:
            if q["name"] == qname:
                return q
        return None

    def delete(self):
        # what to write?
        pass


@add_metaclass(abc.ABCMeta)
class RouterLink(object):
    def __init__(self, data, qos=None):
        # self.network = network
        log.debug("RouterLink Object init" + str(data))
        self.qos = qos
        self.switch = data["switches"][0]
        self.routers = data["routers"]
        self.links = []

    def __getip(self, interfaces, ifname):
        for interface in interfaces:
            if interface["name"] == ifname:
                return interface["ip"], interface["mac"]
        return None

    def create(self):
        for router in self.routers:
            log.debug("Creating RouterLink" + str(router))
            r = utils.get_router_data(router['name'])
            log.debug(r)
            # get IP from the router data r for the interface
            ip, mac = self.__getip(r['interfaces'], router["interface"])
            log.debug(ip)
            log.debug(mac)
            # create a link node to switch
            ovs.create_link(self.switch, router["interface"], router['name'],
                            ip, mac)

            # get the tap interface name
            tapif = ovs.get_port_name(router["name"], router["interface"])
            # apply the Qos to the interface
            if "qos" in router:
                qos = self.getqos(router["qos"])
                tc.config_qos(tapif, qos)

            sourceid = r["id"]
            # link -target node id
            s = utils.get_switch_data(self.switch)
            targetid = s["id"]

            # get the tap interface name
            tapif = ovs.get_port_name(router["name"], router["interface"])

            # store the link endpoints in array (for UI drawing)
            self.links.append({"source": sourceid, "target": targetid,
                               "source-name": router["name"],
                               "target-name": self.switch})

            # update in DB
            self.docid = utils.link_t.insert({'id': utils.generate_id(),
                                              'source': router["name"],
                                              'target': self.switch,
                                              'source-id': sourceid,
                                              'target-id': targetid,
                                              'if1': router["interface"],
                                              'if2': tapif,
                                              'qos': None,
                                              })

    def getifname(self):
        for router in self.routers:
            print ovs.get_port_name(router, "eth1")

    def getqos(self, qname):
        for q in self.qos:
            if q["name"] == qname:
                return q
        return None

    def delete(self):
        # what to write?
        pass




@add_metaclass(abc.ABCMeta)
class SwitchLink(object):
    # class variable
    patchif_index = 0

    def __init__(self, data):
        self.id = utils.generate_id()
        self.src_switch = data["switches"][0]
        self.dst_switch = data["switches"][1]
        self.links = []

    def create(self):
        # add port
        # set port type as patch
        # set port peer mapping
        self.src_patchif = "patch"+str(SwitchLink.patchif_index)
        SwitchLink.patchif_index += 1
        self.dst_patchif = "patch"+str(SwitchLink.patchif_index)
        SwitchLink.patchif_index += 1
        ovs.addport(self.src_switch, self.src_patchif)
        ovs.addport(self.dst_switch, self.dst_patchif)

        ovs.config_port_as_patch(self.src_patchif)
        ovs.config_port_as_patch(self.dst_patchif)

        ovs.peer_patch_ports(self.src_patchif, self.dst_patchif)
        ovs.peer_patch_ports(self.dst_patchif, self.src_patchif)

        # link - source node id
        s = utils.get_switch_data(self.src_switch)
        sourceid = s["id"]
        # link -target node id
        t = utils.get_switch_data(self.dst_switch)
        targetid = t["id"]
        # store the link endpoints in array (for UI drawing)
        self.links.append({"source": sourceid,
                           "target": targetid,
                           "source-name": self.src_switch,
                           "target-name": self.dst_switch
                           })

        # update in DB
        self.docid = utils.link_t.insert({'id': self.id,
                                          'source': self.src_switch,
                                          'target': self.dst_switch,
                                          'source-id': sourceid,
                                          'target-id': targetid,
                                          'if1': self.src_patchif,
                                          'if2': self.dst_patchif,
                                          'qos': None,
                                          })

    def delete(self):
        pass
