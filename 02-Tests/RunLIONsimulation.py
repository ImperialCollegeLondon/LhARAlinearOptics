#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "Simulation" class ... simulation processing tasks
==================================

  Simulation.py -- set "relative" path to code

"""

import os
import Simulation as Simu
import BeamLine   as BL

##! Start:
print("========  Simulation: start  ========")
print()
HOMEPATH = os.getenv('HOMEPATH')
print("HOMEPATH", HOMEPATH)
filename    = os.path.join(HOMEPATH, \
                         '11-Parameters/LIONBeamLine-Params-LsrDrvn.csv')
#                         '11-Parameters/LIONBeamLine-Params-Gauss.csv')
#                         '11-Parameters/LIONBeamLine-Params-Flat.csv')
datafiledir = os.path.join(HOMEPATH, '99-Scratch')
Smltn = Simu.Simulation(100000, filename, datafiledir, 'LIONsimu.dat')
print()
print(" <---- Simulation initialised.")
print(BL.BeamLine.getinstances())
##! Start:
print(" ----> Run simulation test:")
print()
Smltn.RunSim()
print()
print(" <---- Simulation test done.")

##! Complete:
print()
print("========  Simulation: complete  ========")

