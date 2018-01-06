# KNet
Virtual Network Tobology builder

KNet utilizes the Docker containers  openvswitch for building the SDN Test bed.
It has inbuilt CLI interface, UI for Monitoring the topology.

Supported on all Linux distributions.
Tested on Ubuntu 14.04, 16.04


## How to Install in on ubuntu 16.04:

### Install the Prerequisties (docker,openvswitch,ovs-docker, ubuntu docker images)

curl https://raw.githubusercontent.com/knetsolutions/KNet/master/install.sh | sh

### Install the KNet 

1.Create a virtual environment
virtualenv knet
. knet/bin/activate

2.Install the KNet

git clone https://github.com/knetsolutions/KNet
cd KNet
pip install --process-dependency-links .

3.Test the Installation

Open Two terminal, In one terminal run CLI, another terminal run Webserver

To run cli:
cd KNet
python KNet/cli.py

To run UI:
python ui/webserver.py

### Run the Sample Topology
In the CLI.

CreateTopology /home/suresh/KNet/examples/topo7.yaml 

Access the UI:
http://localhost:5000/index.html







Installation - Ubuntu 16.04:
============================
1) openvswitch installation:

sudo apt-get update
# ovs version 2.5.2 available in ubuntu repo
sudo apt-get install openvswitch-switch


2) Docker installation:
https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#install-using-the-repository


sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update

sudo apt-get install docker-ce

3) pull ubuntu images from docker repository:
sudo docker pull ubuntu:trusty
sudo docker pull ubuntu:xenial
sudo docker pull ubuntu


4)
install ovs-docker:

wget https://raw.githubusercontent.com/openvswitch/ovs/master/utilities/ovs-docker
chmod a+rwx ovs-docker
sudo cp ovs-docker /usr/bin/.


Install Ryu Controller:
========================
sudo apt-get install virtualenv python-dev python-pip build-essential
export LC_ALL="en_US.UTF-8"
virtualenv ryu
. ryu/bin/activate
pip install ryu
ryu --version 
4.20


Install Knet
==============================
virtualenv knet
. knet/bin/activate
#download knet packet
pip install knet/.



How to Run:

CLI method:


programming method:
python knet/main.py --input-file examples/topo3.yaml

