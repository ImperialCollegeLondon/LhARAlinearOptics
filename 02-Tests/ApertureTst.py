#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "Aperture" class
================================

  Aperture.py -- set "relative" path to code

"""

import numpy             as np

import BeamLineElement   as BLE


##! Start:
print(" ========  Aperture: tests start  ========")

##! Test singleton class feature:
ApertureTest = 1
print()
print(" ApertureTest:", ApertureTest, \
      " check built-in methods.")

#.. __init__
print("     __init__:")
try:
    Aprtr = BLE.Aperture()
except:
    print('     ----> Correctly trapped no argument exception.')
rStrt = np.array([0.,0.,0.])
vStrt = np.array([[np.pi/2.,np.pi/2.],[0.,0.]])
drStrt = np.array([0.,0.,0.])
dvStrt = np.array([[0.,0.],[0.,0.]])
try:
    Aprtr = BLE.Aperture(" NoApertureParams", rStrt, vStrt, drStrt, dvStrt)
except:
    print('      ----> Correctly trapped no paramters exception.')

#--------> Clean instances and restart:
BLE.BeamLineElement.cleaninstances()

#.. Create valid instance:
Aprtr = BLE.Aperture(" ValidAperture", rStrt, vStrt, drStrt, dvStrt, \
                     [0, 0.2])
    
#.. __repr__
print("     __repr__:")
print("       ---->", repr(Aprtr))
print("     <---- __repr__ done.")
#.. __str__
print("     __str__:")
print(str(Aprtr))
print("     <---- __str__ done.")

##! Check get methods:
ApertureTest = 3
print()
print(" ApertureTest:", ApertureTest, " check get methods.")
print("     ----> print() method; tests all get methods")
print(Aprtr)

##! Check set method:
ApertureTest = 4
print()
print(" ApertureTest:", ApertureTest, " check set method.")
print(Aprtr)

##! Check set method:
ApertureTest += 1
print()
print(" ApertureTest:", ApertureTest, " test transport through aperture.")
R          = np.array([0.005, 0.1, -0.003, -0.2, 0.1, 0.05])
RprimeTest = R
Rprime = Aprtr.Transport(R)
print("     ----> Input phase-space vector:", R)
print("     ----> Relevant portions of transfer matrix:")
print("         ", Aprtr.getTransferMatrix()[0,0], \
                   Aprtr.getTransferMatrix()[0,1], \
                   Aprtr.getTransferMatrix()[0,2], \
                   Aprtr.getTransferMatrix()[0,3])
print("         ", Aprtr.getTransferMatrix()[1,0], \
                   Aprtr.getTransferMatrix()[1,1], \
                   Aprtr.getTransferMatrix()[1,2], \
                   Aprtr.getTransferMatrix()[1,3])
print("         ", Aprtr.getTransferMatrix()[2,0], \
                   Aprtr.getTransferMatrix()[2,1], \
                   Aprtr.getTransferMatrix()[2,2], \
                   Aprtr.getTransferMatrix()[2,3])
print("         ", Aprtr.getTransferMatrix()[3,0], \
                   Aprtr.getTransferMatrix()[3,1], \
                   Aprtr.getTransferMatrix()[3,2], \
                   Aprtr.getTransferMatrix()[3,3])
with np.printoptions(linewidth=500,precision=7,suppress=True):
    print("     ----> Transported phase-space vector:", Rprime)
                        
Diff       = np.subtract(Rprime, RprimeTest)
Norm       = np.linalg.norm(Diff)
with np.printoptions(linewidth=500,precision=7,suppress=True):
    print("     ----> Difference Rprime - RprimeTest:", Diff)
print("     ----> Magnitude of Diff:", Norm)
if Norm > 1E-6:
    raise Exception(\
        " !!!!----> FAILED: aperture transport result not as expected.")
else:
    pass

print(" <---- Aperture transport test successful.")

##! Check elliptical apperture:
ApertureTest += 1
print()
print(" ApertureTest:", ApertureTest, " check elliptical aperture:")

Aprtr = BLE.Aperture("ValidAperture", rStrt, vStrt, drStrt, dvStrt, \
                     [1, 0.2, 0.4])
R     = np.array([0.2, 0.1, -0.003, -0.3, 0.1, 0.05])
Trnsp = Aprtr.Transport(R)
print("         ----> Outside Trnsp:", Trnsp)
if not (Trnsp is None):
    raise Exception(\
            " !!!!----> FAILED: did not recognise coordinate outside",\
            " elliptical aperture.")
else:
    pass

R      = np.array([0.005, 0.1, -0.003, -0.2, 0.1, 0.05])
RprmT  = R
Rprime = Aprtr.Transport(R)
Diff   = np.subtract(Rprime, RprmT)
Norm       = np.linalg.norm(Diff)
with np.printoptions(linewidth=500,precision=7,suppress=True):
    print("     ----> Difference Rprime - RprimeTest:", Diff)
print("     ----> Magnitude of Diff:", Norm)
if Norm > 1E-6:
    raise Exception(\
            " !!!!----> FAILED: aperture transport result not as expected.")
else:
    pass

print(" <---- Elliptical aperture tests successful.")

##! Check rectangular apperture:
ApertureTest += 1
print()
print(" ApertureTest:", ApertureTest, " check rectangular aperture:")

Aprtr = BLE.Aperture("ValidAperture", rStrt, vStrt, drStrt, dvStrt, \
                     [1, 0.2, 0.4])
R     = np.array([0.2, 0.1, -0.003, -0.3, 0.1, 0.05])
Trnsp = Aprtr.Transport(R)
print("         ----> Outside Trnsp:", Trnsp)
if not (Trnsp is None):
    raise Exception(\
                    " !!!!----> FAILED: did not recognise coordinate outside",\
                    " rectangular aperture.")
else:
    pass

Aprtr = BLE.Aperture("ValidAperture", rStrt, vStrt, drStrt, dvStrt, \
                     [2, 0.2, 0.4])
R      = np.array([0.005, 0.1, -0.003, -0.2, 0.1, 0.05])
RprmT  = R
Rprime = Aprtr.Transport(R)
Diff   = np.subtract(Rprime, RprmT)
Norm       = np.linalg.norm(Diff)
with np.printoptions(linewidth=500,precision=7,suppress=True):
    print("     ----> Difference Rprime - RprimeTest:", Diff)
print("     ----> Magnitude of Diff:", Norm)
if Norm > 1E-6:
    raise Exception(\
                " !!!!----> FAILED: aperture transport result not as expected.")
else:
    pass

print(" <---- Aperture transport test successful.")

##! Complete:
print()
print("========  Aperture: tests complete  ========")
