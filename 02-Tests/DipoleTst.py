#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "SectorDipole" class
=============================

  SectorDipole.py -- set "relative" path to code

"""

import os
import numpy as np

import BeamLineElement as BLE
import BeamLine        as BL
import Particle        as Prtcl

HOMEPATH = os.getenv('HOMEPATH')
filename = os.path.join(HOMEPATH, \
                        '11-Parameters/LIONBeamLine-Params-LsrDrvn.csv')
BLI  = BL.BeamLine(filename)

iRefPrtcl = Prtcl.ReferenceParticle.getinstance()


##! Start:
print("========  SectorDipole: tests start  ========")

print("Reference particle:")
xx    = iRefPrtcl.getPrIn()[0]
xx[2] = 194.7585262
iRefPrtcl._PrIn[0] = xx
p0        = iRefPrtcl.getMomentumIn(0)
with np.printoptions(linewidth=500,precision=7,suppress=True):
    print("     ----> Three momentum (in, RPLC):", \
          iRefPrtcl.getPrIn()[0][0:3])
    print("                           Magnitude:", p0)


##! Test built-in emthods:
SectorDipoleTest = 1
print()
print("SectorDipoleTest:", SectorDipoleTest, \
      " check built-in methods.")

#.. __init__
print("    __init__:")
try:
    Dpl = BLE.SectorDipole()
except:
    print('      ----> Correctly trapped no argument exception.')
rStrt = np.array([0.,0.,0.])
vStrt = np.array([0.,0.])
drStrt = np.array([0.,0.,0.])
dvStrt = np.array([0.,0.])
try:
    Dpl = BLE.SectorDipole("NoAngle", rStrt, vStrt, drStrt, dvStrt)
except:
    print('      ----> Correctly trapped no angle exception.')

try:
    Dpl = BLE.SectorDipole("NoField", rStrt, vStrt, drStrt, dvStrt, 0.3)
except:
    print('      ----> Correctly trapped no field exception.')

#.. Create valid instance:
Ang = 45./180.*np.pi
B   = 0.5
Dpl = BLE.SectorDipole("ValidSectorDipole", rStrt, vStrt, drStrt, dvStrt, \
                       Ang, B)
    
#.. __repr__
print("    __repr__:")
print("      ---->", repr(Dpl))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(str(Dpl))
print("    <---- __str__ done.")

##! Check get methods:
SectorDipoleTest = 3
print()
print("SectorDipoleTest:", SectorDipoleTest, " check get methods.")
print("    ----> print() method; tests all get methods")
print(Dpl)

##! Check set method:
SectorDipoleTest = 4
print()
print("SectorDipoleTest:", SectorDipoleTest, " check set method.")
BLE.SectorDipole.setDebug(True)
print(Dpl)
BLE.SectorDipole.setDebug(False)

##! Check set method:
SectorDipoleTest += 1
print()
print("SectorDipoleTest:", SectorDipoleTest, " test transport through dipole.")
R      = np.array([0.5, 0.1, -0.3, -0.2, 0., 0.05])
Rprime = Dpl.Transport(R)
print("     ----> Transported phase-space vector:", Rprime)
RprimeTest = np.array([0.464454646, -0.166046948, -0.504091844, -0.2, \
                       0., 0.05])
Diff       = np.subtract(Rprime, RprimeTest)
Norm       = np.linalg.norm(Diff)
with np.printoptions(linewidth=500,precision=7,suppress=True):
    print("     ----> Difference Rprime - RprimeTest:", Diff)
print("     ----> Magnitude of Diff:", Norm)
if Norm > 1E-6:
    raise Exception(" !!!!----> FAILED:", \
                    "dipole transport result not as expected.")
else:
    print(" <---- SectorDipole transport test successful.")

##! Complete:
print()
print("========  SectorDipole: tests complete  ========")
