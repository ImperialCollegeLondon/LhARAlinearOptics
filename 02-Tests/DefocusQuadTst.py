#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "DefocusQuadrupole" class
=========================================

DefocusQuadrupole.py -- set "relative" path to code

"""

import numpy as np
import scipy as sp
import os

import BeamLineElement as BLE
import LIONbeam        as LNb
import Particle        as Prtcl

HOMEPATH = os.getenv('HOMEPATH')
filename = os.path.join(HOMEPATH, \
                        '11-Parameters/LIONBeamLine-Params-LsrDrvn.csv')
LNbI  = LNb.LIONbeam(filename)

iRefPrtcl = Prtcl.ReferenceParticle.getinstance()

##! Start:
print("========  DefocusQuadrupole: tests start  ========")

print("Reference particle:")
xx    = iRefPrtcl.getPrIn()[0]
xx[2] = 194.7585262
iRefPrtcl._PrIn[0] = xx
p0        = iRefPrtcl.getMomentumIn(0)
with np.printoptions(linewidth=500,precision=7,suppress=True):
    print("     ----> Three momentum (in, RPLC):", \
          iRefPrtcl.getPrIn()[0][0:3])
    print("                           Magnitude:", p0)


##! Test built-in methods:
DefocusQuadrupoleTest = 1
print()
print("DefocusQuadrupoleTest:", DefocusQuadrupoleTest, \
      " check built-in methods.")

#.. __init__
print("    __init__:")
try:
    DfQuad = BLE.DefocusQuadrupole()
except:
    print('      ----> Correctly trapped no argument exception.')
rCtr = np.array([0., 0., 0.])
vCtr = np.array([0., 0.])
drCtr = np.array([0., 0., 0.])
dvCtr = np.array([0., 0.])
try:
    DfQuad = BLE.DefocusQuadrupole("NoStrength", rCtr, vCtr, drCtr, dvCtr)
except:
    print('      ----> Correctly trapped no quadrupole strength exception.')

#.. Create valid instance:
DfQuad = BLE.DefocusQuadrupole("ValidDquad", \
                               rCtr, vCtr, drCtr, dvCtr, 0.1, 100.)
    
#.. __repr__
print("    __repr__:")
print("      ---->", repr(DfQuad))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(str(DfQuad))
print("    <---- __str__ done.")

##! Check get methods:
DefocusQuadrupoleTest = 3
print()
print("DefocusQuadrupoleTest:", DefocusQuadrupoleTest, " check get methods.")
print("    ----> print() method; tests all get methods")
print(DfQuad)

##! Check set method:
DefocusQuadrupoleTest = 4
print()
print("DefocusQuadrupoleTest:", DefocusQuadrupoleTest, " check set method.")
BLE.DefocusQuadrupole.setDebug(True)
print(DfQuad)
BLE.DefocusQuadrupole.setDebug(False)

##! Check set method:
DefocusQuadrupoleTest += 1
print()
print("DefocusQuadrupoleTest:", DefocusQuadrupoleTest, \
      " test transport through defocusing quadrupole.")
R      = np.array([0.5, 0.1, -0.3, -0.2, 0., 0.])
Rprime = DfQuad.Transport(R)
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Input phase-space vector:", R)
print("     ----> Relevant portions of transfer matrix:")
print("         ", DfQuad.getTransferMatrix()[0,0], \
                   DfQuad.getTransferMatrix()[0,1], \
                   DfQuad.getTransferMatrix()[0,2], \
                   DfQuad.getTransferMatrix()[0,3])
print("         ", DfQuad.getTransferMatrix()[1,0], \
                   DfQuad.getTransferMatrix()[1,1], \
                   DfQuad.getTransferMatrix()[1,2], \
                   DfQuad.getTransferMatrix()[1,3])
print("         ", DfQuad.getTransferMatrix()[2,0], \
                   DfQuad.getTransferMatrix()[2,1], \
                   DfQuad.getTransferMatrix()[2,2], \
                   DfQuad.getTransferMatrix()[2,3])
print("         ", DfQuad.getTransferMatrix()[3,0], \
                   DfQuad.getTransferMatrix()[3,1], \
                   DfQuad.getTransferMatrix()[3,2], \
                   DfQuad.getTransferMatrix()[3,3])
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Transported phase-space vector:", Rprime)
RprimeTest = np.array([0.949563524, 10.01608306, -0.112493763,
                       3.456264689, 0.,  0.])
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Pre-calculated          Rprime:", RprimeTest)
Diff       = np.subtract(Rprime, RprimeTest)
Norm       = np.linalg.norm(Diff)
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Difference Rprime - RprimeTest:", Diff)
print("     ----> Magnitude of Diff:", Norm)
if Norm > 1E-6:
    raise Exception(" !!!!----> FAILED: defocusing quadrupole transport", \
                    " result not as expected.")
else:
    print(" <---- Defocusing quadrupole transport test successful.")

    
##! Complete:
print()
print("========  DefocusQuadrupole: tests complete  ========")
