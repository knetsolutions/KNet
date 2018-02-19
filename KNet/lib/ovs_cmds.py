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
import sys
import KNet.lib.utils as utils


def check_controller_format(c):
    res = c.split(':')
    if not res[2].isdigit():
        return False
    if not res[0] in ["udp", "tcp"]:
        return False
    return True


def create_bridge(name):
    # sudo ovs-vsctl add-br ovs-br1
    cmd = ['sudo', 'ovs-vsctl', 'add-br', name]
    utils.run_cmd(cmd)
    # exception to be handled


def create_userspace_bridge(name):
    # sudo ovs-vsctl add-br br1 -- set Bridge br1 datapath_type=netdev
    cmd = ['sudo', 'ovs-vsctl', 'add-br', name, "--",
           'set', 'Bridge', name, 'datapath_type=netdev']
    utils.run_cmd(cmd)
    # exception to be handled


def set_controller(name, controller):
    # sudo ovs-vsctl set-controller ovs-br1 tcp:0.0.0.0:6633
    cmd = ['sudo', 'ovs-vsctl', 'set-controller', name, controller]
    utils.run_cmd(cmd)
    # exception to be handled


def dpid(id):
    # id is a number, which can be 0 to 16 digits
    # This function return 16digit string , prepends 0 in the id.
    temp = id
    Totalsize = 16

    # identify the number of digits
    digit = 1
    while (temp > 9):
        temp = temp / 10
        digit = digit+1

    prepend = ''
    prependbits = 16 - digit
    while (prependbits > 0):
        prepend += '0'
        prependbits -= 1

    r = prepend + str(id)
    return r


def set_datapath_id(name, id):
    # sudo ovs-vsctl set bridge ovs-br1 other_config:datapath-id=#{dpid}"
    # convert id in to 16digit hex
    datapath = "other_config:datapath-id=" + str(dpid(id))
    cmd = ['sudo', 'ovs-vsctl', 'set', 'bridge', name, datapath]
    utils.run_cmd(cmd)
    # exception to be handled


def set_protocol_version(name, version):
    # sudo ovs-vsctl set bridge ovs-br1 protocols=OpenFlow13
    if str("1.3") == version:
        v = "OpenFlow13"
    elif str("1.2") == version:
        v = "OpenFlow12"
    else:
        v = "OpenFlow10"
    version = "protocols="+v
    cmd = ['sudo', 'ovs-vsctl', 'set', 'bridge', name, version]
    # version 1.4,1.5 support to be checked
    utils.run_cmd(cmd)


def delete_bridge(name):
    # sudo ovs-vsctl del-br ovs-br1
    cmd = ['sudo', 'ovs-vsctl', 'del-br', name]
    utils.run_cmd(cmd)


def addport(name, portname):
    # ovs-vsctl add-port br0 tap0
    cmd = ['sudo', 'ovs-vsctl', 'add-port', name, portname]
    utils.run_cmd(cmd)


def config_port_as_patch(portname):
    # ovs-vsctl add-port br0 tap0
    cmd = ['sudo', 'ovs-vsctl', 'set', 'interface', portname, 'type=patch']
    utils.run_cmd(cmd)


def peer_patch_ports(portname, peerport):
    # ovs-vsctl add-port br0 tap0
    peer = "options:peer="+peerport
    cmd = ['sudo', 'ovs-vsctl', 'set', 'interface', portname, peer]
    utils.run_cmd(cmd)


def create_link(swname, ifname, nodename, cidr, mac=None):
    # sudo ovs-docker add-port ovs-br1 eth1 node1 --ipaddress=192.168.1.1/24
    #         --macaddress 00:00:00:00:00:01
    ipa = "--ipaddress=" + cidr
    cmd = ['sudo', 'ovs-docker', 'add-port', swname, ifname, nodename, ipa]
    if mac:
        maca = "--macaddress=" + mac
        cmd.append(maca)
    utils.run_cmd(cmd)


def get_port_name(container, ifname):
    # ref: https://github.com/openvswitch/ovs/blob/master/utilities/ovs-docker
    # fn : get_port_for_container_interface ()
    cn = "external_ids:container_id=" + str(container)
    ifname = "external_ids:container_iface=" + str(ifname)
    cmd = ['sudo', 'ovs-vsctl', '--data=bare', '--no-heading',
           '--columns=name', 'find', 'interface', cn, ifname]
    response = utils.run_cmd(cmd)
    return response.strip("\n")


# admin down link
def admindown_link(ifname):
    cmd = ['sudo', 'ifconfig', ifname, 'down']
    utils.run_cmd(cmd)


# admin up link
def adminup_link(ifname):
    cmd = ['sudo', 'ifconfig', ifname, 'up']
    utils.run_cmd(cmd)
