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
import BeamLine as BL
import Particle as Prtcl
import Simulation as Simu

UsrFw_Debug = False

#--------  Parse arguments:
def startAnalysis(argv):
    print(" UserAnal.startAnalysis:")
    Success = False

    #.. Parse input arguments:

    opts, args = getopt.getopt(argv,"hdi:o:b:n:",\
                               ["ifile=","ofile=","bfile", "nEvts"])

    beamspecfile = None
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
        elif opt in ("-b", "--bfile"):
            beamspecfile = arg
        elif opt in ("-n", "--nEvts"):
            nEvts = int(arg)

    if (inputfile == None and beamspecfile == None) or \
       (inputfile != None and beamspecfile != None):
        print ( \
                'UserAnal.py -b <beam specification file>' + \
                '-i <inputfile> -o <outputfile> -n <nEvts>')
        print("     ----> Specify EITHER -i or -b, NOT both.>")
        sys.exit()

    print(" UserAnal.startAnalysis: ends.")
    
    Success = True
    
    return Success, Debug, \
        beamspecfile, inputfile, outputfile, nEvts

#--------  Do the i/o file handling
def handleFILES(beamspecfile, inputfile, outputfile):
    print(" UserAnal.handleFILES start:")
    Success = False

    HOMEPATH    = os.getenv('HOMEPATH')
    print("     ----> HOMEPATH:", HOMEPATH)
        
    #.. File handling:
    print("     ----> Check input and output files:")

    #.. ----> Input file, if specified:
    ibmIOr = None
    if inputfile != None:
        if not os.path.isfile(inputfile):
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
    
    #.. ----> Output file, if specified:
    ibmIOw = None
    if outputfile != None and not os.path.isabs(outputfile): 
        outputfile = os.path.join(HOMEPATH, outputfile)
    if outputfile != None and not \
       os.path.isdir(os.path.dirname(outputfile)):
        print("         ----> Directory for output file", \
              os.path.dirname(outputfile), "does not exist.")
        exit(1)
            
    #.. ----> Beam specification file, if specified:
    #         Note, reading from specification file, then, instanciation
    #         of Simulation class handles output file
    if beamspecfile != None and ibmIOr == None:
        if not os.path.isfile(beamspecfile):
            beamspecfile = os.path.join(HOMEPATH, beamspecfile)
        if not os.path.isfile(beamspecfile): 
            print("         ----> Beam specification file does not exist.")
            print("               Exit.")
            sys.exit(1)
            
        iBL = BL.BeamLine(beamspecfile)
        print(iBL)
        print(Prtcl.ReferenceParticle.getinstance())

        ofileSPLIT = [None, None]
        if outputfile != None:
            ofileSPLIT = os.path.split(outputfile)
        iSm    = Simu.Simulation(1, None, ofileSPLIT[0], ofileSPLIT[1])

        ibmIOw = iSm.getiBmIOw()

    else:
        if outputfile != None:
            ibmIOw = bmIO.BeamIO(None, outputfile, True)

    print(" UserAnal.handleFILES: ends.")
     
    Success = True
   
    return Success, ibmIOr, ibmIOw

def EventLoop(iUsrAnl, ibmIOr, ibmIOw, nEvtsIn):
    if UsrFw_Debug:
        if iUsrAnl.getnIter() == 0:
            print(" UserAnal.EventLoop start:")
    Success = False

    iSm = Simu.Simulation.getInstance()

    nEvts = 1000
    if nEvtsIn != None:
        nEvts = nEvtsIn
    
    EndOfFile = False
    iEvt = 0
    iCnt = 0
    Scl  = 10
    if UsrFw_Debug:
        if iUsrAnl.getnIter() == 0:        
            print("         ----> Read data file:")
        
    while not (EndOfFile and iEvt >= nEvts):
        #.. Generate or read event:
        if ibmIOr != None:
            EndOfFile = ibmIOr.readBeamDataRecord()
        else:
            nEvt = iSm.getFacility().trackBeam(1, None)

        if not EndOfFile:
            iEvt += 1
            if (iEvt % Scl) == 0:
                if UsrFw_Debug:
                    if iUsrAnl.getnIter() == 0:
                        print("         ----> Read event ", iEvt)
                iCnt += 1
                if iCnt == 10:
                    iCnt = 1
                    Scl  = Scl * 10

            iUsrAnl.EventLoop(ibmIOw)

        if iEvt <0:
            if UsrFw_Debug:
                print(Prtcl.Particle.getParticleInstances()[iEvt])
        if nEvts != None and iEvt == nEvts:
            break

    if UsrFw_Debug:
        if iUsrAnl.getnIter() == 0:
            print("     <----", iEvt, "events read")
            print(" <---- Data-file reading done.")
            print(" UserAnal.EventLoop: ends.")
    
    Success = True
   
    return Success
