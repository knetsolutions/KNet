[![Build Status](https://travis-ci.org/knetsolutions/KNet.svg?branch=master)](https://travis-ci.org/knetsolutions/KNet)
[![Doc Status](https://readthedocs.org/projects/knet-topology-builder/badge/?version=latest)](http://knet-topology-builder.readthedocs.org/en/latest/)

# KNet

KNet is a Virtual Network Tobology builder, Primarily used as SDN Test Environment.

KNet builds the Virtual Network Topology with Switches, Nodes, Links. KNet uses Dockers for building the Nodes, openvswitch for switches.

KNet support QoS parameter configuration for the Links, such as bandwidth, latency, jitter and packetloss.

KNet supports the CLI and Web Interface. 

**Detailed Document is available in [readthedocs](http://knet-topology-builder.readthedocs.io)**

## Getting Started

Currently KNet is compatible with **Python 2.7** only.

KNet can be installed on any Linux distributions. But we have tested only **Ubuntu 14.04 and 16.04.**

Minimum hardware configuration required is 4GB RAM, 2 Core processors. Higher configuration gives better result. 


### Prerequisites

The following script installs the prerequisites in Ubuntu system. 

```
curl https://raw.githubusercontent.com/knetsolutions/KNet/master/install.sh | sh
```

### Installing

Install Knet as below,

```
pip install knet

```

Congrats... Installation Completed. 
This installs the **knet-cli** executable script. Just run **knet-cli** command to get in to CLI.


### How to Run CLI

Execute the below command to get in to KNet CLI
```
knet-cli
```

### CLI Commands

CLI supports the following commands

```
Help
Cleanup
CreateTopology
DeleteTopology
GetTopology
DeleteNode
DeleteSwitch
AdminDownLink
AdminUpLink
PingAll
Ping
Exit
```

To get the detailed help for a command


```
Help CreateTopology

```




## Few Things to know about KNet.


**Topology**

Topology consists of Nodes, Switches, Links, QoS, Network Objects. Nodes are build as Docker Containers. Switches are openvswitch switches. 

**Topology input file**

User should write Topology in YAML file. This Topology file will be input to the KNet for Topology Creation.

Example Topology files(linear,ring,mesh,parial mesh, tree) are available in https://github.com/knetsolutions/knet-example-topologies repository. 


**Node**

Nodes are build as Docker Containers. ubuntu image is used as default Node image. The default management interface is available for this Node. 
Node is just a another real Ubuntu Machine. User can install any sofware (apache, mysql, traffic generator, etc) and use it.

docker commands can be used to control the nodes.

**Switch**

Openvswitch is used for building switches.  openswitch commands can be used to debug the switches.



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
