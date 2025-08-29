#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "UnbstableParticle" class
================================

  Particle.py -- set "relative" path to code

"""

import os
import sys
import numpy as np

import BeamLine as BL
import Particle as Prtcl

##! Start:
print("========  Unstable Particle: tests start  ========")

##! Test trap of no reference particle:
UnstableParticleTest = 0
print()
print("ParticleTest:", UnstableParticleTest, \
      " check need reference particle first!")
try:
    PrtcltInst = Prtcl.Particle()
except:
    print("     ----> Successfully trapped no reference particle")
else:
    print("     ----> Failed successfully to trapped no reference particle", \
          " abort")
    raise Exception()
Prtcl.Particle.cleanParticles()

##! Now create reference particle:
HOMEPATH = os.getenv('HOMEPATH')
filename = os.path.join(HOMEPATH, \
                        '11-Parameters/LIONBeamLine-Params-LsrDrvn.csv')
BLI  = BL.BeamLine(filename)
print(BLI)

##! Test built-in methods:
UnstableParticleTest = 1
print()
print("UnstableParticleTest:", UnstableParticleTest, \
      " check built-in methods.")

#.. __init__
print("    __init__:")
PrtcltInst = Prtcl.UnstableParticle("pion")

PrtcltInst.setLocation("Place 1")
PrtcltInst.setz(1.1)
PrtcltInst.sets(1.2)
TrcSpc = np.array([0.1, 0.002, 0.2, 0.004, 0., 18.])
PrtcltInst.setTraceSpace(TrcSpc)
PrtcltInst.setLocation("Place 2")
PrtcltInst.setz(2.1)
PrtcltInst.sets(2.2)
TrcSpc = np.array([0.15, 0.0025, 0.25, 0.0045, 0., 18.5])
PrtcltInst.setTraceSpace(TrcSpc)
#.. __repr__
print("    __repr__:")
print("      ---->", repr(PrtcltInst))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(PrtcltInst)
print("    <---- __str__ done.")


##! Get second particle - check decay time is different:
#   check when decay time for the particle is set.
UnstableParticleTest = 2
print()
print("UnstableParticleTest:", UnstableParticleTest, " check if decay lengths are random")
PrtcltInst2 = Prtcl.UnstableParticle("pion")
PrtcltInst2.initremainingPath(3.0)
PrtcltInst3 = Prtcl.UnstableParticle("pion")
PrtcltInst3.initremainingPath(3.0)

PrtcltInst2.print()
PrtcltInst3.print()
#print(PrtcltInst2)
#print(PrtcltInst3)


#if (abs(PrtcltInst2.getremainingPath() - PrtcltInst3.getremainingPath()) < 0.0001):
#    print ("Path lengths of the two particles are too close")
#    print ("fail on test ", UnstableParticleTest)
#    sys.exit(0)
#else:
#    print ("Path lengths of the two particles are different - test passed")

UnstableParticleTest = 3
print()
print("UnstableParticleTest:", UnstableParticleTest, " check proton is stable and path infinite." )
ProtonInst = Prtcl.UnstableParticle("proton")
ProtonInst.initremainingPath(3.0)
#Prtcl.UnstableParticle.setDebug(True)
#ProtonInst.print()
print(ProtonInst)
#Prtcl.UnstableParticle.setDebug(False)

print()
UnstableParticleTest = 4
print("UnstableParticleTest:", UnstableParticleTest, " check response to unknown particle type.")
try:
    uKInst = Prtcl.UnstableParticle("neutrino")
except:
    print ("correctly trapped non existant unstable particle - neutrino")

print()
print("========  UnstableParticle: tests complete  ========")
