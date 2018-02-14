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

import os
import subprocess
import sys
import uuid
import tinydb
from tinydb import TinyDB, Query
from beautifultable import BeautifulTable
from KNet.lib.logger import logger as log


# https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
class Singleton(object):
    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance


# UUID Generation
def generate_uuid():
    return str(uuid.uuid4())

'''
ID Generation, Associated with nodes,switches.
First ID should be 0. This ID is used in next-UI Topology Drawaing
'''
id = -1
def generate_id():
    global id
    id = id + 1
    return id

# id must be reset to -1,when deleting the topology. 
# every topology devices must get id from 0.
def reset_id():
    global id
    id = -1
    return

# Executing Command
def run_cmd(cmd):
    try:
        log.debug(str(cmd))
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        log.debug(output)
        return output
        #return subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as ex:
        if ex.returncode == 255:
            raise RuntimeWarning(ex.output.strip())
        raise RuntimeError('cmd execution returned exit status %d:\n%s'
                % (ex.returncode, ex.output.strip()))

# ---------------------------------------------------------------#
# DB Interface
db = TinyDB('/tmp/db.json')
query = Query()
topology_t = db.table('topology')
host_t = db.table('host')
server_t = db.table('server')
node_t = db.table('node')
router_t = db.table('router')
switch_t = db.table('switch')
link_t = db.table('link')
network_t = db.table('network')
qos_t = db.table('qos')

def get_node_data(node_name):
    result = node_t.search(query.name == node_name)
    # print result
    return result[0]


def get_router_data(router_name):
    result = router_t.search(query.name == router_name)
    # print result
    return result[0]


def get_host_data(host_name):
    result = host_t.search(query.name == host_name)
    # print result
    return result[0]

def get_server_data(server_name):
    result = server_t.search(query.name == server_name)
    # print result
    return result[0]

def get_switch_data(switch_name):
    result = switch_t.search(query.name == switch_name)
    # print result
    return result[0]

def purge_db():
    topology_t.purge()
    node_t.purge()
    switch_t.purge()
    link_t.purge()
    network_t.purge()
    qos_t.purge()
# --------------------------------------------------------------- #

#Pretty  Print Interface

def format_createtopo(data):
    log.debug(str(data))
    if not data:
        return ""
    table = BeautifulTable(max_width=120)
    header = []
    row = []
    for d in data:
        header.append(str(d))
        row.append(data[d])
    table.column_headers = header
    table.column_widths["Name"] = 10
    table.column_widths["Status"] = 10
    table.column_widths["Controller"] = 10
    table.column_widths["Hosts"] = 15
    table.column_widths["Switches"] = 15 
    table.column_widths["Links"] = 20
    table.append_row(row)
    return table


def format_topo(data):
    if not data:
        return ""
    table = BeautifulTable(max_width=80)
    header = []
    row = []
    for d in data:
        header.append(str(d))
        row.append(data[d])
    table.column_headers = header
    table.column_widths["Name"] = 20
    table.column_widths["Status"] = 20
    table.column_widths["Controller"] = 20
    table.append_row(row)
    return table

def format_nodes(data):
    if not data:
        return ""
    table = BeautifulTable(max_width=120)
    header = []
    row = []
    # generate header
    for d in data[0]:
        header.append(str(d))
    table.column_headers = header
    # generate rows
    for d in data:
        row = []
        for key in d:
            row.append(d[key])
        table.append_row(row)

    return table

def format_switches(data):
    if not data:
        return ""
    table = BeautifulTable(max_width=120)
    header = []
    row = []
    # generate header
    for d in data[0]:
        header.append(str(d))
    table.column_headers = header
    # generate rows
    for d in data:
        row = []
        for key in d:
            row.append(d[key])
        table.append_row(row)

    return table


def format_links(data):
    # print data
    if not data:
        return ""
    table = BeautifulTable(max_width=120)
    header = []
    row = []
    # generate header
    for d in data[0]:
        header.append(str(d))
    table.column_headers = header
    # generate rows
    for d in data:
        row = []
        for key in d:
            row.append(d[key])
        table.append_row(row)
    return table
