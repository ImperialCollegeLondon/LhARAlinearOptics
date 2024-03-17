#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import struct
import math as mth

import Particle as Prtcl
import BeamLine as BL
import BeamIO   as bmIO

HOMEPATH    = os.getenv('HOMEPATH')
print("     ----> Initialising with HOMEPATH:", HOMEPATH)
Debug = False

ibmIOr = bmIO.BeamIO("99-Scratch", "LIONsimu.dat")
#ParticleFILE = Prtcl.Particle.openParticleFile("99-Scratch", "LIONsimu.dat")

print("     <---- Initialisation done.")

print(" Read events from:", ibmIOr.getdataFILE())

EndOfFile = False
iEvt = 0
iCnt = 0
Scl  = 10
while not EndOfFile:
    #EndOfFile = Prtcl.Particle.readParticle(ParticleFILE)
    EndOfFile = ibmIOr.readBeamDataRecord()

    if BL.BeamLine.getinstance() == None:
        ##! Create LION instance:
        print("     ----> Create LION instance:")
        filename     = os.path.join(HOMEPATH, \
#                         '11-Parameters/LIONBeamLine-Params-LsrDrvn.csv')
                         '11-Parameters/LIONBeamLine-Params-Gauss.csv')
#                         '11-Parameters/LIONBeamLine-Params-Flat.csv')
        print("         ----> Parameters will be read from:", filename)
        LIONbI  = BL.BeamLine(filename)
        if Debug:
            print(LIONbI)
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

print()`
print(" Plot progression:")
Prtcl.Particle.plotTraceSpaceProgression()
Prtcl.Particle.plotLongitudinalTraceSpaceProgression()
print(" <---- Done.")
