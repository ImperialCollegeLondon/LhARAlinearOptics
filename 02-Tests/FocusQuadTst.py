#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "FocusQuadrupole" class
=======================================

FocusQuadrupole.py -- set "relative" path to code

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
print("========  FocusQuadrupole: tests start  ========")

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
FocusQuadrupoleTest = 1
print()
print("FocusQuadrupoleTest:", FocusQuadrupoleTest, \
      " check built-in methods.")

#.. __init__
print("    __init__:")
try:
    FQuad = BLE.FocusQuadrupole()
except:
    print('      ----> Correctly trapped no argument exception.')
rCtr = np.array([0., 0., 0.])
vCtr = np.array([0., 0.])
drCtr = np.array([0., 0., 0.])
dvCtr = np.array([0., 0.])
try:
    FQuad = BLE.FocusQuadrupole("NoStrength", rCtr, vCtr, drCtr, dvCtr)
except:
    print('      ----> Correctly trapped no quadrupole strength exception.')

#.. Create valid instance:
FQuad = BLE.FocusQuadrupole("ValidQuad", rCtr, vCtr, drCtr, dvCtr, \
                            0.1, 100.)
    
#.. __repr__
print("    __repr__:")
print("      ---->", repr(FQuad))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(str(FQuad))
print("    <---- __str__ done.")

##! Check get methods:
FocusQuadrupoleTest = 3
print()
print("FocusQuadrupoleTest:", FocusQuadrupoleTest, " check get methods.")
print("    ----> print() method; tests all get methods")
print(FQuad)

##! Check set method:
FocusQuadrupoleTest = 4
print()
print("FocusQuadrupoleTest:", FocusQuadrupoleTest, " check set method.")
BLE.FocusQuadrupole.setDebug(True)
print(FQuad)
BLE.FocusQuadrupole.setDebug(False)

##! Check transport:
FocusQuadrupoleTest += 1
print()
print("FocusQuadrupoleTest:", FocusQuadrupoleTest, \
      " test transport through focusing quadrupole.")
R      = np.array([0.5, 0.1, -0.3, -0.2, 0., 0.])
Rprime = FQuad.Transport(R)
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Input phase-space vector:", R)
print("     ----> Relevant portions of transfer matrix:")
print("         ", FQuad.getTransferMatrix()[0,0], \
                   FQuad.getTransferMatrix()[0,1], \
                   FQuad.getTransferMatrix()[0,2], \
                   FQuad.getTransferMatrix()[0,3])
print("         ", FQuad.getTransferMatrix()[1,0], \
                   FQuad.getTransferMatrix()[1,1], \
                   FQuad.getTransferMatrix()[1,2], \
                   FQuad.getTransferMatrix()[1,3])
print("         ", FQuad.getTransferMatrix()[2,0], \
                   FQuad.getTransferMatrix()[2,1], \
                   FQuad.getTransferMatrix()[2,2], \
                   FQuad.getTransferMatrix()[2,3])
print("         ", FQuad.getTransferMatrix()[3,0], \
                   FQuad.getTransferMatrix()[3,1], \
                   FQuad.getTransferMatrix()[3,2], \
                   FQuad.getTransferMatrix()[3,3])
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Transported phase-space vector:", Rprime)
RprimeTest = np.array([ 0.169698254, -5.836075396, -0.58761661, \
                        -6.271951923, 0.,  0. ])
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Pre-calculated          Rprime:", RprimeTest)
Diff       = np.subtract(Rprime, RprimeTest)
Norm       = np.linalg.norm(Diff)
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Difference Rprime - RprimeTest:", Diff)
print("     ----> Magnitude of Diff:", Norm)
if Norm > 1E-6:
    raise Exception(" !!!!----> FAILED: focusing quadrupole transport", \
                    " result not as expected.")
else:
    print(" <---- Focusing quadrupole transport test successful.")


##! Complete:
print()
print("========  FocusQuadrupole: tests complete  ========")
