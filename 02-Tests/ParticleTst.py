#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "Particle" class
================================

  Particle.py -- set "relative" path to code

"""

import os
import sys
import numpy as np

import BeamLine as BL
import Particle as Prtcl

##! Start:
print("========  Particle: tests start  ========")

##! Test trap of no reference particle:
ParticleTest = 0
print()
print("ParticleTest:", ParticleTest, \
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
ParticleTest = 1
print()
print("ParticleTest:", ParticleTest, \
      " check built-in methods.")

#.. __init__
print("    __init__:")
PrtcltInst = Prtcl.Particle()

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

##! Check get methods:
ParticleTest = 3
print()
print("ParticleTest:", ParticleTest, " check get methods.")
print("    ----> print(instance); tests all get methods")
print(PrtcltInst)

##! Check remaining set methods:
ParticleTest = 4
print()
print("ParticleTest:", ParticleTest, " check set method.")
Prtcl.Particle.setDebug(True)
print(PrtcltInst)
Prtcl.Particle.setDebug(False)

ParticleTest = 5
print("ParticleTest:", ParticleTest, " check particle is pion.")
PionInst = Prtcl.Particle("pion")
Prtcl.Particle.setDebug(True)
print(PionInst)
Prtcl.Particle.setDebug(False)

ParticleTest = 6
print("ParticleTest:", ParticleTest, " check particle is muon.")
MuonInst = Prtcl.Particle("Muon")
Prtcl.Particle.setDebug(True)
print(MuonInst)
Prtcl.Particle.setDebug(False)

ParticleTest = 7
print("ParticleTest:", ParticleTest, " check explicit particle proton.")
ProtonInst = Prtcl.Particle("proton")
Prtcl.Particle.setDebug(True)
print(ProtonInst)
Prtcl.Particle.setDebug(False)

ParticleTest = 8
print("ParticleTest:", ParticleTest, " check response to unknown particle type.")
uKInst = Prtcl.Particle("neutrino")
Prtcl.Particle.setDebug(True)
print(uKInst)
Prtcl.Particle.setDebug(False)

"""
Legacy; wont work as delete instances after generating ... needs to check
        fillPhaseSpaceAll

##! Check extraction of phase-space:
ParticleTest += 1
print()
Prtcl.Particle.cleanParticles()
Prtcl.ReferenceParticle.cleaninstance()
refPrtcl  = Prtcl.ReferenceParticle()
refPrtclSet = refPrtcl.setReferenceParticle()
print("ParticleTest:", ParticleTest, " check extraction of phase space.")
BLI.setSrcTrcSpc(np.array([0.0001, -0.0001, 0.0002, 0.0001, 0., 20.]))
BLI.setDebug(True)
OK = BLI.trackBeam(1)
BLI.setDebug(False)
print(" Here:", OK)
Prtcl.Particle.setDebug(True)
print(" <---- Prtcl.Particle.fillPhaseSpaceAll():", \
      Prtcl.Particle.fillPhaseSpaceAll())
"""

##! Complete:
print()
print("========  Particle: tests complete  ========")
