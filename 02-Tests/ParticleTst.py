#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "Particle" class
================================

  Particle.py -- set "relative" path to code

"""

import numpy as np

import Particle as Prtcl

##! Start:
print("========  Particle: tests start  ========")

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
PhsSpc = np.array([0.1, 0.002, 0.2, 0.004, 0., 18.])
PrtcltInst.setPhaseSpace(PhsSpc)
PrtcltInst.setLocation("Place 2")
PrtcltInst.setz(2.1)
PrtcltInst.sets(2.2)
PhsSpc = np.array([0.15, 0.0025, 0.25, 0.0045, 0., 18.5])
PrtcltInst.setPhaseSpace(PhsSpc)

#.. __repr__
print("    __repr__:")
print("      ---->", repr(PrtcltInst))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(str(PrtcltInst))
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


##! Complete:
print()
print("========  Particle: tests complete  ========")
