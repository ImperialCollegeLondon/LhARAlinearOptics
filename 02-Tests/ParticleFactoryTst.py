#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "ParticleFactory" class
================================

"""

import os
import sys

import BeamLine as BL
import Particle as Prtcl
from ParticleFactory import ParticleFactory

##! Start:
print("========  ParticleFactory: tests start  ========")

##! Create run and 
FactoryTest = 0
print("FactoryTest:", FactoryTest, " check need reference particle first!")
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

print()
FactoryTest = FactoryTest + 1
print("ParticleFactory:", FactoryTest, " create stable particle - and print it")
p1 = ParticleFactory.createParticle("proton")
p1.print()

print()
FactoryTest = FactoryTest + 1
print("ParticleFactory:", FactoryTest, " create unstable particle - and print it")
p2 = ParticleFactory.createParticle("pion")
p2.print()

print()
FactoryTest = FactoryTest + 1
print("ParticleFactory:", FactoryTest, " Check attempt to instantiate ParticleFactory")
try:
    pf = ParticleFactory()
except:
    print ("ParticleFactory class sucessfully intercepted attempt to instantiate")
else:
    print ("ParticleFactory class failed to intercept attempt to instantiate")

print()
FactoryTest = FactoryTest + 2
print("ParticleFactory:", FactoryTest, " Check Debug flag, should be False, True, True, False")
print ("ParticleFactory debug is ", ParticleFactory.getDebug())
ParticleFactory.setDebug(True)
print ("ParticleFactory debug is ", ParticleFactory.getDebug())
ParticleFactory.setDebug(True)
ParticleFactory.setDebug(False)

print()
print("========  ParticleFactory: tests complete  ========")
