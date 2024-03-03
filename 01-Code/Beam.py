#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class Beam:
===========

  In some sense a "sister" class to Particle.  Whereas an instsance of
  Particle records the passage of aparticle travelling through the
  beam line, an instance of Beam records the collective properties of
  the beam such as emittance, etc., as the beam progresses through the
  beam line. 

  Derived classes:
  ----------------
  

  Class attributes:
  -----------------
    instances : List of instances of Particle class
  __Debug     : Debug flag

      
  Instance attributes:
  --------------------
   All instance attributes are initialised to Null
   _Location[] :   str   : Name of location where parameters are recorded
   _s[]        : float   : s coordinate at which parameters are recorded

    
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

  resetBeamInsances:
               Sets cls.instances []

  setAll2None: Set all instance attributes to None.
        No input or return.

  setLocation: str : Set location string at which phase-space is stored.

         sets: float : Set s coordinate at which phase-space is stored.


  Get methods:
      getDebug, getBeamInstances, getLocation, gets, 
      getTraceSpace, getRPLCPhaseSpace, getPhaseSpace
          -- thought to be self documenting!

  Processing methods:
    cleanBeams : Deletes all Beam instances and resets list of
                 Beams.
         No input; Returns bool flag, True means all good.

    initialiseSums: initiaise sums used to calculate covariance matrix

     incrementSums: increment sums used to calculate covariance matrix
         Input: Instance of particle class


  I/o methods:


  Exceptions:
    badBeam, badParameter


Created on Mon 28Feb24: Version history:
----------------------------------------
 1.0: 28Feb24: First implementation

