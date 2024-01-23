#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "QuadDoublet" class
=======================================

QuadDoublet.py -- set "relative" path to code

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
print("========  QuadDoublet: tests start  ========")

##! Test built-in methods:
QuadDoubletTest = 1
print()
print("QuadDoubletTest:", QuadDoubletTest, \
      " check built-in methods.")

#.. __init__
print("    __init__:")
try:
    QD = BLE.QuadDoublet()
except:
    print('      ----> Correctly trapped no argument exception.')
rStrt = np.array([0., 0., 0.])
vStrt = np.array([0., 0.])
drStrt = np.array([0., 0., 0.])
dvStrt = np.array([0., 0.])
try:
    QD = BLE.QuadDoublet("NoStrength", rStrt, vStrt, drStrt, dvStrt)
except:
    print('      ----> Correctly trapped no doublet argument exception.')

    
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

#.. Create valid instances:
QD1 = BLE.QuadDoublet("ValidQuadDoublet1", rStrt, vStrt, drStrt, dvStrt, \
                      "FD", [0.1, 500., None], 0.01, [0.1, 500., None])
QD2 = BLE.QuadDoublet("ValidQuadDoublet2", rStrt, vStrt, drStrt, dvStrt, \
                      "DF", [0.1, 500., None], 0.01, [0.1, 500., None])
            
#.. __repr__
print("    __repr__:")
print("      ---->", repr(QD1))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(str(QD1))
print(str(QD2))
print("    <---- __str__ done.")

##! Check transport:
QuadDoubletTest += 1
print()
print("QuadDoubletTest:", QuadDoubletTest, \
      " test transport through focusing quadrupole.")
R      = np.array([0.5, 0.1, -0.3, -0.2, 0.1, 0.5])
Rprime = QD1.Transport(R)
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Input phase-space vector:", R)
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Transfer matrix: \n", QD1.getTransferMatrix())
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Transported phase-space vector:", Rprime)
RprimeTest = np.array([ -1.912587754, -34.62556903, -0.660238477, 21.67242421, \
                        2.536991051, 0.5] )
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
print("========  QuadDoublet: tests complete  ========")
