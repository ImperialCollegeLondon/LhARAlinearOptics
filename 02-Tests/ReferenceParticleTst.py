#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "ReferenceParticle" derived class
=================================================

  ReferenceParticle.py -- set "relative" path to code

"""

import os
import sys

import BeamLine as BL
import Particle as Prtcl

##! Start:
print("========  ReferenceParticle: tests start  ========")

##! Test singleton class feature:
ReferenceParticleTest = 1
print()
print("ReferenceParticleTest:", ReferenceParticleTest, \
      " check if class is a singleton.")
refPrtcl  = Prtcl.ReferenceParticle()
refPrtcl1 = Prtcl.ReferenceParticle()
if (id(refPrtcl) - id(refPrtcl)) != 0:
    print("    refPrtcl singleton test: FAIL!")
    raise Exception("ReferenceParticle is not a singleton class!")
else:
    print("    refPrtcl singleton test: success")


##! Check built-in methods:
ReferenceParticleTest = 2
print()
print("ReferenceParticleTest:", ReferenceParticleTest, \
      " check built-in methods.")
print("    __repr__:")
print(refPrtcl)

##! Check get methods:
ReferenceParticleTest = 3
print()
print("ReferenceParticleTest:", ReferenceParticleTest, " check get methods.")
print("    ----> Tests all get methods")
print(refPrtcl)

##! Check set method:
ReferenceParticleTest = 4
print()
print("ReferenceParticleTest:", ReferenceParticleTest, " check set method.")
refPrtcl.setRPDebug(True)
print(refPrtcl)
refPrtcl.setRPDebug(False)

##! Check get instance methodd:
ReferenceParticleTest += 1
print()
print("ReferenceParticleTest:", ReferenceParticleTest, \
      " check get instance method.")
print(Prtcl.ReferenceParticle.getinstances())


##! Load some geometry and then test reference particle load:
Prtcl.ReferenceParticle.cleaninstances()
ReferenceParticleTest += 1
print()
print("ReferenceParticleTest:", ReferenceParticleTest, \
      " load geometry and then test reference particle load.")
HOMEPATH = os.getenv('HOMEPATH')
filename = os.path.join(HOMEPATH, \
                        '11-Parameters/LIONBeamLine-Params-LsrDrvn.csv')
BLI  = BL.BeamLine(filename)
print(BLI)


##! Complete:
print()
print("========  ReferenceParticle: tests complete  ========")
