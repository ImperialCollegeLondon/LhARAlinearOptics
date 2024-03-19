#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys, getopt

import Particle as Prtcl
import BeamLine as BL
import BeamIO   as bmIO
import UserAnal as UsrAnl


def main(argv):
    """
       Parse input arguments:
    """
    opts, args = getopt.getopt(argv,"hdi:o:b:n:",\
                               ["ifile=","ofile=","bfile", "nEvts"])

    inputfile    = None
    outputfile   = None
    Debug        = False
    nEvts        = None
    for opt, arg in opts:
        if opt == '-h':
            print ( \
                    'readBEAMsim.py -i <inputfile> -o <outputfile>' + \
                    ' -n <nEvts>')
            print("     ----> <output file> not yet implemented.>")
            sys.exit()
        if opt == '-d':
            Debug = True
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-n", "--nEvts"):
            nEvts = int(arg)

    if inputfile    == None:
        print ( \
                'readBEAMsim.py -i <inputfile> -o <outputfile>' + \
                ' -n <nEvts>')
        print("     ----> <output file> not yet implemented.>")
        sys.exit()

    print(" readBEAMsim: start")
    
    print("     ----> Initialise:")
    
    HOMEPATH    = os.getenv('HOMEPATH')
    print("         ----> HOMEPATH:", HOMEPATH)
        
    #.. File handling:
    print("         ----> Check input and output files:")

    #.. ----> Input file, if specified:
    if inputfile != None and not os.path.isfile(inputfile):
        inputfile = os.path.join(HOMEPATH, inputfile)
    if not os.path.isfile(inputfile): 
        print("             ----> Input file does not exist.")
        print("                   Exit.")
        sys.exit(1)

    ibmIOr = bmIO.BeamIO(None, inputfile)
    print("             ----> Input file:", inputfile)
    
    if outputfile != None and not os.path.isabs(outputfile): 
        outputfile = os.path.join(HOMEPATH, outputfile)
    if outputfile != None and not os.path.isdir(os.path.dirname(outputfile)):
        print("                 ----> Directory for output file", \
              os.path.dirname(outputfile), "does not exist.")
    else:
        print("                   Output file not implemented.")
    
    print("     <---- Initialisation complete.")

    print("     ----> Read data file:")

    EndOfFile = False
    iEvt = 0
    iCnt = 0
    Scl  = 10
    print("         ----> Read data file:")
    while not EndOfFile:
        EndOfFile = ibmIOr.readBeamDataRecord()
        if not EndOfFile:
            iEvt += 1
            if (iEvt % Scl) == 0:
                print("         ----> Read event ", iEvt)
                iCnt += 1
                if iCnt == 10:
                    iCnt = 1
                    Scl  = Scl * 10
        if iEvt <0:
            print(Prtcl.Particle.getParticleInstances()[iEvt])
        if nEvts != None and iEvt == nEvts:
            break

    print("     <----", iEvt, "events read")

    print(" <---- Data-file reading done.")
        
    print(" User analysis:")
    UsrAnl.UserAnal.plotSomething()
    print(" <---- Done.")
    
    print(" readBEAMsim: ends")
    
"""
   Execute main"
"""
if __name__ == "__main__":
   main(sys.argv[1:])

sys.exit(1)












