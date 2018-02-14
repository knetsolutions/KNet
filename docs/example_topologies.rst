Example Topologies
===================

`https://github.com/knetsolutions/knet-example-topologies` repository consists of SDN, and traditional topology ìnput files.

SDN Folder consists of the below topology input files,

1. Simple Topology
2. Linear1 Topology
3. Linear2 Topology
4. Ring Topology
5. Partial Mesh Topology
6. Full Mesh Topology
7. Tree Topology

Traditional Folder consists of 

1. One Network with Hosts and Server
2. Two Networks with Hosts, Server, Router
3. WAN Topology with Two Routers, Hosts


Star Topology
-------------

Filename: `simple.yaml`

.. figure::  imgs/topo0.png
   :align:   center

   Simple Star Topology.

This topology consists of 4 nodes, and a switch. All Nodes are connected to a same switch.

RYU OpenFlow13 Switch application **simple_switch_13.py** can be used to test this topology.

Linear Topology1
-----------------
Filename: `linear1.yaml`

.. figure::  imgs/topo1.png
   :align:   center

   Simple Linear Topology.

This topology consists of 4 nodes, and two switches. 2 Nodes are connected in each switch. Also these switches are interconnected. Also MAC address is explicitly  mentioned.

RYU OpenFlow13 Switch application **simple_switch_13.py** can be used to test this topology.

Linear Topology2
-----------------

Filename: `linear2.yaml`

.. figure::  imgs/topo2.png
   :align:   center

   Linear Topology with 4 Switches

This topology consists of 4 nodes, and four switches. Each node is connected in each switch. Also these switches are connected linearly and no loop. 

RYU OpenFlow13 Switch application **simple_switch_13.py** can be used to test this topology.

Ring Topology
-----------------------

Filename: `ring.yaml`

.. figure::  imgs/topo4.png
   :align:   center

   Ring Topology.
      
This topology consists of 4 nodes, and four switches. Each node is connected in each switch. Also these switches are connected linearly and forms the loop.

This topology forms a loop, hence  RYU STP application **simple_switch_stp_13.py** to be used to test this topology.



Full Mesh Topology 
-----------------------

Filename: `fmesh.yaml`

.. figure::  imgs/topo5.png
   :align:   center

   Full Mesh Topology.

This topology consists of 4 nodes, and four switches. Each node is connected in each switch. Also these switches are interconnected with each other to form a full mesh.

This topology forms a loop, hence  RYU STP application **simple_switch_stp_13.py** to be used to test this topology.

Partial Mesh Topology 
-----------------------

Filename: `pmesh.yaml`

.. figure::  imgs/topo6.png
   :align:   center

   Partial Mesh Topology.

This topology consists of 4 nodes, and four switches. Each node is connected in each switch. Also these switches are interconnected with some other to form a partial mesh.

This topology forms a loop, hence  RYU STP application **simple_switch_stp_13.py** to be used to test this topology.


Tree Topology 
-----------------------

Filename: `tree.yaml`

.. figure::  imgs/topo7.png
   :align:   center

   Tree Topology.

This topology consists of 8 nodes, and 7 switches. This topology forms a binary tree with depth 3. Root Switch is S1. Second level  switches are S2 and S5. Third level switches are S3, S4, S6, S7. Nodes are connected to switches S3, S4, S6  and S7.

RYU OpenFlow13 Switch application **simple_switch_13.py** can be used to test this topology.