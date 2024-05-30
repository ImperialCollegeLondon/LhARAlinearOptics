#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Start with methods used in analysis main that should be standard for all
analyses.

"""

import sys, getopt
import os
import io
import numpy as np

import BeamIO   as bmIO
import UserAnal as UsrAnl

#--------  Parse arguments:
def startAnalysis(argv):
    print(" UserAnal.startAnalysis:")
    Success = False

    #.. Parse input arguments:

    opts, args = getopt.getopt(argv,"hdi:o:b:n:",\
                               ["ifile=","ofile=","bfile", "nEvts"])

    inputfile    = None
    outputfile   = None
    Debug        = False
    nEvts        = None
    for opt, arg in opts:
        if opt == '-h':
            print ( \
                    'UserAnal.py -i <inputfile> -o <outputfile>' + \
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
                'UserAnal.py -i <inputfile> -o <outputfile>' + \
                ' -n <nEvts>')
        print("     ----> <output file> not yet implemented.>")
        sys.exit()

    print(" UserAna.startAnalysis: ends.")
    
    Success = True
    
    return Success, Debug, inputfile, outputfile, nEvts

def handleFILES(inputfile, outputfile):
    print(" UserAnal.handleFILES start:")
    Success = False

    HOMEPATH    = os.getenv('HOMEPATH')
    print("     ----> HOMEPATH:", HOMEPATH)
        
    #.. File handling:
    print("     ----> Check input and output files:")

    #.. ----> Input file, if specified:
    if inputfile != None and not os.path.isfile(inputfile):
        inputfile = os.path.join(HOMEPATH, inputfile)
    if not os.path.isfile(inputfile): 
        print("         ----> Input file does not exist.")
        print("               Exit.")
        sys.exit(1)

    ibmIOr = bmIO.BeamIO(None, inputfile)
    print("         ----> Input file:", inputfile)
    EndOfFile = ibmIOr.readBeamDataRecord()
    if EndOfFile: 
        print("         ----> End of input file on first read.")
        print("               Exit.")
        sys.exit(1)
    
    if outputfile != None and not os.path.isabs(outputfile): 
        outputfile = os.path.join(HOMEPATH, outputfile)
    if outputfile != None and not os.path.isdir(os.path.dirname(outputfile)):
        print("         ----> Directory for output file", \
              os.path.dirname(outputfile), "does not exist.")
    else:
        print("         ----> Output file not implemented.")

    print(" UserAnal.handleFILES: ends.")
     
    Success = True
   
    return Success, ibmIOr

def EventLoop(iUsrAnl, ibmIOr, ibmIOw, nEvts, Clean=True):
    if iUsrAnl.getIter() == 0:
        print(" UserAnal.EventLoop start:")
    Success = False

    EndOfFile = False
    iEvt = 0
    iCnt = 0
    Scl  = 10
    if iUsrAnl.getIter() == 0:        
        print("         ----> Read data file:")
    while not EndOfFile:
        EndOfFile = ibmIOr.readBeamDataRecord()
        if not EndOfFile:
            iEvt += 1
            if (iEvt % Scl) == 0:
                if iUsrAnl.getIter() == 0:
                    print("         ----> Read event ", iEvt)
                iCnt += 1
                if iCnt == 10:
                    iCnt = 1
                    Scl  = Scl * 10

            iUsrAnl.EventLoop(ibmIOw, Clean)

        if iEvt <0:
            print(Prtcl.Particle.getParticleInstances()[iEvt])
        if nEvts != None and iEvt == nEvts:
            break

    if iUsrAnl.getIter() == 0:
        print("     <----", iEvt, "events read")
        print(" <---- Data-file reading done.")
        print(" UserAnal.EventLoop: ends.")
    
    Success = True
   
    return Success
