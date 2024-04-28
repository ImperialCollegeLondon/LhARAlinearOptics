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
filename     = os.path.join(LhARAOpticsPATH, \
                '11-Parameters/LhARABeamLine-Params-LsrDrvn-Gabor.csv')
#                '11-Parameters/LhARABeamLine-Params-LsrDrvn-Solenoid.csv')
#                '11-Parameters/LhARABeamLine-Params-Gauss-Gabor.csv')
#                '11-Parameters/LhARABeamLine-Params-Gauss-Solenoid.csv')

##! Start:
print("========  LhARAFacility: tests start  ========")

##! Test singleton class feature:
LhARAFacilityTest = 1
print()
print("LhARAFacilityTest:", LhARAFacilityTest, \
      " check if class is a singleton.")
LhARAFclty  = BL.BeamLine(filename)
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

##! Complete:
print()
print("========  LhARAFacility: tests complete  ========")
