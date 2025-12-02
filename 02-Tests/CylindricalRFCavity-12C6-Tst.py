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
                        '11-Parameters/twelveC6forTests.csv')

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
vStrt = np.array([[np.pi/2.,np.pi/2.],[0.,0.]])
drStrt = np.array([0.,0.,0.])
dvStrt = np.array([0.,0.,0.])
try:
    RF = BLE.CylindricalRFCavity("Cavity", rStrt, vStrt, drStrt, dvStrt)
except:
    print('      ----> Correctly trapped no Cylindrical', \
          ' RF cavity parameters exception.')

#.. Clean:
BLE.BeamLineElement.cleaninstances()

BL.BeamLine.setDebug(True)
BLI  = BL.BeamLine(filename)
iRefPrtcl = BL.BeamLine.getcurrentReferenceParticle()

print(" ----> Reference particle:")
print("     ----> Reference particle set:")
print("         ----> In:", iRefPrtcl.getPrIn())
print("              Out:", iRefPrtcl.getPrOut())

p0        = iRefPrtcl.getMomentumIn(0)
with np.printoptions(linewidth=500,precision=7,suppress=True):
    print("         ----> Three momentum (in, RPLC):", \
          iRefPrtcl.getPrIn()[0][0:3], ", Magnitude:", p0)

#.. Create valid instance:
RF = BLE.CylindricalRFCavity("Cavity", rStrt, vStrt, drStrt, dvStrt, \
                             20.0, 200., 0.1)
refPrtclSet = iRefPrtcl.setReferenceParticle(RF)
    
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
print("CylindricalRFCavityTest:", CylindricalRFCavityTest, \
      " check get methods.")
print("    ----> print() method; tests all get methods")
print(RF)

##! Check set method:
CylindricalRFCavityTest = 4
print()
print("CylindricalRFCavityTest:", CylindricalRFCavityTest, \
      " check set method.")
BLE.CylindricalRFCavity.setDebug(True)
print(RF)
BLE.CylindricalRFCavity.setDebug(False)

##! Check set method:
CylindricalRFCavityTest += 1
print()
print("CylindricalRFCavityTest:", CylindricalRFCavityTest, \
      " test transport through Cylindrical RF cavity.")
R      = np.array([0.5, 0.1, -0.3, -0.2, 0.1, 0.2])
BLE.CylindricalRFCavity.setDebug(True)
Rprime = RF.Transport(R)
with np.printoptions(linewidth=500,precision=7,suppress=True):
    print("     ----> Input phase-space vector:", R)
with np.printoptions(linewidth=500,precision=7,suppress=True):
    print("     ----> Relevant portions of transfer matrix:")
with np.printoptions(linewidth=500,precision=7,suppress=True):
    print(RF.getTransferMatrix())
print("     ----> Transported phase-space vector:", Rprime)
RprimeTest = np.array([0.504478038, 0.09999968, -0.308956086, \
                       -0.199999806, 2.599818749, 0.199998877])
Diff       = np.subtract(Rprime, RprimeTest)
Norm       = np.linalg.norm(Diff)
print("     ----> Difference Rprime - RprimeTest:", Diff)
print("     ----> Magnitude of Diff:", Norm)
if Norm > 1E-5:
    raise Exception(" !!!!----> FAILED: Cylindrical RF cavity transport result not as expected.")
else:
    print(" <---- Cylindrical RF cavity transport test successful.")

##! Complete:
print()
print("========  Cylindrical Cylindrical RF cavity: tests complete  ========")
