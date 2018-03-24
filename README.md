[![Build Status](https://travis-ci.org/knetsolutions/KNet.svg?branch=master)](https://travis-ci.org/knetsolutions/KNet)
[![Doc Status](https://readthedocs.org/projects/knet-topology-builder/badge/?version=latest)](http://knet-topology-builder.readthedocs.org/en/latest/)

# KNet

KNet is a Virtual Network Tobology builder. Some of the places, it can be used as,

1.  SDN Test Lab.
2.  Networking Lab
3.  Security Test Environment 
4.  Test Environment for Containarized Applications


KNet builds the Virtual Network Topology with Switches, Hosts, Routers, and Servers. KNet uses Dockers for building the Nodes, openvswitch for switches.

KNet support QoS parameter configuration for the Links, such as bandwidth, latency, jitter and packetloss.

KNet supports the CLI and Web Interface. 

**Detailed Document is available in [readthedocs](http://knet-topology-builder.readthedocs.io)**


![Topology Diagram](docs/imgs/topo0.png?raw=true) 

![Topology Diagram](docs/imgs/routing_img.png?raw=true) 


## Getting Started

Currently KNet is compatible with **Python 2.7** only.

KNet can be installed on any Linux distributions. But we have tested only ** 16.04.**

Minimum hardware configuration required is 4GB RAM, 2 Core processors. Higher configuration gives better result. 


### Prerequisites

The following script installs the prerequisites in Ubuntu 16.04 system. 

```
curl https://raw.githubusercontent.com/knetsolutions/KNet/master/install.sh | bash
```

### Installing

Install Knet as below,

```
pip install knet

```

This installs the **knet-cli** executable script. Just run **knet-cli** command to get in to CLI.


### How to Run CLI

Execute the below command to get in to KNet CLI
```
knet-cli
```

### CLI Commands

CLI supports the following commands

```

Available Commands 
****************************************************
Exit -------Exit
Version -------Version
TcpTest -------TcpTest
TcpTest_Detach -------TcpTest
Exec -------Execute commands in the node
UdpTest -------UdpTest
UdpTest_Detach -------UdpTest
Cleanup -------Cleanup
CreateTopology -------Create Topology in SDN Test Bed
DeleteTopology -------Delete the Topology in SDN Test Bed
GetTopology -------Get the Topology objects in Detail
DeleteNode -------Delete the Node in the Topology
DeleteSwitch -------Delete the Switch in the Topology
AdminDownLink -------Admin down the Link
AdminUpLink -------Admin up the Link
PingAll -------Ping All nodes with each other
Ping -------Ping the soruce node to destination node
****************************************************


```

To get the detailed help for a command


```
Help CreateTopology

```




## Few Things to know about KNet.


**Topology**

Topology consists of Hosts, Servers, Routers, Switches, Links, QoS, . Hosts, Servers, Routers are build as Docker Containers. Switches are openvswitch switches. 

**Topology input file**

User should write Topology in YAML file. This Topology file will be input to the KNet for Topology Creation.

Example Topology files(linear,ring,mesh,parial mesh, tree) are available in https://github.com/knetsolutions/knet-example-topologies repository. 


**Hosts**

Host is built as Docker Containers. Alpine Linux image is used as base Image. Iperf, tcpdump, ping, traceroute, curl tools are preinstalled.


**Server**

Server is built as Docker Containers. Alpine Linux image is used as base Image. Apache web server is  preinstalled.



**Router**

 Router is built as Docker Containers. Alpine Linux image is used as base Image. bird routing package is preinstalled.



**Switch**

Openvswitch is used for building switches.  openvswitch kernel data  module is used.



## UI - Web Interface

KNet UI is optional component. 
It is used for Viewing the Topology.  This Web Interface displayes Topology in Graphical representation and reflects the topology changes. 

KNet UI repo is available in  https://github.com/knetsolutions/knet-ui

**UI Installation**

```
git clone https://github.com/knetsolutions/knet-ui
cd knet-ui
python ui/webserver.py

```
UI can be accessible in  http://localhost:5000/index.html



## Testing

**Start the SDN Controller**

```
ryu-manager --verbose apps/simple_switch_13.py
```

**Start the Knet CLI**

```
knet-cli
```

**Create a Topology**
Note : Topology example files available in https://github.com/knetsolutions/knet-example-topologies
In the KNet cli prompt, use "CreateTopology" command to creates a topology.


Example:
```
KNet-cli#CreateTopology /home/ubuntu/knet-example-topologies/1.0/topo0.yaml
+---------+---------------+------------------------------------------+-------------+------------------+----------------+
| Status  |     Name      |                  Links                   |  Switches   |    Controller    |     Nodes      |
+---------+---------------+------------------------------------------+-------------+------------------+----------------+
| Created | Simple Star T | [u'a1->switch1', u'a2->switch1', u'a3->s | ['switch1'] | tcp:0.0.0.0:6633 | ['a1', 'a2', ' |
|         |   opology 1   |         witch1', u'a4->switch1']         |             |                  |   a3', 'a4']   |
+---------+---------------+------------------------------------------+-------------+------------------+----------------+
KNet-cli#
```


**Start the KNet UI**


```
cd knet-ui
python ui/webserver.py
```

Open the Browser with below URL to see the topology diagram

```
http://localhost:5000/index.html
```

Now you can check the Topology Diagram in the UI http://localhost:5000/index.html. 
![Topology Diagram](docs/imgs/topo0.png?raw=true) 

Make sure, you delete the Topology "DeleteTopology" before you exit the shell.

```
KNet-cli#DeleteTopology
****--------- Topology Deleted---------****
KNet-cli#Exit
(knet) ubuntu@ubuntu:~/KNet$
```


## Built With

* [Dockers](https://www.docker.com/) - The Docker Containers
* [Openvswitch](http://openvswitch.github.io/) - Open vSwitch is a production quality, multilayer virtual switch 
* [Next UI Toolkit](https://github.com/NeXt-UI/next-tutorials) - NeXt UI is a Javascript/CSS framework for rendering Network Topology

## Contributing

Todo.

## Versioning

 For the versions available, see the [tags on this repository](https://github.com/knetsolutions/KNet/tags). 

## Authors

[KNet Solutions](http://knetsolutions.in)

## License

This project is licensed under the Apache License - see the [LICENSE.md](LICENSE.md) file for details
