#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "BeamLineElement" class
=======================================

  BeamLineElement.py -- set "relative" path to code

"""

import numpy as np

import BeamLineElement as BLE

##! Start:
print("========  BeamLineElement: tests start  ========")

##! Test singleton class feature:
BeamLineElementTest = 1
print()
print("BeamLineElementTest:", BeamLineElementTest, \
      " check built-in methods.")

#.. __init__
print("    __init__:")
try:
    BmLnElmnt = BLE.BeamLineElement()
except:
    print('      ----> Correctly trapped no argument exception.')

#.. Create valid instance:
Name = "BLE1"
rStrt = np.array([0.,0.,0.])
vStrt = np.array([[np.pi/2.,np.pi/2.],[0.,0.]])
drStrt = np.array([0.,0.,0.])
dvStrt = np.array([[0.,0.],[0.,0.]])
BmLnElmnt = BLE.BeamLineElement(Name, rStrt, vStrt, drStrt, dvStrt)
    
#.. __repr__
print("    __repr__:")
print("      ---->", repr(BmLnElmnt))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(str(BmLnElmnt))
print("    <---- __str__ done.")

##! Check get methods:
BeamLineElementTest = 3
print()
print("BeamLineElementTest:", BeamLineElementTest, " check get methods.")
print("    ----> print() method; tests all get methods")
print(BmLnElmnt)

##! Check remaining set method:
BeamLineElementTest = 4
print()
print("BeamLineElementTest:", BeamLineElementTest, " check set method.")
BLE.BeamLineElement.setDebug(True)
print(BmLnElmnt)
BLE.BeamLineElement.setDebug(False)

##! Check remaining set method:
BeamLineElementTest += 1
print()
print("BeamLineElementTest:", BeamLineElementTest, \
      " coordinate transformations.")
R      = np.array([0.5, 0.1, -0.3, -0.2, 0., 0.])
print("     ----> Input phase-space vector:", R)
BmLnElmnt.setdrStrt(np.array([0.1, 0.2, 0.3]))
print("     ----> Offset to start of element position:", BmLnElmnt.getdrStrt())
Rprime = BmLnElmnt.Shift2Local(R)
print("         ----> Phase-space vector in local coordiantes:", Rprime)
R2prime = BmLnElmnt.Shift2Laboratory(Rprime)
print("         ----> Phase-space vector back in laboratory coordiantes:", \
      R2prime)
Diff       = np.subtract(R, R2prime)
Norm       = np.linalg.norm(Diff)
print("     ----> Difference R - R2prime:", Diff)
print("     ----> Magnitude of Diff:", Norm)
if Norm > 1E-6:
    raise Exception(" !!!!----> FAILED: coordinate transformations", \
                    " inconsistent.")
else:
    print(" <---- Drift coordinate transformation test successful.")
    

##! Complete:
print()
print("========  BeamLineElement: tests complete  ========")
