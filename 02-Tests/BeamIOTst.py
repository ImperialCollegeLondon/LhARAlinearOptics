#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "BeamIO" class
==============================

  BeamIO.py -- set "relative" path to code

"""

import os
import BeamIO as bmIO

##! Start:
print("========  BeamIO: tests start  ========")

##! Test checks for bad input ...
BeamIOTest = 1
print()
print("BeamIOTest:", BeamIOTest, " checks for vetoing bad i/p arguments.")

try:
    ibmIO  = bmIO.BeamIO()
except:
    print("     ----> Successfully trapped no input arguments")

try:
    ibmIO  = bmIO.BeamIO("99-Scratch")
except:
    print("     ----> Successfully trapped path but no file")
    
try:
    ibmIO  = bmIO.BeamIO("Dummy", "Dummy")
except:
    print("     ----> Successfully trapped bad path")
    
try:
    ibmIOr = bmIO.BeamIO("11-Parameters", "Data4Tests.dat", "Test")
except:
    print("     ----> Successfully trapped bad create flag")

print(" <---- Bad input argument tests done.")

bmIO.BeamIO.cleanBeamIOfiles

##! Test built-in methods:
BeamIOTest += 1
print()
print("BeamIOTTest:", BeamIOTest, \
      " check built-in methods.")

#.. __init__:
print("     __init__:")
ibmIOr = bmIO.BeamIO("11-Parameters", "Data4Tests.dat")
print("         ---> ibmIOr: id, file:", id(ibmIOr), ibmIOr.getdataFILE())
ibmIOw = bmIO.BeamIO("99-Scratch", "Data4Tests.dat", True)
print("         ---> ibmIOw: id, file:", id(ibmIOw), ibmIOw.getdataFILE(), "\n")
#bmIO.BeamIO.setDebug(True)
#bmIO.BeamIO.setDebug(False)

#.. __str__:
print("     __str__:")
print(ibmIOw)

#.. __str__:
print("     __repr__:", repr(ibmIOw), "\n")

print(" <---- Built in method tests done.")



##! Complete:
print()
print("========  BeamIO: tests complete  ========")
