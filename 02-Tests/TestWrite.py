#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import struct
import numpy as np

import Particle as Prtcl

ParticleFILE = Prtcl.Particle.createParticleFile("99-Scratch", "TestFile.dat")

TrcSpc = np.array([1., 2., 3., 4., 5., 6.])

refPrtcl  = Prtcl.ReferenceParticle()

iPrtcl = Prtcl.Particle()
iPrtcl.setLocation("Place 1")
iPrtcl.setz(1.1)
iPrtcl.sets(1.2)
TrcSpc = np.array([0.1, 0.002, 0.2, 0.004, 0., 18.])
iPrtcl.setTraceSpace(TrcSpc)
iPrtcl.setDebug(True)
iPrtcl.writeParticle(ParticleFILE)
iPrtcl.setDebug(False)

iPrtcl = Prtcl.Particle()
iPrtcl.setLocation("Place 1")
iPrtcl.setz(1.1)
iPrtcl.sets(1.2)
TrcSpc = np.array([0.1, 0.002, 0.2, 0.004, 0., 18.])
iPrtcl.setTraceSpace(TrcSpc)
iPrtcl.setLocation("Place 2")
iPrtcl.setz(1.1)
iPrtcl.sets(1.2)
TrcSpc = np.array([0.1, 0.002, 0.2, 0.004, 0., 18.])
iPrtcl.setTraceSpace(TrcSpc)
iPrtcl.setDebug(True)
iPrtcl.writeParticle(ParticleFILE)
iPrtcl.setDebug(False)

iPrtcl = Prtcl.Particle()
iPrtcl.setLocation("Place 1")
iPrtcl.setz(1.1)
iPrtcl.sets(1.2)
TrcSpc = np.array([0.1, 0.002, 0.2, 0.004, 0., 18.])
iPrtcl.setTraceSpace(TrcSpc)
iPrtcl.setLocation("Place 2")
iPrtcl.setz(1.1)
iPrtcl.sets(1.2)
TrcSpc = np.array([0.1, 0.002, 0.2, 0.004, 0., 18.])
iPrtcl.setTraceSpace(TrcSpc)
iPrtcl.setLocation("Place 3")
iPrtcl.setz(1.1)
iPrtcl.sets(1.2)
TrcSpc = np.array([0.1, 0.002, 0.2, 0.004, 0., 18.])
iPrtcl.setTraceSpace(TrcSpc)
iPrtcl.setDebug(True)
iPrtcl.writeParticle(ParticleFILE)
iPrtcl.setDebug(False)

iPrtcl.flushNcloseParticleFile(ParticleFILE)
