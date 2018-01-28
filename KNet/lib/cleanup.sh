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


#cleaning the docker instances
dockerfile=/tmp/dockers.txt
sudo docker ps -a -q > "$dockerfile"
echo "Cleaning docker instances...."
while read -r line
do
    echo "Stoping Docker instance - $line"
    sudo docker stop "$line"
    echo "Deleting Docker instance - $line"
    sudo docker rm "$line"
done < "$dockerfile"
#sudo docker stop $(sudo docker ps -a -q)
#sudo docker rm $(sudo docker ps -a -q)



#cleaning the bridges
echo "Cleaning the Openvswitch bridges ...."
brfile=/tmp/ovsbr.txt
sudo ovs-vsctl show | grep Bridge | cut -d'"' -f2 > "$brfile"
while read -r line
do
    echo "Deleting the Openvswitch bridge $line"
    sudo ovs-vsctl del-br "$line"
done < "$brfile"

#cleaning the DB files
echo "Cleaning the DB file ...."
rm -rf /tmp/db.json

#cleaning the log file
#echo "Remove the log file..."
#cp -rf /tmp/KNet.log /tmp/KNet.log.1
#rm -rf /tmp/KNet.log

#cleaning the tmp files
rm -rf "$dockerfile"
rm -rf  "$brfile"
echo "Cleaning finished....."

