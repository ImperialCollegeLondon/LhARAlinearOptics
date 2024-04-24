#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "LhARAFacility-from-datafile" 
=============================================

  BeamLine.py -- set "relative" path to code

"""

import os

import BeamIO   as bmIO
import BeamLine as BL
import Particle as Prtcl


##! Start:
print("========  LhARAFacility-from-datafile: tests start  ========")

##! Now create pointer to input data file:
HOMEPATH = os.getenv('HOMEPATH')
inputdatafile = os.path.join(HOMEPATH, \
                             '99-Scratch/LhARA-Gauss-Gabor.dat')
#                             '11-Parameters/Data4Tests.dat')

#.. Open data file and read first record to set up geometry
ibmIOr = bmIO.BeamIO(None, inputdatafile)

EndOfFile = False
EndOfFile = ibmIOr.readBeamDataRecord()

print(BL.BeamLine.getinstance())

##! Complete:
print()
print("========  LhARAFacility-from-datafile: tests complete  ========")
