..
	Copyright 2018 KNet Solutions, India, http://knetsolutions.in

	Licensed under the Apache License, Version 2.0 (the "License");
	you may not use this file except in compliance with the License.
	You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

	Unless required by applicable law or agreed to in writing, software
	distributed under the License is distributed on an "AS IS" BASIS,
	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
	See the License for the specific language governing permissions and
	limitations under the License.

.. contents::
  :depth: 1
  :local:

Topology File explained
=======================

Topology input file is defined in YAML(Yet another Markup Language). YAML is human readable data serialization language , commonly used as configuraton file for applications.


Topology Object consists the following main sections,

name 
^^^^^
name defines the topology name. Data type is string

Example:

.. code-block:: bash

	name : Simple Star Topology 1

version
^^^^^^^^
version defines the topology file schema version. The current version is 1.0.

Example:

.. code-block:: bash

    version: 1.0


description
^^^^^^^^^^^^^^^^
**description**  is for detailed description of the topology. Its a multiline string.

Example:

.. code-block:: bash

    description: |
      This topology consists of 4 nodes, and a switch. 
      All Nodes are connected to a same switch.


controller
^^^^^^^^^^^
**controller** is a object defined for SDN Controller. This object contains url property. **url** defines the SDN Controller URL. Data type is string.

All the switches in the topology will be connected to this controller url.

Example:

.. code-block:: bash

    controller:
      url: tcp:0.0.0.0:6633


openflow
^^^^^^^^^^^
**openflow** is a object defined for openflow protocol. This object contains **version** property. data type is number.

This openflow version is applied for all the switches in the topology.

Example:

.. code-block:: bash

    openflow:
      version: 1.3


network
^^^^^^^^^^^
**network** is a list for defining the network objects. Each network object containes **name** and **subnet** property. KNet will manages the IP assignment to the nodes in this network. The network name will be used by the nodes object.

Example:

.. code-block:: bash

    networks:
      -
        name: n1
        subnet: 10.1.1.0/24

qos
^^^^^^^^

**qos** is a list for defining the qos object. Each qos object containes the **name, bandwidth, latency, jitter, pktloss** property. KNet use this qos object for applying qos in the link using linux traffic shaping tool.

qos object will be consumed by link object.

Example:

.. code-block:: bash

    qos:
      -
        name: q1
        bandwidth: 100Mbps
        latency: 100ms
        jitter: 1ms
        pktloss: 0.5%


nodes
^^^^^^^^^^^
nodes object consists of list of nodes. Each node is represented with the **name, image, network, ip, mac** properties.

1. **name** defines the node name. Its a mandatory parameter

2. **image** defines the docker image for the node. Recommended value is "ubuntu:trusty" image. thats is ubuntu 14.04 version. Dont change it until unless you know about this.  Its a mandatory parmeter

3. **network** defines the network belongs to this node. if network is mentioned, IP will be automatically allocated from this network.

4. **ip** defines the static ip for this node. The given ip will be assigned to the node. Either network or ip should present.

5. **mac** defines the  mac id for the interface. Its a optional parameter


Example1:

.. code-block:: bash

    nodes:
      -
        name: a1
        image: ubuntu:trusty
        network: n1


Example2:


.. code-block:: bash

    nodes:
      -
        name: a1
        image: ubuntu:trusty
        ip: 10.10.10.2/24
        mac: 00:00:00:00:00:01

switches
^^^^^^^^^^^

switches object consists of list of switches. Each switch is represented with the **name** proerty.

name defines the switch name. Its a mandatory parameter.

Example1:

.. code-block:: bash

    switches:
      -
        name: switch1

links
^^^^^^^^^^^
links object consists of list of links. Each link is represented with the nodes and switches. 

There are two types of links.

1. Switch to Node Link: This means, Switch is connected with one or more nodes.

2. Switch to Switch Link: This means, switch to connected with another switch.

**Switch to Node Link** 

.. code-block:: bash

    links:
      -
        switches:
          - switch1
        nodes:
          - name: a1
          - name: a2
          - name: a3
          - 
            name: a4
            qos: q2

In the above example, switch1 is connected with 4 nodes (a1, a2, a3, a4), and switch to a4 link will have qos configured.


**Switch to Switch Link**

.. code-block:: bash

    links:
      -
        switches:
          - switch2
          - switch3 

In the above example, switch2 is connected with switch3
