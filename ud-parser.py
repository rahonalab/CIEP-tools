#!/usr/bin/env python3
import sys
import subprocess
import re
import pprint
import glob
import nltk
import spacy_udpipe
import os
import random

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

USAGE = './ud-parser.py language_model language_parfile source_directory target_directory task: (whole/random)'

def build_parser():

    parser = argparse.ArgumentParser(description='ud-parser - build beautiful CoNLL-U files from CIEP raw data')


    parser.add_argument('nltk',help='Punkt model for split sentence')
    parser.add_argument('ud',help='Universal Dependency model for parsing')
    parser.add_argument('source',help='Source for raw texts, must be dir/dir/dir')
    parser.add_argument('target',help='Target destination for processed texts')
    parser.add_argument('-s', '--shuffle', action='store_true', help='Randomized collection of 70 sentences')

    return parser


def check_args(args):
    '''Exit if required arguments not specified'''
    check_flags = {}

def sentencesplit(file_content):
    '''Clean up nasty characters'''
    '''Remove the ^M thing and substitute the RIGHT SINGLE QUOTATION MARK (U+0219) with the Apostrophe (U+0027)'''
    from nltk.tokenize import sent_tokenize        
    sentences=enumerate(sent_tokenize(re.sub(r'(?m)^\@.*\n?','',file_content.replace('’', '\'').replace('\x0C', '').replace('‘', '\'')),language=args.nltk),1)
    return sentences

def udparser(sentences,conllufile,newdoc):
    nlp = spacy_udpipe.load(args.ud)
    for sentence in sentences:
        conllufile.write("# sent_id = "+newdoc+"_s"+str(sentence[0])+"\n")
        conllufile.write("# text = "+sentence[1].replace('\n', '')+"\n")
        for token in nlp(sentence[1]):
            conllufile.write(str(token.i+1)+"\t"+token.text+"\t"+token.lemma_+"\t"+token.pos_+"\t"+token.tag_+"\t"+'_'+"\t"+str(token.head.i+1)+"\t"+token.dep_+"\t"+'_'+"\t"+'_\n')
        conllufile.write("\n")
    conllufile.close() 

def header(file_content,conllufile):
    '''Identify header'''
    header = re.findall(r'@.*',file_content)
    '''Beginning of file'''
    conllufile.write("# newdoc id ")
    '''Format and print header: we just take origtitle and language, and build a newdoc id accordingly'''
    for feature in header:
        if re.compile("@origtitle").search(feature):
                origtitle = feature.split('=')
        if re.compile("@language").search(feature):
                language = feature.split('=')
                newdoc = origtitle[1].split(' ')[0]+origtitle[1].split(' ')[1]+'_'+origtitle[1].split(' ')[4]+origtitle[1].split(' ')[5]+'_'+language[1]
    conllufile.write("= "+newdoc+"\n")
    return(newdoc)

def main():

    global debug
    global args

    parser = build_parser()
    args = parser.parse_args()

    spacy_udpipe.download(args.ud) # download language model
    '''Check arguments'''    
    if check_args(args) is False:
     sys.stderr.write("There was a problem validating the arguments supplied. Please check your input and try again. Exiting...\n")
     sys.exit(1)

    '''Unknown function, I'll check it later''' 
    start_time = time.time()

    for filename in sorted(glob.glob(args.source+'/*.txt')):
        file_content = open(filename).read()
        if args.shuffle:
            '''Create new file as target/random-language.conllu'''
            conllufile= open(args.target+"random-"+args.nltk+".conllu","a+")
            newdoc = header(file_content,conllufile)
            sentences=list(sentencesplit(file_content))
            from random import shuffle
            shuffle(sentences)
            udparser(sentences[1:10],conllufile,newdoc)
        else:
            '''Create new file as target/filename.conllu''' 
            conllufile= open(args.target+filename.split('/')[3].split('.')[0]+".conllu","w+")
            newdoc = header(file_content,conllufile)
            sentences=sentencesplit(file_content)
            udparser(sentences,conllufile,newdoc)
        
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

