#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import struct
import math as mth

import Particle as Prtcl

ParticleFILE = Prtcl.Particle.openParticleFile("99-Scratch", "TestFile.dat")

EndOfFile = False
iEvt = 0
while not EndOfFile:
    EndOfFile = Prtcl.Particle.readParticle(ParticleFILE)
    if not EndOfFile: iEvt += 1

print(iEvt, " events read")
"""
Prtcl.Particle.plotPhaseSpaceProgression()
"""
