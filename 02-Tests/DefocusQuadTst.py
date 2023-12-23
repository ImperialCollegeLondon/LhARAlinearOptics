#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "DefocusQuadrupole" class
=========================================

DefocusQuadrupole.py -- set "relative" path to code

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
print(" ========  DefocusQuadrupole: tests start  ========")

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
rStrt = np.array([0., 0., 0.])
vStrt = np.array([0., 0.])
drStrt = np.array([0., 0., 0.])
dvStrt = np.array([0., 0.])
try:
    DfQuad = BLE.DefocusQuadrupole("NoStrength", rStrt, vStrt, drStrt, dvStrt)
except:
    print('      ----> Correctly trapped no quadrupole strength exception.')


#--------> Clean instances and restart:
BLE.BeamLineElement.cleanInstances()

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
DfQuad = BLE.DefocusQuadrupole("ValidDquad", \
                               rStrt, vStrt, drStrt, dvStrt, 0.1, 100.)
    
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
