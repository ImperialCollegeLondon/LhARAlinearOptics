#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "CylindricalRFCavity" class
===========================================

CylindricalRFCavity.py -- set "relative" path to code

"""

import os
import math  as mth
import numpy as np

import Particle          as Prtcl
import BeamLine          as BL
import BeamLineElement   as BLE
import PhysicalConstants as PhysCnst

constants_instance = PhysCnst.PhysicalConstants()
protonMASS         = constants_instance.mp()

HOMEPATH = os.getenv('HOMEPATH')
filename = os.path.join(HOMEPATH, \
                        '11-Parameters/Dummy4Tests.csv')

##! Start:
print("========  Cylindrical RF cavity: tests start  ========")

##! Test set up of class
CylindricalRFCavityTest = 1
print()
print("CylindricalRFCavityTest:", CylindricalRFCavityTest, \
      " check built-in methods.")

#.. __init__
print("    __init__:")
try:
    RF = BLE.CylindricalRFCavity()
except:
    print('      ----> Correctly trapped no argument exception.')
rStrt = np.array([0.,0.,0.])
vStrt = np.array([0.,0.])
drStrt = np.array([0.,0.,0.])
dvStrt = np.array([0.,0.])
try:
    RF = BLE.CylindricalRFCavity("Cavity", rStrt, vStrt, drStrt, dvStrt)
except:
    print('      ----> Correctly trapped no Cylindrical', \
          ' RF cavity parameters exception.')

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
RF = BLE.CylindricalRFCavity("Cavity", rStrt, vStrt, drStrt, dvStrt, \
                             4.0, 200., 0.)
    
#.. __repr__
print("    __repr__:")
print("      ---->", repr(RF))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(str(RF))
print("    <---- __str__ done.")

##! Check get methods:
CylindricalRFCavityTest = 3
print()
print("CylindricalRFCavityTest:", CylindricalRFCavityTest, " check get methods.")
print("    ----> print() method; tests all get methods")
print(RF)

##! Check set method:
CylindricalRFCavityTest = 4
print()
print("CylindricalRFCavityTest:", CylindricalRFCavityTest, " check set method.")
BLE.CylindricalRFCavity.setDebug(True)
print(RF)
BLE.CylindricalRFCavity.setDebug(False)

##! Check set method:
CylindricalRFCavityTest += 1
print()
print("CylindricalRFCavityTest:", CylindricalRFCavityTest, " test transport through Cylindrical RF cavity.")
R      = np.array([0.5, 0.1, -0.3, -0.2, 0., 0.])
Rprime = RF.Transport(R)
print("     ----> Input phase-space vector:", R)
print("     ----> Relevant portions of transfer matrix:")
print("         ", RF.getTransferMatrix()[0,0], \
                   RF.getTransferMatrix()[0,1], \
                   RF.getTransferMatrix()[0,2], \
                   RF.getTransferMatrix()[0,3])
print("         ", RF.getTransferMatrix()[1,0], \
                   RF.getTransferMatrix()[1,1], \
                   RF.getTransferMatrix()[1,2], \
                   RF.getTransferMatrix()[1,3])
print("         ", RF.getTransferMatrix()[2,0], \
                   RF.getTransferMatrix()[2,1], \
                   RF.getTransferMatrix()[2,2], \
                   RF.getTransferMatrix()[2,3])
print("         ", RF.getTransferMatrix()[3,0], \
                   RF.getTransferMatrix()[3,1], \
                   RF.getTransferMatrix()[3,2], \
                   RF.getTransferMatrix()[3,3])
print("     ----> Transported phase-space vector:", Rprime)
RprimeTest = np.array([0.5, 0.1, -0.3, -0.2, -4.71772766e-06,  1.  ])
Diff       = np.subtract(Rprime, RprimeTest)
Norm       = np.linalg.norm(Diff)
print("     ----> Difference Rprime - RprimeTest:", Diff)
print("     ----> Magnitude of Diff:", Norm)
if Norm > 1E-6:
    raise Exception(" !!!!----> FAILED: Cylindrical RF cavity transport result not as expected.")
else:
    print(" <---- Cylindrical RF cavity transport test successful.")

##! Complete:
print()
print("========  Cylindrical Cylindrical RF cavity: tests complete  ========")
