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

import visualise as vis

##! Start:
print("========  visualise: tests start  ========")


##! RPLC tests first
visualiseTest = 1
print()
print("visualiseTest:", visualiseTest, \
      " initialise for RPLC tests")

ivisRPLC = vis.visualise()

##!Test built in methods:
print()
print("     Test built-in methods:")
#.. __repr__
print("    __repr__:")
print("      ---->", repr(ivisRPLC))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(ivisRPLC)
print("    <---- __str__ done.")


##! RPLC tests first
visualiseTest += 1
print()
print("visualiseTest:", visualiseTest, \
      " now laboratory coordinate system tests")

ivisLab = vis.visualise()

##!Test built in methods:
print()
print("     Test built-in methods:")
#.. __repr__
print("    __repr__:")
print("      ---->", repr(ivisLab))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(ivisLab)
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
    pdf.savefig()
    plt.close()
    
    
##! Complete:
print()
print("========  visualise: tests complete  ========")
