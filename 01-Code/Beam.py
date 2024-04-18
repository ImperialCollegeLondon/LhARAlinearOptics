#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class Beam:
===========

  In some sense a "sister" class to Particle.  Whereas an instance of
  Particle records the passage of a particle travelling through the
  beam line, an instance of Beam records the collective properties of
  the beam such as emittance, etc., as the beam progresses through the
  beam line. 


  Class attributes:
  -----------------
    instances : List of instances of Particle class
  __Debug     : Debug flag

      
  Instance attributes:
  --------------------
   All instance attributes are initialised to Null

   Input arguments:
  _InputDataFile  : Path to BeamIO data file containing events to be read.
  _nEvtMax        : Maximum number of events to read, if not set, read 'em all
  _outputCSVfile  : Path to csv file in which summary of beam processing will
                    be written
  _startlocation  : Location at which extrapolation should start. Integer.
_beamlineSpecificationCSVfile : Kept for backward compatibility, optional.
                                Path to csv file containing specification of
                                beam line.

   _Location[] :   str : Name of location where parameters are recorded
   _s[]        : float : s coordinate at which parameters are recorded
   _nParticles :  list : Number of particles arriving at location
   _CovMtrx    :  list : Covariance matrix by location
   _sigmaxy    :  list : RMS x and y by location.  [0] sigmax, [1] sigmay
   _emittance  :  list : emittance by location; calculated from CovMtrx
                         [0] e_x, [1] e_y, [2] e_L, [3] e_{xy}, [4] e_{6D}
   _Twiss      :  list : Twiss parameters by location
                         [0][0] alpha_x, [0][1] beta_x, [0][2] gamma_x
                         [1][0] alpha_y, [1][1] beta_y, [1][2] gamma_y


  Note on indexing:
  -----------------
  When addressing the lists of BeamLineElements, PhaseSpaceRecords, and
  Bean parameters, the intention is to stick to the following local
  variable-name convention:

    iLoc        -- Address of location of BeamLineElement in
                   BLE.BeamLineElement.getinstances()
    iPhsSpcRcrd -- Address of locationof phase-space record in
                   Prtcl.Partiicle.getTraceSpace()
    iAddr       -- Address in list of CovMtrx etc.

    
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

  Other set methods believed to be self documenting:
   setbeamlineSpecificationCSVfile, setInputDataFile, setoutputCSVfile,
   setnEvtMax, setLocation, sets, setsigmaxy, setEmittance, setTwiss
   

  Get methods:
      getDebug, getbeamlineSpecificationCSVfile,getInputDataFile, 
      getoutputCSVfile, getBeamInstances(cls), getLocation, 
      getnEvtMax, getCovSums, getnParticles, getCovarianceMatrix,
      getsigmaxy, getemittance, getTwiss
          -- thought to be self documenting!

  Processing methods:
    cleanBeams : Deletes all Beam instances and resets list of
                 Beams.
         No input; Returns bool flag, True means all good.

    initialiseSums: initiaise sums used to calculate covariance matrix

     incrementSums: increment sums used to calculate covariance matrix
         Input: Instance of particle class

printProgression : prints evolution of beam parameters by location.

    createReport : creates csv file with evolutio of beam paramters by
                   location.

   initaliseSums : Initials sums needed to calculate covariance matrix

   incrementSums : Incrememnt sums
                input : iPrtcl : instance of particle class by which sums are
                                 to be updated

 calcCovarianceMatrix : Calculate covariance matrix given sums

   evaluateBeam : Read data file and increment sums.  Then, calculate
                  covariance matrix, RMS x and y, emittance, and Twiss
                  paramters

plotBeamProgression : create standard plots
                      (in 99-Scratch/BeamProgressionPlot.pdf!) of beam
                      parameters.


  I/o methods:
    CSV file written out using Report module.

  Exceptions:
    badBeam, badParameter, badParameter, badTraceSpace


Created on Mon 28Feb24: Version history:
----------------------------------------
 1.0: 28Feb24: First implementation

