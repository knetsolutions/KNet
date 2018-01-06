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
import sys
import KNet.lib.utils as utils


'''
tc qdisc add dev veth1 root handle 1:0 netem delay #{@config.latency} @config.jitter} loss #{@config.pktloss}
bandwidth
tc qdisc add dev veth1 parent 1:1 handle 10: tbf rate  #{@config.bandwidth} buffer 1600 limit 3000
'''


def config_qos(tapif, qos):
    cmd = ['sudo', 'tc', 'qdisc', 'add', 'dev', tapif,
           'root', 'handle', '1:0', 'netem', 'delay',
           qos["latency"], qos["jitter"], 'loss', qos["pktloss"]]
    response = utils.run_cmd(cmd)
    cmd = ['sudo', 'tc', 'qdisc', 'add', 'dev', tapif, 'parent', '1:1',
           'handle', '10:', 'tbf', 'rate', qos["bandwidth"], 'buffer', '1600',
           'limit', '3000']
    response = utils.run_cmd(cmd)
