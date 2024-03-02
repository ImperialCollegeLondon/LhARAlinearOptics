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

from   copy  import deepcopy
import numpy as np

import Particle          as Prtcl
import BeamLine          as BL
import BeamLineElement   as BLE


class Beam:
    instances  = []
    __Debug    = False


#--------  "Built-in methods":
    def __init__(self):
        if self.__Debug:
            print(' Beam.__init__: ', \
                  'creating the Beam object')

        #.. Must have reference particle:
        if not isinstance(Prtcl.ReferenceParticle.getinstance(), \
                          Prtcl.ReferenceParticle):
            raise noReferenceBeam(" Reference particle, ", \
                                      "not first in particle list.")

        Beam.instances.append(self)

        #.. Beam instance created with phase-space at each
        #   interface being recorded as None
        self.setAll2None()

        self.initialiseSums()

        if self.__Debug:
            print("     ----> New Beam instance: \n", \
                  Beam.__str__(self))
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
        sx = []
        sy = []
        for iLoc in range(len(self.getCovarianceMatrix())):
            sx1  = np.sqrt(self.getCovarianceMatrix()[iLoc][0,0])
            sy1  = np.sqrt(self.getCovarianceMatrix()[iLoc][2,2])
                
            if self.getDebug():
                print(" Beam.getsigmaxy: iLoc, sx1, sy1:", \
                      iLoc, sx1, sy1)
                
            sx.append(sx1)
            sy.append(sy1)

        return sx, sy

    def getEmittance(self):
        if self.getDebug():
            print(" Beam.getEmittance: start")
            
        eX = []
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
                print("                e2X:", CovX)
                print("                e2Y:", CovY)
                print("                e2L:", CovL)
                print("                e24:", Cov4)

            eX.append(np.sqrt(e2X))
            eY   = np.sqrt(e2Y)
            eL   = np.sqrt(e2L)
            e4   = np.sqrt(e24)
            e6   = np.sqrt(e26)
            
        if self.getDebug():
            print(" Beam.getEmittance:")
            print("     ----> CovX: \n", CovX)
            print("     <---- eX:", eX[iLoc])

        return eX

    
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

