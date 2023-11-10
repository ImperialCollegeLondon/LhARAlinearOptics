#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "Octupole" class
===============================

Octupole.py -- set "relative" path to code

"""

import numpy as np

import BeamLineElement as BLE

##! Start:
print("========  Octupole: tests start  ========")

##! Test singleton class feature:
OctupoleTest = 1
print()
print("OctupoleTest:", OctupoleTest, \
      " check built-in methods.")

#.. __init__
print("    __init__:")
try:
    Oct = BLE.Octupole()
except:
    print('      ----> Correctly trapped no argument exception.')
rCtr = np.array([0.,0.,0.])
vCtr = np.array([0.,0.])
drCtr = np.array([0.,0.,0.])
dvCtr = np.array([0.,0.])
try:
    Oct = BLE.Octupole("Octopole", rCtr, vCtr, drCtr, dvCtr)
except:
    print('      ----> Correctly trapped no octupole length exception.')

#.. Create valid instance:
Oct = BLE.Octupole("Octopole", rCtr, vCtr, drCtr, dvCtr, 1.5)
    
#.. __repr__
print("    __repr__:")
print("      ---->", repr(Oct))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(str(Oct))
print("    <---- __str__ done.")

##! Check get methods:
OctupoleTest = 3
print()
print("OctupoleTest:", OctupoleTest, " check get methods.")
print("    ----> print() method; tests all get methods")
print(Oct)

##! Check set method:
OctupoleTest = 4
print()
print("OctupoleTest:", OctupoleTest, " check set method.")
BLE.Octupole.setDebug(True)
print(Oct)
BLE.Octupole.setDebug(False)

##! Check set method:
OctupoleTest += 1
print()
print("OctupoleTest:", OctupoleTest, " test transport through octupole.")
R      = np.array([0.5, 0.1, -0.3, -0.2, 0., 0.])
Rprime = Oct.Transport(R)
print("     ----> Input phase-space vector:", R)
print("     ----> Relevant portions of transfer matrix:")
print("         ", Oct.getTransferMatrix()[0,0], \
                   Oct.getTransferMatrix()[0,1], \
                   Oct.getTransferMatrix()[0,2], \
                   Oct.getTransferMatrix()[0,3])
print("         ", Oct.getTransferMatrix()[1,0], \
                   Oct.getTransferMatrix()[1,1], \
                   Oct.getTransferMatrix()[1,2], \
                   Oct.getTransferMatrix()[1,3])
print("         ", Oct.getTransferMatrix()[2,0], \
                   Oct.getTransferMatrix()[2,1], \
                   Oct.getTransferMatrix()[2,2], \
                   Oct.getTransferMatrix()[2,3])
print("         ", Oct.getTransferMatrix()[3,0], \
                   Oct.getTransferMatrix()[3,1], \
                   Oct.getTransferMatrix()[3,2], \
                   Oct.getTransferMatrix()[3,3])
print("     ----> Transported phase-space vector:", Rprime)
RprimeTest = np.array([ 1. ,  0.1, -0.45, -0.2 ,  0. ,  0.  ])
Diff       = np.subtract(Rprime, RprimeTest)
Norm       = np.linalg.norm(Diff)
print("     ----> Difference Rprime - RprimeTest:", Diff)
print("     ----> Magnitude of Diff:", Norm)
if Norm > 1E-6:
    raise Exception(" !!!!----> FAILED: octupole transport result not as expected.")
else:
    print(" <---- Octupole transport test successful.")

##! Complete:
print()
print("========  Octupole: tests complete  ========")
