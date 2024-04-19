#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "RPLCswitch" class
==================================

  RPLCswitch.py -- set "relative" path to code

"""

import os
import numpy             as np

import Particle          as Prtcl
import BeamLineElement   as BLE
import BeamLine          as BL

HOMEPATH = os.getenv('HOMEPATH')
filename = os.path.join(HOMEPATH, \
                        '11-Parameters/Dummy4Tests.csv')

##! Start:
print("========  RPLCswitch: tests start  ========")

##! Test singleton class feature:
RPLCswitchTest = 1
print()
print("RPLCswitchTest:", RPLCswitchTest, \
      " check built-in methods.")

#.. __init__
print("    __init__:")
try:
    RPLCswtch = BLE.RPLCswitch()
except:
    print('      ----> Correctly trapped no argument exception.')


#--------> Clean instances and restart:
BLE.BeamLineElement.cleaninstances()
BLI  = BL.BeamLine(filename)
print(BLI)

#.. Create valid instance:
rStrt = np.array([0.,0.,0.])
vStrt = np.array([[np.pi/2.,0.],[0.,0.]])
drStrt = np.array([0.,0.,0.])
dvStrt = np.array([[0.,0.],[0.,0.]])
RPLCswtch = BLE.RPLCswitch("ValidRPLCswitch", rStrt, vStrt, drStrt, dvStrt, \
                           True)
    
#.. __repr__
print("    __repr__:")
print("      ---->", repr(RPLCswtch))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(str(RPLCswtch))
print("    <---- __str__ done.")

##! Check switch:
RPLCswitchTest += 1
print()
print("RPLCswitchTest:", RPLCswitchTest, " test RLPC switch.")
R          = np.array([0.005, 0.1, -0.003, -0.2, 0.1, 0.05])
RprimeTest = np.array([-0.003, -0.2, -0.005, -0.1, 0.1, 0.05])
Rprime = RPLCswtch.Transport(R)
print("     ----> Input phase-space vector:", R)
print("     ----> Transfer matrix:")
print("         ", RPLCswtch.getTransferMatrix()[0,0], \
                   RPLCswtch.getTransferMatrix()[0,1], \
                   RPLCswtch.getTransferMatrix()[0,2], \
                   RPLCswtch.getTransferMatrix()[0,3], \
                   RPLCswtch.getTransferMatrix()[0,4], \
                   RPLCswtch.getTransferMatrix()[0,5])
print("         ", RPLCswtch.getTransferMatrix()[1,0], \
                   RPLCswtch.getTransferMatrix()[1,1], \
                   RPLCswtch.getTransferMatrix()[1,2], \
                   RPLCswtch.getTransferMatrix()[1,3], \
                   RPLCswtch.getTransferMatrix()[1,4], \
                   RPLCswtch.getTransferMatrix()[1,5])
print("         ", RPLCswtch.getTransferMatrix()[2,0], \
                   RPLCswtch.getTransferMatrix()[2,1], \
                   RPLCswtch.getTransferMatrix()[2,2], \
                   RPLCswtch.getTransferMatrix()[2,3], \
                   RPLCswtch.getTransferMatrix()[2,4], \
                   RPLCswtch.getTransferMatrix()[2,5])
print("         ", RPLCswtch.getTransferMatrix()[3,0], \
                   RPLCswtch.getTransferMatrix()[3,1], \
                   RPLCswtch.getTransferMatrix()[3,2], \
                   RPLCswtch.getTransferMatrix()[3,3], \
                   RPLCswtch.getTransferMatrix()[3,4], \
                   RPLCswtch.getTransferMatrix()[3,5])
print("         ", RPLCswtch.getTransferMatrix()[4,0], \
                   RPLCswtch.getTransferMatrix()[4,1], \
                   RPLCswtch.getTransferMatrix()[4,2], \
                   RPLCswtch.getTransferMatrix()[4,3], \
                   RPLCswtch.getTransferMatrix()[4,4], \
                   RPLCswtch.getTransferMatrix()[4,5])
print("         ", RPLCswtch.getTransferMatrix()[5,0], \
                   RPLCswtch.getTransferMatrix()[5,1], \
                   RPLCswtch.getTransferMatrix()[5,2], \
                   RPLCswtch.getTransferMatrix()[5,3], \
                   RPLCswtch.getTransferMatrix()[5,4], \
                   RPLCswtch.getTransferMatrix()[5,5])
with np.printoptions(linewidth=500,precision=7,suppress=True):
    print("     ----> Transported phase-space vector:", Rprime)
                        
Diff       = np.subtract(Rprime, RprimeTest)
Norm       = np.linalg.norm(Diff)
with np.printoptions(linewidth=500,precision=7,suppress=True):
    print("     ----> Difference Rprime - RprimeTest:", Diff)
print("     ----> Magnitude of Diff:", Norm)
if Norm > 1E-6:
    raise Exception(" !!!!----> FAILED: drift transport result not as expected.")
else:
    print(" <---- RPLCswitch transport test successful.")

##! Check switch:
RPLCswitchTest += 1
print()
print("RPLCswitchTest:", RPLCswitchTest, " test 2D rotation.")
BLE.BeamLineElement.cleaninstances()
BL.BeamLine.cleaninstance()
Prtcl.Particle.cleanAllParticles()
BLI  = BL.BeamLine(filename)
print(BLI)
RPLCswtch = BLE.RPLCswitch("ValidRPLCswitch", rStrt, vStrt, drStrt, dvStrt)
Rprime = RPLCswtch.Transport(R)
with np.printoptions(linewidth=500,precision=7,suppress=True):
    print("     ----> Transported phase-space vector:", Rprime)
print("     ----> Input phase-space vector:", R)
print("     ----> Transfer matrix:")
print("         ", RPLCswtch.getTransferMatrix()[0,0], \
                   RPLCswtch.getTransferMatrix()[0,1], \
                   RPLCswtch.getTransferMatrix()[0,2], \
                   RPLCswtch.getTransferMatrix()[0,3], \
                   RPLCswtch.getTransferMatrix()[0,4], \
                   RPLCswtch.getTransferMatrix()[0,5])
print("         ", RPLCswtch.getTransferMatrix()[1,0], \
                   RPLCswtch.getTransferMatrix()[1,1], \
                   RPLCswtch.getTransferMatrix()[1,2], \
                   RPLCswtch.getTransferMatrix()[1,3], \
                   RPLCswtch.getTransferMatrix()[1,4], \
                   RPLCswtch.getTransferMatrix()[1,5])
print("         ", RPLCswtch.getTransferMatrix()[2,0], \
                   RPLCswtch.getTransferMatrix()[2,1], \
                   RPLCswtch.getTransferMatrix()[2,2], \
                   RPLCswtch.getTransferMatrix()[2,3], \
                   RPLCswtch.getTransferMatrix()[2,4], \
                   RPLCswtch.getTransferMatrix()[2,5])
print("         ", RPLCswtch.getTransferMatrix()[3,0], \
                   RPLCswtch.getTransferMatrix()[3,1], \
                   RPLCswtch.getTransferMatrix()[3,2], \
                   RPLCswtch.getTransferMatrix()[3,3], \
                   RPLCswtch.getTransferMatrix()[3,4], \
                   RPLCswtch.getTransferMatrix()[3,5])
print("         ", RPLCswtch.getTransferMatrix()[4,0], \
                   RPLCswtch.getTransferMatrix()[4,1], \
                   RPLCswtch.getTransferMatrix()[4,2], \
                   RPLCswtch.getTransferMatrix()[4,3], \
                   RPLCswtch.getTransferMatrix()[4,4], \
                   RPLCswtch.getTransferMatrix()[4,5])
print("         ", RPLCswtch.getTransferMatrix()[5,0], \
                   RPLCswtch.getTransferMatrix()[5,1], \
                   RPLCswtch.getTransferMatrix()[5,2], \
                   RPLCswtch.getTransferMatrix()[5,3], \
                   RPLCswtch.getTransferMatrix()[5,4], \
                   RPLCswtch.getTransferMatrix()[5,5])
with np.printoptions(linewidth=500,precision=7,suppress=True):
    print("     ----> Transported phase-space vector:", Rprime)
                        
Diff       = np.subtract(Rprime, RprimeTest)
Norm       = np.linalg.norm(Diff)
with np.printoptions(linewidth=500,precision=7,suppress=True):
    print("     ----> Difference Rprime - RprimeTest:", Diff)
print("     ----> Magnitude of Diff:", Norm)
if Norm > 1E-6:
    raise Exception( \
            " !!!!----> FAILED: drift transport result not as expected.")
else:
    print(" <---- RPLCswitch transport test successful.")
    

##! Complete:
print()
print("========  RPLCswitch: tests complete  ========")
