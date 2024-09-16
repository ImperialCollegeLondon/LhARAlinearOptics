#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

import UserFramework as UsrFw
import UserAnal      as UsrAnl


def main(argv):

    Success, Debug, \
        beamspecfile, inputfile, bdsimfile, outputfile, \
        nEvts = UsrFw.startAnalysis(argv)
    if not Success:
        print(" <---- Failed at UsrFw.startAnalysis, exit")
        exit(1)

    print(beamspecfile)
    print(type(beamspecfile))
    Success, ibmIOr, ibmIOw = UsrFw.handleFILES(beamspecfile, \
                                                inputfile, outputfile)
    if not Success:
        print(" <---- Failed at UsrFw.handleFILES, exit")
        exit(1)

    #.. ----> Instanciate user analysis:
    iUsrAnl = UsrAnl.UserAnal(Debug)
        
    #.. ----> Execute event loop:
    Success = UsrFw.EventLoop(iUsrAnl, ibmIOr, outputfile, nEvts)
    if not Success:
        print(" <---- Failed at UsrFw.EventLoop, exit")
        exit(1)

    #.. ----> End of event loop, wrap up:
    print(" UserAnalysis: calling UsrAnal.UserEnd after event loop:")
    iUsrAnl.UserEnd()
    print(" <---- Done.")

"""
   Execute main"
"""
if __name__ == "__main__":
   main(sys.argv[1:])

sys.exit(1)
