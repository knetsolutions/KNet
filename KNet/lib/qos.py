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


@add_metaclass(abc.ABCMeta)
class Qos(object):

    def __init__(self, data, container):
        self.id = utils.generate_uuid()
        self.name = data["name"]
        self.bandwidth = data["bandwidth"]
        self.latency = data["latency"]
        self.jitter = data["jitter"]
        self.pktloss = data["pktloss"]

    def create(self):
        pass

    def delete(self):
        pass

    def get(self):
        pass
