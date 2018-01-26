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
import os
from six import add_metaclass, text_type
from smallcli.libs.shell import Shell

# main CLI application


def knetcli():
    cpath = os.path.dirname(os.path.abspath(__file__)) + "/cli"
    print "directory ", cpath

    cprefix = "KNet.cli."
    hdr = '''
    ****************************************************************
    *                                                               *
    *    Knet Virtual Network Topology Builder -   Interactive CLI  *
    *                                                               *
    *                                                               *
    *    Author:  KNet Solutions                                    *
    *                                                               *
    *****************************************************************
    '''
    cli = Shell(appname="KNet-cli", symbol="#", hdr=hdr, cmdpath=cpath,
                cmdprefix=cprefix)
    cli()
    print "exiting"

# if __name__ == "__main__":
#    cli(sys.argv)
