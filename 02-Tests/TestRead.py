#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import struct
import math as mth

import Particle as Prtcl
import BeamLine as BL

ParticleFILE = Prtcl.Particle.openParticleFile("99-Scratch", "TestFile.dat")

HOMEPATH = os.getenv('HOMEPATH')
filename = os.path.join(HOMEPATH, \
                        '11-Parameters/LIONBeamLine-Params-LsrDrvn.csv')
BLI  = BL.BeamLine(filename)

EndOfFile = False
iEvt = 0
while not EndOfFile:
    EndOfFile = Prtcl.Particle.readParticle(ParticleFILE, 7)
    if not EndOfFile: iEvt += 1

print(iEvt, " events read")
"""
Prtcl.Particle.plotPhaseSpaceProgression()
"""
