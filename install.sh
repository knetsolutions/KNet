#!/bin/bash
# Copyright 2018 KNet Solutions, India, http://knetsolutions.in
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# install openvswitch
export LC_ALL="en_US.UTF-8"
sudo apt-get update
sudo apt-get install virtualenv python-dev python-pip build-essential
sudo apt-get install -y openvswitch-switch

# install Docker
sudo apt-get -y install \
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
sudo apt-get install -y docker-ce

# Download the ovs-docker script
wget https://raw.githubusercontent.com/openvswitch/ovs/master/utilities/ovs-docker
chmod a+rwx ovs-docker
sudo cp ovs-docker /usr/bin/.

# Pull the Ubuntu Docker images
sudo docker pull ubuntu:trusty
sudo docker pull ubuntu:xenial
sudo docker pull ubuntu

#Verify the prerequisites
sudo docker  --version
sudo docker images ubuntu
sudo ovs-vsctl show
sudo ovs-docker -h