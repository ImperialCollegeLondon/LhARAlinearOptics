#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "LhARAFacility" class ... initialisation and get methods
=====================================

  BeamLine.py -- set "relative" path to code

"""

import BeamLine as BL
import Particle      as Prtcl
import sys
import os

LhARAOpticsPATH    = os.getenv('LhARAOpticsPATH')
print(LhARAOpticsPATH)
filename     = os.path.join(LhARAOpticsPATH, \
                        '11-Parameters/LhARABeamLine-Params-LsrDrvn.csv')

##! Start:
print("========  LhARAFacility: tests start  ========")

##! Test singleton class feature:
LhARAFacilityTest = 1
print()
print("LhARAFacilityTest:", LhARAFacilityTest, \
      " check if class is a singleton.")
LhARAFclty  = BL.BeamLine(filename)
Prtcl.ReferenceParticle.cleaninstance()
LhARAFclty1 = BL.BeamLine(filename)
print("    LhARAFclty singleton test:", id(LhARAFclty), id(LhARAFclty1), \
      id(LhARAFclty)-id(LhARAFclty1))
if LhARAFclty != LhARAFclty1:
    raise Exception("BeamLine is not a singleton class!")

##! Check built-in methods:
LhARAFacilityTest = 2
print()
print("LhARAFacilityTest:", LhARAFacilityTest, \
      " check built-in methods.")
print("    __repr__:")
print(LhARAFclty)

##! Check get methods:
LhARAFacilityTest = 3
print()
print("LhARAFacilityTest:", LhARAFacilityTest, " check get methods.")
print("    ----> Tests all get methods")
print(LhARAFclty)

##! Check set method:
LhARAFacilityTest = 4
print()
print("LhARAFacilityTest:", LhARAFacilityTest, " check set method.")
BL.BeamLine.setDebug(True)
print(LhARAFclty)
BL.BeamLine.setDebug(False)

##! Complete:
print()
print("========  LhARAFacility: tests complete  ========")
