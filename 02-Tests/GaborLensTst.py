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
import BeamLine        as BL
import Particle        as Prtcl

HOMEPATH = os.getenv('HOMEPATH')
filename = os.path.join(HOMEPATH, \
                        '11-Parameters/LIONBeamLine-Params-LsrDrvn.csv')
BLI  = BL.BeamLine(filename)

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
    GbL = BLE.GaborLens()
except:
    print('      ----> Correctly trapped no argument exception.')
rStrt = np.array([0.,0.,0.])
vStrt = np.array([0.,0.])
drStrt = np.array([0.,0.,0.])
dvStrt = np.array([0.,0.])
try:
    GbL = BLE.GaborLens("GaborLens1", rStrt, vStrt, drStrt, dvStrt)
except:
    print('      ----> Correctly trapped no solenoid GbL args exception.')

#.. Create valid instance:
BLE.GaborLens.setDebug(True)
GbL = BLE.GaborLens("GaborLens2", rStrt, vStrt, drStrt, dvStrt, \
                    0.2, 65.E3, 0.06, 0.05, 0.5)
BLE.GaborLens.setDebug(False)
    
#.. __repr__
print("    __repr__:")
print("      ---->", repr(GbL))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(str(GbL))
print("    <---- __str__ done.")

##! Check get methods:
GaborLensTest = 3
print()
print("GaborLensTest:", GaborLensTest, " check get methods.")
print("    ----> print() method; tests all get methods")
print(GbL)

##! Check set method:
GaborLensTest = 4
print()
print("GaborLensTest:", GaborLensTest, " check set method.")
BLE.GaborLens.setDebug(True)
print(GbL)
BLE.GaborLens.setDebug(False)

##! Check set method:
GaborLensTest += 1
print()
print("GaborLensTest:", GaborLensTest, " test transport through solenoid.")
R      = np.array([0.5, 0.1, -0.3, -0.2, 0., 0.00])
Rprime = GbL.Transport(R)
print("     ----> Input trace-space vector:", R)
print("     ----> Transported trace-space vector:", Rprime)
RprimeTest = np.array([00.489048232, -0.142924944, -0.360654729, -0.03773338, \
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
