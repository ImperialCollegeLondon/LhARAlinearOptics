#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "muonDECAY" class
=================================

  Assumes that nuSim code is in python path.

  Script starts by testing built in methods.  Then a soak test with a
  large number of decays is executed.  Finally a set of reference plots
  are generated.

"""

from pylorentz import Momentum4 as mmtm4
import matplotlib.pyplot as plt
import numpy as np
import math as mt

import muonDECAY as md

import Particle   as Prtcl
import Simulation as Simu
import PhysicalConstants as physCNST

##! Start:
print("========  muonDECAY: tests start  ========")
Prtcl.ReferenceParticle("muon")

##! Create instance, test built-in methods:
muonDECAYTest = 1
print()
print(" muonDECAYTest:", muonDECAYTest, \
      " Muon, print quantities.")
try:
    Prtcl.muon.setDebug("String")
except:
    pass
muon=Prtcl.muon()
print("    __str__:", muon)
print("    --repr__", repr(muon))

##! Create instance, test dynamic methods:
muonDECAYTest = 2
print()
print("muonDECAYTest:", muonDECAYTest, \
      " Create muon decay, print quantities.")
Dcy=md.muonDECAY()
print("          _v_e:", Dcy.getve())
print("       _v_numu:", Dcy.getvnumu())
print("         _v_nue:", Dcy.getvnue())
iPC = physCNST.PhysicalConstants()
SumE = Dcy.getve()[0] + Dcy.getvnumu()[0] + Dcy.getvnue()[0]
DifE = SumE - iPC.mMuon()
print("    Sum energy:", SumE, "; difference to muon mass:", DifE)
muon.setDECAY(Dcy)
print("     ---> Print decay for this muon:")
print(muon.getDECAY())

del muon
del Dcy

##! Soak test, generate many decays:
muonDECAYTest = 3
print()
print("muonDECAYTest:", muonDECAYTest, " Create many decays.")
muon = []
for i in range(100000):
    pn = Prtcl.muon()
    pn.setDECAY(md.muonDECAY())
    muon.append(pn)
for i in range(5):
    print(muon[i].getDECAY())

##! Plot result of soak test:
muonDECAYTest = 4
print()
print("muonDECAYTest:", muonDECAYTest, " plots from soak test.")

t         = np.array([])
Ee        = np.array([])
Enumu     = np.array([])
cosTheta  = np.array([])
phi       = np.array([])
s = 0.

epLX     = np.array([])
epLY     = np.array([])
epLZ     = np.array([])
epRX     = np.array([])
epRY     = np.array([])
epRZ     = np.array([])

#.. set muon energy and momentum:
Emu = 8000.
Pmu = mt.sqrt(Emu**2 - iPC.mMuon()**2)
muonL = mmtm4(Emu, 0., 0., Pmu)
print(muonL)
print("     ----> muon 4 momentum:", muonL)
printBOOSTchk = False
for imuon in muon:
    t     = np.append(t,     imuon.getRemainingLifetime())
    Ee    = np.append(Ee,     imuon.getDECAY().getve()[0])
    Enumu = np.append(Enumu, imuon.getDECAY().getvnumu()[0])

    p_e   = imuon.getDECAY().getve()[1:]
    p_numu = imuon.getDECAY().getvnumu()[1:]

    mag_e  = np.linalg.norm(p_e)

    phi = np.append(phi,     mt.atan2(p_e[1],p_e[0]))
    cosTheta = np.append(cosTheta,     p_e[2]/mag_e)

    elecR = mmtm4(imuon.getDECAY().getve()[0], \
                  imuon.getDECAY().getve()[1], \
                  imuon.getDECAY().getve()[2], \
                  imuon.getDECAY().getve()[3])

    elecL = elecR.boost_particle(muonL)
    
    if not printBOOSTchk:
        print("         ----> electron 4 momentum in muon rest frame, mass:", \
              elecR, elecR.m)
        print("         ----> electron 4 momentum in      lab  frame, mass:", \
              elecL, elecL.m)
        elecL1 = mmtm4(Emu, 0., 0., -Pmu)
        elecR1 = elecL.boost_particle(elecL1)
        print("         ----> electron 4 momentum in muon rest frame, mass:", \
              elecR1, elecR1.m)
        printBOOSTchk = True

    epLX = np.append(epLX, elecL[1])
    epLY = np.append(epLY, elecL[2])
    epLZ = np.append(epLZ, elecL[3])
    
    epRX = np.append(epRX, elecR[1])
    epRY = np.append(epRY, elecR[2])
    epRZ = np.append(epRZ, elecR[3])

    
#-- Lifetime distribution:
n, bins, patches = plt.hist(t, bins=100, color='y', log=True)
plt.xlabel('Time (s)')
plt.ylabel('Entries')
plt.title('Lifetime distribution')
# add a 'best fit' line
l = 1./iPC.tauMuon()
y = n[0]*np.exp(-l*bins)
plt.plot(bins, y, '-', color='b')
plt.savefig('99-Scratch/muonPLOT1.pdf')
plt.close()

n, bins, patches = plt.hist(Ee, bins=50, color='y')
plt.xlabel('Energy (MeV)')
plt.ylabel('Frequency')
plt.title('Electron energy distribution in rest frame')
plt.savefig('99-Scratch/muonPLOT2.pdf')
plt.close()

n, bins, patches = plt.hist(Enumu, bins=50, color='y')
plt.xlabel('Energy (MeV)')
plt.ylabel('Frequency')
plt.title('Muon-neutrino energy distribution in rest frame')
plt.savefig('99-Scratch/muonPLOT3.pdf')
plt.close()

#-- Angular distributions:
n, bins, patches = plt.hist(phi, bins=50, color='y', range=(-4.,4.))
plt.xlabel('Phi')
plt.ylabel('Frequency')
plt.title('Electron phi distribution')
plt.savefig('99-Scratch/muonPLOT4.pdf')
plt.close()

n, bins, patches = plt.hist(cosTheta, bins=50, color='y', \
                            range=(-1.1,1.1))
plt.xlabel('Cos(theta)')
plt.ylabel('Frequency')
plt.title('Electron cos(theta) distribution')
plt.savefig('99-Scratch/muonPLOT5.pdf')
plt.close()

#-- Muon distributions:
h, xedges, yedges, image = plt.hist2d(epLX, epLY, bins=50)
plt.xlabel('pmuX')
plt.ylabel('pmuY')
plt.title('Electron transverse momentum laboratory')
plt.savefig('99-Scratch/muonPLOT6.pdf')
plt.close()

n, bins, patches = plt.hist(epLZ, bins=50, color='y')
plt.xlabel('pmuZ')
plt.ylabel('Frequency')
plt.title('Electron longitudinal momentum distribution laboratory')
plt.savefig('99-Scratch/muonPLOT7.pdf')
plt.close()

h, xedges, yedges, image = plt.hist2d(epRX, epRY, bins=50)
plt.xlabel('pmuX')
plt.ylabel('pmuY')
plt.title('Electron transverse momentum muon rest frame')
plt.savefig('99-Scratch/muonPLOT8.pdf')
plt.close()

n, bins, patches = plt.hist(epRZ, bins=50, color='y')
plt.xlabel('pmuZ')
plt.ylabel('Frequency')
plt.title('Electron longitudinal momentum distribution muon rest frame')
plt.savefig('99-Scratch/muonPLOT9.pdf')
plt.close()

##! Complete:
print()
print("========  muonDECAY: tests complete  ========")
