#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 15:04:12 2023

@author: alfredo
"""

import Tracing_code as Tr

beamline_file = 'DRACOBeamLine-Params-LsrDrvn.csv'
data_file     = 'DRACOsimu.dat'

#We start with beamline plotting 

Tr.BeamlinePlotter.Tracer(19.5, 20.5, colour='b', label='E=20MeV', filename=data_file, facility = beamline_file, maxz = 2.135)
Tr.BeamlinePlotter.Tracer(20.5, 21.5, colour='r', label='E=21MeV', filename=data_file, facility = beamline_file, maxz = 2.135)

Tr.BeamlinePlotter.plt_apt(filename=beamline_file)
Tr.BeamlinePlotter.plt_solenoid(filename=beamline_file)

Tr.BeamlinePlotter.plt_show()

