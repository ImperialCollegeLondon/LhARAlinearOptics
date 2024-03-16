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
                               ["ifile=","ofile=","bfile", "nEvts"])

    beamlinefile = None
    inputfile    = None
    outputfile   = None
    Debug        = False
    nEvts        = None
    for opt, arg in opts:
        if opt == '-h':
            print ( \
                    'runBEAMsim.py -b <beamlinefile>'  + \
                    ' -i <inputfile> -o <outputfile>' + \
                    ' -n <nEvts>')
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

    if inputfile    == None or \
       beamlinefile == None:
        print ( \
                'runBEAMsim.py -b <beamlinefile>'  + \
                ' -i <inputfile> -o <outputfile>' + \
                ' -n <nEvts>')
        sys.exit()

    print(" runBEAMsim: start")
    
    print("     ----> Initialise:")
    
    HOMEPATH    = os.getenv('HOMEPATH')
    print("         ----> HOMEPATH:", HOMEPATH)
        
    #.. File handling:
    #.. ----> Beam line specitication file:
    print("         ----> Check beam line specification file:")
    if not os.path.isfile(beamlinefile):
        beamlinefile = os.path.join(HOMEPATH, beamlinefile)
    print("             ----> Beamline parameters will be read from:", \
          beamlinefile)
    
    #.. ----> Input file, if specified:
    if inputfile != None and not os.path.isfile(inputfile):
        inputfile = os.path.join(HOMEPATH, inputfile)
    print("             ----> Input file:", inputfile)
    
    particlefile  = os.path.join(HOMEPATH, inputfile)
    print("             ----> Particles will be read from:", \
          particlefile)
    
    outputFILE = None
    if outputfile != None:
        outputFILE = os.path.join(HOMEPATH, outputfile)
        print("         ----> Write beamline summary file to:", outputFILE)
    
    iBm = Bm.Beam(filename, particlefile, nEvts, outputFILE)

    print("     <---- Beam instance initialised.")

    print("     ----> Create report:")

    iBm.createReport()

    print("     <---- Create report:")
        
    print("     ----> Plot beam progression:")

    iBm.setDebug(True)
    iBm.plotBeamProgression()

    print("     <---- Beam progression plot done.")
        
    print(" runBEAMsim: ends")
    
"""
   Execute main"
"""
if __name__ == "__main__":
   main(sys.argv[1:])

sys.exit(1)
