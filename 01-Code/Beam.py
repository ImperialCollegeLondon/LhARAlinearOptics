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
            
        self.setAll2None()

#--------  Check and initialise all inputs:  --------  --------  --------

        #.. Check and load parameter file
        if _BeamLineSpecificationCVSfile == None:
            raise Exception( \
                        " Beam.__init__: no parameter file given.")
        self.setBeamLineSpecificationCVSfile( \
                           _BeamLineSpecificationCVSfile)
        if  not os.path.isfile(self.getBeamLineSpecificationCVSfile()):
            raise Exception( \
                    " Beam.__init__: pandas data frame invalid.")

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
        if _OutputDataFile == None:
            pass
        else:
            self.setOutputDataFile(_OutputDataFile)
            print(self.getOutputDataFile())
            dirname, filename = os.path.split(self.getOutputDataFile())
            print(dirname, filename)
            if not os.path.isdir(dirname):
                raise Exception( \
                        " Beam.__init__: output data frame invalid.")

        Beam.instances.append(self)

#--------  <---- Check and initialise all inputs done.:  --------  --------

#--------  Load specification file, i.e. initialise geometry:  --------
#          (and load reference particle)

        iBm = BL.BeamLine(self.getBeamLineSpecificationCVSfile())
        for iBLE in BLE.BeamLineElement.getinstances():
            if not isinstance(iBLE, BLE.Facility):
                self.setLocation(iBLE.getName())
        self.initialiseSums()

#--------  <---- Load specification file, i.e. initialise geometry: done. -

#--------  Open input data file:  --------  --------  --------  --------

        ParticleFILE = Prtcl.Particle.openParticleFile("", \
                                                       _InputDataFile)
        self.setInputDataFile(ParticleFILE)
        #.. Must have reference particle:
        if not isinstance(Prtcl.ReferenceParticle.getinstance(), \
                          Prtcl.ReferenceParticle):
            raise noReferenceBeam(" Reference particle, ", \
                                      "not first in particle list.")

#--------  <---- Open input data file and load reference particle: done.  --

#--------  Loop over particles, form summs: --------  --------  --------

        self.evaluateBeam()

