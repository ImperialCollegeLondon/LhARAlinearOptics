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

    beamlinefile = ""
    inputfile    = ""
    outputfile   = ""
    Debug        = False
    nEvts        = -1
    for opt, arg in opts:
        if opt == '-h':
            print ( \
                    'plotBeam.py -b <beamlinefile>'  + \
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

    if inputfile    == "" or \
       beamlinefile == "":
        print ( \
                'plotBeam.py -b <beamlinefile>'  + \
                ' -i <inputfile> -o <outputfile>' + \
                ' -n <nEvts>')
        sys.exit()

    print(" plotBEAM: start")
    
    print("     ----> Initialise:")
    
    HOMEPATH    = os.getenv('HOMEPATH')
    print("         ----> HOMEPATH:", HOMEPATH)
        
    #.. Create beam line instance:
    print("         ----> Create beam line instance:")
    filename     = os.path.join(HOMEPATH, beamlinefile)
    print("             ----> Parameters will be read from:", filename)
    
    iBL  = BL.BeamLine(filename)
    if Debug:
        print(iBL)
    
    ParticleFILE = Prtcl.Particle.openParticleFile(HOMEPATH, inputfile)
    print("         ----> Read events from:", ParticleFILE)
    
    #print (' O/p plot file:', outputfile)

    iBm = Bm.Beam()

    print("         ----> Beam instance initialised.")

    print("     <---- Initialisation done.")

    """
       Read particle file:
    """
    print("     ----> Event loop:")
    EndOfFile = False
    iEvt = 0
    iCnt = 0
    Scl  = 10
    while not EndOfFile:
        EndOfFile = Prtcl.Particle.readParticle(ParticleFILE)
        if not EndOfFile:
            iEvt += 1
            if (iEvt % Scl) == 0:
                print("         ----> Read event ", iEvt)
                iCnt += 1
                if iCnt == 10:
                    iCnt = 1
                    Scl  = Scl * 10

            iPrtcl = Prtcl.Particle.getParticleInstances()[1]
            iBm.incrementSums(iPrtcl)

            Cleaned = Prtcl.Particle.cleanParticles()
            if Debug:
                print("         ----> Cleaned:", Cleaned)

        if nEvts > 0 and iEvt >= nEvts:
            break
            
    print("     <----", iEvt, "events read")
    
    """
       Calculate collective quantities:
    """
    print("     ----> Calculate collective quantities:")

    iBm.calcCovarianceMatrix()
    iBm.setsigmaxy()
    iBm.setEmittance()

    iBm.setDebug(True)
    iBm.setTwiss()
    iBm.setDebug(False)


    for iLoc in range(len(iBm.getsigmaxy())):
        print("         ----> iLoc:", iLoc)
        print("             ---->   sigma_x,   sigma_y:", \
              iBm.getsigmaxy()[iLoc][0], iBm.getsigmaxy()[iLoc][1])
        print("             ----> epsilon_x, epsilon_y:", \
              iBm.getemittance()[iLoc][0], iBm.getemittance()[iLoc][1])
        print("             ----> epsilon_4, epsilon_l:", \
              iBm.getemittance()[iLoc][2], iBm.getemittance()[iLoc][3])
        print("             ---->            epsilon_6:", \
              iBm.getemittance()[iLoc][4])
        print("             ---->      Twiss paramters:", \
              iBm.getTwiss()[iLoc][4])

    print("     <---- colective quantities done.")
        
    print(" plotBEAM: ends")
    


    
"""
   Execute main"
"""
if __name__ == "__main__":
   main(sys.argv[1:])

sys.exit(1)