@author: kennethlong
"""

from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
from   copy   import deepcopy
import math   as     mth
import numpy  as     np
import os

import Particle          as Prtcl
import BeamLine          as BL
import BeamLineElement   as BLE
import Report            as Rprt
import BeamIO            as bmIO


class Beam:
    instances  = []
    __Debug    = False


#--------  "Built-in methods":
    def __init__(self, _InputDataFile=None, _nEvtMax=None, \
                       _outputCSVfile=None, _startlocation=None, \
                       _beamlineSpecificationCSVfile=None):

        if self.getDebug():
            print(' Beam.__init__: ', \
                  'creating the Beam object')
            
        Beam.instances.append(self)

        self.setAll2None()

#--------  Check and initialise all inputs:  --------  --------  --------

        #.. Load parameter file
        #.. Check and open input data file
        if _InputDataFile == None:
            raise Exception( \
                        " Beam.__init__: no input data file given.")

        if _nEvtMax == None:
            pass
        elif isinstance(_nEvtMax, int):
            self.setnEvtMax(_nEvtMax)
        else:
            raise Exception(" Bad maximum number of events to read")

        #.. Check and output data file
        if _outputCSVfile == None:
            pass
        else:
            self.setoutputCSVfile(_outputCSVfile)
            dirname, filename = os.path.split(self.getoutputCSVfile())
            if not os.path.isdir(dirname):
                raise Exception( \
                        " Beam.__init__: output data frame invalid.")

        #.. Check and set start location:
        if _startlocation == None:
            pass
        else:
            self.setstartlocation(_startlocation)

#--------  <---- Check and initialise all inputs done.:  --------  --------

#--------  Open input data file, read first record, initialise sums:  -----

        _ibmIOr = bmIO.BeamIO(None, _InputDataFile)
        self.setBeamIOread(_ibmIOr)
        ParticleFILE = self.getBeamIOread().getdataFILE()
        self.setInputDataFile(ParticleFILE)

        EndOfFile = False
        EndOfFile = self.getBeamIOread().readBeamDataRecord()

        if BL.BeamLine.getinstance() == None:
            self.setbeamlineSpecificationCSVfile( \
                                        _beamlineSpecificationCSVfile)
            iBm = BL.BeamLine(self.getbeamlineSpecificationCSVfile())
        
        for iBLE in BLE.BeamLineElement.getinstances():
            if not isinstance(iBLE, BLE.Facility):
                self.setLocation(iBLE.getName())
        self.initialiseSums()
        
        #.. Must have reference particle:
        if not isinstance(Prtcl.ReferenceParticle.getinstance(), \
                          Prtcl.ReferenceParticle):
            raise noReferenceBeam(" Reference particle, ", \
                                      "not first in particle list.")

#--------  <---- Open input data file and load reference particle: done.  --

        if self.__Debug:
            print("     ----> New Beam instance: \n", \
                  Beam.__str__(self))
            print(" Beam.__init__: no maximum number of events requested,", \
                  " will read 'em all!")
            print(" <---- Beam instance created.")
            
    def __repr__(self):
        return "Beam(<InputDataFile>, " + \
               "nEvtMax=None, <OutputFile>=None, " + \
               "[<BeamLineSpecCSV>=None] )"

    def __str__(self):
        self.print()
        return " Beam __str__ done."

    def print(self):
        print(" Beam:")
        print(" -----")
        print("     ----> Debug flag:", self.getDebug())
        print("     ----> Beam specification file:", \
              self.getbeamlineSpecificationCSVfile())
        print("     ----> Input data file:", \
              self.getInputDataFile())
        print("     ----> Number of events to read:", \
              self.getnEvtMax())
        print("     ----> Output data file:", \
              self.getoutputCSVfile())
        print("     ----> Start location:", \
              self.getstartlocation())
        print("     ----> Beam parameters by location:")
        
        for iLoc in range(self.getstartlocation(), len(self.getLocation())):
            iAddr = iLoc - self.getstartlocation()
            if len(self.getnParticles()) > iAddr:
                print("         ----> iLoc, location:", \
                      iLoc, self.getLocation()[iLoc], \
                      " nParticles:", int(self.getnParticles()[iAddr]))
            if len(self.getsigmaxy()) > iAddr:
                print("             ---->   sigma_x,   sigma_y:", \
                      self.getsigmaxy()[iAddr][0], \
                      self.getsigmaxy()[iAddr][1])
            if len(self.getemittance()) > iAddr:
                print("             ----> epsilon_x, epsilon_y:", \
                      self.getemittance()[iAddr][0], \
                      self.getemittance()[iAddr][1])
                print("             ----> epsilon_4, epsilon_l:", \
                      self.getemittance()[iAddr][2], \
                      self.getemittance()[iAddr][3])
                print("             ---->            epsilon_6:", \
                      self.getemittance()[iAddr][4])
            if len(self.getTwiss()) > iAddr:
                print("             ---->      Twiss paramters:", \
                      self.getTwiss()[iAddr])

        return " <---- Beam parameter dump complete."

    
#--------  "Set method" only Debug
#.. Method believed to be self documenting(!)

    @classmethod
    def setDebug(cls, Debug=False):
        if cls.__Debug:
            print(" Beam.setDebug: ", Debug)
        cls.__Debug = Debug

    @classmethod
    def resetBeamInstances(cls):
        if len(cls.instances) > 0:
            cls.instances = []
        
    def setAll2None(self):
        self._bmIOr                        = None
        self._InputDataFile                = None
        self._nEvtMax                      = None
        self._outputCSVfile                = None
        self._startlocation                = None
        self._beamlineSpecificationCSVfile = None

        self._Location   = []
        self._CovSums    = []
        self._nParticles = []
        self._CovMtrx    = []
        self._sigmaxy    = []
        self._emittance  = []
        self._Twiss      = []

    def setbeamlineSpecificationCSVfile(self, _beamlineSpecificationCSVfile):
        self._beamlineSpecificationCSVfile = \
                        _beamlineSpecificationCSVfile

    def setBeamIOread(self, _bmIOr):
        self._bmIOr = _bmIOr

    def setInputDataFile(self, _InputDataFile):
        self._InputDataFile = _InputDataFile

    def setoutputCSVfile(self, _outputCSVfile):
        self._outputCSVfile = _outputCSVfile

    def setnEvtMax(self, _nEvtMax):
        if isinstance(_nEvtMax, int):
            self._nEvtMax = _nEvtMax
        else:
            raise Exception(" Bad maximum number of events to read")
        
    def setstartlocation(self, _startlocation):
        if isinstance(_startlocation, int):
            self._startlocation = _startlocation
        else:
            raise Exception(" Bad start location")
        
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

        for iAddr in range(len(self.getCovarianceMatrix())):
            sx1  = mth.sqrt(self.getCovarianceMatrix()[iAddr][0,0])
            sy1  = mth.sqrt(self.getCovarianceMatrix()[iAddr][2,2])
                
            if self.getDebug():
                print(" Beam.getsigmaxy: iAddr, sx1, sy1:", \
                      iAddr, sx1, sy1)
                
            self._sigmaxy.append([sx1, sy1])
        
        if self.getDebug():
            print(" <---- Beam.setsigmaxy: done.")

    def setEmittance(self):
        if self.getDebug():
            print(" Beam.setEmittance: start")

        CovX = None
        CovY = None
        CovL = None
        Cov4 = None
        
        if len(self.getnParticles()) < 1 or \
           self.getnParticles()[0] < 10:
            return
        else:
            nPrtcls = self.getnParticles()[0] 
            
        for iAddr in range(len(self.getCovarianceMatrix())):
            if iAddr < len(self.getnParticles()):
                nPrtcls = self.getnParticles()[iAddr]
                
            if nPrtcls < 10: break
            
            if self.getDebug():
                print("     ----> iAddr:", iAddr)
                with np.printoptions(linewidth=500,precision=10,\
                                     suppress=True):
                    print("         CovMtrx: \n", \
                          self.getCovarianceMatrix()[iAddr]) 

            CovX = self.getCovarianceMatrix()[iAddr][0:2,0:2]
            CovY = self.getCovarianceMatrix()[iAddr][2:4,2:4]
            CovL = self.getCovarianceMatrix()[iAddr][4:6,4:6]
            Cov4 = self.getCovarianceMatrix()[iAddr][0:4,0:4]
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
            e26  = np.linalg.det(self.getCovarianceMatrix()[iAddr])
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
                print("     ----> CovY: \n", CovY)
                print("     ----> CovL: \n", CovL)
                print("     ----> Cov4: \n", Cov4)
                print("     <---- eX:", self.getemittance()[iAddr][0])
                print("     <---- eY:", self.getemittance()[iAddr][1])
                print("     <---- eL:", self.getemittance()[iAddr][2])
                print("     <---- e4:", self.getemittance()[iAddr][3])
                print("     <---- e6:", self.getemittance()[iAddr][4])

        if self.getDebug():
            print(" <---- Beam.setEmittance: done.")

    def setTwiss(self):
        if self.getDebug():
            print(" Beam.setTwiss: start")
 
        if len(self.getnParticles()) < 1 or \
           self.getnParticles()[0] < 10:
            return
        else:
            nPrtcls = self.getnParticles()[0] 
            
        for iAddr in range(len(self.getCovarianceMatrix())):
            if iAddr < len(self.getnParticles()):
                nPrtcls = self.getnParticles()[iAddr]
                
            if nPrtcls < 10: break
            
            if self.getDebug():
                print("     ----> iAddr:", iAddr)
                with np.printoptions(linewidth=500,precision=10,\
                                     suppress=True):
                    print("         CovMtrx: \n", \
                          self.getCovarianceMatrix()[iAddr])
                print("     ----> ex, ey:", self.getemittance()[iAddr][0], \
                                            self.getemittance()[iAddr][1])
            emX = None
            emY = None
            if self.getemittance()[iAddr][0] > 0.:
                emX = self.getCovarianceMatrix()[iAddr][0:2,0:2] / \
                                       self.getemittance()[iAddr][0]
            if self.getemittance()[iAddr][1] > 0.:
                emY = self.getCovarianceMatrix()[iAddr][2:4,2:4] / \
                                       self.getemittance()[iAddr][1]

            if self.getemittance()[iAddr][0] > 0.:
                ax = -emX[0,1]
                bx =  emX[0,0]
                gx =  emX[1,1]
            else:
                ax = None
                bx = None
                gx = None

            if self.getemittance()[iAddr][1] > 0.:
                ay = -emY[0,1]
                by =  emY[0,0]
                gy =  emY[1,1]
            else:
                ay = None
                by = None
                gy = None

            self._Twiss.append([[ax, bx, gx], [ay, by, gy]])

            if self.getDebug():
                print("         ----> Twiss paramters, x, y:", \
                      self._Twiss[iAddr])

        if self.getDebug():
            print(" <---- Beam.setTwiss: done.")

                      
#--------  "Get methods" only; version, reference, and constants
#.. Methods believed to be self documenting(!)

    @classmethod
    def getDebug(cls):
        return cls.__Debug

    def getbeamlineSpecificationCSVfile(self):
        return self._beamlineSpecificationCSVfile

    def getBeamIOread(self):
        return self._bmIOr
        
    def getInputDataFile(self):
        return self._InputDataFile
        
    def getoutputCSVfile(self):
        return self._outputCSVfile
        
    @classmethod
    def getBeamInstances(cls):
        return cls.instances

    def getLocation(self):
        return self._Location
    
    def getnEvtMax(self):
        return self._nEvtMax

    def getstartlocation(self):
        if self._startlocation == None:
            startlocation = 1
        else:
            startlocation = self._startlocation
        return startlocation

    def getCovSums(self):
        return self._CovSums
    
    def getCovMtrx(self):
        return self._CovMtrx
    
    def getnParticles(self):
        return self._nParticles
    
    def getCovarianceMatrix(self):
        return self._CovMtrx

    def getsigmaxy(self):
        return self._sigmaxy

    def getemittance(self):
        return self._emittance

    def getTwiss(self):
        return self._Twiss

    
#--------  Processing methods:
    def initialiseSums(self):
        if self.getDebug():
            print(" Beam.intialiseSums start:")
            
        CovSums = np.zeros((6,6))

        iLocMin = self.getstartlocation()
            
        for iLoc in range(iLocMin, \
                          len(BLE.BeamLineElement.getinstances())):
            
            iBLE = BLE.BeamLineElement.getinstances()[iLoc]
            if self.getDebug():
                print("     ----> iLoc, BLE name, type:", \
                      iLoc, iBLE.getName(), type(iBLE))

            self._CovSums.append(deepcopy(CovSums))
            self._nParticles.append(0.)
                
        if self.getDebug():
            print(" Beam.initialiseSums: n, CovSums:")
            for i in range(len(self.getnParticles())):
                with np.printoptions(linewidth=500,precision=7,
                                     suppress=True):
                    print("     ----> ", i, "\n", self._CovSums[i])
            
    def incrementSums(self, iPrtcl):
        startlocation = self.getstartlocation()
            
        if self.getDebug():
            print(" Beam.incrementSums start:")
            print("     ----> Start location:", \
                  startlocation)
            print("     ----> Number of locations:", \
                  len(self.getCovSums()))
            print("     ----> Particle trace space:")
            for iAddr in range(len(iPrtcl.getTraceSpace())):
                with np.printoptions(linewidth=500,precision=7,\
                                     suppress=True):
                    print("         ----> iAddr, trace space:", \
                          iAddr, \
                          iPrtcl.getTraceSpace()[iAddr])
            
        for iPhsSpcRcrd in range(startlocation-1, \
                                 len(iPrtcl.getTraceSpace())):
            iLoc  = iPhsSpcRcrd + 1
            iAddr = iLoc - startlocation
            if self.getDebug():
                print("         ----> Phs, iLoc, iAddr:", \
                      iPhsSpcRcrd, iLoc, iAddr, \
                      iPrtcl.getTraceSpace()[iPhsSpcRcrd])
                print("         ----> Location:", iLoc)
                with np.printoptions(linewidth=500,precision=10,\
                                     suppress=True):
                    print("                CovSums_(i): \n", \
                          self.getCovSums()[iAddr])
                    print("         ----> iAddr, startlocation, ", \
                          "len(getnPartcles):", iAddr, startlocation, \
                          len(self.getnParticles()))
                    
            self._nParticles[iAddr] += 1

            for i in range(6):
                for j in range(i,6):
                    self._CovSums[iAddr][i,j]     = \
                        self._CovSums[iAddr][i,j] + \
                        iPrtcl.getTraceSpace()[iPhsSpcRcrd][i] * \
                        iPrtcl.getTraceSpace()[iPhsSpcRcrd][j]
                    if i != j:
                        self._CovSums[iAddr][j,i] = \
                            deepcopy(self._CovSums[iAddr][i,j])

            if self.getDebug():
                print("         ----> Location:", iLoc)
                with np.printoptions(linewidth=500,precision=7,\
                                     suppress=True):
                    print("                CovSums_(i+1): \n", \
                          self.getCovSums()[iAddr]) 
                                
        if self.getDebug():
            print(" <---- Beam.incrementSums: Done")

    def calcCovarianceMatrix(self):
        if self.getDebug():
            print(" Beam.calcCovarianceMatrix start:")
            print("     ----> Number of locations:", \
                  len(self.getCovSums()))

        for iAddr in range(len(self.getCovSums())):
            if self.getDebug():
                print("         ----> Location:", iAddr)
                print("               Number of particles:", \
                      self.getnParticles()[iAddr])
                with np.printoptions(linewidth=500,precision=7,\
                                     suppress=True):
                    print("                CovSums: \n", \
                          self.getCovSums()[iAddr])
                    
            if self.getnParticles()[iAddr] < 1:
                break
            
            self._CovMtrx.append(                             \
                                self.getCovSums()[iAddr] /         \
                                float(self.getnParticles()[iAddr]) \
                                 )
            
            if self.getDebug():
                print("     <---- Covariance matrix:")
                with np.printoptions(linewidth=500,precision=7, \
                                     suppress=True):
                    print("                CovMtrx: \n", \
                          self.getCovarianceMatrix()[iAddr]) 

    def evaluateBeam(self):
        print(" Beam.evaluateBeam: perform sums to get covariance matrices")
        
        EndOfFile = False
        iEvt = 0
        iCnt = 0
        Scl  = 1

        ParticleFILE = self.getInputDataFile()
        print("     ----: event loop")
        while not EndOfFile:
            EndOfFile = self.getBeamIOread().readBeamDataRecord()
            if not EndOfFile:
                iEvt += 1
                if (iEvt % Scl) == 0:
                    print("         ----> Read event ", iEvt)
                    iCnt += 1
                    if iCnt == 10:
                        iCnt = 1
                        Scl  = Scl * 10

                iPrtcl = Prtcl.Particle.getParticleInstances()[1]
                self.incrementSums(iPrtcl)

                Cleaned = Prtcl.Particle.cleanParticles()
            
            if self.getDebug():
                print("     ----> Cleaned:", Cleaned)

            if self.getnEvtMax() != None and iEvt >= self.getnEvtMax():
                break
            
        print("     <----", iEvt, "events read")

        print("     ----> calculate covariance matrix:")
        self.calcCovarianceMatrix()
        print("     <---- done.")
        print("     ----> calculate sigma x, y:")
        self.setsigmaxy()
        print("     <---- done.")
        print("     ----> calculate emittances:")
        self.setEmittance()
        print("     <---- done.")
        print("     ----> Twiss paramters:")
        self.setTwiss()
        print("     <---- done.")
        
        
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
        for iAddr in range(len(self.getLocation())):
            with np.printoptions(linewidth=500,precision=5, \
                                 suppress=True):
                print(self.getLocation()[iAddr], \
                      ": z, s, trace space:", \
                      self.getz()[iAddr], self.gets()[iAddr])

    def getHeader(self):
        HeaderList = ["Name", "nPrtcls", "sigmaxy", "emittance", "Twiss"]
        return HeaderList

    def getLines(self):
        DataList = []
        iLocMin = self.getstartlocation()

        if self.getDebug():
            print(" Beam.getLines:")
            print("     ----> Start location:", self.getstartlocation())
            print("     ----> Number of locations:", \
                  len(self.getLocation()))
            print("     ----> Start location:", iLocMin)
        
        for iLoc in range(iLocMin, \
                          len(BLE.BeamLineElement.getinstances())-1):
            iAddr = iLoc - iLocMin
            if self.getDebug():
                print("         ----> iLoc, Name, iAddr:", \
                      iLoc, self.getLocation()[iLoc-1], iAddr)
                print("         ----> len: location, nParticles, ", \
                      "sigmaxy, emittance, Twiss:", \
                      len(self.getLocation()), \
                      len(self.getnParticles()), \
                      len(self.getsigmaxy()), \
                      len(self.getemittance()), \
                      len(self.getTwiss()))

            nPrtcls = None
            if iAddr < len(self.getnParticles()):
                nPrtcls = self.getnParticles()[iAddr]
            else:
                nPrtcls = None
                
            if iAddr < len(self.getemittance()):
                DataList.append([  \
                                   self.getLocation()[iLoc-1], \
                                   nPrtcls, \
                                   self.getsigmaxy()[iAddr], \
                                   self.getemittance()[iAddr], \
                                   self.getTwiss()[iAddr] \
                                 ])
            elif iAddr < len(self.getsigmaxy()):
                DataList.append([  \
                                   self.getLocation()[iLoc-1], \
                                   nPrtcls, \
                                   self.getsigmaxy()[iAddr], \
                                   None, \
                                   None  \
                                 ])
            else:
                DataList.append([  \
                                   self.getLocation()[iLoc-1], \
                                   None, \
                                   None, \
                                   None, \
                                   None, \
                                 ])

        return DataList
    
    def createReport(self):

        if self.getoutputCSVfile() == None:
            print(" Beam.createReport: no data file given, skip.")
        else:
            Name   = BLE.BeamLineElement.getinstances()[0].getName()
            iRprt  = Rprt.Report(Name, None, self.getoutputCSVfile(),
                             self.getHeader(), self.getLines())
            if self.getDebug():
                print("Beam.createReport:")
                print(iRprt)

            iRprt.asCSV()


    def plotBeamProgression(self):
        if self.getDebug():
            print(" Beam.plotBeamProgression: start")

        font = {'family': 'serif', \
                'color':  'darkred', \
                'weight': 'normal', \
                'size': 16, \
                }
        plt.rcParams["figure.figsize"] = (10., 7.5)
        
        s     = []
        sx    = []
        sy    = []
        ex    = []
        ey    = []

        iRefPrtcl = Prtcl.ReferenceParticle.getinstance()

        print(BL.BeamLine.getinstance())
        
        iLocMin = self.getstartlocation()

        if self.getDebug():
            print("     ----> Start location:", self.getstartlocation())
            print("     ----> Number of locations:", \
                  len(self.getLocation()))
        
        for iLoc in range(iLocMin, \
                          len(BLE.BeamLineElement.getinstances())-1):
            iAddr = iLoc - iLocMin
            s.append(iRefPrtcl.getsOut()[iLoc-1])
            sx.append(self.getsigmaxy()[iAddr][0])
            sy.append(self.getsigmaxy()[iAddr][1])
            ex.append(self.getemittance()[iAddr][0])
            ey.append(self.getemittance()[iAddr][1])
            
            if self.getDebug():
                print("     ----> iLoc, s, sx, sy:", \
                      iLoc, self.getLocation()[iLoc], \
                      s[iAddr], sx[iAddr], sy[iAddr])

        self.setDebug(False)
        plotFILE = '99-Scratch/BeamProgressionPlot.pdf'
        with PdfPages(plotFILE) as pdf:
            fig, axs = plt.subplots(nrows=3, ncols=1, \
                                    layout="constrained")
            # add an artist, in this case a nice label in the middle...
            Ttl = "Test"
            fig.suptitle(Ttl, fontdict=font)
        
            axs[1].plot(s, sx, color='b', marker='o', markersize=4, \
                        label='s_x')
            axs[1].plot(s, sy, color='r', marker='s', markersize=4, \
                        label='s_y')
            axs[1].legend()
            axs[1].set_xlabel('s (m)')
            axs[1].set_ylabel('s_{xy} (m)')

            axs[2].plot(s, ex, color='b', marker='o', markersize=4, \
                        label='e_x')
            axs[2].plot(s, ey, color='r', marker='s', markersize=4, 
                        label='e_y')
            axs[2].legend()
            axs[2].set_xlabel('s (m)')
            axs[2].set_ylabel('e_{xy} (m)')

            
            pdf.savefig()
            plt.close()
            
        if self.getDebug():
            print(" <----  Beam.plotBeamProgression done.")

                
"""
Derived class extrapolateBeam(Beam):
=====================================

  The Beam class provides methods to calculate the collective
  properties of the beam such as emittance, etc., from the
  distributions of beam particles as the beam progresses through the 
  beam line.  The extrapolateBeam derived class uses the transfer
  matrices to extrapolate the initial phase-space distribution along
  the beam line.


  Class attributes:
  -----------------
    instances : List of instances of Particle class
  __Debug     : Debug flag

      
  Instance attributes:
  --------------------
   All instance attributes are initialised to Null

   Input arguments:
  _InputDataFile  : Path to BeamIO data file containing events to be read.
  _nEvtMax        : Maximum number of events to read, if not set, read 'em all
   _outputCSVfile : Path to csv file in which summary of beam processing will
                    be written

    
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


  Get methods:
      getDebug, getbeamlineSpecificationCSVfile,getInputDataFile, 
      getoutputCSVfile, getextrapolateBeamInstances
          -- thought to be self documenting!

  Processing methods:
    cleanextrapolateBeams : Deletes all extrapolateBeam instances
                             and resets list of extrapolateBeam.
         No input; Returns bool flag, True means all good.


  I/o methods:
    CSV file written out using Report module.

  Exceptions:
    badBeam, badParameter, badParameter, badTraceSpace


