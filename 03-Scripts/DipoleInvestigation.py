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

plt.plot(pltin[:, 1], pltin[:, 0], ".", label="RrIn")
plt.plot(pltout[:, 1], pltout[:, 0], "y", label="RrOut")
plt.xlabel("z")
plt.ylabel("y")
plt.legend()
plt.savefig("99-Scratch/test.pdf")

fig2 = plt.figure(figsize=(10, 10))
ax2 = plt.axes(projection="3d")

ax2.plot(
    listRrIn[:, 0],
    listRrIn[:, 1],
    listRrIn[:, 2],
    label="RrIn",
)
ax2.plot(
    listRrOut[:, 0],
    listRrOut[:, 1],
    listRrOut[:, 2],
    label="RrOut",
    color="purple",
)
ax2.legend()
ax2.set_xlabel("x")
ax2.set_ylabel("y")
ax2.set_zlabel("z")


plt.savefig("99-Scratch/3dtest.pdf")
