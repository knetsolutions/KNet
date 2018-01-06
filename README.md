# KNet
Virtual Network Tobology builder

KNet utilizes the Docker containers  openvswitch for building the SDN Test bed.

Supported on all Linux distributions.
Tested on Ubuntu 14.04, 16.04

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

