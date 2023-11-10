#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "Solenoid" class
===============================

Solenoid.py -- set "relative" path to code

"""

import numpy as np
import scipy as sp

import BeamLineElement as BLE

##! Start:
print("========  Solenoid: tests start  ========")

##! Test singleton class feature:
SolenoidTest = 1
print()
print("SolenoidTest:", SolenoidTest, \
      " check built-in methods.")

#.. __init__
print("    __init__:")
try:
    Sol = BLE.Solenoid()
except:
    print('      ----> Correctly trapped no argument exception.')
rCtr = np.array([0.,0.,0.])
vCtr = np.array([0.,0.])
drCtr = np.array([0.,0.,0.])
dvCtr = np.array([0.,0.])
try:
    Sol = BLE.Solenoid("Solenoid1", rCtr, vCtr, drCtr, dvCtr)
except:
    print('      ----> Correctly trapped no solenoid length exception.')

#.. Create valid instance:
Sol = BLE.Solenoid("Solenoid2", rCtr, vCtr, drCtr, dvCtr, 0.5, 1.4)
    
#.. __repr__
print("    __repr__:")
print("      ---->", repr(Sol))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(str(Sol))
print("    <---- __str__ done.")

##! Check get methods:
SolenoidTest = 3
print()
print("SolenoidTest:", SolenoidTest, " check get methods.")
print("    ----> print() method; tests all get methods")
print(Sol)

##! Check set method:
SolenoidTest = 4
print()
print("SolenoidTest:", SolenoidTest, " check set method.")
BLE.Solenoid.setDebug(True)
print(Sol)
BLE.Solenoid.setDebug(False)

##! Check set method:
SolenoidTest += 1
print()
print("SolenoidTest:", SolenoidTest, " test transport through solenoid.")
R      = np.array([0.5, 0.1, -0.3, -0.2, 0., 0.])
p      = 194.7585
Brho   = 1./(sp.constants.c*1.E-9) * p / 1000.
Rprime = Sol.Transport(R, Brho)
print("     ----> Input phase-space vector:", R)
print("     ----> Relevant portions of transfer matrix:")
print("         ", Sol.getTransferMatrix()[0,0], \
                   Sol.getTransferMatrix()[0,1], \
                   Sol.getTransferMatrix()[0,2], \
                   Sol.getTransferMatrix()[0,3])
print("         ", Sol.getTransferMatrix()[1,0], \
                   Sol.getTransferMatrix()[1,1], \
                   Sol.getTransferMatrix()[1,2], \
                   Sol.getTransferMatrix()[1,3])
print("         ", Sol.getTransferMatrix()[2,0], \
                   Sol.getTransferMatrix()[2,1], \
                   Sol.getTransferMatrix()[2,2], \
                   Sol.getTransferMatrix()[2,3])
print("         ", Sol.getTransferMatrix()[3,0], \
                   Sol.getTransferMatrix()[3,1], \
                   Sol.getTransferMatrix()[3,2], \
                   Sol.getTransferMatrix()[3,3])
print("     ----> Transported phase-space vector:", Rprime)
RprimeTest = np.array([0.228273338, -0.166572584, -0.54739631, 0.092788839, \
                       0., 0. ])
Diff       = np.subtract(Rprime, RprimeTest)
Norm       = np.linalg.norm(Diff)
with np.printoptions(linewidth=500,precision=7,suppress=True):
    print("     ----> Difference Rprime - RprimeTest:", Diff)
print("     ----> Magnitude of Diff:", Norm)
if Norm > 1E-6:
    raise Exception(" !!!!----> FAILED: solenoid transport result not as expected.")
else:
    print(" <---- Solenoid transport test successful.")

##! Complete:
print()
print("========  Solenoid: tests complete  ========")
