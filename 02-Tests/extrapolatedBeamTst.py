#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "extrapolateBeam" class
============================

  extrapolateBeam.py -- set "relative" path to code

"""

import os
import numpy as np

import Particle        as Prtcl
import BeamLineElement as BLE
import BeamLine        as BL
import Beam            as Bm

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

##! Now create pointer to input data file:
HOMEPATH = os.getenv('HOMEPATH')
inputdatafile = os.path.join(HOMEPATH, \
                             '11-Parameters/Data4Tests.dat')

##! Now create pointer to output data file:
outputdatafile = os.path.join(HOMEPATH, \
                              '99-Scratch/exBeamParameters.csv')

##! Create valid instance
extrapolateBeamTest += 1
print()
print("extrapolateBeamTest:", extrapolateBeamTest, " create valid instance:")
exBmInst = Bm.extrapolateBeam(inputdatafile, 1000, outputdatafile, None)

##!Test built in methods:
extrapolateBeamTest += 1
print()
print("extrapolateBeamTest:", extrapolateBeamTest, " test built-in methods:")
#.. __repr__
print("    __repr__:")
print("      ---->", repr(exBmInst))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(exBmInst)
print("    <---- __str__ done.")

##! Check creation of report:
extrapolateBeamTest += 1
print()
print("extrapolateBeamTest:", extrapolateBeamTest, \
      " creation of pandas report.")

exBmInst.extrapolateBeam()
print(exBmInst)
exBmInst.createReport()

##! Check start of calculation beyond source:
extrapolateBeamTest += 1
print()
print("extrapolateBeamTest:", extrapolateBeamTest, \
      " start extrapolation beyond source:")
outputdatafile = os.path.join(HOMEPATH, \
                       '99-Scratch/exBeamParameters1.csv')
exBmInst.getInputDataFile().close()
Bm.Beam.cleanBeams()
BL.BeamLine.cleaninstance()
BLE.BeamLineElement.cleaninstances()
Prtcl.Particle.cleanAllParticles()
exBmInst = Bm.extrapolateBeam(inputdatafile, 1000, outputdatafile, 3)
exBmInst.extrapolateBeam()
print(exBmInst)
exBmInst.createReport()

##! Complete:
print()
print("========  extrapolateBeam: tests complete  ========")
