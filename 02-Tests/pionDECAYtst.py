#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "pionDECAY" class
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

import pionDECAY as pd

import Particle   as Prtcl
import Simulation as Simu
import PhysicalConstants as physCNST

##! Start:
print("========  pionDECAY: tests start  ========")
Prtcl.ReferenceParticle("pion")

##! Create instance, test built-in methods:
pionDECAYTest = 1
print()
print(" pionDECAYTest:", pionDECAYTest, \
      " Pion, print quantities.")
try:
    Prtcl.pion.setDebug("String")
except:
    pass
pion=Prtcl.pion()
print("    __str__:", pion)
print("    --repr__", repr(pion))

##! Create instance, test dynamic methods:
pionDECAYTest = 2
print()
print("pionDECAYTest:", pionDECAYTest, \
      " Create pion decay, print quantities.")
Dcy=pd.pionDECAY()
print("         _v_mu:", Dcy.getvmu())
print("       _v_numu:", Dcy.getvnumu())
iPC = physCNST.PhysicalConstants()
SumE = Dcy.getvmu()[0] + Dcy.getvnumu()[0]
DifE = SumE - iPC.mPion()
print("    Sum energy:", SumE, "; difference to muon mass:", DifE)
pion.setDECAY(Dcy)
print("     ---> Print decay for this pion:")
print(pion.getDECAY())

del pion
del Dcy

##! Soak test, generate many decays:
pionDECAYTest = 3
print()
print("pionDECAYTest:", pionDECAYTest, " Create many decays.")
pion = []
for i in range(100000):
    pn = Prtcl.pion()
    pn.setDECAY(pd.pionDECAY())
    pion.append(pn)
for i in range(5):
    print(pion[i].getDECAY())


##! Plot result of soak test:
pionDECAYTest = 4
print()
print("pionDECAYTest:", pionDECAYTest, " plots from soak test.")

t         = np.array([])
Emu       = np.array([])
Enumu     = np.array([])
cosTheta  = np.array([])
phi       = np.array([])
s = 0.

mupLX     = np.array([])
mupLY     = np.array([])
mupLZ     = np.array([])
mupRX     = np.array([])
mupRY     = np.array([])
mupRZ     = np.array([])

#.. set pion energy and momentum:
Epi = 8000.
Ppi = mt.sqrt(Epi**2 - iPC.mPion()**2)
pionL = mmtm4(Epi, 0., 0., Ppi)
print("     ----> pion 4 momentum:", pionL)
printBOOSTchk = False
for ipion in pion:
    t      = np.append(t,     ipion.getRemainingLifetime())
    Emu    = np.append(Emu,   ipion.getDECAY().getvmu()[0])
    Enumu  = np.append(Enumu, ipion.getDECAY().getvnumu()[0])

    p_mu   = ipion.getDECAY().getvmu()[1:]
    p_numu = ipion.getDECAY().getvnumu()[1:]

    mag_mu    = np.linalg.norm(p_mu)
    
    phi = np.append(phi,     mt.atan2(p_mu[1],p_mu[0]))
    cosTheta = np.append(cosTheta,     p_mu[2]/mag_mu)

    muonR = mmtm4(ipion.getDECAY().getvmu()[0], \
                  ipion.getDECAY().getvmu()[1], \
                  ipion.getDECAY().getvmu()[2], \
                  ipion.getDECAY().getvmu()[3])

    muonL = muonR.boost_particle(pionL)
    
    if not printBOOSTchk:
        print("         ----> muon 4 momentum in pion rest frame, mass:", \
              muonR, muonR.m)
        print("         ----> muon 4 momentum in      lab  frame, mass:", \
              muonL, muonL.m)
        pionL1 = mmtm4(Epi, 0., 0., -Ppi)
        pionR  = pionL.boost_particle(pionL1)
        print("         ----> pion 4 momentum in pion rest frame, mass:", \
              pionR, pionR.m)
        muonR1 = muonL.boost_particle(pionL1)
        print("         ----> muon 4 momentum in pion rest frame, mass:", \
              muonR1, muonR1.m)
        printBOOSTchk = True

    mupLX = np.append(mupLX, muonL[1])
    mupLY = np.append(mupLY, muonL[2])
    mupLZ = np.append(mupLZ, muonL[3])
    
    mupRX = np.append(mupRX, muonR[1])
    mupRY = np.append(mupRY, muonR[2])
    mupRZ = np.append(mupRZ, muonR[3])

    
#-- Lifetime distribution:
n, bins, patches = plt.hist(t, bins=100, color='y', log=True)
plt.xlabel('Time (s)')
plt.ylabel('Entries')
plt.title('Lifetime distribution')
# add a 'best fit' line
l = 1./iPC.tauPion()
y = n[0]*np.exp(-l*bins)
plt.plot(bins, y, '-', color='b')
plt.savefig('99-Scratch/pionPLOT1.pdf')
plt.close()

n, bins, patches = plt.hist(Emu, bins=50, color='y', range=(100.,120.))
plt.xlabel('Energy (MeV)')
plt.ylabel('Frequency')
plt.title('muon energy distribution')
plt.savefig('99-Scratch/pionPLOT2.pdf')
plt.close()

n, bins, patches = plt.hist(Enumu, bins=50, color='y', range=(20.,40.))
plt.xlabel('Energy (MeV)')
plt.ylabel('Frequency')
plt.title('Muon-neutrino energy distribution')
plt.savefig('99-Scratch/pionPLOT3.pdf')
plt.close()

#-- Angular distributions:
n, bins, patches = plt.hist(phi, bins=50, color='y', range=(-4.,4.))
plt.xlabel('Phi')
plt.ylabel('Frequency')
plt.title('muon phi distribution')
plt.savefig('99-Scratch/pionPLOT4.pdf')
plt.close()

n, bins, patches = plt.hist(cosTheta, bins=50, color='y', \
                            range=(-1.1,1.1))
plt.xlabel('Cos(theta)')
plt.ylabel('Frequency')
plt.title('Muon cos(theta) distribution')
plt.savefig('99-Scratch/pionPLOT5.pdf')
plt.close()

#-- Muon distributions:
h, xedges, yedges, image = plt.hist2d(mupLX, mupLY, bins=50)
plt.xlabel('pmuX')
plt.ylabel('pmuY')
plt.title('muon transverse momentum laboratory')
plt.savefig('99-Scratch/pionPLOT6.pdf')
plt.close()

n, bins, patches = plt.hist(mupLZ, bins=50, color='y')
plt.xlabel('pmuZ')
plt.ylabel('Frequency')
plt.title('Muon longitudinal momentum distribution laboratory')
plt.savefig('99-Scratch/pionPLOT7.pdf')
plt.close()

h, xedges, yedges, image = plt.hist2d(mupRX, mupRY, bins=50)
plt.xlabel('pmuX')
plt.ylabel('pmuY')
plt.title('muon transverse momentum pion rest frame')
plt.savefig('99-Scratch/pionPLOT8.pdf')
plt.close()

n, bins, patches = plt.hist(mupRZ, bins=50, color='y')
plt.xlabel('pmuZ')
plt.ylabel('Frequency')
plt.title('Muon longitudinal momentum distribution pion rest frame')
plt.savefig('99-Scratch/pionPLOT9.pdf')
plt.close()

##! Complete:
print()
print("========  pionDECAY: tests complete  ========")
