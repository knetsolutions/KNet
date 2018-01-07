# KNet

KNet is a Virtual Network Tobology builder, Primarily used as SDN Test Environment.

KNet builds the Virtual Network Topology with Switches, Nodes, Links. KNet uses Dockers for building the Nodes, openvswitch for switches.

KNet support QoS parameter configuration for the Links, such as bandwidth, latency, jitter and packetloss.

KNet supports the CLI and Web Interface. 


## Getting Started

KNet can be installed on any Linux distributions. But we have tested only Ubuntu 14.04 and 16.04.

Minimum hardware configuration required is 4GB RAM, 2 Core processors. Higher configuration gives better result. 


### Prerequisites

The following script installs the prerequisites in Ubuntu system. 

```
curl https://raw.githubusercontent.com/knetsolutions/KNet/master/install.sh | sh
```

### Installing

KNet is developed in Python 2.7. I suggest to install it in VirtualEnv as below. 

**Create a Python Virtual environment**

```
export LC_ALL="en_US.UTF-8"
cd $HOME
virtualenv knet
. knet/bin/activate
```

Example output
```
ubuntu@ubuntu:~$ export LC_ALL="en_US.UTF-8"
ubuntu@ubuntu:~$ cd $HOME
ubuntu@ubuntu:~$ virtualenv knet
Running virtualenv with interpreter /usr/bin/python2
New python executable in /home/ubuntu/knet/bin/python2
Also creating executable in /home/ubuntu/knet/bin/python
Installing setuptools, pkg_resources, pip, wheel...done.
ubuntu@ubuntu:~$ . knet/bin/activate
(knet) ubuntu@ubuntu:~$ 

```

**Installing KNet**
Install the KNet in the virtual environment as below
```
git clone https://github.com/knetsolutions/KNet
cd KNet
pip install --process-dependency-links .
```

Example Output:
```
(knet) ubuntu@ubuntu:~$ git clone https://github.com/knetsolutions/KNet
Cloning into 'KNet'...
remote: Counting objects: 231, done.
remote: Compressing objects: 100% (89/89), done.
remote: Total 231 (delta 135), reused 226 (delta 133), pack-reused 0
Receiving objects: 100% (231/231), 718.91 KiB | 409.00 KiB/s, done.
Resolving deltas: 100% (135/135), done.
Checking connectivity... done.
(knet) ubuntu@ubuntu:~$ 
(knet) ubuntu@ubuntu:~$ cd KNet/
(knet) ubuntu@ubuntu:~/KNet$ pip install --process-dependency-links .
Processing /home/ubuntu/KNet
Collecting six==1.11.0 (from KNet==1.0)
.....(output omitted)
(knet) ubuntu@ubuntu:~/KNet$
```
Congrats... Installation Completed.


## Few Things to know about KNet.


**Topology**

Topology consists of Nodes, Switches, Links, QoS, Network Objects. Nodes are build as Docker Containers. Switches are openvswitch switches. 

**Topology input file**

User should write Topology in YAML file. This Topology file will be input to the KNet for Topology Creation.

Example Topology files(linear,ring,mesh,parial mesh, tree) are available in examples folder. 

**CLI**

KNet comes with simple CLI (Command Line Interface). It supports the following commands

```
Help
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

**UI (Web Interface)**

KNet comes with Web Interface. Its used for Viewing the Topology. Configuration is NOT supported. This Web Interface displayes Topology in Graphical representation and reflects the topology changes. 

**Node**

Nodes are build as Docker Containers. ubuntu image is used as default Node image. The default management interface is available for this Node. 
Node is just a another real Ubuntu Machine. User can install any sofware (apache, mysql, traffic generator, etc) and use it.

docker commands can be used to control the nodes.

**Switch**

Openvswitch is used for building switches.  openswitch commands can be used to debug the switches.

**Cleanup Script**

Cleanup script is included in the repo(cleanup.sh).

Suppose, you created topology and exit the cli without deleted  the topology. The Topology footprints (docker containers, switches) exists in the system. So next time , topology creation may fail. 

Its best practice before you start the KNet application, runs the cleanup script. It cleans all the docker nodes,openvswitches  exists in your system.

## Testing

**Start the SDN Controller**

```
ryu-manager --verbose apps/simple_switch_13.py
```


**Start the KNet UI**

Run in the VirtualEnvironment,

```
cd $HOME/KNet
python ui/webserver.py >/dev/null 2>&1 &
```

Open the Browser with below URL to see the topology diagram

```
http://localhost:5000/index.html
```

Run in the VirtualEnvironment,

**Start the KNet CLI**

1. Start the CLI
```
cd $HOME/KNet
python python KNet/cli.py
```

2. Create a Topology
In the KNet cli prompt, use "CreateTopology" command to creates a topology.


Example:
```
KNet-cli#CreateTopology /home/ubuntu/KNet/examples/topo0.yaml
+---------+---------------+------------------------------------------+-------------+------------------+----------------+
| Status  |     Name      |                  Links                   |  Switches   |    Controller    |     Nodes      |
+---------+---------------+------------------------------------------+-------------+------------------+----------------+
| Created | Simple Star T | [u'a1->switch1', u'a2->switch1', u'a3->s | ['switch1'] | tcp:0.0.0.0:6633 | ['a1', 'a2', ' |
|         |   opology 1   |         witch1', u'a4->switch1']         |             |                  |   a3', 'a4']   |
+---------+---------------+------------------------------------------+-------------+------------------+----------------+
KNet-cli#
```

Now you can check the Topology Diagram in the UI http://localhost:5000/index.html. 
![Topology Diagram](docs/topology_diagram.png?raw=true) 

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

* **KNet Solutions** 

## License

This project is licensed under the Apache License - see the [LICENSE.md](LICENSE.md) file for details
