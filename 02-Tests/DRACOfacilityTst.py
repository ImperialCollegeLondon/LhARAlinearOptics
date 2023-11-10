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
import DRACObeam        as LNb
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

DRACObI  = LNb.DRACObeam(filename)
print(DRACObI)

print()
print("     <---- DRACOFacilityTest:", DRACOFacilityTest, \
      " facility instance created.")

##! Check generation
DRACOFacilityTest += 1
print()
print("     ----> DRACOFacilityTest:", DRACOFacilityTest, \
      " check generation/tracking.")

print("         ----> First using hard-coded phase space at source.")
DRACObI.setDebug(True)
DRACObI.setSrcPhsSpc(np.array([0.0001, -0.0001, 0.0002, 0.0001, 0., 20.]))
OK = DRACObI.trackDRACO(1)
DRACObI.setDebug(False)

print("         ----> Second using generated beam:")
DRACObI.setSrcPhsSpc()
print(DRACObI)

NEvt = 10
OK = DRACObI.trackDRACO(NEvt)

print("     ----> Find one event that made it to end of beam line:")

Prt    = False
iPrtcl = 0

while not Prt:
    OK = DRACObI.trackDRACO(1)
    iPrtclInst = Prtcl.Particle.instances[len(Prtcl.Particle.instances)-1]
    if iPrtcl >= NEvt:
        print("         ----> No events made it to end of delivery section.")
        Prt = True
    if iPrtclInst.getz()[len(iPrtclInst.getLocation())-1] > 2.1:
        OK     = iPrtclInst.printProgression()
        PhsSpc = iPrtclInst.getPhaseSpace()[0]
        Prt    = True
print("     <---- Done printing one event that made it to end of delivery:")


##! End:
print()
print(" <---- Tests finished.")


##! Complete:
print()
print("========  DRACOFacility tests complete  ========")
