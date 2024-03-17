#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import struct
import math as mth

import Particle  as Prtcl
import BeamLine as BL
import BeamIO   as bmIO

##! Start:
print("========  DRACO event reading: start  ========")

HOMEPATH    = os.getenv('HOMEPATH')
print("     ----> Initialising with HOMEPATH:", HOMEPATH)
Debug = False

writePATH = HOMEPATH + "/99-Scratch"
"""
ParticleFILE = Prtcl.Particle.openParticleFile(writePATH, \
                                               "DRACOSimulation.dat")
"""
ibmIOr = bmIO.BeamIO(writePATH, "DRACOsimulation.dat")

EndOfFile = False
iEvt = 0
iCnt = 0
Scl  = 10
iPrt = 0

print("     <---- Initialisation done.")

##! Read data file:
print("     ----> Starting to read events:")

while not EndOfFile:
#while iEvt < 10000:
    #EndOfFile = Prtcl.Particle.readParticle(ParticleFILE)
    EndOfFile = ibmIOr.readBeamDataRecord()
    
    if BL.BeamLine.getinstance() == None:
        ##! Create DRACO instance:
        print("     ----> Create DRACO instance:")
        filename     = os.path.join(HOMEPATH, \
                        '11-Parameters/DRACOBeamLine-Params-LsrDrvn.csv')
        print("         ----> Parameters will be read from:", filename)
        DRACObI  = BL.BeamLine(filename)
        if Debug:
            print(DRACObI)

    else:
        if not EndOfFile:
            iEvt += 1
            if (iEvt % Scl) == 0:
                print("         ----> Read event ", iEvt)
                iCnt += 1
                if iCnt == 10:
                    iCnt = 1
                    Scl  = Scl * 10
                        
print("     <---- Event loop done, ", iEvt, "events read")

##! Plot progression:
print("     ----> Plot progression:")
Prtcl.Particle.plotTraceSpaceProgression()
Prtcl.Particle.plotLongitudinalTraceSpaceProgression()
print(" <---- Done.")
print("========  DRACO event reading: end  ========")
