#!/usr/bin/env python3
import sys
import subprocess
import re
import pprint
import treetaggerwrapper
import glob

try:
    import argparse
except ImportError:
    checkpkg.check(['python-argparse'])

import time
import socket

"""

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

USAGE = './treetagger.py language_treetagger language_parfile source_directory target_directory'

def build_parser():

    parser = argparse.ArgumentParser(description='treetagger - tokenization, pos-tagging and lemmatization using Schmidt\'s treetagger')


    parser.add_argument('language')
    parser.add_argument('parfile')
    parser.add_argument('source')
    parser.add_argument('target')

    return parser

def main():

    global debug

    parser = build_parser()
    args = parser.parse_args()

    '''Check arguments'''    
    if check_args(args) is False:
     sys.stderr.write("There was a problem validating the arguments supplied. Please check your input and try again. Exiting...\n")
     sys.exit(1)

    '''Unknown function, I'll check it later''' 
    start_time = time.time()
    for filename in sorted(glob.glob(args.source+'/*.xml')):
        tagger= treetaggerwrapper.TreeTagger(TAGDIR='.',TAGLANG=args.language,TAGPARFILE=args.parfile)
        tagger.tag_file_to(filename,args.target+filename.split('/')[3].split('.')[0]+".vrt")
       
def check_args(args):
    '''Exit if required arguments not specified'''
    check_flags = {}

def exec_command(command):
    """Execute command.
       Return a tuple: returncode, output and error message(None if no error).
    """
    sub_p = subprocess.Popen(command,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    output, err_msg = sub_p.communicate()
    return (sub_p.returncode, output, err_msg)


if __name__ == "__main__":
    main()
    sys.exit(0)