@author: kennethlong
"""

from   copy   import deepcopy
import math   as     mth
import numpy  as     np
import pandas as     pnds

import Particle          as Prtcl
import BeamLine          as BL
import BeamLineElement   as BLE


class Beam:
    instances  = []
    __Debug    = False


#--------  "Built-in methods":
    def __init__(self, _BeamLineSpecificationCVSfile=None, \
                 _InputDataFile=None, \
                 _nEvtMax=None, \
                 _OutputDataFile=None, \
                 ):
        if self.__Debug:
            print(' Beam.__init__: ', \
                  'creating the Beam object')

        #.. Check and load parameter file
        if _BeamLineSpecificationCVSfile == None:
            raise Exception( \
                        " Beam.__init__: no parameter file given.")

        self._BeamLineSpecificationCVSfile = \
                           _BeamLineSpecificationCVSfile
        self._BeamLineParamPandas = BLE.BeamLine.csv2pandas( \
                           _BeamLineSpecificationCVSfile)
        if not isinstance(self._BeamLineParamPandas, pnds.DataFrame):
            raise Exception( \
                    " Beam.__init__: pandas data frame invalid.")

        #.. Check and open input data file
        if _InputDataFile == None:
            raise Exception( \
                        " Beam.__init__: no input data file given.")

        #.. Must have reference particle:
        if not isinstance(Prtcl.ReferenceParticle.getinstance(), \
                          Prtcl.ReferenceParticle):
            raise noReferenceBeam(" Reference particle, ", \
                                      "not first in particle list.")

        if _nEvtMax == None:
            pass
        elif isinstance(_nEvtMax, int):
            self.setnEvtMax(_nEvtMax)
        else:
            raise Exception(" Bad maximum number of events to read")

        Beam.instances.append(self)

        #.. Beam instance created with phase-space at each
        #   interface being recorded as None
        self.setAll2None()

        self.initialiseSums()

        if self.__Debug:
            print("     ----> New Beam instance: \n", \
                  Beam.__str__(self))
            print(" Beam.__init__: no maximum number of events requested,", \
                  " will read 'em all!")
            print(" <---- Beam instance created.")
            
    def __repr__(self):
        return "Beam()"

    def __str__(self):
        self.print()
        return " Beam __str__ done."

    def print(self):
        print("\n Beam:")
        print(" -----")
        print("     ----> Debug flag:", self.getDebug())
        print("     ----> Number of records:", \
              len(self.getLocation()))
        if len(self.getLocation()) > 0:
            print("     ----> Record of trace space:")
        for iLctn in range(len(self.getLocation())):
            print("         ---->", self.getLocation()[iLctn], ":")
            print("             ----> s", self.gets()[iLctn])
            try:
                print("             ----> ", \
              BLE.BeamLineElement.getinstances()[iLctn+1].getName(), \
                      "; length ", \
              BLE.BeamLineElement.getinstances()[iLctn+1].getLength())
            except:
                print("             ----> ", \
                      BLE.BeamLineElement.getinstances()[iLctn+1].getName())
        return " <---- Beam parameter dump complete."

    
#--------  "Set method" only Debug
#.. Method believed to be self documenting(!)

    @classmethod
    def setDebug(cls, Debug=False):
        if cls.__Debug:
            print(" Beam.setdebug: ", Debug)
        cls.__Debug = Debug

    @classmethod
    def resetBeamInstances(cls):
        if len(cls.instances) > 0:
            cls.instances = []
        
    def setAll2None(self):
        self._Location   = []
        self._s          = []
        self._CovSums    = []
        self._nParticles = []
        self._CovMtrx    = []
        self._sigmaxy    = []
        self._emittance  = []
        self._Twiss      = []

    def setnEvtMax(self, _nEvtMax):
        if isinstance(_nEvtMax, int):
            self._nEvtMax = _nEvtMax
        else:
            raise Exception(" Bad maximum number of events to read")
        
    def setLocation(self, Location):
        Success = False
        if isinstance(Location, str):
            self._Location.append(Location)
            Success = True
        return Success

    def sets(self, s):
        Success = False
        if isinstance(s, float):
            self._s.append(s)
            Success = True
        return Success

    def setsigmaxy(self):
        if self.getDebug():
            print(" Beam.setsigmaxy: start")

        for iLoc in range(len(self.getCovarianceMatrix())):
            sx1  = mth.sqrt(self.getCovarianceMatrix()[iLoc][0,0])
            sy1  = mth.sqrt(self.getCovarianceMatrix()[iLoc][2,2])
                
            if self.getDebug():
                print(" Beam.getsigmaxy: iLoc, sx1, sy1:", \
                      iLoc, sx1, sy1)
                
            self._sigmaxy.append([sx1, sy1])
        
        if self.getDebug():
            print(" <---- Beam.setsigmaxy: done.")

    def setEmittance(self):
        if self.getDebug():
            print(" Beam.setEmittance: start")
            
        for iLoc in range(len(self.getCovarianceMatrix())):
            if self.getDebug():
                print("     ----> iLoc:", iLoc)
                with np.printoptions(linewidth=500,precision=10,\
                                     suppress=True):
                    print("         CovMtrx: \n", \
                          self.getCovarianceMatrix()[iLoc]) 

            CovX = self.getCovarianceMatrix()[iLoc][0:2,0:2]
            CovY = self.getCovarianceMatrix()[iLoc][2:4,2:4]
            CovL = self.getCovarianceMatrix()[iLoc][4:6,4:6]
            Cov4 = self.getCovarianceMatrix()[iLoc][0:4,0:4]
            if self.getDebug():
                with np.printoptions(linewidth=500,precision=10,\
                                     suppress=True):
                    print("                CovMtrx_X: \n", CovX)
                    print("                CovMtrx_Y: \n", CovY)
                    print("                CovMtrx_L: \n", CovL)
                    print("                CovMtrx_4: \n", Cov4)

            e2X  = np.linalg.det(CovX)
            e2Y  = np.linalg.det(CovY)
            e2L  = np.linalg.det(CovL)
            e24  = np.linalg.det(Cov4)
            e26  = np.linalg.det(self.getCovarianceMatrix()[iLoc])
            if self.getDebug():
                print("                e2X:", e2X)
                print("                e2Y:", e2Y)
                print("                e2L:", e2L)
                print("                e24:", e24)
                print("                e24:", e26)

            if e2X < 0. and abs(e2X) < 0.01: e2X = 0.
            if e2Y < 0. and abs(e2Y) < 0.01: e2Y = 0.
            if e2L < 0. and abs(e2L) < 0.01: e2L = 0.
            if e24 < 0. and abs(e24) < 0.01: e24 = 0.
            if e26 < 0. and abs(e26) < 0.01: e26 = 0.
            self._emittance.append([                \
                                     mth.sqrt(e2X), \
                                     mth.sqrt(e2Y), \
                                     mth.sqrt(e2L), \
                                     mth.sqrt(e24), \
                                     mth.sqrt(e26)])
            
        if self.getDebug():
            print(" Beam.getEmittance:")
            print("     ----> CovX: \n", CovX)
            print("     <---- eX:", self.getemittance()[iLoc][0])
            print("     <---- eY:", self.getemittance()[iLoc][1])
            print("     <---- eL:", self.getemittance()[iLoc][2])
            print("     <---- e4:", self.getemittance()[iLoc][3])
            print("     <---- e6:", self.getemittance()[iLoc][4])

        if self.getDebug():
            print(" <---- Beam.setEmittance: done.")

    def setTwiss(self):
        if self.getDebug():
            print(" Beam.setTwiss: start")
 
        for iLoc in range(len(self.getCovarianceMatrix())):
            if self.getDebug():
                print("     ----> iLoc:", iLoc)
                with np.printoptions(linewidth=500,precision=10,\
                                     suppress=True):
                    print("         CovMtrx: \n", \
                          self.getCovarianceMatrix()[iLoc])
                print("     ----> ex, ey:", self.getemittance()[iLoc][0], \
                                            self.getemittance()[iLoc][1])
        
            emX = self.getCovarianceMatrix()[iLoc][0:2,0:2] / \
                                       self.getemittance()[iLoc][0]
            emY = self.getCovarianceMatrix()[iLoc][2:4,2:4] / \
                                       self.getemittance()[iLoc][1]

            ax = -emX[0,1]
            bx =  emX[0,0]
            gx =  emX[1,1]

            ay = -emX[0,1]
            by =  emX[0,0]
            gy =  emX[1,1]

            self._Twiss.append([[ax, bx, gx], [ay, by, gy]])

            if self.getDebug():
                print("         ----> Twiss paramters, x, y:", \
                      self._Twiss[iLoc])

        if self.getDebug():
            print(" <---- Beam.setTwiss: done.")

                      
#--------  "Get methods" only; version, reference, and constants
#.. Methods believed to be self documenting(!)

    @classmethod
    def getDebug(cls):
        return cls.__Debug

    @classmethod
    def getBeamInstances(cls):
        return cls.instances

    def getLocation(self):
        return self._Location
    
    def gets(self):
        return self._s

    def getCovSums(self):
        return self._CovSums
    
    def getnParticles(self):
        return self._nParticles
    
    def getCovarianceMatrix(self):
        return self._CovMtrx

    def getsigmaxy(self):
        return self._sigmaxy

    def getemittance(self):
        return self._emittance

    
#--------  Utilities:
    @classmethod
    def cleanBeams(cls):
        DoneOK = False
        
        for iBm in cls.getBeamInstances():
            del iBm
            
        cls.resetBeamInstances()
        DoneOK = True

        return DoneOK
    

    def printProgression(self):
        for iLoc in range(len(self.getLocation())):
            with np.printoptions(linewidth=500,precision=5, \
                                 suppress=True):
                print(self.getLocation()[iLoc], \
                      ": z, s, trace space:", \
                      self.getz()[iLoc], self.gets()[iLoc])


#--------  Covariance matrix calculation:
    def initialiseSums(self):
        if self.getDebug():
            print(" Beam.intialiseSums start:")
            
        CovSums = np.zeros((6,6))

        iLoc = -1
        for iBLE in BLE.BeamLineElement.getinstances():
            if not isinstance(iBLE, BLE.Facility):
                if self.getDebug():
                    print("     ----> BLE name, type:", \
                          iBLE.getName(), type(iBLE))

                iLoc += 1
                    
                self._CovSums.append(deepcopy(CovSums))
                self._nParticles.append(0.)
                
        if self.getDebug():
            print(" Beam.initialiseSums: n, CovSums:")
            for i in range(len(self.getnParticles())):
                with np.printoptions(linewidth=500,precision=7,
                                     suppress=True):
                    print("     ----> ", i, "\n", self._CovSums[i])
            
    def incrementSums(self, iPrtcl):
        if self.getDebug():
            print(" Beam.incrementSums start:")
            print("     ----> Number of locations:", \
                  len(self.getCovSums()))
            print("     ----> Particle trace space:")
            for iLoc in range(len(iPrtcl.getTraceSpace())):
                with np.printoptions(linewidth=500,precision=7,\
                                     suppress=True):
                    print("         ----> iLoc, trace space:", \
                          iLoc, \
                          iPrtcl.getTraceSpace()[iLoc])
            
        CovSumsIncrmnt = np.zeros((6,6))
        
        for iLoc in range(len(iPrtcl.getTraceSpace())):
            if self.getDebug():
                print("         ----> Location:", iLoc)
                with np.printoptions(linewidth=500,precision=10,\
                                     suppress=True):
                    print("                CovSums_(i): \n", \
                          self.getCovSums()[iLoc]) 
            
            self._nParticles[iLoc] += 1

            for i in range(6):
                for j in range(i,6):
                    self._CovSums[iLoc][i,j]     = \
                        self._CovSums[iLoc][i,j] + \
                        iPrtcl.getTraceSpace()[iLoc][i] * \
                        iPrtcl.getTraceSpace()[iLoc][j]
                    if i != j:
                        self._CovSums[iLoc][j,i] = \
                            deepcopy(self._CovSums[iLoc][i,j])

            if self.getDebug():
                print("         ----> Location:", iLoc)
                with np.printoptions(linewidth=500,precision=7,\
                                     suppress=True):
                    print("                CovSums_(i+1): \n", \
                          self.getCovSums()[iLoc]) 
                                
        if self.getDebug():
            print(" <---- Beam.incrementSums: Done")

    def calcCovarianceMatrix(self):
        if self.getDebug():
            print(" Beam.calcCovarianceMatrix start:")
            print("     ----> Number of locations:", \
                  len(self.getCovSums()))

        for iLoc in range(len(self.getCovSums())):
            if self.getDebug():
                print("         ----> Location:", iLoc)
                print("               Number of particles:", \
                      self.getnParticles()[iLoc])
                with np.printoptions(linewidth=500,precision=7,\
                                     suppress=True):
                    print("                CovSums: \n", \
                          self.getCovSums()[iLoc])
                    
            if self.getnParticles()[iLoc] > 0:
                self._CovMtrx.append(                             \
                                self.getCovSums()[iLoc] /         \
                                float(self.getnParticles()[iLoc]) \
                                     )
                
            if self.getDebug():
                print("     <---- Covariance matrix:")
                with np.printoptions(linewidth=500,precision=7, \
                                     suppress=True):
                    print("                CovMtrx: \n", \
                          self.getCovarianceMatrix()[iLoc]) 


#--------  Covariance matrix calculation:
    
#--------  Exceptions:
class noReferenceBeam(Exception):
    pass

class badBeam(Exception):
    pass

class badParameter(Exception):
    pass

class badTraceSpace(Exception):
    pass

