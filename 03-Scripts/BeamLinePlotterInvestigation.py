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
axtest.set_xlim(-1, 12)
axtest.set_ylim(-5, 5)

plt.savefig("99-Scratch/beamlineplot.pdf")
