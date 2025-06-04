#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Start with methods used in analysis main that should be standard for all
analyses.

"""

import sys, getopt
import argparse as ap
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

    #.. Parse input arguments:

    prsr = ap.ArgumentParser()

    prsr.add_argument("-b", "--beamspecfile", \
                      help="beam specification file (.csv)")    
    prsr.add_argument("-i", "--inputfile", \
                      help="input file (.dat)")    
    prsr.add_argument("-o", "--outputfile", \
                      help="output file (.dat)")

    prsr.add_argument("-n", "--nEvents", help="number of events", \
                      default=1000, type=int)
    
    prsr.add_argument("-d", "--debug", help="debug flag (boolean)", \
                      default=False, type=bool)
    prsr.add_argument("-z", "--bdsimfile", \
                help="boolean flag; if true input file is in BDSIM format", \
                      default=False, type=bool)
    
    print(" UserAnal.startAnalysis:")
    Success = False

    """
    print("args:", args)

    opts, args = getopt.getopt(argv,"hdiz:o:b:n:",\
                            ["ifile=","BDSIMfile","ofile=","bfile=", "nEvts="])
    """

    beamspecfile = None
    inputfile    = None
    outputfile   = None
    Debug        = False
    bdsimfile    = False
    nEvts        = None

    Debug = prsr.parse_args().debug
    inputfile = prsr.parse_args().inputfile
    bdsimfile = prsr.parse_args().bdsimfile
    outputfile = prsr.parse_args().outputfile
    beamspecfile = prsr.parse_args().beamspecfile
    nEvts = prsr.parse_args().nEvents

    if (inputfile == None and beamspecfile == None) or \
       (inputfile != None and beamspecfile != None and not bdsimfile):
        prsr.print_usage()
        print ("     ----> Need either input file or beam specification file.")
        print ("     ----> And, can only specify -b and -i if bdsimfile")
        sys.exit()

    if beamspecfile != None:
        print("     ----> Beam specification file (-b):", beamspecfile)
    if inputfile != None:
        print("     ---->              Input file (-i):", inputfile)
    if outputfile != None:
        print("     ---->             Output file (-o):", outputfile)
    if nEvts != None:
        print("     ---->        Number of events (-n):", nEvts)
    if bdsimfile != None:
        print("     ---->       BDSIM input file? (-z):", bdsimfile)
    if Debug != None:
        print("     ---->              Debug flag (-d):", Debug)
    print(" UserAnal.startAnalysis: ends.")
    
    Success = True
    
    return Success, Debug, \
        beamspecfile, inputfile, bdsimfile, outputfile, nEvts

#--------  Do the i/o file handling
def handleFILES(beamspecfile, inputfile, outputfile, bdsimFILE=False):
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

        ibmIOr = bmIO.BeamIO(None, inputfile, False, bdsimFILE)
        print("         ---->              Input file:", inputfile)
        if bdsimFILE:
            print("             ----> BDSIM file:", bdsimFILE)
            

        if not bdsimFILE:
            EndOfFile = ibmIOr.readBeamDataRecord()
            if EndOfFile: 
                print("         ----> End of input file on first read.")
                print("               Exit.")
                sys.exit(1)
    
    #.. ----> Output file, if specified:
    ibmIOw = None
    if outputfile != None and not os.path.isabs(outputfile): 
        outputfile = os.path.join(HOMEPATH, outputfile)
        print("         ---->             Output file:", outputfile)
    if outputfile != None and not \
       os.path.isdir(os.path.dirname(outputfile)):
        print("         ----> Directory for output file", \
              os.path.dirname(outputfile), "does not exist.")
        exit(1)
            
    #.. ----> Beam specification file, if specified:
    #         Note, reading from specification file, then, instanciation
    #         of Simulation class handles output file
    if beamspecfile != None:
        if not os.path.isfile(beamspecfile):
            beamspecfile = os.path.join(HOMEPATH, beamspecfile)
        if not os.path.isfile(beamspecfile): 
            print("         ----> Beam specification file does not exist.")
            print("               Exit.")
            sys.exit(1)
            
        print("         ----> Beam specification file:", beamspecfile)
        iBL = BL.BeamLine(beamspecfile)

        ofileSPLIT = [None, None]
        if outputfile != None:
            ofileSPLIT = os.path.split(outputfile)
        print(" ofileSPLIT:", ofileSPLIT)
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

    iSm = Simu.Simulation.getinstances()

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

    EndOfRun = False
    while not EndOfRun:
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
                print(Prtcl.Particle.getinstances()[iEvt])
        if nEvts != None and iEvt == nEvts or EndOfFile:
            EndOfRun = True

    if UsrFw_Debug:
        if iUsrAnl.getnIter() == 0:
            print("     <----", iEvt, "events read")
            print(" <---- Data-file reading done.")
            print(" UserAnal.EventLoop: ends.")
    
    Success = True
   
    return Success
