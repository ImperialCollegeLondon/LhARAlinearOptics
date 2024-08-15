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
import matplotlib as mpl
import matplotlib.pyplot as plt
from datetime import date
from scipy.optimize import curve_fit

import BeamLineElement   as BLE
import BeamLine          as BL
import Particle          as Prtcl
import PhysicalConstants as PhysCnst

mpl.rc('text', usetex=True)
mpl.rcParams['text.latex.preamble']="\\usepackage{bm}"

#.. Physical Constants
constants_instance = PhysCnst.PhysicalConstants()
protonMASS         = constants_instance.mp()

HOMEPATH = os.getenv('HOMEPATH')
filename = os.path.join(HOMEPATH, \
                        '11-Parameters/LIONBeamLine-Params-LsrDrvn.csv')
BLI  = BL.BeamLine(filename)

iRefPrtcl = Prtcl.ReferenceParticle.getinstances()


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
          1., 25., 1000, 2.50e15, 70., 0.8, 2.80e-14, 4.00e-07, 4.00e20, 25., \
         20., 15.]
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
      " test parameterised laser-driven source distribution", \
      "check.")
Src1 = BLE.Source("Source2", rStrt, vStrt, drStrt, dvStrt, \
                  0, [0.000004, 0.000004, 0.998, 1., 25., 1000, 2.50e15, 70., 0.8, 2.80e-14, 4.00e-07, 4.00e20, 25., 20., 15.])
print(Src1)
print(" Test generation:")
print("     ----> First particle: KE, cosThetaPhi:", \
      Src1.getParticle())

##! Next: Get data for plots:
PrtclX   = np.array([])
PrtclY   = np.array([])
PrtclKE  = np.array([])
PrtclcT  = np.array([])
PrtclT   = np.array([])
PrtclPhi = np.array([])

SrcX     = np.array([])
SrcY     = np.array([])
SrcXp    = np.array([])
SrcYp    = np.array([])
SrcE     = np.array([])

g_E       = Src1.getLaserDrivenProtonEnergyProbDensity()
E_max_MeV = Src1.getderivedParameters()[4] / (1.6e-19 * 1e6)
E_min_MeV = Src1.getderivedParameters()[5] / (1.6e-19 * 1e6)

print("     ----> Generate many particles:")
for i in range(100000):
    X, Y, KE, cTheta, Phi = Src1.getParticle()
    
    TrcSpcFrmSrc = Src1.getParticleFromSource()
    PhsSpcFrmSrc = Prtcl.Particle.RPLCTraceSpace2PhaseSpace(TrcSpcFrmSrc)
    
    SrcX         = np.append(SrcX,  TrcSpcFrmSrc[0])
    SrcY         = np.append(SrcY,  TrcSpcFrmSrc[2])
    SrcXp        = np.append(SrcXp, TrcSpcFrmSrc[1])
    SrcYp        = np.append(SrcYp, TrcSpcFrmSrc[3])
    SrcE         = np.append(SrcE,  TrcSpcFrmSrc[5])

    p        = mth.sqrt(np.dot(PhsSpcFrmSrc[1], PhsSpcFrmSrc[1]))
    Etot     = mth.sqrt(protonMASS**2 + \
                        np.dot(PhsSpcFrmSrc[1], PhsSpcFrmSrc[1]))
    
    KE       = Etot - protonMASS
    PrtclKE  = np.append(PrtclKE , KE)

    cTheta   = PhsSpcFrmSrc[1][2] / p
    PrtclcT  = np.append(PrtclcT , cTheta)

    Theta    = mth.acos(cTheta) * 180. / mth.pi
    PrtclT   = np.append(PrtclT , Theta)

    Phi      = mth.atan2(PhsSpcFrmSrc[1][0], PhsSpcFrmSrc[1][1])
    if Phi < 0.: Phi += mth.pi
    Phi *= 180. / mth.pi
    PrtclPhi = np.append(PrtclPhi, Phi)

    PrtclX   = np.append(PrtclX , PhsSpcFrmSrc[0][0])
    PrtclY   = np.append(PrtclY , PhsSpcFrmSrc[0][1])
    
    
print("     <---- Done.")
    
##! Next: Make plots:
SourceTest += 1
print()
print("SourceTest:", SourceTest, \
      " plot distributions and compare with expectation.")

print("     ----> Make plots:")
today = date.today().strftime("%d/%m/%Y")

#.. ----> Kinetic energy:
print("         ----> Kinetic energy:")

n, bins, patches = plt.hist(PrtclKE, \
                            bins=100, color='k', \
                            histtype='step', label='Generated Distribution')

Ee, g_E = Src1.getLaserDrivenProtonEnergyProbDensity()

dE2     = (E_max_MeV - E_min_MeV) / 100. / 2.
Ee[-1] -= dE2

# Normalise:
hist_heights, bin_edges = np.histogram(PrtclKE, bins=100)
histCntnts = np.sum(hist_heights)
g_scaled   = g_E * histCntnts

