#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "GaborLens" class
===============================

BeamLineElement.py -- set "relative" path to code

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
print("========  GaborLens: tests start  ========")

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
GaborLensTest = 1
print()
print("GaborLensTest:", GaborLensTest, \
      " check built-in methods.")

#.. __init__
print("    __init__:")
try:
    Sol = BLE.GaborLens()
except:
    print('      ----> Correctly trapped no argument exception.')
rCtr = np.array([0.,0.,0.])
vCtr = np.array([0.,0.])
drCtr = np.array([0.,0.,0.])
dvCtr = np.array([0.,0.])
try:
    Sol = BLE.GaborLens("GaborLens1", rCtr, vCtr, drCtr, dvCtr)
except:
    print('      ----> Correctly trapped no solenoid length exception.')

#.. Create valid instance:
Sol = BLE.GaborLens("GaborLens2", rCtr, vCtr, drCtr, dvCtr, 0.5, 1.E15)
    
#.. __repr__
print("    __repr__:")
print("      ---->", repr(Sol))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(str(Sol))
print("    <---- __str__ done.")

##! Check get methods:
GaborLensTest = 3
print()
print("GaborLensTest:", GaborLensTest, " check get methods.")
print("    ----> print() method; tests all get methods")
print(Sol)

##! Check set method:
GaborLensTest = 4
print()
print("GaborLensTest:", GaborLensTest, " check set method.")
BLE.GaborLens.setDebug(True)
print(Sol)
BLE.GaborLens.setDebug(False)

##! Check set method:
GaborLensTest += 1
print()
print("GaborLensTest:", GaborLensTest, " test transport through solenoid.")
R      = np.array([0.5, 0.1, -0.3, -0.2, 0., 0.00])
Rprime = Sol.Transport(R)
print("     ----> Input trace-space vector:", R)
print("     ----> Transported trace-space vector:", Rprime)
RprimeTest = np.array([0.535307163, 0.040555484, -0.390519525, -0.16035225, \
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
    print(" <---- GaborLens transport test successful.")

##! Complete:
print()
print("========  GaborLens: tests complete  ========")
