#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import Simulation as Simu

##! Start:
print("========  Simulation: start  ========")
print()
HOMEPATH = os.getenv('HOMEPATH')
print("HOMEPATH", HOMEPATH)

filename    = os.path.join(HOMEPATH, \
                '11-Parameters/RFtest.csv')
datafiledir = os.path.join(HOMEPATH, '99-Scratch')

Smltn = Simu.Simulation(1000, filename, datafiledir, 'LhARAsimu.dat')
print()
print(" <---- Simulation initialised.")

##! Start:
print(" ----> Run simulation test:")
print()
Smltn.RunSim()
print()
print(" <---- Simulation test done.")

##! Complete:
print()
print("========  Simulation: complete  ========")