#--------  <---- Open input data file and load reference particle: done.  --

        if self.__Debug:
            print("     ----> New Beam instance: \n", \
                  Beam.__str__(self))
            print(" Beam.__init__: no maximum number of events requested,", \
                  " will read 'em all!")
            print(" <---- Beam instance created.")
            
    def __repr__(self):
        return "Beam(<BeamLineSpecCSV>, <InputDataFile>, " + \
               "nEvtMax=None, <OutputFile>=None)"

    def __str__(self):
        self.print()
        return " Beam __str__ done."

    def print(self):
        print("\n Beam:")
        print(" -----")
        print("     ----> Debug flag:", self.getDebug())
        print("     ----> Beam specification file:", \
              self.getBeamLineSpecificationCVSfile())
        print("     ----> Input data fole:", \
              self.getInputDataFile())
        print("     ----> Number of events to read:", \
              self.getnEvtMax())
        print("     ----> Output data fole:", \
              self.getOutputDataFile())
        print("     ----> Beam parameters by location:")
        for iLoc in range(len(self.getLocation())):
            print("         ----> iLoc:", iLoc, self.getLocation()[iLoc], \
                  " nParticles:", self.getnParticles()[iLoc])
            print("             ---->   sigma_x,   sigma_y:", \
                  self.getsigmaxy()[iLoc][0], self.getsigmaxy()[iLoc][1])
            print("             ----> epsilon_x, epsilon_y:", \
                  self.getemittance()[iLoc][0], self.getemittance()[iLoc][1])
            print("             ----> epsilon_4, epsilon_l:", \
                  self.getemittance()[iLoc][2], self.getemittance()[iLoc][3])
            print("             ---->            epsilon_6:", \
                  self.getemittance()[iLoc][4])
            print("             ---->      Twiss paramters:", \
                  self.getTwiss()[iLoc])
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
        self._BeamLineSpecificationCVSfile = None
        self._InputDataFile                = None
        self._nEvtMax                      = None
        self._OutputDataFile               = None

        self._Location   = []
        self._CovSums    = []
        self._nParticles = []
        self._CovMtrx    = []
        self._sigmaxy    = []
        self._emittance  = []
        self._Twiss      = []

    def setBeamLineSpecificationCVSfile(self, _BeamLineSpecificationCVSfile):
        self._BeamLineSpecificationCVSfile = \
                        _BeamLineSpecificationCVSfile

    def setInputDataFile(self, _InputDataFile):
        self._InputDataFile = _InputDataFile

    def setOutputDataFile(self, _OutputDataFile):
        self._OutputDataFile = _OutputDataFile

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
            emX = None
            emY = None
            if self.getemittance()[iLoc][0] > 0.:
                emX = self.getCovarianceMatrix()[iLoc][0:2,0:2] / \
                                       self.getemittance()[iLoc][0]
            if self.getemittance()[iLoc][1] > 0.:
                emY = self.getCovarianceMatrix()[iLoc][2:4,2:4] / \
                                       self.getemittance()[iLoc][1]

            if self.getemittance()[iLoc][0] > 0.:
                ax = -emX[0,1]
                bx =  emX[0,0]
                gx =  emX[1,1]
            else:
                ax = None
                bx = None
                gx = None

            if self.getemittance()[iLoc][1] > 0.:
                ay = -emX[0,1]
                by =  emX[0,0]
                gy =  emX[1,1]
            else:
                ay = None
                by = None
                gy = None

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

    def getBeamLineSpecificationCVSfile(self):
        return self._BeamLineSpecificationCVSfile

    def getInputDataFile(self):
        return self._InputDataFile
        
    def getOutputDataFile(self):
        return self._OutputDataFile
        
    @classmethod
    def getBeamInstances(cls):
        return cls.instances

    def getLocation(self):
        return self._Location
    
    def getnEvtMax(self):
        return self._nEvtMax

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

    def getTwiss(self):
        return self._Twiss

    
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

    def getHeader(self):
        HeaderList = ["Name", "nPrtcls", "sigmaxy", "emittance", "Twiss"]
        return HeaderList

    def getLines(self):
        DataList = []
        for iLoc in range(len(self.getLocation())):
            DataList.append([  \
                               self.getLocation()[iLoc], \
                               self.getnParticles()[iLoc], \
                               self.getsigmaxy()[iLoc], \
                               self.getemittance()[iLoc], \
                               self.getTwiss()[iLoc] \
                               ])
        return DataList
    
    def createReport(self):

        if self.getOutputDataFile() == None:
            print(" Beam.createReport: no data file given, skip.")
        else:
            Name   = BLE.BeamLineElement.getinstances()[0].getName()
            iRprt  = Rprt.Report(Name, None, self.getOutputDataFile(),
                             self.getHeader(), self.getLines())
            if self.getDebug():
                print("Beam.createReport:")
                print(iRprt)

            iRprt.asCSV()


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

    def evaluateBeam(self):
        print(" Beam.evaluateBeam: perform sums to get covariance matrices")
        
        EndOfFile = False
        iEvt = 0
        iCnt = 0
        Scl  = 10

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

            if self.getnEvtMax() > 0 and iEvt >= self.getnEvtMax():
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
        
        for iLoc in range(len(self.getLocation())):
            s.append(iRefPrtcl.getsOut()[iLoc])
            sx.append(self.getsigmaxy()[iLoc][0])
            sy.append(self.getsigmaxy()[iLoc][1])
            ex.append(self.getemittance()[iLoc][0])
            ey.append(self.getemittance()[iLoc][1])
            
            if self.getDebug():
                print("     ----> iLoc, s, sx, sy:", \
                      iLoc, s[iLoc], sx[iLoc], sy[iLoc])

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
        """
            for iLoc in range(len(xLoc)):

                #axs[0, 0].set_title('x,y')
                axs[0, 0].hist2d(xLoc[iLoc], yLoc[iLoc], bins=100)
                axs[0, 0].set_xlabel('x (m)')
                axs[0, 0].set_ylabel('y (m)')
            
                #axs[0, 1].set_title('delta')
                
                axs[0, 1].hist(ELoc[iLoc], 100)
                axs[0, 1].set_yscale('linear')
                if logE:
                    axs[0, 1].set_yscale('log')
                axs[0, 1].set_xlabel('delta')
                axs[0, 1].set_ylabel('Number')
            
                #axs[1, 0].set_title('x, xprime')
                axs[1, 0].hist2d(xLoc[iLoc], xpLoc[iLoc], bins=100)
                axs[1, 0].set_xlabel('x (m)')
                axs[1, 0].set_ylabel('xprime (m)')

                #axs[1, 1].set_title('y, yprime')
                axs[1, 1].hist2d(yLoc[iLoc], ypLoc[iLoc], bins=100)
                axs[1, 1].set_xlabel('y (m)')
                axs[1, 1].set_ylabel('yprime (m)')

                axs[2, 0].hist(ELab[iLoc], 100)
                axs[2, 0].set_yscale('linear')
                if logE:
                    axs[2, 0].set_yscale('log')
                axs[2, 0].set_xlabel('Kinetic energy (MeV)')
                axs[2, 0].set_ylabel('Number')

                axs[2, 1].hist(Scl[iLoc], 100)
                axs[2, 1].set_yscale('linear')
                if logE:
                    axs[2, 1].set_yscale('log')
                axs[2, 1].set_xlabel('Epsilon')
                axs[2, 1].set_ylabel('Number')

        
        """
        if self.getDebug():
            print(" <----  Beam.plotBeamProgression done.")

                
#--------  Exceptions:
class noReferenceBeam(Exception):
    pass

class badBeam(Exception):
    pass

class badParameter(Exception):
    pass

class badTraceSpace(Exception):
    pass

