#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class UserAnal:
===============

  Dummy class created to help user develop their own analysis.

  Out of the box provides three "user hooks":

   UserInit: called at instanitation to allow user to initialise.

   UserAnal: called in the event loop to allow user to do whatever is needed
             for their analysis.

    UserEnd: called at the end of execution before termination to allow
             user to dump summaries, statistics, plots etc.

  Class attributes:
  -----------------
    instances : List of instances of Particle class
  __Debug     : Debug flag

      
  Instance attributes:
  --------------------
    
  Methods:
  --------
  Built-in methods __init__, __repr__ and __str__.
      __init__ : Creates instance of beam-line element class.
      __repr__: One liner with call.
      __str__ : Dump of constants

  Set methods:
     setDebug: set class debug flag
           Input: bool, True/False
          Return: None


Created on Tue 27Feb24: Version history:
----------------------------------------
 1.0: 27Feb24: First implementation

@author: kennethlong
"""

import io
import math  as mth
import numpy as np

import Particle        as Prtcl
import Beam            as Bm
import BeamLine        as BL
import BeamLineElement as BLE
import BeamIO          as bmIO

class UserAnal:
    instances  = []
    __Debug    = False

    Iter = 0


#--------  UserHooks:
    def UserInit(self):
        if self.getDebug():
            print("\n UserAnal.UserInit: initialsation")

        #--------  Initialise iteration records:
        self.setnIter(0)
        self.setCost(None)
        self.setBLEparams([])
        self.setBLEparamsRef([])
        
        #--------  Reading source distribution, so, now create
        #          PoPLaR beam line:
        self.getBLEparams().append(["User:1:Capture:Drift:1", 0.1])
        self.getBLEparams().append(["User:1:Capture:FQ:1", 0.025, 130.])
        self.getBLEparams().append(["User:1:Capture:Drift:2", 0.1])
        self.getBLEparams().append(["User:1:Capture:DQ:1", 0.013, 130.])
        self.getBLEparams().append(["User:1:Capture:Drift:3", None])

        self.setBeamLine()

        self.setBLEparamsRef(self.getBLEparams())
        
    def UserEvent(self, iPrtcl):
        pass

    def UserEnd(self):
        if self.getDebug():
            print(" EnvelopeOptimisation.UserEnd: start")

        iBm = Bm.Beam.getBeamInstances()[0]
        if self.getDebug():
            print("     ----> Dump of Beam instance: \n", iBm)

        Scl  = iBm.getsigmaxy()[-1][0] / iBm.getsigmaxy()[-1][1]
        if Scl < 1.: Scl = 1./Scl

        Cost = mth.pi * iBm.getsigmaxy()[-1][0] * iBm.getsigmaxy()[-1][1] * \
            Scl
        
        if self.getCost() == None or Cost < self.getCost():
            print("     ----> nIter, Previous cost, new cost:", \
                  self.getnIter(), self.getCost(), Cost)
            self.setCost(Cost)
            self.setBLEparamsRef(self.getBLEparams())

    def setupIteration(self, beamspecfile, ibmIOr, iUsrAnl, NewParam=True):
        if self.getDebug():
            print(" EnvelopeOptimisation.setupIteration: start:")

        self.setnIter(self.getnIter()+1)
        BL.BeamLine.cleaninstance()
        BLE.BeamLineElement.cleaninstances()
        Prtcl.Particle.cleanAllParticles()
        
        if ibmIOr != None:
            inputfile = ibmIOr.getdataFILE().name
            ibmIOr.getdataFILE().close()
            bmIO.BeamIO.cleanBeamIOfiles()
    
            ibmIOr = bmIO.BeamIO(None, inputfile)
            EndOfFile = ibmIOr.readBeamDataRecord()

        else:
            iBl = BL.BeamLine(beamspecfile)

        if self.getDebug():
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print("     ----> Ref parameters:", self.getBLEparamsRef())
        
        self.setBLEparams(self.getBLEparamsRef())
        if self.getDebug():
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print("     ---->     Parameters:", self.getBLEparams())
        
        if NewParam:
            self.newBLEparams()
            if self.getDebug():
                with np.printoptions(linewidth=500,precision=7,suppress=True):
                    print("     ----> New parameters:", self.getBLEparams())

        self.setBeamLine()
        
        iBm = Bm.Beam.getBeamInstances()[0]
        if self.getDebug():
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print("     ----> Initial Beam instance: \n", iBm)

        iBm._sigmaxy    = [iBm._sigmaxy[0]]
        iBm._emittance  = [iBm._emittance[0]]
        iBm._Twiss      = [iBm._Twiss[0]]
        if self.getDebug():
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print("     ---->   sigmaxy[0]:", iBm.getsigmaxy()[0])
                print("     ----> emittance[0]:", iBm.getemittance()[0])
                print("     ---->     Twiss[0]:", iBm.getTwiss()[0])
                print("     ----> Updated Beam instance: \n", iBm)

        return ibmIOr

    def newBLEparams(self):

        GoodLength = False
        while not GoodLength:
            r = np.random.normal(0., 1., 6)
            st = 0.
            
            d  = max(0., self.getBLEparamsRef()[0][1] + 0.02*r[0])
            self.getBLEparams()[0] = ["User:1:Capture:Drift:1", d]
            st += d
        
            l  = max( 0., self.getBLEparamsRef()[1][1] + 0.002*r[1])
            sq = max(90., self.getBLEparamsRef()[1][2] + 2.00*r[2])
            self.getBLEparams()[1] = ["User:1:Capture:FQ:1", l, sq]
            st += l
        
            d  = max(0., self.getBLEparamsRef()[2][1] + 0.002*r[3])
            self.getBLEparams()[2] = ["User:1:Capture:Drift:2", d]
            st += d

            """
            l  = max( 0., self.getBLEparamsRef()[3][1] + 0.02*r[4])
            """
            sq = max(90., self.getBLEparamsRef()[3][2] + 2.00*r[5])
            l  = 2.*l

            self.getBLEparams()[3] = ["User:1:Capture:DQ:1", l, sq]
            st += l

            if st < 1.:
                GoodLength = True
                self.getBLEparams()[4] = ["User:1:Capture:Drift:3", None]

    def setBeamLine(self):
        if self.getDebug():
            print("\n Envelopeptimisation.setBeamLine: start")
        #--------  Get beam line defined so far and reference particle:
        iBL      = BL.BeamLine.getinstance()
        refPrtcl = Prtcl.ReferenceParticle.getinstance()

        #.. Last beam line element:
        iLst = iBL.getElement()[-1]
        
        #--------  Reading source distribution, so, now create
        #          PoPLaR beam line:

        #.. Position of next beam-line element start:
        rStrt  = iLst.getrStrt() + iLst.getStrt2End()
        vStrt  = iLst.getvEnd()
        drStrt = np.array([0.,0.,0.])
        dvStrt = np.array([[0.,0.],[0.,0.]])

        #.. Add drift 1:
        iBLE    = BLE.Drift(self.getBLEparams()[0][0],    \
                            rStrt, vStrt, drStrt, dvStrt, \
                            self.getBLEparams()[0][1])
        BL.BeamLine.addBeamLineElement(iBLE)
        refPrtclSet = refPrtcl.setReferenceParticleAtDrift(iBLE)
        
        #.. Quad doublet:
        rStrt  = iBLE.getrStrt() + iBLE.getStrt2End()
        iBLE    = BLE.FocusQuadrupole(self.getBLEparams()[1][0], \
                            rStrt, vStrt, drStrt, dvStrt,        \
                            self.getBLEparams()[1][1],           \
                            self.getBLEparams()[1][2])
        BL.BeamLine.addBeamLineElement(iBLE)
        refPrtclSet = refPrtcl.setReferenceParticleAtDrift(iBLE)
        
        rStrt  = iBLE.getrStrt() + iBLE.getStrt2End()
        iBLE    = BLE.Drift(self.getBLEparams()[2][0],    \
                            rStrt, vStrt, drStrt, dvStrt, \
                            self.getBLEparams()[2][1])
        BL.BeamLine.addBeamLineElement(iBLE)
        refPrtclSet = refPrtcl.setReferenceParticleAtDrift(iBLE)
        
        rStrt  = iBLE.getrStrt() + iBLE.getStrt2End()
        iBLE    = BLE.DefocusQuadrupole(self.getBLEparams()[3][0], \
                            rStrt, vStrt, drStrt, dvStrt,          \
                            self.getBLEparams()[3][1],             \
                            self.getBLEparams()[3][2])
        BL.BeamLine.addBeamLineElement(iBLE)
        refPrtclSet = refPrtcl.setReferenceParticleAtDrift(iBLE)
        
        #.. Add drift to energy selection collimator:
        rStrt  = iBLE.getrStrt() + iBLE.getStrt2End()
        length = 1. - rStrt[2]
        iBLE    = BLE.Drift(self.getBLEparams()[4][0],    \
                            rStrt, vStrt, drStrt, dvStrt, \
                            length)
        BL.BeamLine.addBeamLineElement(iBLE)
        refPrtclSet = refPrtcl.setReferenceParticleAtDrift(iBLE)
        
        #--------  Print at end:
        if self.getDebug():
            print(" UserAnal.UserInit: Beam line:")
            print(BL.BeamLine.getinstance())
            if BL.BeamLine.getinstance() == None:
                print("     ----> No beam line!  Quit.")
                exit(1)
    
    
#--------  Set/get methods
    def setnIter(self, nIter):
        self.nIter = nIter
            
    def setCost(self, Cost):
        self.Cost  = Cost
            
    def setBLEparams(self, BLEparams):
        self.BLEparams = BLEparams

    def setBLEparamsRef(self, BLEparamsRef):
        self.BLEparamsRef = BLEparamsRef

    def getnIter(self):
        return self.nIter
            
    def getCost(self):
        return self.Cost
        
    def getBLEparams(self):
        return self.BLEparams

    def getBLEparamsRef(self):
        return self.BLEparamsRef


#--------  "Built-in methods":
    def __init__(self, Debug=False):
        self.setDebug(Debug)
        if self.getDebug():
            print(' UserAnal.__init__: ', \
                  'creating the user analysis object object')

        UserAnal.instances.append(self)

        self.setAll2None()

        self.UserInit()

        if self.getDebug():
            print("     ----> New UserAnal instance: \n", \
                  UserAnal.__str__(self))
            print(" <---- UserAnal instance created.")
            
    def __repr__(self):
        return "UserAnal()"

    def __str__(self):
        self.print()
        return " UserAnal __str__ done."

    def print(self):
        print("\n UserAnal:")
        print(" ---------")
        print("     ----> Debug flag:", self.getDebug())
        return " <---- UserAnal parameter dump complete."

    
#--------  "Set method" only Debug
#.. Method believed to be self documenting(!)

    @classmethod
    def setDebug(cls, Debug=False):
        cls.__Debug = Debug
        if cls.__Debug:
            print(" UserAnal.setDebug: ", Debug)

    def setAll2None(self):
        pass

    
#--------  "Get methods" only; version, reference, and constants
#.. Methods believed to be self documenting(!)

    @classmethod
    def getDebug(cls):
        return cls.__Debug

    @classmethod
    def getUserAnalInstances(cls):
        return cls.instances


#--------  Processing methods:
    def EventLoop(self, ibmIOw):

        nPrtcl = 0
        for iPrtcl in Prtcl.Particle.getParticleInstances():
            nPrtcl += 1
            if isinstance(iPrtcl, Prtcl.ReferenceParticle):
                iRefPrtcl = iPrtcl
                continue
            iLoc = -1

            self.UserEvent(iPrtcl)

            if isinstance(ibmIOw, io.BufferedWriter):
                iPrtcl.writeParticle(ibmIOw)
        
        Prtcl.Particle.cleanParticles()

        

#--------  Exceptions:
class noReferenceParticle(Exception):
    pass

