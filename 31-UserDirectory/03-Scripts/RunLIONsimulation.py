#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "Simulation" class ... simulation processing tasks
==================================

  Simulation.py -- set "relative" path to code

"""

import os
import LIONSimu as Simu

##! Start:
print("========  Simulation: start  ========")
print()
HOMEPATH = os.getenv('HOMEPATH')
print("HOMEPATH", HOMEPATH)
filename    = os.path.join(HOMEPATH, \
                         '11-Parameters/LIONBeamLine-Params-LsrDrvn.csv')
datafiledir = os.path.join(HOMEPATH, '99-Scratch')
Smltn = Simu.Simulation(2000000, filename, datafiledir, 'LIONsimu.dat')
print()
print(" <---- Simulation initialised.")

##! Start:
print(" ----> Run simulation test:")
print()
Smltn.setDebug(True)
Smltn.RunSim()
print(Smltn.getNEvt())
print()
print(" <---- Simulation test done.")

##! Complete:
print()
print("========  Simulation: complete  ========")
