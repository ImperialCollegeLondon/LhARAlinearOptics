#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import struct
import math as mth

import Particle as Prtcl
import BeamLine as BL
import BeamIO   as bmIO

##! Start:
print("========  Read and plot: start  ========")

HOMEPATH    = os.getenv('HOMEPATH')
print(" ----> Initialising with HOMEPATH:", HOMEPATH)
print()
Debug = False

#ParticleFILE = Prtcl.Particle.openParticleFile("99-Scratch", "LhARAsimu.dat")
ibmIOr = bmIO.BeamIO("99-Scratch", "LhARAsimu.dat")

print(" <---- Initialisation done.")

print(" ----> Read event file:")

EndOfFile = False
iEvt = 0
iCnt = 0
Scl  = 10
while not EndOfFile:
    #EndOfFile = Prtcl.Particle.readParticle(ParticleFILE)
    EndOfFile = ibmIOr.readBeamDataRecord()

    if BL.BeamLine.getinstance() == None:
        filename     = os.path.join(HOMEPATH, \
#                '11-Parameters/LhARABeamLine-Params-LsrDrvn-Gabor.csv')
#                '11-Parameters/LhARABeamLine-Params-LsrDrvn-Solenoid.csv')
#                '11-Parameters/LhARABeamLine-Params-Gauss-Gabor.csv')
                '11-Parameters/LhARABeamLine-Params-Gauss-Solenoid.csv')
        print("         ----> Parameters will be read from:", filename)
        LhARAbI  = BL.BeamLine(filename)
        if Debug:
            print(LhARAbI)
    else:
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
print(" ----> Plot progression:")
Prtcl.Particle.plotTraceSpaceProgression()
Prtcl.Particle.plotLongitudinalTraceSpaceProgression()
print(" <---- Done.")

##! Complete:
print()
print("========  Read and plot: complete  ========")
