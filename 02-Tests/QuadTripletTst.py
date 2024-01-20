#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "QuadTriplet" class
=======================================

QuadTriplet.py -- set "relative" path to code

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
print("========  QuadTriplet: tests start  ========")

##! Test built-in methods:
QuadTripletTest = 1
print()
print("QuadTripletTest:", QuadTripletTest, \
      " check built-in methods.")

#.. __init__
print("    __init__:")
try:
    QT = BLE.QuadTriplet()
except:
    print('      ----> Correctly trapped no argument exception.')
rStrt = np.array([0., 0., 0.])
vStrt = np.array([0., 0.])
drStrt = np.array([0., 0., 0.])
dvStrt = np.array([0., 0.])
try:
    QT = BLE.QuadTriplet("NoStrength", rStrt, vStrt, drStrt, dvStrt)
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
QT = BLE.QuadTriplet("ValidQuad1", rStrt, vStrt, drStrt, dvStrt)
            
#.. __repr__
print("    __repr__:")
print("      ---->", repr(QT))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(str(QT))
print("    <---- __str__ done.")

##! Check get methods:
QuadTripletTest = 3
print()
print("QuadTripletTest:", QuadTripletTest, " check get methods.")
print("    ----> print() method; tests all get methods")
print(QT)

##! Check set method:
QuadTripletTest = 4
print()
print("QuadTripletTest:", QuadTripletTest, " check set method.")
BLE.QuadTriplet.setDebug(True)
print(QT)
BLE.QuadTriplet.setDebug(False)

##! Check transport:
QuadTripletTest += 1
print()
print("QuadTripletTest:", QuadTripletTest, \
      " test transport through focusing quadrupole.")
R      = np.array([0.5, 0.1, -0.3, -0.2, 0.1, 0.5])
Rprime = QT.Transport(R)
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Input phase-space vector:", R)
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Transfer matrix: \n", QT.getTransferMatrix())
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Transported phase-space vector:", Rprime)
RprimeTest = np.array([ 0.361914303, -2.717602932, -0.419983646, -2.322331701, \
                        1.260471929, 0.5 ])
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
print("========  QuadTriplet: tests complete  ========")
