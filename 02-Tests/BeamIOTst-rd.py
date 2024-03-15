#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "BeamIO" class
==============================

  BeamIO.py -- set "relative" path to code

  Testing Read functionality.

"""

import os
import sys

import BeamIO          as bmIO
import BeamLine        as BL
import BeamLineElement as BLE
import Particle        as Prtcl

##! Start:
print("========  BeamIO (read): tests start  ========")

##! First check can read data format version 1:
HOMEPATH = os.getenv('HOMEPATH')
filename = os.path.join(HOMEPATH, \
                        '11-Parameters/LIONBeamLine-Params-LsrDrvn.csv')
BLI  = BL.BeamLine(filename)

BeamIOTest = 1
print()
print("BeamIOTest:", BeamIOTest, " check data format v1 can be read OK.")

ibmIOr = bmIO.BeamIO("11-Parameters", "Data4Tests.dat")

EndOfFile = False
iEvt = 0
iCnt = 0
nEvt = 100
Scl  = 10
print("     ----> Read data format 1 file:")
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
    if iEvt <0:
        print(Prtcl.Particle.getParticleInstances()[iEvt])
    if iEvt == nEvt:
        break

print("     <----", iEvt, "events read")

Prtcl.Particle.cleanParticles()
Prtcl.ReferenceParticle.cleaninstance()
BLE.BeamLineElement.cleanInstances()
bmIO.BeamIO.cleanBeamIOfiles()

print(" <---- Version 1 data format read check done!")


##! Test writing and reading of beam-line setup:
BeamIOTest += 1
print()
print("BeamIOTTest:", BeamIOTest, \
      " check reading of beam-line and particles.")

ibmIOr = bmIO.BeamIO("99-Scratch", "Data4Tests.dat")

EndOfFile = False
iEvt = 0
iCnt = 0
nEvt = 100
Scl  = 10
print("     ----> Read data format >1 file:")
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
    if iEvt <0:
        print(Prtcl.Particle.getParticleInstances()[iEvt])
    if iEvt == nEvt:
        break

print("     <----", iEvt, "events read")

print(" <---- Version 2 data format read check done!")

##! Complete:
print()
print("========  BeamIO (read): tests complete  ========")
