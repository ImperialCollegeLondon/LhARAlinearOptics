#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "Drift" class
=============================

  Drift.py -- set "relative" path to code

"""

import numpy as np

import BeamLineElement as BLE

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
rCtr = np.array([0.,0.,0.])
vCtr = np.array([0.,0.])
drCtr = np.array([0.,0.,0.])
dvCtr = np.array([0.,0.])
try:
    Drft = BLE.Drift("NoDriftLength", rCtr, vCtr, drCtr, dvCtr)
except:
    print('      ----> Correctly trapped no drift length exception.')

#.. Create valid instance:
Drft = BLE.Drift("ValidDrift", rCtr, vCtr, drCtr, dvCtr, 1.5)
    
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
BLE.Drift.setDebug(True)
print(Drft)
BLE.Drift.setDebug(False)

##! Check set method:
DriftTest += 1
print()
print("DriftTest:", DriftTest, " test transport through drift.")
R      = np.array([0.5, 0.1, -0.3, -0.2, 0., 0.])
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
print("     ----> Transported phase-space vector:", Rprime)
RprimeTest = np.array([ 0.65,  0.1,  -0.6,  -0.2,   0.,    0.  ])
Diff       = np.subtract(Rprime, RprimeTest)
Norm       = np.linalg.norm(Diff)
print("     ----> Difference Rprime - RprimeTest:", Diff)
print("     ----> Magnitude of Diff:", Norm)
if Norm > 1E-6:
    raise Exception(" !!!!----> FAILED: drift transport result not as expected.")
else:
    print(" <---- Drift transport test successful.")

##! Complete:
print()
print("========  Drift: tests complete  ========")