Created on Mon 28Feb24: Version history:
----------------------------------------
 1.0: 09Apr24: First implementation

@author: kennethlong
"""

class extrapolateBeam(Beam):
    instances  = []
    __Debug    = False


#--------  "Built-in methods":
    def __init__(self, _InputDataFile=None, _nEvtMax=None, \
                       _outputCSVfile=None, _startlocation=None,\
                       _beamlineSpecificationCSVfile=None):
        
        if self.__Debug:
            print(' extrapolateBeam.__init__: ', \
                  'creating the Beam object:', \
                  'start location =', _startlocation)
            
        extrapolateBeam.instances.append(self)

#--------  Check and initialise all inputs:  --------  --------  --------

        Beam.__init__(self, _InputDataFile, _nEvtMax, _outputCSVfile, \
                      _startlocation, _beamlineSpecificationCSVfile)

#--------  <---- Check and initialise all inputs done.:  --------  --------

        if self.__Debug:
            print("     ----> New extrapolateBeam instance: \n", \
                  extrapolateBeam.__str__(self))
            print(" <---- Beam instance created.")
            
    def __repr__(self):
        return "extrapolateBeam(<BeamLineSpecCSV>, <InputDataFile>, " + \
               "nEvtMax=None, startlocation=None <OutputFile>=None)"

    def __str__(self):
        print(" extrapolateBeam:")
        print(" -----------------")
        print("     ----> Start location:", self.getstartlocation())
        self.print()
        return " extrapolateBeam __str__ done."


#--------  "Set method" only Debug
#.. Method believed to be self documenting(!)

    @classmethod
    def setDebug(cls, Debug=False):
        if cls.__Debug:
            print(" extrapolateBeam.setdebug: ", Debug)
        cls.__Debug = Debug

    @classmethod
    def resetextrapolateBeamInstances(cls):
        if len(cls.instances) > 0:
            cls.instances = []
        
    def setAll2None(self):
        Beam.setAll2None(self)
        
    
#--------  "Get methods" only; version, reference, and constants
#.. Methods believed to be self documenting(!)

    @classmethod
    def getDebug(cls):
        return cls.__Debug

    @classmethod
    def getextrapolateBeamInstances(cls):
        return cls.instances

#--------  Processing methods:    
    def initialiseSums(self):
        if self.getDebug():
            print(" extrapolateBeam.intialiseSums start:")
            
        CovSums = np.zeros((6,6))

        iLoc = self.getstartlocation()
            
        iBLE = BLE.BeamLineElement.getinstances()[iLoc]
        if self.getDebug():
            print("     ----> iLoc, BLE name, type:", \
                  iLoc, iBLE.getName(), type(iBLE))

        self._CovSums.append(deepcopy(CovSums))
        self._nParticles.append(0.)
                
        if self.getDebug():
            print("     ----> n, CovSums:")
            for i in range(len(self.getnParticles())):
                with np.printoptions(linewidth=500,precision=7,
                                     suppress=True):
                    print("         ----> n =", i, "\n", self._CovSums[i])

    def incrementSums(self, iPrtcl):
        startlocation = self.getstartlocation()
            
        if self.getDebug():
            print(" extrapolateBeam.incrementSums start:")
            print("     ----> Number of locations:", \
                  len(self.getCovSums()))
            print("     ----> Start location", startlocation, \
                  BLE.BeamLineElement.getinstances()[startlocation].getName())
            print("     ----> Particle trace space:")
            print("         ----> Number of trace-space vectors:", \
                  len(iPrtcl.getTraceSpace()))
            if len(iPrtcl.getTraceSpace()) > startlocation:
                with np.printoptions(linewidth=500,precision=7,\
                                     suppress=True):
                    print("         ----> iLoc, trace space:", \
                          startlocation, \
                          iPrtcl.getTraceSpace()[startlocation-1])

        if len(iPrtcl.getTraceSpace()) > startlocation:
            
            iAddr = 0
            if self.getDebug():
                print("     ----> Start location:", startlocation, \
                BLE.BeamLineElement.getinstances()[startlocation].getName())
            
            self._nParticles[iAddr] += 1

            if self.getDebug():
                print("         ----> Location:", startlocation)
                with np.printoptions(linewidth=500,precision=10,\
                                     suppress=True):
                    print("                CovSums_(i): \n", \
                          self.getCovSums()[iAddr])

            for i in range(6):
                for j in range(i,6):
                    self._CovSums[iAddr][i,j]     = \
                        self._CovSums[iAddr][i,j] + \
                        iPrtcl.getTraceSpace()[startlocation-1][i] * \
                        iPrtcl.getTraceSpace()[startlocation-1][j]
                    if i != j:
                        self._CovSums[iAddr][j,i] = \
                            deepcopy(self._CovSums[iAddr][i,j])
            if self.getDebug():
                print("         ----> Location:", startlocation)
                with np.printoptions(linewidth=500,precision=7,\
                                     suppress=True):
                    print("                CovSums_(i+1): \n", \
                          self.getCovSums()[iAddr]) 

        if self.getDebug():
            print(" <---- extrapolateBeam.incrementSums: Done")

    def extrapolateCovarianceMatrix(self):
        if self.getDebug():
            print(" extrapolateBeam.extrapolateCovarianceMatrix start:")

        iRefPrtcl = Prtcl.ReferenceParticle.getinstance()

        iLocMin = self.getstartlocation()
        if self.getDebug():
            print("     ----> iLocMin:", iLocMin)
        
        for jLoc in range(iLocMin+1, \
                          len(BLE.BeamLineElement.getinstances())):
            
            jAddr       = jLoc - iLocMin 
            iLoc        = jLoc - 1
            iAddr       = iLoc - iLocMin 
            iPhsSpcRcrd = iLoc - 1
            if self.getDebug():
                print("         ---->            Location:", jLoc)
                print("         ---->   Previous location:", iLoc)
                print("         ----> Traces-space record:", iPhsSpcRcrd)
                print("         ---->               jAddr:", jAddr)
                print("         ---->               iAddr:", iAddr)
                          
            jBLE  = BLE.BeamLineElement.getinstances()[jLoc]
            iBLE  = BLE.BeamLineElement.getinstances()[iLoc]
            
            if self.getDebug():
                print("     ----> iBLE name, type:", \
                      iBLE.getName(), type(iBLE))
                print("     ----> jBLE name, type:", \
                      jBLE.getName(), type(jBLE))

            if isinstance(jBLE, BLE.Drift) or \
               isinstance(jBLE, BLE.Aperture) or \
               isinstance(jBLE, BLE.Octupole) or \
               isinstance(jBLE, BLE.CylindricalRFCavity) or \
               isinstance(jBLE, BLE.RPLCswitch):
                pass
            else:
                TrcSpc       = iRefPrtcl.getTraceSpace()[iPhsSpcRcrd]
                TrnsfrMtrx   = jBLE.setTransferMatrix(TrcSpc)
                
            TrnsfrMtrx       = jBLE.getTransferMatrix()
            TrnspsTrnsfrMtrx = np.transpose(TrnsfrMtrx)
                
            if self.getDebug():
                print("         ----> Name:", jBLE.getName())
                with np.printoptions(linewidth=500,precision=10,\
                                     suppress=True):
                    print("         ----> Transfer matrix: \n", \
                          TrnsfrMtrx)
                    print("         ----> Transpose of transfer matrix: \n", \
                          TrnspsTrnsfrMtrx)
                    print("         ----> iLoc, covariance matrix:", \
                          iLoc, " \n", \
                          self.getCovMtrx()[iAddr])

            CovInv  = np.matmul(self.getCovMtrx()[iAddr], TrnspsTrnsfrMtrx)
            CovMtrx = np.matmul(TrnsfrMtrx, CovInv)

            self._CovMtrx.append(CovMtrx)
            
            if self.getDebug():
                with np.printoptions(linewidth=500,precision=10, \
                                     suppress=True):
                    print("         ----> jLoc, CovMtrx: \n", \
                          self.getCovMtrx()[jAddr])

    def extrapolateBeam(self):
        print(" extrapolateBeam.extrapolateBeam: transport beam envelope")
        
        EndOfFile = False
        iEvt = 0
        iCnt = 0
        Scl  = 1

        ParticleFILE = self.getInputDataFile()
        print("     ----: event loop")
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
                self.incrementSums(iPrtcl)

                Cleaned = Prtcl.Particle.cleanParticles()
            
            if self.getDebug():
                print("     ----> Cleaned:", Cleaned)

            if self.getnEvtMax() != None and iEvt >= self.getnEvtMax():
                break
            
        print("     <----", iEvt, "events read")

        print("     ----> calculate covariance matrix:")
        self.calcCovarianceMatrix()
        print("     <---- done.")
        print("     ----> extrapolate covariance matrix:")
        self.extrapolateCovarianceMatrix()
        print("     <---- done.")
        print("     ----> calculate sigma x, y:")
        self.setsigmaxy()
        print("     <---- done.")
        print("     ----> calculate emittances:")
        self.setEmittance()
        print("     <---- done.")
        print("     ----> Twiss paramters:")
        self.setTwiss()
        print("     <---- done.")
        

#--------  Utilities:
    @classmethod
    def cleanextrapolateBeams(cls):
        DoneOK = False
        
        for iexBm in cls.getextrapolateBeamInstances():
            del iexBm
            
        cls.resetextrapolateBeamInstances()
        DoneOK = True

        return DoneOK

    
#--------  Exceptions:
class noReferenceBeam(Exception):
    pass

class badBeam(Exception):
    pass

class badParameter(Exception):
    pass

class badTraceSpace(Exception):
    pass

