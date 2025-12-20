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

import matplotlib.pyplot as plt
import numpy as np
import math as mt

import pionDECAY as pd
import Simulation as Simu
import PhysicalConstants as physCNST

##! Start:
print("========  pionDECAY: tests start  ========")

##! Create instance, test built-in methods:
pionDECAYTest = 1
print()
print(" pionDECAYTest:", pionDECAYTest, \
      " Create pion decay, print quantities.")
try:
    pd.pionDECAY.setDebug("String")
except:
    pass
pd.pionDECAY.setDebug(True)
Dcy=pd.pionDECAY()
print("    __str__:", Dcy)
print("    --repr__", repr(Dcy))
pd.pionDECAY.setDebug(False)
del Dcy

##! Create instance, test dynamic methods:
pionDECAYTest = 2
print()
print("pionDECAYTest:", pionDECAYTest, \
      " Create pion decay, print quantities.")
Dcy=pd.pionDECAY()
print("     _Lifetime:", Dcy.getLifetime())
print("         _v_mu:", Dcy.getvmu())
print("       _v_numu:", Dcy.getvnumu())
iPC = physCNST.PhysicalConstants()
SumE = Dcy.getvmu()[0] + Dcy.getvnumu()[0]
DifE = SumE - iPC.mPion()
print("    Sum energy:", SumE, "; difference to muon mass:", DifE)
del Dcy

##! Soak test, generate many decays:
pionDECAYTest = 3
print()
print("pionDECAYTest:", pionDECAYTest, " Create many decays.")
Dcy = []
for i in range(100000):
    Dcy.append(pd.pionDECAY())
for i in range(5):
    print(Dcy[i])

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
for piDcy in Dcy:
    t      = np.append(t,     piDcy.getLifetime())
    Emu    = np.append(Emu,   piDcy.getvmu()[0])
    Enumu  = np.append(Enumu, piDcy.getvnumu()[0])

    p_mu   = piDcy.getvmu()[1:]
    p_numu = piDcy.getvnumu()[1:]

    mag_mu    = np.linalg.norm(p_mu)
    
    phi = np.append(phi,     mt.atan2(p_mu[1],p_mu[0]))
    cosTheta = np.append(cosTheta,     p_mu[2]/mag_mu)
                    
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

##! Complete:
print()
print("========  pionDECAY: tests complete  ========")
