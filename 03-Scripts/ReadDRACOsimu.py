#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import struct
import math as mth

import Particle  as Prtcl
import DRACObeam as LNb

##! Start:
print("========  DRACO event reading: start  ========")

HOMEPATH    = os.getenv('HOMEPATH')
print("     ----> Initialising with HOMEPATH:", HOMEPATH)
Debug = False

writePATH = HOMEPATH + "/99-Scratch"
ParticleFILE = Prtcl.Particle.openParticleFile(writePATH, \
                                               "DRACOsimu.dat")
EndOfFile = False
iEvt = 0
iCnt = 0
Scl  = 10
iPrt = 0
print("     ----> Read events from:", ParticleFILE)

##! Create DRACO instance:
print("     ----> Create DRACO instance:")
filename     = os.path.join(HOMEPATH, \
                        '11-Parameters/DRACOBeamLine-Params-LsrDrvn.csv')
print("         ----> Parameters will be read from:", filename)
DRACObI  = LNb.DRACObeam(filename)
if Debug:
    print(DRACObI)

print("     <---- Initialisation done.")

##! Read data file:
print("     ----> Starting to read events:")

while not EndOfFile:
#while iEvt < 10000:
    EndOfFile = Prtcl.Particle.readParticle(ParticleFILE)
    if not EndOfFile:
        iEvt += 1
        if (iEvt % Scl) == 0:
            print("         ----> Read event ", iEvt)
            iCnt += 1
            if iCnt == 10:
                iCnt = 1
                Scl  = Scl * 10
    iPrtcl  = Prtcl.Particle.getParticleInstances() \
              [len(Prtcl.Particle.getParticleInstances())-1]
    nPhsSpc = len(iPrtcl.getPhaseSpace())
    
    if Debug and iEvt < 10:
        print(iPrtcl)

print("     <---- Event loop done, ", iEvt, "events read")

##! Plot progression:
print("     ----> Plot progression:")

Prtcl.Particle.plotPhaseSpaceProgression()
print(" <---- Done.")
print("========  DRACO event reading: end  ========")
