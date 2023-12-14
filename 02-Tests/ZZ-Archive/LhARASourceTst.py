#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "LhARASource" class ... initialisation and get methods
=====================================

  LhARASource.py -- set "relative" path to code

"""

import os
import sys
import math as mth
import numpy as np
import matplotlib.pyplot as plt

import LhARASource   as LS
import Simulation    as Simu

##! Start:
print("========  LhARASource: tests start  ========")

LhARAOpticsPATH    = os.getenv('LhARAOpticsPATH')
print(LhARAOpticsPATH)
filename     = os.path.join(LhARAOpticsPATH, \
                        '11-Parameters/LhARABeamLine-Params-tst.csv')
rootfilename = os.path.join(LhARAOpticsPATH, \
                            '99-Scratch/LhARA-Simulation-tst.root')
print(filename)
print(rootfilename)
print("     ----> Set up dummy simulation class for access to random ", \
      "number generators, etc.")
Smltn  = Simu.Simulation(100, filename, rootfilename)
print(" <---- Done.")

##! Test singleton class feature:
LhARASourceTest = 1
print()
print("LhARASourceTest:", LhARASourceTest, \
      " check if class is a singleton.")
LhARASrc  = LS.LhARASource()
LhARASrc1 = LS.LhARASource()
print("    LhARASrc singleton test:", id(LhARASrc), id(LhARASrc1), \
      id(LhARASrc)-id(LhARASrc1))
if LhARASrc != LhARASrc1:
    raise Exception("LhARASource is not a singleton class!")

##! Check built-in methods:
LhARASourceTest += 1
print()
print("LhARASourceTest:", LhARASourceTest, \
      " check built-in methods.")
print("    __repr__:")
print(LhARASrc)

##! Check get methods:
LhARASourceTest += 1
print()
print("LhARASourceTest:", LhARASourceTest, " check get methods.")
print("    ----> Tests all get methods")
print(LhARASrc)

##! Check set method:
LhARASourceTest += 1
print()
print("LhARASourceTest:", LhARASourceTest, " check set method.")
LS.LhARASource.setDebug(True)
print(LhARASrc)
LS.LhARASource.setDebug(False)

##! Delete instances and continue
LS.LhARASource.cleanInstance()

##! Check input parameter checks:
LhARASourceTest += 1
print()
print("LhARASourceTest:", LhARASourceTest, " check bad input parameter ", \
      "check.")
try:
    LhARASrc = LS.LhARASource(1.)
except:
    print("     ----> Bad mode trapped OK.")
LS.LhARASource.cleanInstance()
try:
    LhARASrc = LS.LhARASource(1, [1., 2, 1., 2])
except:
    print("     ----> Bad parameter type trapped OK.")
LS.LhARASource.cleanInstance()
print(" <---- Bad i/p arguments checks done.")

##! Ca commence: check gaussian source distribution:
LhARASourceTest += 1
print()
print("LhARASourceTest:", LhARASourceTest, \
      " test gaussian source distribution ", \
      "check.")
LS.LhARASource.setDebug(True)
LhARASrc = LS.LhARASource(1, [0.000004, 0.000004, 0.998, 15., 0.3, \
                              5.E-2, 2.5E-2, 0.002, \
                              5.E-2, 7.5E-2, 0.00287])
LS.LhARASource.setDebug(False)
print(LhARASrc)
print(" Test generation:")
print("     ----> First particle: trace space:", \
      LhARASrc.getParticleFromSource())

SrcX     = np.array([])
SrcY     = np.array([])
SrcXp    = np.array([])
SrcYp    = np.array([])
SrcE     = np.array([])

for i in range(10000):
    TrcSpcFrmSrc = LhARASrc.getParticleFromSource()
    SrcX         = np.append(SrcX,  TrcSpcFrmSrc[0])
    SrcY         = np.append(SrcY,  TrcSpcFrmSrc[2])
    SrcXp        = np.append(SrcXp, TrcSpcFrmSrc[1])
    SrcYp        = np.append(SrcYp, TrcSpcFrmSrc[3])
    SrcE         = np.append(SrcE,  TrcSpcFrmSrc[5])
    
n, bins, patches = plt.hist(SrcX, \
                            bins=50, color='y', range=(-0.006,0.006), \
                            log=False)
plt.xlabel('X')
plt.ylabel('Entries')
plt.title('X position at exit from source')
plt.savefig('99-Scratch/LhARASourceTst_plot6.pdf')
plt.close()

n, bins, patches = plt.hist(SrcY, \
                            bins=50, color='y', range=(-0.006,0.006), \
                            log=False)
plt.xlabel('Y')
plt.ylabel('Entries')
plt.title('Y position at exit from source')
plt.savefig('99-Scratch/LhARASourceTst_plot7.pdf')
plt.close()

n, bins, patches = plt.hist(SrcXp, \
                            bins=50, color='y', range=(-0.05,0.05), \
                            log=False)
plt.xlabel('X-prime')
plt.ylabel('Entries')
plt.title('X-prime position at exit from source')
plt.savefig('99-Scratch/LhARASourceTst_plot8.pdf')
plt.close()

n, bins, patches = plt.hist(SrcYp, \
                            bins=50, color='y', range=(-0.05,0.05), \
                            log=False)
plt.xlabel('Y-prime')
plt.ylabel('Entries')
plt.title('Y-prime position at exit from source')
plt.savefig('99-Scratch/LhARASourceTst_plot9.pdf')
plt.close()

n, bins, patches = plt.hist(SrcE, \
                            bins=50, color='y', range=(13., 17.), \
                            log=False)
plt.xlabel('Kinetic energy')
plt.ylabel('Entries')
plt.title('Kinetic energy at exit from source')
plt.savefig('99-Scratch/LhARASourceTst_plot10.pdf')
plt.close()


##! Nex: check paramterised laser-driven source distribution:
LhARASourceTest += 1
print()
print("LhARASourceTest:", LhARASourceTest, \
      " test parameterised laser-driven source distribution ", \
      "check.")
LS.LhARASource.setDebug(True)
LS.LhARASource.cleanInstance()
LhARASrc = LS.LhARASource(0, [0.000004, 0.000004, 0.998, 1., 25., 1000, \
                              5.E-2, 2.5E-2, 5.E-2, 7.5E-2, \
                              0.002, 0.00287])
LS.LhARASource.setDebug(False)
print(LhARASrc)
print(" Test generation:")
print("     ----> First particle: trace space:", \
      LhARASrc.getParticleFromSource())

SrcX     = np.array([])
SrcY     = np.array([])
SrcXp    = np.array([])
SrcYp    = np.array([])
SrcE     = np.array([])

for i in range(10000):
    TrcSpcFrmSrc = LhARASrc.getParticleFromSource()
    SrcX         = np.append(SrcX,  TrcSpcFrmSrc[0])
    SrcY         = np.append(SrcY,  TrcSpcFrmSrc[2])
    SrcXp        = np.append(SrcXp, TrcSpcFrmSrc[1])
    SrcYp        = np.append(SrcYp, TrcSpcFrmSrc[3])
    SrcE         = np.append(SrcE,  TrcSpcFrmSrc[5])
    
n, bins, patches = plt.hist(SrcX, \
                            bins=50, color='y', range=(-0.006,0.006), \
                            log=False)
plt.xlabel('X')
plt.ylabel('Entries')
plt.title('LsrDrvnSrc: X position at exit from source')
plt.savefig('99-Scratch/LhARASourceTst_plot16.pdf')
plt.close()

n, bins, patches = plt.hist(SrcY, \
                            bins=50, color='y', range=(-0.006,0.006), \
                            log=False)
plt.xlabel('Y')
plt.ylabel('Entries')
plt.title('LsrDrvnSrc: Y position at exit from source')
plt.savefig('99-Scratch/LhARASourceTst_plot17.pdf')
plt.close()

n, bins, patches = plt.hist(SrcXp, \
                            bins=50, color='y', range=(-0.05,0.05), \
                            log=False)
plt.xlabel('X-prime')
plt.ylabel('Entries')
plt.title('LsrDrvnSrc: X-prime position at exit from source')
plt.savefig('99-Scratch/LhARASourceTst_plot18.pdf')
plt.close()

n, bins, patches = plt.hist(SrcYp, \
                            bins=50, color='y', range=(-0.05,0.05), \
                            log=False)
plt.xlabel('Y-prime')
plt.ylabel('Entries')
plt.title('LsrDrvnSrc: Y-prime position at exit from source')
plt.savefig('99-Scratch/LhARASourceTst_plot19.pdf')
plt.close()

n, bins, patches = plt.hist(SrcE, \
                            bins=50, color='y', range=(1., 25.), \
                            log=False)
plt.xlabel('Kinetic energy')
plt.ylabel('Entries')
plt.title('LsrDrvnSrc: Kinetic energy at exit from source')
plt.savefig('99-Scratch/LhARASourceTst_plot110.pdf')
plt.close()

    
##! Complete:
print()
print("========  LhARASource: tests complete  ========")
