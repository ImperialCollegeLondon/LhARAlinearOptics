#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "Simulation" class ... simulation processing tasks
==================================

  Simulation.py -- set "relative" path to code

"""

import os
import Simulation as Simu

##! Start:
print("========  Simulation: start  ========")
print()
LhARAOpticsPATH = os.getenv('LhARAOpticsPATH')
print("LhARAOpticsPATH", LhARAOpticsPATH)
filename  = os.path.join(LhARAOpticsPATH, \
                         '11-Parameters/LhARABeamLine-Params-tst.csv')
rootfilename = os.path.join(LhARAOpticsPATH, \
                            '99-Scratch/LhARAOptics-RunSimulationTst.root')
Smltn = Simu.Simulation(100000, filename, rootfilename)
print()
print(" <---- Simulation initialised.")

##! Start:
print(" ----> Run simulation test:")
print()
Smltn.setDebug(True)
Smltn.RunSim()
print()
print(" <---- Simulation test done.")

##! Complete:
print()
print("========  Simulation: complete  ========")
