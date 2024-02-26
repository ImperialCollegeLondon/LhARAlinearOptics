#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import Beam_tracer_code as Br
import BeamLine as BL
import os

HOMEPATH = os.getenv("HOMEPATH")

beamline_file = "LhARABeamLine-Params-Gauss.csv"
data_file = "LhARAsimu.dat"


# We start with beamline plotting

fig, axs = Br.BeamlinePlotter.Tracer(
    0,
    2000,
    colour="b",
    label="20MeV",
    filename=data_file,
    facility=beamline_file,
    maxz=0.5,
    HOMEPATH=HOMEPATH,
)
# Tr.BeamlinePlotter.Tracer(12.5, 13.5, colour='r', label='E=21MeV', filename=data_file, facility = beamline_file, maxz = 0.1, HOMEPATH = HOMEPATH, NEvts = 200)
# Tr.BeamlinePlotter.Tracer(17, 18, colour='r', label='E=11MeV', filename=data_file, facility = beamline_file, maxz = 2.135, HOMEPATH = HOMEPATH)


BL.BeamLine.plotBeamLineYZ(axs[2])

axs[2].set_aspect("equal")

Br.BeamlinePlotter.plt_save()
