#!/usr/bin/python

from __future__ import print_function
import argparse  
import os
import fnmatch

 ## RETRIEVE files from filesystem
def getfiles(path, ext, verbose=True) :  

  if len(path) <= 1 :   
    print("!Please Supply an Input File");
    return []  

  try :
    input_path = str(path).strip()
    
    if os.path.exists(input_path) == 0 :
      if verbose :
        print ("!Input Path does not exist (input_path = {0})".format(input_path))
      return []
   
    if os.path.isdir(input_path) == 0 :
      if verbose :
        print ("*Input Path is Valid (input_path = {0})".format(input_path))
      return input_path

    matches = []
    for root, dirs, files in os.walk(path, topdown=False):
      for filename in fnmatch.filter(files, "*." + ext):
        matches.append(os.path.join(root, filename))
             
    if len(matches) > 0 :
      if verbose :
        # used <http://stackoverflow.com/questions/3395138/using-multiple-arguments-for-string-formatting-in-python-e-g-s-s>
        print ("*Found Files in Path (input_path = {0}, total-files = {1})".format(input_path, len(matches)))
      return matches
   
      if verbose :
        print ("!No Files Found in Path (input_path = {0})".format(input_path))

  except ValueError :
    print ("!Invalid Input (input_path = {0})".format(input_path))
  
  if verbose :
    print("!Returning Empty File Array")
  return []