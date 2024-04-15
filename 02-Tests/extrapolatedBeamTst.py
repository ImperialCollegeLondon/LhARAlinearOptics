#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "extrapolateBeam" class
============================

  extrapolateBeam.py -- set "relative" path to code

"""

import os
import sys
import numpy as np

import BeamLine as BL
import Beam     as Bm

##! Start:
print("========  extrapolateBeam: tests start  ========")

##! Test trap of no reference particle:
extrapolateBeamTest = 0
print()
print("extrapolateBeamTest:", extrapolateBeamTest, \
      " check need reference particle first!")
try:
    exBmInst = Bm.extrapolateBeam()
except:
    print("     ----> Successfully trapped no reference beam")
else:
    print("     ----> Failed successfully to trap no reference beam", \
          " abort")
    raise Exception()
Bm.extrapolateBeam.cleanextrapolateBeams()

##! Now create reference beam:
HOMEPATH = os.getenv('HOMEPATH')
filename = os.path.join(HOMEPATH, \
                        '11-Parameters/LIONBeamLine-Params-Gauss.csv')

##! Now create pointer to input data file:
inputdatafile = os.path.join(HOMEPATH, \
                       '11-Parameters/Data4Tests.dat')

##! Now create pointer to output data file:
outputdatafile = os.path.join(HOMEPATH, \
                       '99-Scratch/extrapolateBeamParamteres.csv')

##! Test input arguments:
extrapolateBeamTest += 1
print()
print("extrapolateBeamTest:", extrapolateBeamTest, \
      " check trap no beam specification file!")
try:
    exBmInst = Bm.extrapolateBeam()
except:
    print("     ----> Successfully trapped no beam specigication file")
else:
    print(\
    "     ----> Failed successfully to trap no beam specification file", \
          " abort")
    raise Exception()
Bm.extrapolateBeam.cleanextrapolateBeams()

##! Create valid instance
extrapolateBeamTest += 1
print()
print("extrapolateBeamTest:", extrapolateBeamTest, " create valid instance:")
exBmInst = Bm.extrapolateBeam(inputdatafile, 1000, outputdatafile, None, \
                               filename)

##! Create valid instance
extrapolateBeamTest += 1
print()
print("extrapolateBeamTest:", extrapolateBeamTest, " test built-in methods:")
#.. __repr__
print("    __repr__:")
print("      ---->", repr(exBmInst))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
#print(exBmInst)
print("    <---- __str__ done.")

##! Check creation of report:
extrapolateBeamTest += 1
print()
print("extrapolateBeamTest:", extrapolateBeamTest, " creation of pandas report.")
print(BL.BeamLine.getinstance())

exBmInst.extrapolateBeam()
exBmInst.createReport()
#print(exBmInst)

##! Check start of calculation beyond source:
extrapolateBeamTest += 1
print()
print("extrapolateBeamTest:", extrapolateBeamTest, \
      " start extrapolation beyond source:")
exBmInst.getInputDataFile().close()
Bm.extrapolateBeam.cleanextrapolateBeams()
exBmInst = Bm.extrapolateBeam(inputdatafile, 1000, outputdatafile, 3, \
                               filename)
exBmInst.extrapolateBeam()
exBmInst.createReport()
#print(exBmInst)


##! Complete:
print()
print("========  extrapolateBeam: tests complete  ========")
