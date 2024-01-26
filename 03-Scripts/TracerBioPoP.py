#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 15:04:12 2023

@author: alfredo
"""

import Tracing_code as Tr
import os
HOMEPATH = os.getenv('HOMEPATH')

beamline_file = 'LhARABeamLine-Params-Gauss-Gabor.csv'
data_file     = 'LhARAsimu.dat'



#We start with beamline plotting 

Tr.BeamlinePlotter.Tracer(1.5, 21.5, colour='b', label='20MeV', filename=data_file, facility = beamline_file, maxz = 0.21, HOMEPATH = HOMEPATH, NEvts = 200)
#Tr.BeamlinePlotter.Tracer(12.5, 13.5, colour='r', label='E=21MeV', filename=data_file, facility = beamline_file, maxz = 0.1, HOMEPATH = HOMEPATH, NEvts = 200)
#Tr.BeamlinePlotter.Tracer(17, 18, colour='r', label='E=11MeV', filename=data_file, facility = beamline_file, maxz = 2.135, HOMEPATH = HOMEPATH)

Tr.BeamlinePlotter.plt_apt(filename=beamline_file, HOMEPATH = HOMEPATH)
Tr.BeamlinePlotter.plt_quad(filename=beamline_file, HOMEPATH = HOMEPATH)
Tr.BeamlinePlotter.plt_solenoid(filename=beamline_file, HOMEPATH = HOMEPATH)

Tr.BeamlinePlotter.plt_save()

