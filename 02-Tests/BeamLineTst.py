#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "BeamLine" class ... initialisation and get methods
==========================

  BeamLine.py -- set "relative" path to code

"""

import BeamLine as BL
import Particle as Prtcl
import sys
import os

LhARAOpticsPATH    = os.getenv('LhARAOpticsPATH')
filename     = os.path.join(LhARAOpticsPATH, \
                        '11-Parameters/LhARABeamLine-Params-Gauss-Gabor.csv')

##! Start:
print("========  BeamLine: tests start  ========")

##! Test singleton class feature:
BeamLineTest = 1
print()
print("BeamLineTest:", BeamLineTest, \
      " check if class is a singleton.")
BmLn  = BL.BeamLine(filename)
BmLn1 = BL.BeamLine(filename)
print("    BmLn singleton test:", id(BmLn), id(BmLn1), \
      id(BmLn)-id(BmLn1))
if BmLn != BmLn1:
    raise Exception("BeamLine is not a singleton class!")

##! Check built-in methods:
BeamLineTest = 2
print()
print("BeamLineTest:", BeamLineTest, \
      " check built-in methods.")
print("    __repr__:")
print(BmLn)

##! Check get methods:
BeamLineTest = 3
print()
print("BeamLineTest:", BeamLineTest, " check get methods.")
print("    ----> Tests all get methods")
print(BmLn)

##! Check set method:
BeamLineTest = 4
print()
print("BeamLineTest:", BeamLineTest, " check set method.")
BL.BeamLine.setDebug(True)
print(BmLn)
BL.BeamLine.setDebug(False)

iRefPrtcl = Prtcl.ReferenceParticle.getinstance()
print(iRefPrtcl)

##! Complete:
print()
print("========  BeamLine: tests complete  ========")
