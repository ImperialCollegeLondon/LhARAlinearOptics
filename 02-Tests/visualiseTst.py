#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script for "visualise" class
=================================

  visualise.py -- set "relative" path to code

"""

from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import os

import visualise as vis
import BeamLine  as BL
import Beam      as Bm
import BeamIO    as bmIO
import Particle  as Prtcl

##! Start:
print("========  visualise: tests start  ========")

##! Now create pointer to input data file:
HOMEPATH = os.getenv('HOMEPATH')
inputdatafile = os.path.join(HOMEPATH, \
#                             '99-Scratch/LION-test.dat')
#                             '99-Scratch/LhARA-Gauss-Gabor.dat')
#                             '11-Parameters/Data4Tests.dat')
                             '99-Scratch/HorizRight.dat')
#.. Open data file and read first record to set up geometry
ibmIOr = bmIO.BeamIO(None, inputdatafile)

EndOfFile = False
EndOfFile = ibmIOr.readBeamDataRecord()

print(BL.BeamLine.getinstance())

for i in range(1001):
    ibmIOr.readBeamDataRecord()
Prtcl.Particle.fillPhaseSpaceAll()

##! RPLC tests first
visualiseTest = 1
print()
print("visualiseTest:", visualiseTest, \
      " initialise for RPLC tests")

ivisRPLCx = vis.visualise("RPLC", "xs")
ivisRPLCy = vis.visualise("RPLC", "ys")

##!Test built in methods:
print()
print("     Test built-in methods:")
#.. __repr__
print("    __repr__:")
print("      ---->", repr(ivisRPLCx))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(ivisRPLCx)
print("    <---- __str__ done.")


##! RPLC tests first
visualiseTest += 1
print()
print("visualiseTest:", visualiseTest, \
      " now laboratory coordinate system tests")

ivisLabx = vis.visualise("Lab", "xz")
ivisLaby = vis.visualise("Lab", "yz")

##!Test built in methods:
print()
print("     Test built-in methods:")
#.. __repr__
print("    __repr__:")
print("      ---->", repr(ivisLabx))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(ivisLabx)
print("    <---- __str__ done.")


##! Finally, make the plots:
visualiseTest += 1
print()
print("visualiseTest:", visualiseTest, \
      " make the plots:")
      
font = {'family': 'serif', \
        'color':  'darkred', \
        'weight': 'normal', \
        'size': 16, \
        }

plt.rcParams["figure.figsize"] = (10., 7.5)

plotFILE = '99-Scratch/visualiseRPLC.pdf'
with PdfPages(plotFILE) as pdf:
    fig, axs = plt.subplots(nrows=2, ncols=1, \
                            layout="constrained")
    # add an artist, in this case a nice label in the middle...
    Ttl = "Test RPLC visualise"
    fig.suptitle(Ttl, fontdict=font)
    axs[0].set_xlim(-1., 22.)
    axs[0].set_ylim(-0.05, 0.05)
    axs[1].set_xlim(-1., 22.)
    axs[1].set_ylim(-0.05, 0.05)

    ivisRPLCx.Particles(axs[0], 1000)
    ivisRPLCx.BeamLine(axs[0])
    ivisRPLCy.Particles(axs[1], 1000)    
    ivisRPLCy.BeamLine(axs[1])
    
    pdf.savefig()
    plt.close()
    
plotFILE = '99-Scratch/visualiseLab.pdf'
with PdfPages(plotFILE) as pdf:
    fig, axs = plt.subplots(nrows=3, ncols=1, \
                            layout="constrained")
    gs     = axs[2].get_gridspec()
    axs[2].remove()
    gs     = axs[1].get_gridspec()
    axs[1].remove()
    axs[1] = fig.add_subplot(gs[1:])


    # add an artist, in this case a nice label in the middle...
    Ttl = "Test lab coordinate system visualise"
    fig.suptitle(Ttl, fontdict=font)
    axs[0].set_xlim(-1., 18.)
    axs[0].set_ylim(-0.05, 0.05)
    axs[1].set_ylim(-1., 18.)
    axs[1].set_ylim(-6., 6.)
    
    ivisLaby.Particles(axs[0], 1000)
    ivisLaby.BeamLine(axs[0])
    ivisLabx.Particles(axs[1], 1000)
    ivisLabx.BeamLine(axs[1])
    
    pdf.savefig()
    plt.close()
    
    
##! Complete:
print()
print("========  visualise: tests complete  ========")
