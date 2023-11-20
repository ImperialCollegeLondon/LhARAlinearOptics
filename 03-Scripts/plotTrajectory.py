#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math  as mth
import numpy as np
import os

import Particle as Prtcl
import BeamLineElement as BLE
import LIONbeam as LNb

"""
  Initialise by setting up the LION beamline, make LION beam line
  instance.
"""
HOMEPATH    = os.getenv('HOMEPATH')
print("plotTrajectory: initialising with HOMEPATH:", HOMEPATH)
filename     = os.path.join(HOMEPATH, \
                        '11-Parameters/LIONBeamLine-Params-LsrDrvn.csv')
print("     ----> Parameters will be read from:", filename)
LNbI  = LNb.LIONbeam(filename)
print(LNbI)
print("     <---- LION beam line initialised.")

"""
  Open data file.
"""
print("     ----> Open particle data file:")
ParticleFILE = Prtcl.Particle.openParticleFile("99-Scratch", "LIONsimu.dat")
print("     <---- Done.")

"""
  Loop over particles and find the first one that makes it all the way
  through.

  Then call tracking routines.
"""
print(" plotTrajectory: loop over particles, find one that get through.")
EndOfFile = False
iEvt      = 0
iPrtcl    = None
while not EndOfFile:
    EndOfFile = Prtcl.Particle.readParticle(ParticleFILE)
    iEvt      += 1
    iPrtcl    = Prtcl.Particle.getParticleInstances()[0]
    if iPrtcl.getz()[len(iPrtcl.getz())-1] > 1.88:
        print("     ----> iEvt:", iEvt, " made it all the way.")
        break
    else:
        cleaned = Prtcl.Particle.cleanParticles()

print("     ----> Track particle through LION:")
LNbI.setDebug(True)
LNbI.setSrcTrcSpc(iPrtcl.getTraceSpace()[0])
OK = LNbI.trackLION(1)
LNbI.setDebug(False)
iPrtcl1 = Prtcl.Particle.getParticleInstances()[0]

"""
  Loop over elements on the LION beam line.
  - Documentation in header of LIONbeam.py and BeamLineElement.py.
  - Each beam-line element has a position and orientation three vector
    that specifies the position and orientation of the element.  The
    parameters that define the element depend on the element in question and
    are defined in BeamLineElement.py
"""
print(" plotTrajectory: loop over elements in LION beam line.")

iSrcElmnt = 0
iBlE      = BLE.BeamLineElement.getinstances()[0]
iSrcElmnt += 1
print("     ----> Source element  :", iSrcElmnt, "; type:", type(iBlE))

iElmnt = 0
for iBlE in BLE.BeamLineElement.getinstances():
    iElmnt += 1
    print("     ----> Beam line element :", iElmnt, "; type:", type(iBlE))

"""
  Print coordinates of particle at interfaces.
   - Documentation in header of Particle.py
   - Trace space is numpy array: x, x', y, y', t and E
"""
print(" plotTrajectory: print coordinates of particle at interfaces", \
      "along LION beam line.")
for iLoc in range(len(iPrtcl1.getTraceSpace())):
    with np.printoptions(linewidth=500,precision=7,suppress=True):
        print("     ---->", iPrtcl1.getLocation()[iLoc], ":", \
              iPrtcl1.getTraceSpace()[iLoc]) 

print()
print(" <---- Done.")
