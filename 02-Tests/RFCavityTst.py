#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "RFCavity" class
===============================

RFCavity.py -- set "relative" path to code

"""

import numpy as np

import BeamLineElement as BLE

##! Start:
print("========  RF Cavity: tests start  ========")

##! Test singleton class feature:
RFCavityTest = 1
print()
print("RFCavityTest:", RFCavityTest, \
      " check built-in methods.")

#.. __init__
print("    __init__:")
try:
    RF = BLE.RFCavity()
except:
    print('      ----> Correctly trapped no argument exception.')
rCtr = np.array([0.,0.,0.])
vCtr = np.array([0.,0.])
drCtr = np.array([0.,0.,0.])
dvCtr = np.array([0.,0.])
try:
    RF = BLE.RFCavity("Cavity", rCtr, vCtr, drCtr, dvCtr)
except:
    print('      ----> Correctly trapped no RF cavity parameters exception.')

#.. Create valid instance:
RF = BLE.RFCavity("Cavity", rCtr, vCtr, drCtr, dvCtr, 1.5, 1E6, 1.5)
    
#.. __repr__
print("    __repr__:")
print("      ---->", repr(RF))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(str(RF))
print("    <---- __str__ done.")

##! Check get methods:
RFCavityTest = 3
print()
print("RFCavityTest:", RFCavityTest, " check get methods.")
print("    ----> print() method; tests all get methods")
print(RF)

##! Check set method:
RFCavityTest = 4
print()
print("RFCavityTest:", RFCavityTest, " check set method.")
BLE.RFCavity.setDebug(True)
print(RF)
BLE.RFCavity.setDebug(False)

##! Check set method:
RFCavityTest += 1
print()
print("RFCavityTest:", RFCavityTest, " test transport through RF cavity.")
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
    raise Exception(" !!!!----> FAILED: RF cavity transport result not as expected.")
else:
    print(" <---- RF cavity transport test successful.")

##! Complete:
print()
print("========  RF Cavity: tests complete  ========")
