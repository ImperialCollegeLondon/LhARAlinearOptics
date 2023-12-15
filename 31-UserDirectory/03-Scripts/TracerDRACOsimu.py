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

Tr.BeamlinePlotter.Tracer(10, 20, colour='r', label='E<40MeV', filename=data_file, facility = beamline_file, HOMEPATH = '/Users/alfredo/Desktop/PhD/LhARA/LhARAlinearOptics', maxz = 2.135)
#Tr.BeamlinePlotter.Tracer(40, 100, colour='b', label='E>40MeV', filename=data_file, facility = beamline_file, HOMEPATH = '/Users/alfredo/Desktop/PhD/LhARA/LhARAlinearOptics')

Tr.BeamlinePlotter.plt_apt(filename=beamline_file, HOMEPATH = '/Users/alfredo/Desktop/PhD/LhARA/LhARAlinearOptics/')
Tr.BeamlinePlotter.plt_solenoid(filename=beamline_file, HOMEPATH = '/Users/alfredo/Desktop/PhD/LhARA/LhARAlinearOptics/')

Tr.BeamlinePlotter.plt_show()