# Plot required distribution:
plt.plot(Ee, g_scaled, color='r', label='Required Distribution', linewidth=1)

y_max_cutoff = g_scaled[-1]
x            = E_max_MeV
plt.vlines(x, ymin=0, ymax=y_max_cutoff, color='r', \
           linestyle='-', linewidth=1)  # [MeV]

plt.xlabel('Kinetic energy (MeV)', loc='right')
plt.ylabel('Entries', loc='top')
plt.yscale("log")
plt.legend(loc="best")

plt.title('ExpSourceTst (' + today + '): Kinetic energy distribution',
          fontname="Times New Roman",  size=12)
plt.savefig('99-Scratch/SourceTst_K.pdf')
plt.close()

print("         <---- Done.")

#.. ----> Cumulative probability:
print("         ----> Cumulative probability:")

cumPROB = []
sigT    = []
for eps in Ee:
    eps1 = eps * (1.6e-19 * 1e6)
    cumPROB.append(Src1.getLaserCumProb(eps1))
    sigT.append(Src1.g_theta(eps))
    
plt.plot(Ee, cumPROB, color='k', label='Required Distribution', linewidth=1)

plt.xlabel('Kinetic energy (MeV)', loc='right')
plt.ylabel('Cumulative probability', loc='top')
plt.yscale("linear")
plt.legend(loc="best")
plt.title('ExpSourceTst (' + today + '): cumulative probability', \
          fontname="Times New Roman",  size=12)

plt.savefig('99-Scratch/SourceTst_cumulativePDF.pdf')
plt.close()

#.. ----> cos(theta) and theta distribution:
print("         ----> cos(theta) and theta distribution:")

n, bins, patches = plt.hist(PrtclcT, \
                            bins=50, color='k', \
                            histtype='step')

plt.xlabel('$\\cos\\theta_S$', loc='right')
plt.ylabel('Entries', loc='top')
plt.title('ExpSourceTst (' + today + \
          '): $\\cos\\theta_S$ distribution', \
          fontname="Times New Roman",  size=12)

plt.savefig('99-Scratch/SourceTst_costheta.pdf')
plt.close()

n, bins, patches = plt.hist(PrtclT, \
                            bins=50, color='k', \
                            histtype='step')

plt.xlabel('$\\theta_S$ ($^\\circ$)', loc='right')
plt.ylabel('Entries', loc='top')
plt.title('ExpSourceTst (' + today + \
          '): $\\theta_S$ distribution', \
          fontname="Times New Roman",  size=12)

plt.savefig('99-Scratch/SourceTst_theta.pdf')
plt.close()

plt.plot(Ee, sigT, color='r', label='Required dependence', linewidth=1)

plt.xlabel('Kinetic energy (MeV)', loc='right')
plt.ylabel('$\\sigma_{\\theta_S}$ ($^\\circ$)', loc='top')
plt.title('ExpSourceTst (' + today + \
          '): $\\sigma_{\\theta_S}$ versus kinetic energy',\
          fontname="Times New Roman",  size=12)
plt.legend(loc="best")

plt.savefig('99-Scratch/SourceTst_sigTK.pdf')
plt.close()

plt.hist2d(PrtclKE, PrtclT, \
           bins=50, norm=mpl.colors.LogNorm())
plt.colorbar()

plt.xlabel('Kinetic energy (MeV)', loc='right')
plt.ylabel('$\\theta_S$ ($^\\circ$)', loc='top')
plt.title('ExpSourceTst (' + today + \
          '): $(\\theta_S, K)$ distribution', \
          fontname="Times New Roman",  size=12)

plt.savefig('99-Scratch/SourceTst_thetaK.pdf')
plt.close()

print("         <---- Done.")

#.. ----> phi distribution:
print("         ----> phi distribution:")

n, bins, patches = plt.hist(PrtclPhi, \
                            bins=50, color='k', \
                            histtype='step')

plt.xlabel('$\\phi_S$ ($^\\circ$)', loc='right')
plt.ylabel('Entries', loc='top')
plt.title('ExpSourceTst (' + today + \
          '): $\\phi_S$ distribution', \
          fontname="Times New Roman",  size=12)

plt.savefig('99-Scratch/SourceTst_phi.pdf')
plt.close()

print("         <---- Done.")

#.. ----> x,y distribution:
print("         ----> (x, y) distribution:")

plt.hist2d(PrtclX, PrtclY, \
           bins=50, norm=mpl.colors.LogNorm())
plt.colorbar()

plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.title('ExpSourceTst (' + today + \
          '): (x, y) distribution', \
          fontname="Times New Roman",  size=12)

plt.savefig('99-Scratch/SourceTst_xy.pdf')
plt.close()

print("         <---- Done.")

##! Next: Tabulate parameters:
SourceTest += 1
print()
print("SourceTest:", SourceTest, \
      " test tabulation of parameters.")

print("     ----> Tabulate paramters:")
Src.tabulateParameters('99-Scratch/SourceTst_ParameterTable.tex')


##! Complete:
print()
print("========  Source: tests complete  ========")
