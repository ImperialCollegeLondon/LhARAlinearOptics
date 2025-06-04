#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "BeamIO" class
==============================

  BeamIO.py -- set "relative" path to code.

  Testing Write functionality.

"""

import os

import BeamIO   as bmIO
import BeamLine as BL

##! Start:
print("========  BeamIO (write): tests start  ========")

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
    ibmIOr = bmIO.BeamIO("12-Data4Tests", "Data4Tests.dat", "Test")
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
ibmIOr = bmIO.BeamIO("12-Data4Tests", "V2Data4Tests.dat")
print("         ---> ibmIOr: id, file:", id(ibmIOr), ibmIOr.getdataFILE())

bmIO.BeamIO.cleanBeamIOfiles

ibmIOw = bmIO.BeamIO("99-Scratch", "Data4Tests.dat", True)
print("         ---> ibmIOw: id, file:", id(ibmIOw), ibmIOw.getdataFILE(), \
      "\n")

#.. __str__:
print("     __str__:")
print(ibmIOw)

#.. __str__:
print("     __repr__:", repr(ibmIOw), "\n")

print(" <---- Built in method tests done.")


##! Test writing and reading of beam-line setup:
BeamIOTest += 1
print()
print("BeamIOTTest:", BeamIOTest, \
      " check writing and reading of beam-line setup.")

LhARAOpticsPATH    = os.getenv('LhARAOpticsPATH')
filename     = os.path.join(LhARAOpticsPATH, \
#                '11-Parameters/LhARABeamLine-Params-LsrDrvn-Gabor.csv')
#                '11-Parameters/LhARABeamLine-Params-LsrDrvn-Solenoid.csv')
#                '11-Parameters/LhARABeamLine-Params-Gauss-Gabor.csv')
                '11-Parameters/LhARABeamLine-Params-Gauss-Solenoid.csv')
LhARAFclty  = BL.BeamLine(filename)
#print(LhARAFclty)

LhARAFclty.writeBeamLine(ibmIOw.getdataFILE())
#bmIO.BeamIO.setDebug(True)
#bmIO.BeamIO.setDebug(False)

LhARAFclty.trackBeam(1000, ibmIOw.getdataFILE())

ibmIOw.flushNclosedataFile(ibmIOw.getdataFILE())

print(" <---- Writing and reading of beam-line setup tests done.")


##! Complete:
print()
print("========  BeamIO (write): tests complete  ========")
