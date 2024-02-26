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

##! Create LhARA instance:
print("     ----> Create LhARA instance:")
filename = os.path.join(HOMEPATH, "11-Parameters/DipoleTest.csv")
print("         ----> Parameters will be read from:", filename)
LhARAbI = BL.BeamLine(filename)

listRrIn = np.array(Prtcl.ReferenceParticle.getinstance().getRrIn())
listRrOut = np.array(Prtcl.ReferenceParticle.getinstance().getRrOut())

pltin = listRrIn[:, 1:3:1]
pltout = listRrOut[:, 1:3:1]

print(pltin)
print(pltout)

fig, ax = plt.subplots()

BL.BeamLine.plotBeamLineYZ(ax)

ax.plot(pltin[:, 1], pltin[:, 0], ".", label="RrIn")
ax.plot(pltout[:, 1], pltout[:, 0], "y", label="RrOut")
ax.set_aspect("equal")
ax.set_xlabel("z [m]")
ax.set_ylabel("y [m]")
ax.legend()
plt.savefig("99-Scratch/test.pdf")
