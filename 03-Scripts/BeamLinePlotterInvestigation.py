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

figwedgetest, axwedgetest = plt.subplots()

axwedgetest.set_xlim(-2, 2)
axwedgetest.set_ylim(-2, 2)
R = 1
rad2deg = lambda rad: rad / (2 * np.pi) * 360


patchBLE = patches.Wedge(
    center=[0, 0],
    r=R - 0.1,
    theta1=0,
    theta2=rad2deg(np.pi / 4),
    width=0.2,
)
r = mpl.transforms.Affine2D().rotate_deg(-90)
t = mpl.transforms.Affine2D().translate(0, R - 0.2)

rta = r + t + axwedgetest.transData

patchBLE.set_transform(rta)

axwedgetest.add_patch(patchBLE)
plt.savefig("99-Scratch/wedges.pdf")
