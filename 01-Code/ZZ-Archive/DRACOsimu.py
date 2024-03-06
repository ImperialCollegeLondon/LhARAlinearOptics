#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class Simulation
================

  CEO class for linear optics simulation of DRACO beam line.

  Class attributes:
  -----------------
  __instance : Set on creation of first (and only) instance.
     __Debug : Debug flag

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
    _dataFileName : data file for o/p
    
  Methods:
  --------
  Built-in methods __new__, __repr__ and __str__.
      __new__ : Creates singleton class and prints version, PDG
                reference, and values of constants used.
      __repr__: One liner with call.
      __str__ : Dump of contents

  Set methods:
           setDebug: Input bool -- sets class debug flag

  Get methods:
      CdVrsn()     : Returns code version number.
      getRandomSeed: Returns random seed
           getDebug: Return class debug flag
       getDRACObeam: Get instance of DRACObeam class
     getdataFileDir: Get path to directory containing data file
    getdataFileName: Get data file name
            getNEvt: Get number of events to generate.
  
  Simulation methods:
      getRandom    : Returns uniformly distributed randum number
      getParabolic : Generates a parabolic distributed random number from
                     -p1 to p1 (p1 input)
             RunSim: Run sumulation

  Utilities:
             print: Prints conditions underwhich simulation is run.


Created on Thu 10Jan21;11:04: Version history:
----------------------------------------------
 1.0: 28Sep23: First implementation

@author: kennethlong
"""

#--------  Module dependencies
import random as __Rnd
import numpy as np
import sys

import DRACObeam
import Particle as Prtcl

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
        raise Exception("DRACOSimu.getParabolic; p multiply defined")

    return p


#--------  Simulation class  --------
class Simulation(object):
    import random as __Rnd
    import time as __T
    
    __RandomSeed = __T.time()

    __Debug     = False
    __instance  = None


#--------  "Built-in methods":
    def __new__(cls, NEvt=5, _filename=None, \
                _dataFileDir=None, _dataFileName=None):
        if cls.__instance is None:
            print('DRACOSimu.__new__: creating the Simulation object')
            print('------------------')
            cls.__instance = super(Simulation, cls).__new__(cls)
            
            cls.__Rnd.seed(int(cls.__RandomSeed))

            cls._NEvt          = NEvt
            cls._ParamFileName = _filename
            cls._dataFileDir   = _dataFileDir
            cls._dataFileName  = _dataFileName

            # Create DRACObeam instance:
            cls.__DRACObm = DRACObeam.DRACObeam(_filename)

            # Summarise initialisation
            cls.print(cls)

        return cls.__instance

    def __repr__(self):
        return "Simulation()"

    def __str__(self):
        self.__repr__()
        self.print()

            
#--------  "Set methods":
#.. Methods believed to be self documenting(!)
    @classmethod
    def setDebug(cls, _Debug=False):
        cls.__Debug = _Debug


#--------  "Get methods":
#.. Methods believed to be self documenting(!)

    def CdVrsn(self):
        return 1.0

    def getRandomSeed(self):
        return DRACOSimu.__RandomSeed

    @classmethod
    def getDebug(cls):
        return cls.__Debug

    @classmethod
    def getDRACObeam(cls):
        return cls.__DRACObm

    @classmethod
    def getdataFileDir(cls):
        return cls._dataFileDir

    @classmethod
    def getdataFileName(cls):
        return cls._dataFileName

    def getNEvt(self):
        return self._NEvt

#--------  Utilities:
    def print(self):
        print(" DRACOSimu.print:")
        print("                        Version:", self.CdVrsn(self))
        print("      State of random generator:", self.__Rnd.getstate()[0])
        print("   Number of events to generate:", self._NEvt)
        print("   Beam line specification file:", self._ParamFileName)
        print(" data file directory for output:", self._dataFileDir)
        print("       data filename for output:", self._dataFileName)

        
#--------  Simulation run methods
    def RunSim(self):
        print()
        print('DRACOSimu.RunSim: simulation begins')
        print('-----------------')

        runNumber =  26                   # set run number

        #.. Open file to store events:
        ParticleFILE = Prtcl.Particle.createParticleFile( \
                                       self.getdataFileDir(), \
                                       self.getdataFileName() )
                                                          
        #.. Transport particles through LhARA:
        
        nEvt = self.getDRACObeam().trackDRACO(self.getNEvt(), ParticleFILE)

        #.. Flush and close particle file:
        Prtcl.Particle.flushNcloseParticleFile(ParticleFILE)
