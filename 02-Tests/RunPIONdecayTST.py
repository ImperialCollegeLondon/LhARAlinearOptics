#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "Simulation" class ... simulation processing tasks
==================================

  Simulation.py -- set "relative" path to code

"""

import os
import Simulation as Simu

import BeamLine as BL

Debug = False

##! Start:
print("========  Simulation: start  ========")
print()
HOMEPATH = os.getenv('HOMEPATH')
print("HOMEPATH", HOMEPATH)
filename    = os.path.join(HOMEPATH, \
                '11-Parameters/decayCHAINpion.csv')
datafiledir = os.path.join(HOMEPATH, '99-Scratch')
Smltn = Simu.Simulation(10000, filename, datafiledir, 'pionDECAYtst.dat')
if Debug:
    print(BL.BeamLine.getinstances())
print()
print(" <---- Simulation initialised.")

##! Start:
print(" ----> Run simulation test:")
Smltn.RunSim()
print()
print(" <---- Simulation test done.")

##! Complete:
print()
print("========  Simulation: complete  ========")
