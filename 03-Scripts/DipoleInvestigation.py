# -*- coding: utf-8 -*-

import os
import struct
import math as mth

import Particle as Prtcl
import BeamLine as BL

##! Start:
print("========  Read and plot: start  ========")

HOMEPATH    = os.getenv('HOMEPATH')
print(" ----> Initialising with HOMEPATH:", HOMEPATH)
print()
Debug = False

ParticleFILE = Prtcl.Particle.openParticleFile("99-Scratch", "DipoleTest.dat")

print(Prtcl.getParticleInstances())

##! Create LhARA instance:
print("     ----> Create LhARA instance:")
filename     = os.path.join(HOMEPATH, \
                        '11-Parameters/DipoleTest.csv')
print("         ----> Parameters will be read from:", filename)
LhARAbI  = BL.BeamLine(filename)
elementlist  = LhARAbI.getElement()
print(elementlist[3].getAngle())

