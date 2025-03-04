#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "Source" class
=============================

  Source.py -- set "relative" path to code

"""

import os
import math  as mth
import numpy as np
import matplotlib.pyplot as plt

import BeamLineElement as BLE
import BeamLine        as BL
import Particle        as Prtcl

HOMEPATH = os.getenv('HOMEPATH')
filename = os.path.join(HOMEPATH, \
                        '11-Parameters/LIONBeamLine-Params-LsrDrvn.csv')
BLI  = BL.BeamLine(filename)

iRefPrtcl = Prtcl.ReferenceParticle.getinstance()


##! Start:
print("========  Source: tests start  ========")

##! Test creation and built-in methods:
SourceTest = 1
print()
print("SourceTest:", SourceTest, \
      " check creation and built-in methods.")

#.. __init__
print("    __init__:")
try:
    Src = BLE.Source()
except:
    print('      ----> Correctly trapped no argument exception.')
rStrt = np.array([0.,0.,0.])
vStrt = np.array([[np.pi/2.,np.pi/2.],[0.,0.]])
drStrt = np.array([0.,0.,0.])
dvStrt = np.array([[0.,0.],[0.,0.]])
try:
    Src = BLE.Source(rStrt, vStrt, drStrt, dvStrt)
except:
    print('      ----> Correctly trapped no Source paramters exception.')

#.. Create valid instance:
Mode  = 0
Param = [0.000004, 0.000004, 0.998,    \
          1., 25., 1000, 2.50e15, 70., 0.8, 2.80e-14, 4.00e-07, 4.00e20, 25.]
Src = BLE.Source("Source0", rStrt, vStrt, drStrt, dvStrt, Mode, Param)
    
#.. __repr__
print("    __repr__:")
print("      ---->", repr(Src))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(str(Src))
print("    <---- __str__ done.")

print(" <---- Creation and built in method tests done!  --------  --------")


##! Next: check paramterised laser-driven source distribution:
SourceTest += 1
print()
print("SourceTest:", SourceTest, \
      " test parameterised laser-driven source distribution ", \
      "check.")
Src1 = BLE.Source("Source2", rStrt, vStrt, drStrt, dvStrt, \
                  0, [0.000004, 0.000004, 0.998, 1., 25., 1000, 2.50e15, 70., 0.8, 2.80e-14, 4.00e-07, 4.00e20, 25.])
print(Src1)
print(" Test generation:")
print("     ----> First particle: KE, cosThetaPhi:", \
      Src1.getParticle())

PrtclX   = np.array([])
PrtclY   = np.array([])
PrtclKE  = np.array([])
PrtclcT  = np.array([])
PrtclPhi = np.array([])

SrcX     = np.array([])
SrcY     = np.array([])
SrcXp    = np.array([])
SrcYp    = np.array([])
SrcE     = np.array([])

E_max_MeV = Src1.getderivedParameters()[4] / (1.6e-19 * 1e6)
E_min_MeV = Src1.getderivedParameters()[5] / (1.6e-19 * 1e6)

print("     ----> Generate many particles:")
for i in range(1000000):
    X, Y, KE, cTheta, Phi = Src1.getParticle()
    
    PrtclKE  = np.append(PrtclKE , KE)

n, bins, patches = plt.hist(PrtclKE, \
                            bins=100, color='y', \
                            log=False, label='Generated Distribution')

Ee, g_E = Src1.getLaserDrivenProtonEnergyProbDensity()
E   = np.linspace(E_min_MeV,E_max_MeV,100)
print(" In ExpSource: E_min_MeV,E_max_MeV:", E_min_MeV,E_max_MeV)

# Normalise:
hist_heights, bin_edges = np.histogram(PrtclKE, bins=100)
histCntnts = np.sum(hist_heights)
g_scaled   = g_E * histCntnts

# Plot required distribution:
plt.plot(Ee, g_scaled, color='k', label='Required Distribution', linewidth=2)

E_max_cutoff_index = np.argmin(np.abs(E - E_max_MeV))
y_max_cutoff = g_scaled[E_max_cutoff_index]
dE2          = (E_max_MeV - E_min_MeV) / 100. / 2.
plt.vlines(x=E_max_MeV+dE2, ymin=0, ymax=y_max_cutoff, color='k', \
           linestyle='-', linewidth=2)  # [MeV]

plt.xlabel('Energy (MeV)')
plt.ylabel('Entries')
plt.yscale("log")
plt.legend(loc="best")
plt.title('LsrDrvnSrc: Energy distribution')
plt.savefig('99-Scratch/SourceTst_plot13_Dist.pdf')
plt.close()

cumPROB = []
for eps in E:
    eps1 = eps * (1.6e-19 * 1e6)
    cumPROB.append(Src1.getLaserCumProb(eps1))
plt.plot(E, cumPROB, color='k', label='Required Distribution', linewidth=2)
plt.xlabel('Energy (MeV)')
plt.ylabel('Cumulative probability')
plt.yscale("linear")
plt.legend(loc="best")
plt.title('LsrDrvnSrc: cumulative probability')
plt.savefig('99-Scratch/SourceTst_plot14_Dist.pdf')
plt.close()


##! Complete:
print()
print("========  Source: tests complete  ========")
