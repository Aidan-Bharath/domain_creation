# -*- coding: utf-8 -*-
"""
Created on Sun Mar 08 17:40:39 2015

@author: ABHARATH
"""

import psutil, os

def killProcTree(pid, including_parent=False):    
    pid = os.getpid()    
    parent = psutil.Process(pid)
    for child in parent.children(recursive=True):
        child.kill()
    if including_parent:
        parent.kill()

if __name__ == "__main__":
    killProcTree(0)