#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for setting up the "DRACOFacility"
==============================================

  DRACOFacility.py -- set "relative" path to code

"""

import os
import sys
import math  as mth
import scipy as sp
import numpy as np
import matplotlib.pyplot as plt


import Simulation      as Sml
import BeamLine        as BL
import BeamLineElement as BLE
import Particle        as Prtcl

##! Start:
print("========  DRACOFacility tests  ========")
HOMEPATH    = os.getenv('HOMEPATH')
print("Initialising with HOMEPATH:", HOMEPATH)
filename     = os.path.join(HOMEPATH, \
                        '11-Parameters/DRACOBeamLine-Params-LsrDrvn.csv')
print(" <---- Parameters will be read from:", filename)

##! Start:
print()
print(" ----> Tests start:")

##! Create facility instance:
DRACOFacilityTest = 1
print()
print("     ----> DRACOFacilityTest:", DRACOFacilityTest, \
      " create facility instance.")

BL.BeamLine.setDebug(True)
DRACObI  = BL.BeamLine(filename)
print(DRACObI)
BL.BeamLine.setDebug(False)

print()
print("     <---- DRACOFacilityTest:", DRACOFacilityTest, \
      " facility instance created.")

##! Check generation
DRACOFacilityTest += 1
print()
print("     ----> DRACOFacilityTest:", DRACOFacilityTest, \
      " check generation/tracking.")

print("         ----> First using hard-coded trace space at source.")
DRACObI.setDebug(True)
DRACObI.setSrcTrcSpc(np.array([0.0001, -0.0001, 0.0002, 0.0001, 0., 20.]))
OK = DRACObI.trackBeam(1)
DRACObI.setDebug(False)

print("         ----> Second using generated beam:")
DRACObI.setSrcTrcSpc()
print(DRACObI)

NEvt = 10000
OK = DRACObI.trackBeam(NEvt)

"""
       ---> Had to scratch this bit because upgraded clean-up means it
            wont work.
print("     ----> Find one event that made it to end of beam line:")

Prt    = False
iPrtcl = 0

print(" Here:", len(Prtcl.Particle.getParticleInstances()))

while not Prt:
    OK = DRACObI.trackDRACO(1)
    print(" HereHere:", len(Prtcl.Particle.getParticleInstances()))
    iPrtclInst = Prtcl.Particle.instances[ \
                            len(Prtcl.Particle.getParticleInstances())-1]
    if iPrtcl >= NEvt:
        print("         ----> No events made it to end of delivery section.")
        Prt = True
    if iPrtclInst.getz()[len(iPrtclInst.getLocation())-1] > 2.1:
        OK     = iPrtclInst.printProgression()
        TrcSpc = iPrtclInst.getTraceSpace()[0]
        Prt    = True
print("     <---- Done printing one event that made it to end of delivery:")
"""

##! End:
print()
print(" <---- Tests finished.")


##! Complete:
print()
print("========  DRACOFacility tests complete  ========")
