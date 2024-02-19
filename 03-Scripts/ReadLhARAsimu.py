#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# --------------------------------------------------------------------------------------
# Import Libraries
# --------------------------------------------------------------------------------------

import Particle as Prtcl
import BeamLine as BL
import matplotlib.pyplot as plt
import matplotlib as mpl

# --------------------------------------------------------------------------------------
# Import Functions
# --------------------------------------------------------------------------------------

from Utilities import save_all_figs

# --------------------------------------------------------------------------------------
# Global Plotting Settings
# --------------------------------------------------------------------------------------

mpl.rcParams["figure.dpi"] = 300


print("========  Initialisation: START  ========")
print()

# --------------------------------------------------------------------------------------
# HOMEPATH
# --------------------------------------------------------------------------------------

HOMEPATH = os.getenv("HOMEPATH")

print("----> Initialising with HOMEPATH:", HOMEPATH)

# --------------------------------------------------------------------------------------
# Data and Plot Files
# --------------------------------------------------------------------------------------

eventFILE = "DipoleTest.dat"
ParticleFILE = Prtcl.Particle.openParticleFile("99-Scratch", eventFILE)
filename = os.path.join(HOMEPATH, "11-Parameters/DipoleTest.csv")
figDIRECTORY = "99-Scratch/"

# --------------------------------------------------------------------------------------
# Intiialise the BeamLine
# --------------------------------------------------------------------------------------

LhARAbI = BL.BeamLine(filename)

print("----> Create LhARA instance:")
print("     ----> Parameters will be read from:", filename)

print("========  Initialisation: END  ========")
print()

# --------------------------------------------------------------------------------------
# Read Events
# --------------------------------------------------------------------------------------

print("========  Read: START  ========")
print()

print(
    "----> Read event file:",
    eventFILE,
)

EndOfFile = False
iEvt = 0
iCnt = 0
Scl = 10
while not EndOfFile:
    EndOfFile = Prtcl.Particle.readParticle(ParticleFILE)
    if not EndOfFile:
        iEvt += 1
        if (iEvt % Scl) == 0:
            print("     ----> Read event ", iEvt)
            iCnt += 1
            if iCnt == 10:
                iCnt = 1
                Scl = Scl * 10

print("<----", iEvt, "events read")

print("========  Read: STOP  ========")
print()

# --------------------------------------------------------------------------------------
# Plotting
# --------------------------------------------------------------------------------------

print("========  Plotting: START  ========")
print()

figRPLC, axRPLC = plt.subplots(
    nrows=2, ncols=1, figsize=(11.0, 11.0), constrained_layout=True
)
axRPLC[0].set_ylim(-5, 5)
axRPLC[1].set_ylim(-5, 5)

figLAB, axLAB = plt.subplots(
    nrows=2, ncols=1, figsize=(11.0, 11.0), constrained_layout=True
)

axLAB[0].set_ylim(-5, -5)
axLAB[1].set_ylim(-5, 5)
print(" ----> Plot progression:")

print("     ----> Plot LAB:")
linesLAB = Prtcl.Particle.plotParticleTrajectory_Lab(axyz=axLAB[1], axxz=axLAB[0])
print("     <---- Done.")

print("     ----> Plot LAB YZ BeamLineElements:")
patches = BL.BeamLine.plotBeamLineYZ(axLAB[1])
print("     <---- Done.")

print("     ----> Plot RPLC:")
linesRPLC = Prtcl.Particle.plotParticleTrajectory_RPLC(axyz=axRPLC[1], axxz=axRPLC[0])
print("     <---- Done.")


print("========  Plotting: END  ========")
print()

save_all_figs(
    prefix="ReadLhARAsimu",
    loc=figDIRECTORY,
    dpi=300,
)
