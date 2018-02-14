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
Topology_schema = {
    "type": "object",
    "properties": {
        "Topology": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "controller": {
                    "type": "object",
                    "properties": {
                        "url": {"type": "string"}
                        },
                 },
                "openflow": {
                    "type": "object",
                    "properties": {
                        "version": {"type": "number"}
                        }
                },      
                "hosts": {
                    "type": "array",
                    "properties": {
                        "name": {"type": "string"},
                        "image": {"type": "string"}
                    }
                },  # end of hosts
                "switches": {
                    "type": "array",
                    "properties": {
                        "name": {"type": "string"},
                        "datapathid": {"type": "number"},
                        "openflow": {
                            "type": "object",
                            "properties": {
                                "version": {"type": "number"}
                            }
                        }
                    }
                },  # end of switches
                "links": {
                    "type": "array",
                    "properties": {
                        "switches": {"type": "array"},
                        "nodes": {"type": "array"},
                        "network": {"type": "string"}
                    }
                },  # end of links
                "networks": {
                    "type": "array",
                    "properties": {
                        "name": {"type": "string"},
                        "type": {"type": "string"}
                     }
                },  # end of networks
                "qos": {
                    "type": "array",
                    "properties": {
                        "name": {"type": "string"},
                        "bandwidth": {"type": "string"},
                        "latency": {"type": "string"},
                        "jitter": {"type": "string"},
                        "pktloss": {"type": "string"},
                     }
                }  # end of qos
            }  # end of properties of Topology
        }  # end of Topology
    }  # end of properties of Topology_schema
}  # end of Topology_schema
