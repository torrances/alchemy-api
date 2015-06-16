#!/usr/bin/python
import json
import sys
import os
import argparse

##  ARGPARSE USAGE  
 ##  <https://docs.python.org/2/howto/argparse.html>  
parser = argparse.ArgumentParser(description="Visualize AlchemyAPI Taxonomy")  
group = parser.add_mutually_exclusive_group()  
group.add_argument("-v", "--verbose", action="store_true")  
group.add_argument("-q", "--quiet", action="store_true")  
parser.add_argument("input", help="The input path to an AlchemyAPI Taxonomy TSV Output file")  
parser.add_argument("output", help="The output path for writing (exporting).")  
args = parser.parse_args()

infile = args.input
outfile = "{0}.d".format(args.output)

file = open(infile)
graph = open(outfile, "w+")
graph.write("digraph temp {\n")

dict = {}

lines = [line.rstrip('\n') for line in file]
for line in lines:
	
	taxonomy = line.split("\t")[1]
	taxonomy = taxonomy.replace(", ", "_")
	taxonomy = taxonomy.replace(" and ", "_")
	taxonomy = taxonomy.replace(" ", "_")

	score = line.split("\t")[0]

	for entity in taxonomy[1:].split("/") : 
		if entity in dict :
			dict[entity] = float(dict[entity]) + float(score)
		else:
			dict[entity] = score

	graph.write("\t{0} -> {1}\n".format("thing", taxonomy[1:].split("/")[0]))
	graph.write("\t{0}\n".format(taxonomy[1:].replace("/", " -> ")))


for entity in dict :
	score = str(dict[entity])
	pos = score.find("e")
	if pos != -1 : 
		score = score[:pos]
	graph.write("\t{0} [shape=ellipse, height={1}];\n".format(entity, score))

graph.write("}")

graph.close
file.close

# create graph
print(outfile)
# dot -Tpng -O str(outfile)