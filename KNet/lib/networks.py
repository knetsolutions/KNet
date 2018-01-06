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
import sys
import ipaddress
import KNet.lib.utils as utils


@add_metaclass(abc.ABCMeta)
class Network(object):

    def __init__(self, data):
        self.id = utils.generate_uuid()
        self.name = data["name"]
        self.subnet = data["subnet"]
        self.netmask = self.subnet.split('/')[1]
        # convert in to unicode - compatibility with ipaddress module
        self.subnet = unicode(self.subnet, "utf-8")
        self.ipaddresses = list(ipaddress.ip_network(self.subnet).hosts())
        self.index = 0
        self.max = len(self.ipaddresses)

    def getip(self):
        self.index = self.index + 1
        ip = str(self.ipaddresses[self.index]) + "/" + self.netmask
        return ip
