#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "BeamIO" class
==============================

  BeamIO.py -- set "relative" path to code

  Testing Read of BDSIM particle file functionality.

"""

import os
import sys

import BeamIO          as bmIO
import BeamLine        as BL
import BeamLineElement as BLE
import Particle        as Prtcl

##! Start:
print("========  BeamIO (read BDSIM particle file): tests start  ========")

##! First check can read data format version 1:
HOMEPATH = os.getenv('HOMEPATH')

BeamIOTest = 1
print()
print("BeamIOTest:", BeamIOTest, " check file can be read OK.")

ibmIOr = bmIO.BeamIO("12-Data4Tests", "BDSIM-Data4Tests.dat", False, True)

filename     = os.path.join('11-Parameters', 'LhARA-Stage1-BeamDelivery.csv')

iFF = BL.BeamLine(filename)

EndOfFile = False
iEvt = 0
iCnt = 0
nEvt = 100
Scl  = 10
print("     ----> Read BDSIM data format file:")
while not EndOfFile:
    EndOfFile = ibmIOr.readBeamDataRecord()
    if not EndOfFile:
        iEvt += 1
        if (iEvt % Scl) == 0:
            print("         ----> Read event ", iEvt)
            iCnt += 1
            if iCnt == 10:
                iCnt = 1
                Scl  = Scl * 10
    if iEvt < 1:
        print(Prtcl.Particle.getParticleInstances()[iEvt])
    if iEvt == nEvt:
        break

print("     <----", iEvt, "events read")

print(" <---- Data read check done!")

##! Complete:
print()
print("========  BeamIO (read BDSIM particle file): tests complete  ========")
