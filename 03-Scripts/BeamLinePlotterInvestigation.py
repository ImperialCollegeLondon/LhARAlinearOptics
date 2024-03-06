#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import struct
import math as mth
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

import Particle as Prtcl
import BeamLine as BL

HOMEPATH = os.getenv("HOMEPATH")
print(" ----> Initialising with HOMEPATH:", HOMEPATH)

##! Create LhARA instance:
print("     ----> Create LhARA instance:")
filename = os.path.join(HOMEPATH, "11-Parameters/DipoleTest.csv")
print("         ----> Parameters will be read from:", filename)
LhARAbI = BL.BeamLine(filename)

figtest, axtest = plt.subplots()
BL.BeamLine.plotBeamLineYZ(axtest)
axtest.set_xlim(-1, 14)
axtest.set_ylim(-1, 6)
axtest.set_aspect("equal")
axtest.set_xlabel("z [m]")
axtest.set_ylabel("y [m]")
figtest.legend()

plt.savefig("99-Scratch/BeamLinePlot - DipoleTest.pdf")
