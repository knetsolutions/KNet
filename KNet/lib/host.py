'''Copyright 2018 KNet Solutions, India, http://knetsolutions.in

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''
from __future__ import unicode_literals
import sys
import abc
from six import add_metaclass, text_type
import KNet.lib.utils as utils
import KNet.lib.docker_cmds as docker


@add_metaclass(abc.ABCMeta)
class Host(object):
    def __init__(self, data):
        self.id = utils.generate_id()
        self.name = data["name"]
        self.img = data["image"]
        self.status = "initialized"
        self.interfaces = data["interfaces"]

        # DB Updation
        self.docid = utils.host_t.insert({'id': self.id, 'name': self.name,
                                          'img': self.img,
                                          'interfaces': self.interfaces,
                                          'status': self.status})
        # print self.docid

    def create(self):
        # sudo docker run -itd --name=node1  ubuntu:trusty
        self.uuid = docker.create_container(self.name, self.img)
        self.status = "created"
        # update the status in DB
        utils.host_t.update({'status': self.status}, doc_ids=[self.docid])

    def delete(self):
        docker.stop_container(self.name)
        docker.delete_container(self.name)
        self.status = "deleted"
        # update the status in DB
        utils.host_t.remove(doc_ids=[self.docid])

    def get(self):
        return utils.host_t.get(doc_id=self.docid)
