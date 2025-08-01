#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class Simulation
================

  CEO class for linear optics simulation of beam lines.

  Class attributes:
  -----------------
  __instance   : Set on creation of first (and only) instance.
  __Debug      : Debug flag
  __PrgrssPrnt : Flag to set printing of progress (defalt True)
__RandomSeed   : Seed for random number, set to time at load of class.  
__Facility     : Address of instance of a facility

  Packages loaded:
  ----------------
  "time"  : to get current date/time
  "random": uniform random number generator
      
  Methods defined at Module level:
  --------------------------------
    getRandom : no input, returns random numerm calls random.random.
 getParabolic : Generate random number distributed as an inverted parabola
                from -p1 to p1.
           Input : p1 [float]
       Return : Probability [float]

  Instance attributes:
  --------------------
            _NEvt : Number of events to generate
   _ParamFileName : csv file containing parameters of the simulation
    _RootFileName : Root file for o/p
    
  Methods:
  --------
  Built-in methods __new__, __repr__ and __str__.
      __new__ : Creates singleton class and prints version, PDG
                reference, and values of constants used.
      __repr__: One liner with call.
      __str__ : Dump of contents

  Get/set methods:
      CdVrsn()     : Returns code version number.
      getRandomSeed: Returns random seed
           setDebug: Set debug flag
           getDebug: Get debug flag
   getFacility: Get __Facility
            getNEvt: Get NEvt
  
  Simulation methods:
      getRandom    : Returns uniformly distributed randum number
      getParabolic : Generates a parabolic distributed random number from
                     -p1 to p1 (p1 input)
            RunSim : CEO method to run simulation.

          Utilities:
                print : Print summary of paramters


Created on Thu 10Jan21;11:04: Version history:
----------------------------------------------
 1.0: 21Jul23: First implementation

