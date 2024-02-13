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
filename = os.path.join(HOMEPATH, "11-Parameters/LhARABeamLine-Params-Gauss.csv")
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

figRPLCxz, axRPLCxz = plt.subplots()
figRPLCyz, axRPLCyz = plt.subplots()

figLABxz, axLABxz = plt.subplots()
figLAByz, axLAByz = plt.subplots()

print(" ----> Plot progression:")

print("     ----> Plot LAB:")
linesLAB = Prtcl.Particle.plotParticleTrajectory_Lab(axyz=axLAByz, axxz=axLABxz)
print("     <---- Done.")

print("     ----> Plot LAB YZ BeamLineElements:")
patches = BL.BeamLine.plotBeamLineYZ(axLAByz)
print("     <---- Done.")

print("     ----> Plot RPLC:")
linesRPLC = Prtcl.Particle.plotParticleTrajectory_RPLC(axyz=axRPLCyz, axxz=axRPLCxz)
print("     <---- Done.")

axLAByz.autoscale(enable=True)
axLABxz.autoscale(enable=True)
axLAByz.set_aspect("equal")

axRPLCyz.autoscale(enable=True)
axRPLCxz.autoscale(enable=True)

print("========  Plotting: END  ========")
print()

save_all_figs(
    prefix="ReadLhARAsimu",
    loc=figDIRECTORY,
    dpi=300,
)
