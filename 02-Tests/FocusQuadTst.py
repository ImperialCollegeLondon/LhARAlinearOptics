#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "FocusQuadrupole" class
=======================================

FocusQuadrupole.py -- set "relative" path to code

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
print("========  FocusQuadrupole: tests start  ========")

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
rStrt = np.array([0., 0., 0.])
vStrt = np.array([0., 0.])
drStrt = np.array([0., 0., 0.])
dvStrt = np.array([0., 0.])
try:
    FQuad = BLE.FocusQuadrupole("NoStrength", rStrt, vStrt, drStrt, dvStrt)
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
FQuad = BLE.FocusQuadrupole("ValidQuad1", rStrt, vStrt, drStrt, dvStrt, \
                            0.1, 100.)
FQuad = BLE.FocusQuadrupole("ValidQuad1", rStrt, vStrt, drStrt, dvStrt, \
                            0.1, None, 153.93033817278908)
            
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
R      = np.array([0.5, 0.1, -0.3, -0.2, 0.1, 0.5])
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
RprimeTest = np.array([ 0.356538237, -6.855300654, -0.406762285, \
                        -5.375084494, 1.260471929, 0.5 ])
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
