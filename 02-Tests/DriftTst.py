#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "Drift" class
=============================

  Drift.py -- set "relative" path to code

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
print("========  Drift: tests start  ========")

##! Test singleton class feature:
DriftTest = 1
print()
print("DriftTest:", DriftTest, \
      " check built-in methods.")

#.. __init__
print("    __init__:")
try:
    Drft = BLE.Drift()
except:
    print('      ----> Correctly trapped no argument exception.')
rStrt = np.array([0.,0.,0.])
vStrt = np.array([[np.pi/2.,np.pi/2.],[0.,0.]])
drStrt = np.array([0.,0.,0.])
dvStrt = np.array([[0.,0.],[0.,0.]])
try:
    Drft = BLE.Drift("NoDriftLength", rStrt, vStrt, drStrt, dvStrt)
except:
    print('      ----> Correctly trapped no drift length exception.')

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
Drft = BLE.Drift("ValidDrift", rStrt, vStrt, drStrt, dvStrt, 1.5)
    
#.. __repr__
print("    __repr__:")
print("      ---->", repr(Drft))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(str(Drft))
print("    <---- __str__ done.")

##! Check get methods:
DriftTest = 3
print()
print("DriftTest:", DriftTest, " check get methods.")
print("    ----> print() method; tests all get methods")
print(Drft)

##! Check set method:
DriftTest = 4
print()
print("DriftTest:", DriftTest, " check set method.")
print(Drft)

##! Check set method:
DriftTest += 1
print()
print("DriftTest:", DriftTest, " test transport through drift.")
R      = np.array([0.5, 0.1, -0.3, -0.2, 0.1, 0.05])
Rprime = Drft.Transport(R)
print("     ----> Input phase-space vector:", R)
print("     ----> Relevant portions of transfer matrix:")
print("         ", Drft.getTransferMatrix()[0,0], \
                   Drft.getTransferMatrix()[0,1], \
                   Drft.getTransferMatrix()[0,2], \
                   Drft.getTransferMatrix()[0,3])
print("         ", Drft.getTransferMatrix()[1,0], \
                   Drft.getTransferMatrix()[1,1], \
                   Drft.getTransferMatrix()[1,2], \
                   Drft.getTransferMatrix()[1,3])
print("         ", Drft.getTransferMatrix()[2,0], \
                   Drft.getTransferMatrix()[2,1], \
                   Drft.getTransferMatrix()[2,2], \
                   Drft.getTransferMatrix()[2,3])
print("         ", Drft.getTransferMatrix()[3,0], \
                   Drft.getTransferMatrix()[3,1], \
                   Drft.getTransferMatrix()[3,2], \
                   Drft.getTransferMatrix()[3,3])
with np.printoptions(linewidth=500,precision=7,suppress=True):
    print("     ----> Transported phase-space vector:", Rprime)
RprimeTest = np.array([ 0.65, 0.1, -0.6, -0.2, 1.840707893, 0.05])
                        
Diff       = np.subtract(Rprime, RprimeTest)
Norm       = np.linalg.norm(Diff)
with np.printoptions(linewidth=500,precision=7,suppress=True):
    print("     ----> Difference Rprime - RprimeTest:", Diff)
print("     ----> Magnitude of Diff:", Norm)
if Norm > 1E-6:
    raise Exception(" !!!!----> FAILED: drift transport result not as expected.")
else:
    print(" <---- Drift transport test successful.")

##! Complete:
print()
print("========  Drift: tests complete  ========")
