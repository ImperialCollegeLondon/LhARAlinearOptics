#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import struct
import math as mth
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np

import Particle as Prtcl
import BeamLine as BL

##! Start:
print("========  Read and plot: start  ========")

HOMEPATH = os.getenv("HOMEPATH")
print(" ----> Initialising with HOMEPATH:", HOMEPATH)
print()
Debug = True
ParticleFILE = Prtcl.Particle.openParticleFile("99-Scratch", "LhARAsimu.dat")

##! Create LhARA instance:
print("     ----> Create LhARA instance:")
filename = os.path.join(HOMEPATH, "11-Parameters/RFtest.csv")
print("         ----> Parameters will be read from:", filename)

LhARAbI  = BL.BeamLine(filename)
if Debug:
    print(LhARAbI)

print("     <---- LhARA instance created.")

print("     ----> Read events from:", ParticleFILE)

print()
print(" <---- Initialisation done.")

##! Create LhARA instance:
print(" ----> Read event file:")
print()

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
print(" ----> Plot progression:")
Prtcl.Particle.plotTraceSpaceProgression()
Prtcl.Particle.plotLongitudinalTraceSpaceProgression()
print(" <---- Done.")

##! Complete:
print()
print("========  Read and plot: complete  ========")


