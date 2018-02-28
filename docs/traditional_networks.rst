
.. contents::
  :depth: 1
  :local:

Traditional Networks Topology
==================================

KNet Supports building Traditional Network Topology with Routers, Firewall Nodes.

Router node is built with "bird routing daemon" and "shorewall" firewall sofware.

http://bird.network.cz/

http://shorewall.net/shorewall_quickstart_guide.htm

Example traditional network topology examples are available in knet-example-topologies repository.


Network Topology with Routers:
------------------------------------

Topology example (ex2 - Simple WAN Topology) consists of two routers .  Router node is inbuilt with firewall.

Provisioning the Router Node:
****************************************************

1. Login to Router Node shell


.. code-block:: bash

  sudo docker exec -it R1 bash

2. Edit the bird configuration file (/etc/bird.conf). The default configuration consists of ospf configuration.

.. code-block:: bash

  vi /etc/bird.conf

Change the router id:

.. code-block:: bash

  router id 1.1.1.1;

Enable the ospf configuration in the required interfaces

.. code-block:: bash

  protocol ospf MyOSPF {
     rfc1583compat yes;
     area 0.0.0.0 {
        stub no;
       interface "eth1" {
           hello 10;
           retransmit 6;
           cost 10;
           transmit delay 5;
           dead count 5;
           wait 50;
           type broadcast;
       };

       interface "eth2" {
           hello 10;
           retransmit 6;
           cost 10;
           transmit delay 5;
           dead count 5;
           wait 50;
           type broadcast;
       };

    };
  }


3. Start the bird routing daemon

.. code-block:: bash

  bird -c /etc/bird.conf -d &
   

4. Check the log files

.. code-block:: bash

  cat /var/log/bird.log


The detailed information of bird routing configuration is available in bird website.

Repeat the same for all the Routers.


Testing
**************
1. Check the Routing tables of Router Node.

.. code-block:: bash
   
   ip route

2. Perform the Ping end to end ping from the hosts


How to configure Firewall:
------------------------------------

1. Login to the Router Node

2. Edit the shorewall configuration.

3. Start the shorewall.


