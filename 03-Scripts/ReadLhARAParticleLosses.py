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

eventFILE = "LhARAsimu.dat"
ParticleFILE = Prtcl.Particle.openParticleFile("99-Scratch", eventFILE)
filename = os.path.join(
    HOMEPATH, "11-Parameters/LhARABeamLine-Params-Gauss-Solenoid.csv"
)
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
# Particle Losses
# --------------------------------------------------------------------------------------

fig, ax = plt.subplots()

Prtcl.Particle.plotParticleLosses(ax)

save_all_figs(
    prefix="ParticleLosses",
    loc=figDIRECTORY,
    dpi=300,
)
