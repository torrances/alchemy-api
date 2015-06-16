#!/usr/bin/python

###################################################################################
###																				###
###	 PURPOSE																	###
###	 generates a tab-separated values file with  alchemy-api taxonomy output	###
###																				###
###	 CREATED																	###
###  10:34 PM 6/15/2015	craigtrim@gmail.com										###
###																				###
###################################################################################

from __future__ import print_function
from alchemyapi import AlchemyAPI
import argparse  
import file_utils
import json
import sys
import os
from collections import namedtuple

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

def taxonomize(text) :
	rows = []
	response = alchemyapi.taxonomy('text', text)
	if response['status'] == 'OK' :
		parsed_json = json.loads(json.dumps(response))
		for node in parsed_json['taxonomy']:
			rows.append(("{0}\t{1}\t{2}\n".format(node['score'], node['label'], text)))
	return rows


for file in file_utils.getfiles(args.input, "txt", True) :
	text = "";

	fname = file.split("/")[-1]
	print("*Input Filename is {0} from file {1}".format(fname, file))

	target = open("{0}/{1}.tsv".format(args.output, fname), "w+")

	lines = [line.rstrip('\n') for line in open(file)]
	for line in lines :
		text = text + " " + line

		for row in taxonomize(line) :
			target.write(row)

	for row in taxonomize(text) :
		target.write(row)

	target.close