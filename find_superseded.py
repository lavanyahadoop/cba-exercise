# Python program which takes a directory as its argument and lists the file which are redundant and could be deleted.
# Project: CBA Exercise
# Author: Lavanya Soundarrajan
# Last Updated: 25/08/2018
# Usage: python find_superseded.py  D:\Works\myfiles

import os
import platform
import datetime
import os.path
import re
from pathlib import Path
import sys

fn = sys.argv[1]
if os.path.exists(fn):
    #raw = '/users/home/Desktop/myfiles1/'
    path = Path(fn)

# Find the last modified date for the given file
    files_container = []
    def creation_date(path_to_file):
        if platform.system() == 'Windows':
            return str(datetime.datetime.fromtimestamp(os.path.getmtime(path_to_file)))
        else:
            stat = os.stat(path_to_file)
            return str(datetime.datetime.fromtimestamp(stat.st_mtime))

# get list of files from the given input path
    matches = []
    for dirName, subdirList, fileList in os.walk(path):
        fileList = [f for f in fileList if not f[0] == '.']  # ignores hidden files if any during search
        subdirList[:] = [d for d in subdirList if not d[0] == '.']  # ignores hidden directories if any during search
        for fname in fileList:
            matches.append(os.path.join(dirName, fname))
    print( "\n" )

# Algorithm to find the superseded file details based on last modified date
    for level1_item in matches:
        level1_head, level1_tail = os.path.split(level1_item)
        for level2_item in matches:
            if(level1_item != level2_item):
                level2_head, level2_tail = os.path.split(level2_item)
                level1_file_name_without_extn  = os.path.splitext(level1_tail)[0]
                level2_file_name_without_extn = os.path.splitext(level2_tail)[0]
                level1_extn = os.path.splitext(level1_tail)[1]
                level2_extn = os.path.splitext(level2_tail)[1]
                if (level1_file_name_without_extn == level2_file_name_without_extn and (re.search('(\.bak|\.bk+)', level1_extn) or (re.search('(\.bak|\.bk+)', level2_extn)) or (level1_tail == level2_tail))):
                    if (creation_date(level1_item) > creation_date(level2_item)): #last modified date check
                        print(level2_item + " may be superseded by " + level1_item)
    print("\n")