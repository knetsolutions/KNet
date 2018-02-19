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
import abc
from six import add_metaclass, text_type
import sys
import KNet.lib.utils as utils
import KNet.lib.ovs_cmds as ovs


@add_metaclass(abc.ABCMeta)
class Switch(object):

    def __init__(self, data, controller):
        self.id = utils.generate_id()
        self.name = data["name"]
        if "openflow" in data:
          self.version = str(data["openflow"]["version"])
        else:
          self.version = None
        self.controller = controller
        self.status = "initialized"
        if "datapathid" in data:
            self.datapathid = int(data["datapathid"])
        else:
            self.datapathid = int(self.id)
        # Insert the switch details in to DB
        self.docid = utils.switch_t.insert({'id': self.id, 'name': self.name,
                                            'ofversion': self.version,
                                            'controller': self.controller,
                                            'datapathid': self.datapathid,
                                            'status': self.status})

    def create(self):
        #ovs.create_bridge(self.name)
        ovs.create_userspace_bridge(self.name)
        # controller format:
        if self.controller:
            if not ovs.check_controller_format(self.controller):
                return False
            ovs.set_controller(self.name, self.controller)
            ovs.set_protocol_version(self.name, str(self.version))
        ovs.set_datapath_id(self.name, self.datapathid)
        # Update theDB
        self.status = "created"
        utils.switch_t.update({'status': self.status}, doc_ids=[self.docid])

    def delete(self):
        ovs.delete_bridge(self.name)
        # Update the DB
        self.status = "deleted"
        # utils.switch_t.update({'status': self.status}, doc_ids=[self.docid])
        utils.switch_t.remove(doc_ids=[self.docid])

    def get(self):
        return utils.switch_t.get(doc_id=self.docid)
