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
import yaml
import argparse
from KNet.lib.topology import Topology

# main application
def main(argv):
    parser = argparse.ArgumentParser("KNet Test app")
    parser.add_argument("--input-file", required=True, help="Topology input file")
    args = parser.parse_args(argv[1:])
    with open(args.input_file) as fp:
        tdata = yaml.load(fp)
    t = Topology()
    print t.create(tdata)
    print t.get()

if __name__ == "__main__":
    main(sys.argv)
