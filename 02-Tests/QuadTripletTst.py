#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "QuadTriplet" class
===================================

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
rStrt = np.array([0.,0.,0.])
vStrt = np.array([[np.pi/2.,np.pi/2.],[0.,0.]])
drStrt = np.array([0.,0.,0.])
dvStrt = np.array([0.,0.,0.])
try:
    QT = BLE.QuadTriplet("NoStrength", rStrt, vStrt, drStrt, dvStrt)
except:
    print('      ----> Correctly trapped no Triplet argument exception.')

    
#--------> Clean instances and restart:
BLE.BeamLineElement.cleaninstances()

BLI  = BL.BeamLine(filename)
iRefPrtcl = Prtcl.ReferenceParticle.getinstances()

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

#.. Create valid instances:
QT1 = BLE.QuadTriplet("ValidQuadTriplet1", rStrt, vStrt, drStrt, dvStrt, \
                      "FDF", [0.1, 500., None], 0.01, \
                             [0.2, 500., None], 0.01, \
                             [0.1, 500., None])
QT2 = BLE.QuadTriplet("ValidQuadTriplet2", rStrt, vStrt, drStrt, dvStrt, \
                      "DFD", [0.1, 500., None], 0.01, \
                             [0.2, 500., None], 0.01, \
                             [0.1, 500., None])
            
#.. __repr__
print("    __repr__:")
print("      ---->", repr(QT1))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(str(QT1))
print(str(QT2))
print("    <---- __str__ done.")

##! Check transport:
QuadTripletTest += 1
print()
print("QuadTripletTest:", QuadTripletTest, \
      " test transport through focusing quadrupole.")
R      = np.array([0.5, 0.1, -0.3, -0.2, 0.1, 0.5])
Rprime = QT1.Transport(R)
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Input phase-space vector:", R)
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Transfer matrix: \n", QT1.getTransferMatrix())
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Transported phase-space vector:", Rprime)
RprimeTest = np.array([ -8.583918885, 266.6145409, 5.385698434, 91.8026567, \
                        4.973982101, 0.5] )
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
