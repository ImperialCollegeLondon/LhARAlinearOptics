#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "Solenoid" class
===============================

Solenoid.py -- set "relative" path to code

"""

import os
import numpy as np

import BeamLineElement as BLE
import LIONbeam        as LNb
import Particle        as Prtcl

HOMEPATH = os.getenv('HOMEPATH')
filename = os.path.join(HOMEPATH, \
                        '11-Parameters/LIONBeamLine-Params-LsrDrvn.csv')
LNbI  = LNb.LIONbeam(filename)

iRefPrtcl = Prtcl.ReferenceParticle.getinstance()


##! Start:
print("========  Solenoid: tests start  ========")

print("Reference particle:")
xx    = iRefPrtcl.getPrIn()[0]
xx[2] = 194.7585262
iRefPrtcl._PrIn[0] = xx
p0        = iRefPrtcl.getMomentumIn(0)
with np.printoptions(linewidth=500,precision=7,suppress=True):
    print("     ----> Three momentum (in, RPLC):", \
          iRefPrtcl.getPrIn()[0][0:3])
    print("                           Magnitude:", p0)


##! Test built in methods:
SolenoidTest = 1
print()
print("SolenoidTest:", SolenoidTest, \
      " check built-in methods.")

#.. __init__
print("    __init__:")
try:
    Sol = BLE.Solenoid()
except:
    print('      ----> Correctly trapped no argument exception.')
rCtr = np.array([0.,0.,0.])
vCtr = np.array([0.,0.])
drCtr = np.array([0.,0.,0.])
dvCtr = np.array([0.,0.])
try:
    Sol = BLE.Solenoid("Solenoid1", rCtr, vCtr, drCtr, dvCtr)
except:
    print('      ----> Correctly trapped no solenoid length exception.')

#.. Create valid instance:
Sol = BLE.Solenoid("Solenoid2", rCtr, vCtr, drCtr, dvCtr, 0.5, 1.4)
    
#.. __repr__
print("    __repr__:")
print("      ---->", repr(Sol))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(str(Sol))
print("    <---- __str__ done.")

##! Check get methods:
SolenoidTest = 3
print()
print("SolenoidTest:", SolenoidTest, " check get methods.")
print("    ----> print() method; tests all get methods")
print(Sol)

##! Check set method:
SolenoidTest = 4
print()
print("SolenoidTest:", SolenoidTest, " check set method.")
BLE.Solenoid.setDebug(True)
print(Sol)
BLE.Solenoid.setDebug(False)

##! Check set method:
SolenoidTest += 1
print()
print("SolenoidTest:", SolenoidTest, " test transport through solenoid.")
R      = np.array([0.5, 0.1, -0.3, -0.2, 0., 0.00])
Rprime = Sol.Transport(R)
print("     ----> Input trace-space vector:", R)
print("     ----> Transported trace-space vector:", Rprime)
RprimeTest = np.array([0.228273338, -0.166572584, -0.54739631, 0.092788839, \
                       0., 0. ])
Diff       = np.subtract(Rprime, RprimeTest)
Norm       = np.linalg.norm(Diff)
with np.printoptions(linewidth=500,precision=7,suppress=True):
    print("     ----> Difference Rprime - RprimeTest:", Diff)
print("     ----> Magnitude of Diff:", Norm)
if Norm > 1E-6:
    raise Exception(" !!!!----> FAILED:", \
                    "solenoid transport result not as expected.")
else:
    print(" <---- Solenoid transport test successful.")

##! Complete:
print()
print("========  Solenoid: tests complete  ========")
