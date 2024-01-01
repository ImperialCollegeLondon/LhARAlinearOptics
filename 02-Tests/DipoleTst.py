#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "SectorDipole" class
=============================

  SectorDipole.py -- set "relative" path to code

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
print("========  SectorDipole: tests start  ========")

##! Test built-in methods:
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
RprimeTest = np.array([0.580323519, 0.022084405, -0.504091844, -0.2, \
                       -0.659963612, 0.05])
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