@author: kennethlong
"""

#--------  Module dependencies
import random as __Rnd
import numpy as np
import sys

import BeamIO          as BmIO
import BeamLine        as BL
import BeamLineElement as BLE
import Particle        as Prtcl

#--------  Module methods
def getRandom():
    return __Rnd.random()

def getParabolic(p1):
    ran = getRandom()
    a = np.array( [ 1., 0., (-3.*p1*p1), (2.*p1*p1*p1*(2.*ran - 1.)) ] )
    r = np.roots(a)
    isol = 0
    for ri in r:
        if not isinstance(ri, complex):
            if ri >= -p1:
                if ri <= p1:
                    isol += 1
                    p = ri
    if isol != 1:
        raise Exception("Simulation.getParabolic; p multiply defined")

    return p

#--------  Simulation class  --------
class Simulation(object):
    import random as __Rnd
    import time as __T
    
    __RandomSeed = __T.time()

    __Debug      = False
    __PrgrssPrnt = True
    __instance   = None


#--------  "Built-in methods":
    def __new__(cls, NEvt=5, filename=None, 
                _dataFileDir=None, _dataFileName=None, \
                _inputFILE=None, _BDSIMfile=False):
        
        if cls.__instance is None:
            if cls.getDebug():
                print('Simulation.__new__: creating the Simulation object')
                print('-------------------')
            cls.__instance = super(Simulation, cls).__new__(cls)
            
            cls.setAll2None()
            
            cls.__Rnd.seed(int(cls.__RandomSeed))

            cls.setNEvt(NEvt)
            if filename != None:
                cls.setBeamLineSpecificationFile(filename)

            if _dataFileDir  != None:
                cls.setdataFileDir(_dataFileDir)
            if _dataFileName != None:
                cls.setdataFileName(_dataFileName)

            if _inputFILE != None:
                cls.setinputFILE(_inputFILE, _BDSIMfile)

            # Open file for read:
            if _inputFILE != None:
                cls._iBmIOr = BmIO.BeamIO(None, _inputFILE, False, _BDSIMfile)
                if not cls.getiBmIOr().getBDSIMfile():
                    print("     ----> Reading particles from file:")
                    print("         ----> Need to read & skip first record")
                    cls.getiBmIOr().readBeamDataRecord()
                    p0iBmIOr = BLE.Facility.getinstances().getp0()
                    print("             ---->", \
                          "Reference particle momentum from input file:", \
                          p0iBmIOr)
                    BL.BeamLine.cleaninstance()
                    BLE.BeamLineElement.cleaninstances()
                    Prtcl.Particle.cleanAllParticles()
    
            # Create Facility instance:
            cls.setFacility(BL.BeamLine(filename))
            p0BLfile = BLE.Facility.getinstances().getp0()
            print("             ---->", \
                  "Reference particle momentum from beam line file:", \
                  p0BLfile)
            if p0iBmIOr != p0BLfile:
                print("     ****", \
                  "Reference particle momentum from beam line file", \
                  " is not the same as that read from input file, abort.", \
                  "****" )
                raise referenceMOMENTUMmismatch()
            print("         <---- Beam line set up.")

            # Open file for write:
            if _dataFileDir != None or _dataFileName != None:
                cls._iBmIOw = BmIO.BeamIO(_dataFileDir, _dataFileName, True)
            
            # Summarise initialisation
            if cls.getDebug():
                cls.print(cls)

        return cls.__instance

    def __repr__(self):
        return "Simulation()"

    def __str__(self):
        self.__repr__()
        self.print()
        return " Simulation.__str__ done."

    def print(self):
        print(" Simulation.print:")
        print("                        Version:", self.CdVrsn())
        print("      State of random generator:", self.__Rnd.getstate()[0])
        print("   Number of events to generate:", self.getNEvt())
        print("   Beam line specification file:", \
              self.getBeamLineSpecificationFile())
        print(" data file directory for output:", self.getdataFileDir())
        print("       data filename for output:", self.getdataFileName())
        if self.getinputFILE() != None:
            print("                Input file path:", self.getinputFILE()[0])
            print("               Input file BDSIM:", self.getinputFILE()[1])
        print(" BeamIO output file instance id:", id(self.getiBmIOw()))
        print("  BeamIO input file instance id:", id(self.getiBmIOr()))
            
#--------  "Set/Get methods" only; version, reference, and constants
#.. Methods believed to be self documenting(!)
    @classmethod
    def setAll2None(cls):
            cls._NEvt          = None
            cls._ParamFileName = None
            cls._dataFileDir   = None
            cls._dataFileName  = None
            cls._inputFILE     = None
            cls._BDSIMfile     = None
            cls._iBmIOw        = None
            cls._iBmIOr        = None
            cls._Facility      = None

    @classmethod
    def CdVrsn(self):
        return 1.0

    @classmethod
    def setNEvt(self, NEvt):
        if not isinstance(NEvt, int):
            raise badParameter()
        
        self._NEvt = NEvt

    @classmethod
    def setBeamLineSpecificationFile(self, BLspecfile):
        if not isinstance(BLspecfile, str):
            raise badParameter()

        self._ParamFileName = BLspecfile

    @classmethod
    def setdataFileDir(self, dataFileDir):
        if dataFileDir is not None and not isinstance(dataFileDir, str):
            raise badParameter()
        
        self._dataFileDir = dataFileDir

    @classmethod
    def setdataFileName(self, dataFileName):
        if not isinstance(dataFileName, str):
            raise badParameter()
        
        self._dataFileName = dataFileName

    @classmethod
    def setinputFILE(self, _inputFILE, _BDSIMfile):
        if not isinstance(_inputFILE, str):
            raise badParameter("inputFILE")
        if not isinstance(_BDSIMfile, bool):
            raise badParameter("_BDSIMfile")
        
        self._inputFILE = [_inputFILE, _BDSIMfile]
        
    @classmethod
    def setDebug(cls, _Debug=False):
        cls.__Debug = _Debug

    def getRandomSeed(self):
        return Simulation.__RandomSeed

    @classmethod
    def getDebug(cls):
        return cls.__Debug

    @classmethod
    def setProgressPrint(cls, _PrgrssPrnt=True):
        cls.__PrgrssPrnt = _PrgrssPrnt

    @classmethod
    def setiBmIOw(self, _iBmIOw):
        self._iBmIOw = _iBmIOw

    @classmethod
    def setiBmIOr(self, _iBmIOr):
        self._iBmIOr = _iBmIOr

    @classmethod
    def setFacility(cls, _Facility):
        cls._Facility = _Facility

    @classmethod
    def getFacility(cls):
        return cls._Facility

    @classmethod
    def getdataFileDir(cls):
        return cls._dataFileDir

    @classmethod
    def getdataFileName(cls):
        return cls._dataFileName

    @classmethod
    def getinputFILE(cls):
        return cls._inputFILE

    @classmethod
    def getNEvt(self):
        return self._NEvt

    @classmethod
    def getBeamLineSpecificationFile(self):
        return self._ParamFileName

    @classmethod
    def getiBmIOw(self):
        return self._iBmIOw

    @classmethod
    def getiBmIOr(self):
        return self._iBmIOr

    @classmethod
    def getProgressPrint(cls):
        return cls.__PrgrssPrnt

    @classmethod
    def getinstances(cls):
        return cls.__instance

#--------  Utilities:

        
#--------  Simulation run methods
    def RunSim(self):
        if self.getDebug():
            print()
            print('Simulation.RunSim: simulation begins')
            print('-----------------')

        dataFILE = None
        if self.getiBmIOw() != None:
            dataFILE = self.getiBmIOw().getdataFILE()
            
        #.. Write facility:
        if self.getiBmIOw() != None:
            BL.BeamLine.getinstances().writeBeamLine(dataFILE)

        #.. Check if Source Mode!=3 (read from file):
        if BLE.BeamLineElement.getinstances()[1].getMode() != 3:

            #.. Transport particles through facility:
            nEvt = self.getFacility().trackBeam(self.getNEvt(), dataFILE)

        else:
            
            #.. Source from file, loop and
            #   transport particles through facility:
            EndOfFile = False
            iEvt      = 0
            Scl  = 10
            iCnt = 1
            while not EndOfFile and iEvt < self.getNEvt():
                try:
                    EndOfFile = Prtcl.Particle.readParticle( \
                                              self.getinputFILE()[0])
                except:
                    EndOfFile = self.getiBmIOr().readBeamDataRecord()

                if not EndOfFile and iEvt < self.getNEvt():
                    iEvt += 1

                    if (iEvt % Scl) == 0:
                        if (self.getDebug() or self.getNEvt() > 1) and \
                           self.getProgressPrint():
                            print("         ----> Generating event ", iEvt)
                        if iCnt == 10:
                            iCnt = 1
                            Scl  = Scl * 10
                        iCnt += 1
                    
                    iPrtcl = Prtcl.Particle.getinstances()[-1]
                    nEvt = self.getFacility().trackBeam(1, dataFILE, iPrtcl)

        #.. Flush and close particle file:
        if self.getiBmIOw() != None:
            self.getiBmIOw().flushNclosedataFile(dataFILE)

#--------  Exceptions:
class badParameter(Exception):
    pass

class referenceMOMENTUMmismatch(Exception):
    pass
