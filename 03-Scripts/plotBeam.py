#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys, getopt
import struct
import math as mth

import Particle as Prtcl
import BeamLine as BL
import Beam     as Bm

def main(argv):
    """
       Parse input arguments:
    """
    opts, args = getopt.getopt(argv,"hdi:o:b:n:",\
                               ["ifile=","nEvts", "ofile=","bfile"])

    beamlinefile = None
    inputfile    = None
    outputfile   = None
    Debug        = False
    nEvts        = None
    for opt, arg in opts:
        if opt == '-h':
            print ( \
                    'plotBeam.py '  + \
                    ' -i <inputfile> -n <nEvts> -o <outputfile>' + \
                    ' [-b <beamlinefile>]')
            sys.exit()
        if opt == '-d':
            Debug = True
        elif opt in ("-b", "--bfile"):
            beamlinefile = arg
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-n", "--nEvts"):
            nEvts = int(arg)

    if inputfile    == None:
        print ( \
                'plotBeam.py '  + \
                ' -i <inputfile> -n <nEvts> -o <outputfile>' + \
                ' [-b <beamlinefile>]')
        sys.exit()

    print(" plotBEAM: start")
    
    print("     ----> Initialise:")
    
    HOMEPATH    = os.getenv('HOMEPATH')
    print("         ----> HOMEPATH:", HOMEPATH)
        
    #.. Create beam instance:
    if beamlinefile != None:
        print("         ----> Create beam instance:")
        filename     = os.path.join(HOMEPATH, beamlinefile)
        print("             ----> Beamline parameters will be read from:", \
              filename)
        
    particlefile  = os.path.join(HOMEPATH, inputfile)
    print("             ----> Particles will be read from:", \
          particlefile)
    
    CSVoutputFILE = None
    if outputfile != None:
        CSVoutputFILE = os.path.join(HOMEPATH, outputfile)
        print("         ----> Write beamline summary file to:", CSVoutputFILE)
    
    iBm = Bm.Beam(particlefile, nEvts, CSVoutputFILE)

    print("     <---- Beam instance initialised.")

    print("     ----> Evaluate beam:")

    iBm.evaluateBeam()

    print("     <---- Beam evaluated.")
        
    print("     ----> Create report:")

    iBm.createReport()

    print("     <---- Report created.")
        
    print("     ----> Plot beam progression:")

    iBm.plotBeamProgression()

    print("     <---- Beam progression plot done.")
        
    print(" plotBEAM: ends")
    
"""
   Execute main"
"""
if __name__ == "__main__":
   main(sys.argv[1:])

sys.exit(1)
