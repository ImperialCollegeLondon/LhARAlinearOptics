#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "GaborLens" class
===============================

BeamLineElement.py -- set "relative" path to code

"""

import numpy as np
import scipy as sp
import math  as mth
import os

import PhysicalConstants as PhysCnst
import BeamLineElement   as BLE
import BeamLine          as BL
import Particle          as Prtcl

constants_instance = PhysCnst.PhysicalConstants()
protonMASS         = constants_instance.mp()

HOMEPATH = os.getenv('HOMEPATH')
filename = os.path.join(HOMEPATH, \
                        '11-Parameters/Dummy4Tests.csv')

##! Start:
print("========  GaborLens: tests start  ========")

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
vStrt = np.array([[np.pi/2.,np.pi/2.],[0.,0.]])
drStrt = np.array([0.,0.,0.])
dvStrt = np.array([[0.,0.],[0.,0.]])
try:
    GbL = BLE.GaborLens("GaborLens1", rStrt, vStrt, drStrt, dvStrt)
except:
    print('      ----> Correctly trapped no solenoid GbL args exception.')

    
#--------> Clean instances and restart:
BLE.BeamLineElement.cleaninstances()

BLI  = BL.BeamLine(filename)
iRefPrtcl = Prtcl.ReferenceParticle.getinstance()

print(" ----> Reference particle:")
pz = 194.7585262
E0 = mth.sqrt(protonMASS**2 + pz**2)
p0 = np.array([0., 0., pz, E0])
iRefPrtcl.setPrIn(p0)
iRefPrtcl.setPrOut(p0)

print("     ----> Reference particle set:")
print("         ----> In:", iRefPrtcl.getPrIn())
print("              Out:", iRefPrtcl.getPrOut())

p0        = iRefPrtcl.getMomentumIn(0)
with np.printoptions(linewidth=500,precision=7,suppress=True):
    print("         ----> Three momentum (in, RPLC):", \
          iRefPrtcl.getPrIn()[0][0:3], ", Magnitude:", p0)

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
