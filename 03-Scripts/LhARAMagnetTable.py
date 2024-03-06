#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "LhARAFacility" class ... initialisation and get methods
=====================================

  BeamLine.py -- set "relative" path to code

"""

import sys
import os

import LaTeX           as LTX
import BeamLine        as BL
import Particle        as Prtcl
import BeamLineElement as BLE


LhARAOpticsPATH    = os.getenv('LhARAOpticsPATH')
print(LhARAOpticsPATH)
filename     = os.path.join(LhARAOpticsPATH, \
                    '11-Parameters/LhARABeamLine-Params-LsrDrvn-Solenoid.csv')
#                        '11-Parameters/LhARABeamLine-Params-Gauss-Gabor.csv')

##! Start:
print("========  LhARAMagnetTable  ========")

##! Test singleton class feature:
LhARAMagnetTable = 1
print()
print("LhARAMagnetTable:", LhARAMagnetTable, "start.")
LhARAFclty  = BL.BeamLine(filename)

print(LhARAFclty)

##! Table header:
LTX.TableHeader('99-Scratch/LhARAMagnetTable.tex', '|l|c|c|')

Line = " \\textbf{Name} & \\textbf{Length} & $\\bm{k_n}$ "
LTX.TableLine('99-Scratch/LhARAMagnetTable.tex', Line)
Line = "                & (m)              &           $ "
LTX.TableLine('99-Scratch/LhARAMagnetTable.tex', Line)
Line = "\\hline"
LTX.TableLine('99-Scratch/LhARAMagnetTable.tex', Line)

##! Table body:
for iBLE in BLE.BeamLineElement.getinstances():
    if isinstance(iBLE, BLE.Solenoid):
        print(" Element:", iBLE.getName())
        print(" Length:", iBLE.getLength())
        print(" Strength:", iBLE.getStrength())

##! Table header:
LTX.TableTrailer('99-Scratch/LhARAMagnetTable.tex')

##! Complete:
print()
print("========  LhARAFacility: tests complete  ========")
