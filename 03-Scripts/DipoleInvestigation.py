# -*- coding: utf-8 -*-

import os
import struct
import math as mth
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

pltin = listRrIn[:, 0:3:2]
pltout = listRrOut[:, 0:3:2]

print(pltin)
print(pltout)

plt.plot(pltin[:, 1], pltin[:, 0], ".", label="RrIn")
plt.plot(pltout[:, 1], pltout[:, 0], "x", label="RrOut")
plt.xlabel("z")
plt.ylabel("x")
plt.legend()
plt.savefig("99-Scratch/test.pdf")
