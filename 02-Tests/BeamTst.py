#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "Beam" class
============================

  Beam.py -- set "relative" path to code

"""

import os
import numpy as np

import Particle        as Prtcl
import BeamLineElement as BLE
import BeamLine        as BL
import Beam            as Bm

##! Start:
print("========  Beam: tests start  ========")

##! Test trap of no reference particle:
BeamTest = 0
print()
print("BeamTest:", BeamTest, \
      " check need reference particle first!")
try:
    BmInst = Bm.Beam()
except:
    print("     ----> Successfully trapped no argument exception")
else:
    print("     ----> Failed successfully to trapped no argument exception:",\
          " abort")
    raise Exception()
Bm.Beam.cleanBeams()

##! Now create pointer to input data file:
HOMEPATH = os.getenv('HOMEPATH')
inputdatafile = os.path.join(HOMEPATH, \
                       '11-Parameters/Data4Tests.dat')

##! Now create pointer to output data file:
outputdatafile = os.path.join(HOMEPATH, \
                       '99-Scratch/BeamParameters.csv')

##! Create valid instance
BeamTest += 1
print()
print("BeamTest:", BeamTest, " create valid instance:")
BmInst = Bm.Beam(inputdatafile, 1000, outputdatafile, None)

##! Test buit-in methods:
BeamTest += 1
print()
print("BeamTest:", BeamTest, " test built-in methods:")
#.. __repr__
print("    __repr__:")
print("      ---->", repr(BmInst))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(BmInst)
print("    <---- __str__ done.")

##! Check creation of report:
BeamTest += 1
print()
print("BeamTest:", BeamTest, \
      " creation of pandas report.")

BmInst.evaluateBeam()
BmInst.createReport()

##! Check start of calculation beyond source:
BeamTest += 1
print()
print("BeamTest:", BeamTest, \
      " start extrapolation beyond source:")
outputdatafile = os.path.join(HOMEPATH, \
                       '99-Scratch/BeamParameters1.csv')
BmInst.getInputDataFile().close()
Bm.Beam.cleanBeams()
BL.BeamLine.cleaninstance()
BLE.BeamLineElement.cleaninstances()
Prtcl.Particle.cleanAllParticles()
BmInst = Bm.Beam(inputdatafile, 1000, outputdatafile, 3)
print(BmInst)
BmInst.evaluateBeam()
BmInst.createReport()

##! Complete:
print()
print("========  Beam: tests complete  ========")
