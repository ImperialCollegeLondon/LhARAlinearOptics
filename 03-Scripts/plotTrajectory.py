#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math  as mth
import numpy as np
import os

import Particle as Prtcl
import BeamLineElement as BLE
import BeamLine as BL
import BeamIO   as bmIO

"""
  Initialise by setting up the LION beamline, make LION beam line
  instance.
"""
HOMEPATH    = os.getenv('HOMEPATH')

print("     <---- Beam line initialised.")

"""
  Open data file.
"""
print("     ----> Open particle data file:")
#ParticleFILE = Prtcl.Particle.openParticleFile("99-Scratch", "LIONsimu.dat")
ibmIOr = bmIO.BeamIO("99-Scratch", "LIONsimu.dat")
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
EndOfFile = ibmIOr.readBeamDataRecord()
while not EndOfFile:
    EndOfFile = ibmIOr.readBeamDataRecord()
    #EndOfFile = Prtcl.Particle.readParticle(ParticleFILE)

    if BL.BeamLine.getinstances() == None:
        filename     = os.path.join(HOMEPATH, \
                        '11-Parameters/LIONBeamLine-Params-LsrDrvn.csv')
        BLI  = BL.BeamLine(filename)

    else:
        iEvt      += 1
        iPrtcl    = Prtcl.Particle.getinstances()[0]
        if iPrtcl.gets()[len(iPrtcl.gets())-1] > 1.88:
            print("     ----> iEvt:", iEvt, " made it all the way.")
            break
        else:
            cleaned = Prtcl.Particle.cleanParticles()

    print("     ----> Track particle through LION:")
    BLI.setDebug(True)
    BLI.setSrcTrcSpc(iPrtcl.getTraceSpace()[0])
    OK = BLI.trackBeam(1)
    BLI.setDebug(False)
    iPrtcl1 = Prtcl.Particle.getinstances()[1]
    """
  Loop over elements on the LION beam line.
  - Documentation in header of BeamLine.py and BeamLineElement.py.
  - Each beam-line element has a position and orientation three vector
    that specifies the position and orientation of the element.  The
    parameters that define the element depend on the element in question and
    are defined in BeamLineElement.py
    """
    print(" plotTrajectory: loop over elements in LION beam line.")

    iSrcElmnt = 0
    iBlE      = BLE.BeamLineElement.getinstances()[1]
    iSrcElmnt += 1
    print("     ----> Source element  :", iSrcElmnt, "; type:", type(iBlE))

    iElmnt = 0
    for iBLE in BLE.BeamLineElement.getinstances():
        if isinstance(iBLE, BLE.Facility):
            continue
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
