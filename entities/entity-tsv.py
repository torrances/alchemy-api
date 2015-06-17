#!/usr/bin/python

from __future__ import print_function
from alchemyapi import AlchemyAPI
import argparse  
import file_utils
import json
import sys
import os
from collections import namedtuple

# Create the AlchemyAPI Object
alchemyapi = AlchemyAPI()

##  ARGPARSE USAGE  
##  <https://docs.python.org/2/howto/argparse.html>  
parser = argparse.ArgumentParser(description="Call AlchemyAPI Taxonomy")  
group = parser.add_mutually_exclusive_group()  
parser.add_argument("input", help="The input path for importing. This can be either a file or directory.")  
parser.add_argument("output", help="The output path for writing (exporting).")  
args = parser.parse_args()
print("*Input Path is {0}".format(args.input))
print("*Output Path is {0}".format(args.output))

def extract(text) :
    response = alchemyapi.entities('text', text, {'sentiment': 1})
    rows = []
    if response['status'] != 'OK':
        print('Error in entity extraction call: ', response['statusInfo'])
        return rows
    else :
        for entity in response['entities']:
            rows.append("{0}\t{1}\t{2}\t{3}\n".format(
                entity['text'].encode('utf-8'), 
                entity['type'], 
                entity['relevance'], 
                entity['sentiment']['type']))
    return rows

def create(input, output) :
    for file in file_utils.getfiles(input, "txt", True) :

        fname = file.split("/")[-1]
        print("*Input Filename is {0} from file {1}".format(fname, file))

        target = open("{0}/{1}.tsv".format(output, fname), "w+")

        lines = [line.rstrip('\n') for line in open(file)]
        for line in lines :
            for row in extract(line) :
                target.write(row)
        
        target.close

create(args.input, args.output)