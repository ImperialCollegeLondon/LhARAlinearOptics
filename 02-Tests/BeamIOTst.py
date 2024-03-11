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

LhARAOpticsPATH = os.getenv('LhARAOpticsPATH')
filename        = os.path.join(LhARAOpticsPATH, \
                        '11-Parameters/LhARABeamLine-Params-Gauss-Gabor.csv')
rootfilename    = os.path.join(LhARAOpticsPATH, \
                            '99-Scratch/LhARA-BeamIO-tst.dat')

##! Test checks for bad input ...
BeamIOTest = 1
print()
print("BeamIOTest:", BeamIOTest, " checks for vetoing bad i/p arguments.")

ibmIO  = bmIO.BeamIO()

print(" <---- Bad input argument tests done.")


##! Test built-in methods:
BeamIOTest += 1
print()
print("BeamIOTTest:", BeamIOTest, \
      " check built-in methods.")

#.. __init__:
print("     __init__:")
ibmIO = bmIO.BeamIO()
print("         ---> ibmIO: id:", id(ibmIO), "\n")

#.. __str__:
print("     __str__:")
print(ibmIO)

#.. __str__:
print("     __repr__:", repr(ibmIO), "\n")

print(" <---- Built in method tests done.")



##! Complete:
print()
print("========  BeamIO: tests complete  ========")
