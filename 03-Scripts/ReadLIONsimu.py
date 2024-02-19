#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import struct
import math as mth

import Particle as Prtcl
import BeamLine as BL

HOMEPATH    = os.getenv('HOMEPATH')
print("     ----> Initialising with HOMEPATH:", HOMEPATH)
Debug = False

ParticleFILE = Prtcl.Particle.openParticleFile("99-Scratch", "LIONsimu.dat")

##! Create LION instance:
print("     ----> Create LION instance:")
filename     = os.path.join(HOMEPATH, \
                        '11-Parameters/LIONBeamLine-Params-LsrDrvn.csv')
print("         ----> Parameters will be read from:", filename)
LIONbI  = BL.BeamLine(filename)
if Debug:
    print(LIONbI)

print("     <---- Initialisation done.")

print(" Read events from:", ParticleFILE)

EndOfFile = False
iEvt = 0
iCnt = 0
Scl  = 10
while not EndOfFile:
    EndOfFile = Prtcl.Particle.readParticle(ParticleFILE)
    if not EndOfFile:
        iEvt += 1
        if (iEvt % Scl) == 0:
            print("     ----> Read event ", iEvt)
            iCnt += 1
            if iCnt == 10:
                iCnt = 1
                Scl  = Scl * 10

print(" <----", iEvt, "events read")

print()
print(" Plot progression:")
Prtcl.Particle.plotTraceSpaceProgression()
Prtcl.Particle.plotLongitudinalTraceSpaceProgression()
print(" <---- Done.")
