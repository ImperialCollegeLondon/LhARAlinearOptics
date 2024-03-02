#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "Beam" class
============================

  Beam.py -- set "relative" path to code

"""

import os
import numpy as np

import BeamLine as BL
import Beam as Bm

##! Start:
print("========  Beam: tests start  ========")

##! Test trap of no reference particle:
BeamTest = 0
print()
print("BeamTest:", BeamTest, " check need reference particle first!")
try:
    BmInst = Bm.Beam()
except:
    print("     ----> Successfully trapped no reference beam")
else:
    print("     ----> Failed successfully to trapped no reference beam", \
          " abort")
    raise Exception()
Bm.Beam.cleanBeams()

##! Now create reference beam:
HOMEPATH = os.getenv('HOMEPATH')
filename = os.path.join(HOMEPATH, \
                        '11-Parameters/LIONBeamLine-Params-LsrDrvn.csv')
BLI  = BL.BeamLine(filename)
print(BLI)

##! Test built-in methods:
BeamTest = 1
print()
print("BeamTest:", BeamTest, " check built-in methods.")

#.. __init__
print("    __init__:")
BmInst = Bm.Beam()

BmInst.setLocation("Place 1")
BmInst.sets(1.2)

BmInst.setLocation("Place 2")
BmInst.sets(2.2)

#.. __repr__
print("    __repr__:")
print("      ---->", repr(BmInst))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(BmInst)
print("    <---- __str__ done.")

##! Check get methods:
BeamTest = 3
print()
print("BeamTest:", BeamTest, " check get methods.")
print("    ----> print(instance); tests all get methods")
print(BmInst)

##! Check remaining set methods:
BeamTest = 4
print()
print("BeamTest:", BeamTest, " check set method.")
Bm.Beam.setDebug(True)
print(BmInst)
Bm.Beam.setDebug(False)


##! Complete:
print()
print("========  Beam: tests complete  ========")
