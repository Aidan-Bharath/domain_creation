# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 23:04:38 2015

@author: Aidan
"""

import numpy as np
import pandas as pd
from blaze import Data

def convBlaze(files):
    
    for i,j in files.iteritems():
        files[i] = Data(j)

    return files

def saveSQLite(files,saveDir):
    return
    



if __name__ == "__main__":
    
    files = convBlaze(files)