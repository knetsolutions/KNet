
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

As all nodes are ubuntu nodes, we can just install Apache Webserver and Locust https://locust.io/ (HTTP Load Testing Tool) start using it. 

Objective is create the example topology0, and Install the Apache Web Server in a4 node.   Install Locust in a1 node.  Trigger the Locust to test the apache web server(a4). Locust will generate huge http connections to the Apache web server and load it.


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


Start the Ryu Controller L4Switch application,
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

L4Switch(https://github.com/knetsolutions/knet/L4Switch.py) application creates flow based on srcip, dstip, protocol,srcport, dstport. 



.. figure::  imgs/traffic/ryu_l4_s.png
   :align:   center


Install the Apache WebServer on a4 node 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

  sudo docker exec -it a4 bash
  sudo apt-get update
  sudo apt-get install apache2
  sudo service apache restart

.. figure::  imgs/traffic/apache_install_s.png
   :align:   center

.. figure::  imgs/traffic/apache_start_s.png
   :align:   center



Install the Locust Tool on a1 node
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

  sudo docker exec -it a1 bash
  sudo apt-get update
  sudo apt-get install python-dev python-pip
  sudo pip install locustio


.. figure::  imgs/traffic/locust_install_s.png
   :align:   center


Run the Locust HTTP Load test 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In the a1 node, Create a locust input file (loadtest.py)

.. code-block:: python

  from locust import HttpLocust, TaskSet
  def index(l):
      l.client.get("/index.html")

  class UserBehavior(TaskSet):
      tasks = {index: 2}

  class WebsiteUser(HttpLocust):
      task_set = UserBehavior
      min_wait = 0
      max_wait = 0

Start the locust as below,
10.20.20.5 is a4 IP

.. code-block:: bash

  locust -f loadtest.py --no-web --host http://10.20.20.5
  

.. figure::  imgs/traffic/locust_run_s.png
   :align:   center



The output shows , how many connections per second requested and the response time, etc.

.. figure::  imgs/traffic/locust_output_s.png
   :align:   center


Check the flow tables in ovs

.. code-block:: bash

  sudo ovs-ofctl -O OpenFlow13 dump-flows switch1
  sudo ovs-ofctl -O OpenFlow13 dump-flows switch1 | wc

.. figure::  imgs/traffic/flow_tables_s.png
   :align:   center


.. figure::  imgs/traffic/flow_tables_count_s.png
   :align:   center


I could able to simulate around 2000 Flows in 2 minutes. we can test flow setup rate using this test.



