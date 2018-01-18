
.. contents::
  :depth: 1
  :local:

Traffic Tests
=================


TCP and UDP Tests using IPERF :
------------------------------------

As all nodes are ubuntu nodes, we can just install iperf and start use it. In this below example shows the IPERF traffic gene

Objective is create the example topology0, and generate the IPERF Tests between node a1 and a4.  a4 will act as iperf server, and a1 will act as iperf client.

a1 node ip is 10.20.20.2
a4 node ip is 10.20.20.5



Create the Topology using KNet CLI.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. figure::  imgs/traffic/topology_cli_s.png
   :align:   center



View the Topology Web UI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure::  imgs/traffic/topology_ui_s.png
   :align:   center


Start the Ryu Controller SimpleSwitch13 application,
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure::  imgs/traffic/ryu_s.png
   :align:   center


Install the IPERF on a1 node 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

	sudo docker exec -it a1 bash
	sudo apt-get update
	sudo apt-get install iperf

.. figure::  imgs/traffic/iperf_install1_s.png
   :align:   center

.. figure::  imgs/traffic/iperf_install2_s.png
   :align:   center


Install the IPERF on a4 node
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Repeat the IPERF installation methond mentioned in above step in node a4.


Start the IPERF in a4 node as TCP Server.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: bash

	sudo docker exec -it a4 bash
	iperf -s

.. figure::  imgs/traffic/iperf_server_start_s.png
   :align:   center


Start the IPERF in a1 node as TCP Client.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: bash

	sudo docker exec -it a1 bash
	iperf -c 10.20.20.5

.. figure::  imgs/traffic/iperf_client_output_s.png
   :align:   center


Check the Results.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Server Side


.. figure::  imgs/traffic/iperf_server_output_s.png
   :align:   center



Check the OVS flows.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure::  imgs/traffic/ovs_flows_s.png
   :align:   center



References
^^^^^^^^^^^^^^^^^^^^
IPERF supports UDP Traffic tests as well , Below links can help you for udp tests.

1. https://iperf.fr/iperf-doc.php

2. https://openmaniak.com/iperf.php



HTTP Tests Using Apache WebServer & Locust :
---------------------------------------------

Todo
