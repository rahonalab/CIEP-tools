#!/usr/bin/env python3
import sys
import subprocess
import nltk
import re
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

USAGE = './xmlize.py language_sentence_splitter source_directory target_directory'

def build_parser():

    parser = argparse.ArgumentParser(description='xmlize - Convert CIEP texts to XML')

    parser.add_argument('language')
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
    for filename in sorted(glob.glob(args.source+'/*.txt')):
        '''Create new file as target/filename.xml''' 
        xmlfile= open(args.target+filename.split('/')[3].split('.')[0]+".xml","w+") 
        file_content = open(filename).read()
        '''Identify header'''
        header = re.findall(r'@.*',file_content)
    
        '''Beginning of file'''
        xmlfile.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
        xmlfile.write("<text ")
        '''Format and print header'''
        for feature in header:
            if feature != '@endheader':
                value = feature.split('=')
                xmlfile.write(re.sub('@','',value[0])+"=\""+value[1]+"\" ")
        xmlfile.write(">\n<body>\n")
    
        '''Split text into sentences and annotate it'''
        from nltk.tokenize import sent_tokenize
        '''Clean up nasty characters'''
        '''Remove the ^M thing and substitute the RIGHT SINGLE QUOTATION MARK (U+0219) with the Apostrophe (U+0027)'''
        sentences=sent_tokenize(re.sub(r'(?m)^\@.*\n?','',file_content.replace('’', '\'').replace('\x0C', '').replace('‘', '\'')),language=args.language)
        for sentence in enumerate(sentences,1):
            xmlfile.write("<s id=\""+str(sentence[0])+"\">"+sentence[1]+"</s>\n")
    
        '''Close body & text'''
        xmlfile.write("</body>\n</text>")
        '''Close file'''
        xmlfile.close()

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

