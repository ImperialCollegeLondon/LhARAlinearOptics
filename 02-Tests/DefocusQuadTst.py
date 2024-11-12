#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "DefocusQuadrupole" class
=========================================

DefocusQuadrupole.py -- set "relative" path to code

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
print(" ========  DefocusQuadrupole: tests start  ========")

##! Test built-in methods:
DefocusQuadrupoleTest = 1
print()
print("DefocusQuadrupoleTest:", DefocusQuadrupoleTest, \
      " check built-in methods.")

#.. __init__
print("    __init__:")
try:
    DfQuad = BLE.DefocusQuadrupole()
except:
    print('      ----> Correctly trapped no argument exception.')
rStrt = np.array([0.,0.,0.])
vStrt = np.array([[np.pi/2.,np.pi/2.],[0.,0.]])
drStrt = np.array([0.,0.,0.])
dvStrt = np.array([[0.,0.],[0.,0.]])
try:
    DfQuad = BLE.DefocusQuadrupole("NoStrength", rStrt, vStrt, drStrt, dvStrt)
except:
    print('      ----> Correctly trapped no quadrupole strength exception.')


#--------> Clean instances and restart:
BLE.BeamLineElement.cleaninstances()

BLI  = BL.BeamLine(filename)
iRefPrtcl = Prtcl.ReferenceParticle.getinstances()

print("     ----> Reference particle set:")
print("         ----> In:", iRefPrtcl.getPrIn())
print("              Out:", iRefPrtcl.getPrOut())

p0        = iRefPrtcl.getMomentumIn(0)
with np.printoptions(linewidth=500,precision=7,suppress=True):
    print("         ----> Three momentum (in, RPLC):", \
          iRefPrtcl.getPrIn()[0][0:3], ", Magnitude:", p0)

#.. Create valid instance:
DfQuada = BLE.DefocusQuadrupole("ValidDquad1", rStrt, vStrt, drStrt, dvStrt, \
                               0.1, 100.)
print(" Set reference particle phase space for:", DfQuada.getName())
refPrtclSet = iRefPrtcl.setReferenceParticle(DfQuada)
DfQuad = BLE.DefocusQuadrupole("ValidDquad2", rStrt, vStrt, drStrt, dvStrt, \
                               0.1, None, 153.93033817278908)
print(" Set reference particle phase space for:", DfQuad.getName())
refPrtclSet = iRefPrtcl.setReferenceParticle(DfQuad)
    
#.. __repr__
print("    __repr__:")
print("      ---->", repr(DfQuad))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(str(DfQuad))
print("    <---- __str__ done.")

##! Check get methods:
DefocusQuadrupoleTest = 3
print()
print("DefocusQuadrupoleTest:", DefocusQuadrupoleTest, " check get methods.")
print("    ----> print() method; tests all get methods")
print(DfQuad)

##! Check set method:
DefocusQuadrupoleTest += 1
print()
print("DefocusQuadrupoleTest:", DefocusQuadrupoleTest, \
      " test transport through defocusing quadrupole.")
R      = np.array([0.5, 0.1, -0.3, -0.2, 0.1, 0.5])
Rprime = DfQuad.Transport(R)
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Input phase-space vector:", R)
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Transfer matrix: \n", DfQuad.getTransferMatrix())
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Transported phase-space vector:", Rprime)
RprimeTest = np.array([0.674153745, 3.561111554, -0.229746796, 1.531745398, \
                       1.260471929, 0.5])
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Pre-calculated          Rprime:", RprimeTest)
Diff       = np.subtract(Rprime, RprimeTest)
Norm       = np.linalg.norm(Diff)
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Difference Rprime - RprimeTest:", Diff)
print("     ----> Magnitude of Diff:", Norm)
if Norm > 1E-6:
    raise Exception(" !!!!----> FAILED: defocusing quadrupole transport", \
                    " result not as expected.")
else:
    print(" <---- Defocusing quadrupole transport test successful.")

    
##! Check position displacement
DefocusQuadrupoleTest += 1
print()
print("DefocusQuadrupoleTest:", DefocusQuadrupoleTest, \
      " check handling of position displacement.")

rStrt = np.array([0.,0.,0.])
vStrt = np.array([[np.pi/2.,np.pi/2.],[0.,0.]])
drStrt = np.array([0.2,0.1,0.])
dvStrt = np.array([[0.,0.],[0.,0.]])
DQuad1 = BLE.DefocusQuadrupole("ValidQuad3", rStrt, vStrt, drStrt, dvStrt, \
                             0.1, None, 153.93033817278908)
refPrtclSet = iRefPrtcl.setReferenceParticle(DQuad1)

R      = np.array([0.5, 0.1, -0.3, -0.2, 0.1, 0.5])
Rprime = DQuad1.Transport(R)
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Input phase-space vector:", R)
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Transfer matrix: \n", DQuad1.getTransferMatrix())
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Transported phase-space vector:", Rprime)
RprimeTest = np.array([ 0.608918361, 2.189714009, -0.200329912, 2.089382607, \
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
    print(" <---- Defocusing quadrupole transport test successful.")

    
##! Complete:
print()
print("========  DefocusQuadrupole: tests complete  ========")
