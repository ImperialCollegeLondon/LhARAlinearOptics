#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys, getopt

import Simulation as Simu
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
    nEvts        = 10000
    for opt, arg in opts:
        if opt == '-h':
            print ( \
                    'runBEAMsim.py -b <beamlinefile>'  + \
                    ' -i <inputfile> -o <outputfile>' + \
                    ' -n <nEvts>')
            print("     ----> <input file> not yet implemented.>")
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

    if beamlinefile == None or \
       outputfile    == None:
        print ( \
                'runBEAMsim.py -b <beamlinefile>'  + \
                ' -i <inputfile> -o <outputfile>' + \
                ' -n <nEvts>')
        print("     ----> <input file> not yet implemented.>")
        sys.exit()

    print(" runBEAMsim: start")
    
    print("     ----> Initialise:")
    
    HOMEPATH    = os.getenv('HOMEPATH')
    print("         ----> HOMEPATH:", HOMEPATH)
        
    #.. File handling:
    print("         ----> Check input and output files:")
    #.. ----> Beam line specitication file:
    if not os.path.isfile(beamlinefile):
        beamlinefile = os.path.join(HOMEPATH, beamlinefile)
    if not os.path.isfile(beamlinefile):
        print("             ----> Beam line parameter file does not exist.")
        print("                   Exit.")
        sys.exit(1)
        
    print("             ----> Beamline parameters will be read from:", \
          beamlinefile)

    #.. ----> Input file, if specified:
    if inputfile != None and not os.path.isfile(inputfile):
        inputfile = os.path.join(HOMEPATH, inputfile)
    if inputfile != None and not os.path.isfile(inputfile): 
        print("             ----> Input file does not exist.")
        print("                   Exit.")
        sys.exit(1)

    if inputfile != None:
        if os.path.isfile(inputfile): 
            print("             ----> Input file not implemented.")
            print("                   Exit.")
            sys.exit(1)
    #print("             ----> Input file:", inputfile)
    
    if not os.path.isabs(outputfile): 
        outputfile = os.path.join(HOMEPATH, outputfile)
    if not os.path.isdir(os.path.dirname(outputfile)):
        print("                 ----> Directory for output file", \
              os.path.dirname(outputfile), "does not exist.")
        print("                   Exit.")
        sys.exit(1)

    print("             ----> Write beamline summary file to:", outputfile)
    
    Smltn = Simu.Simulation(nEvts, beamlinefile, None, outputfile)

    print("     <---- Initialisation complete.")

    print("     ----> Run simulation:")

    Smltn.RunSim()

    print("     <---- Simulation done.")
        
    print(" runBEAMsim: ends")
    
"""
   Execute main"
"""
if __name__ == "__main__":
   main(sys.argv[1:])

sys.exit(1)
