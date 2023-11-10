#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "Dipole" class
=============================

  Dipole.py -- set "relative" path to code

"""

import numpy as np

import BeamLineElement as BLE

##! Start:
print("========  Dipole: tests start  ========")

##! Test singleton class feature:
DipoleTest = 1
print()
print("DipoleTest:", DipoleTest, \
      " check built-in methods.")

#.. __init__
print("    __init__:")
try:
    Dpl = BLE.Dipole()
except:
    print('      ----> Correctly trapped no argument exception.')
rCtr = np.array([0.,0.,0.])
vCtr = np.array([0.,0.])
drCtr = np.array([0.,0.,0.])
dvCtr = np.array([0.,0.])
try:
    Dpl = BLE.Dipole("NoAngle", rCtr, vCtr, drCtr, dvCtr)
except:
    print('      ----> Correctly trapped no dipole angle exception.')

try:
    Dpl = BLE.Dipole("NoAngle", rCtr, vCtr, drCtr, dvCtr, 0.3)
except:
    print('      ----> Correctly trapped no length exception.')

#.. Create valid instance:
Dpl = BLE.Dipole("ValidDipole", rCtr, vCtr, drCtr, dvCtr, 0.03, 0.03)
    
#.. __repr__
print("    __repr__:")
print("      ---->", repr(Dpl))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(str(Dpl))
print("    <---- __str__ done.")

##! Check get methods:
DipoleTest = 3
print()
print("DipoleTest:", DipoleTest, " check get methods.")
print("    ----> print() method; tests all get methods")
print(Dpl)

##! Check set method:
DipoleTest = 4
print()
print("DipoleTest:", DipoleTest, " check set method.")
BLE.Dipole.setDebug(True)
print(Dpl)
BLE.Dipole.setDebug(False)

##! Check set method:
DipoleTest += 1
print()
print("DipoleTest:", DipoleTest, " test transport through dipole.")
R      = np.array([0.5, 0.1, -0.3, -0.2, 0., 0.])
Rprime = Dpl.Transport(R)
print("     ----> Input phase-space vector:", R)
print("     ----> Relevant portions of transfer matrix:")
print("         ", Dpl.getTransferMatrix()[0,0], \
                   Dpl.getTransferMatrix()[0,1], \
                   Dpl.getTransferMatrix()[0,2], \
                   Dpl.getTransferMatrix()[0,3])
print("         ", Dpl.getTransferMatrix()[1,0], \
                   Dpl.getTransferMatrix()[1,1], \
                   Dpl.getTransferMatrix()[1,2], \
                   Dpl.getTransferMatrix()[1,3])
print("         ", Dpl.getTransferMatrix()[2,0], \
                   Dpl.getTransferMatrix()[2,1], \
                   Dpl.getTransferMatrix()[2,2], \
                   Dpl.getTransferMatrix()[2,3])
print("         ", Dpl.getTransferMatrix()[3,0], \
                   Dpl.getTransferMatrix()[3,1], \
                   Dpl.getTransferMatrix()[3,2], \
                   Dpl.getTransferMatrix()[3,3])
print("     ----> Transported phase-space vector:", Rprime)
RprimeTest = np.array([ 0.50500125,  0.0999925,  -0.3000075,  -0.19999875,   0.,    0.  ])
Diff       = np.subtract(Rprime, RprimeTest)
Norm       = np.linalg.norm(Diff)
print("     ----> Difference Rprime - RprimeTest:", Diff)
print("     ----> Magnitude of Diff:", Norm)
if Norm > 1E-6:
    raise Exception(" !!!!----> FAILED: dipole transport result not as expected.")
else:
    print(" <---- Dipole transport test successful.")

##! Complete:
print()
print("========  Dipole: tests complete  ========")
