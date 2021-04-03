# config.py

# This will contain special paths and variables that will be used across the project

import os,sys
import pandas as pd


def root_dir(): 
    ''' Find the root directory for this github repository ''' 
    dir2 = os.path.dirname(os.path.realpath(__file__))
    dir1 = os.path.split(dir2)[0]
    return os.path.split(dir1)[0]

ROOT_DIR = root_dir()
DATA_DIR = os.path.join(ROOT_DIR,'data')
