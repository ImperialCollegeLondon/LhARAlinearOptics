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

setTraceSpace: np.ndarray(6,) : trace space 6 floats

setRPLCPhaseSpace: [np.ndarray(3,), np.ndarray(3,)]: two three vectors

setLabPhaseSpace: [np.ndarray(3,), np.ndarray(3,)]: two three vectors

recordBeam: i/p: Location, s, z, TraceSpace:
                calls, setLocation, sets, setTraceSpace in turn
                to store all variables.

  setSourceTraceSpace: set trace space after source
           Input: numpy.array(6,); 6D phase to store
          Return: Success: bool, True if stored OK.


  Get methods:
      getDebug, getBeamInstances, getLocation, gets, 
      getTraceSpace, getRPLCPhaseSpace, getPhaseSpace
          -- thought to be self documenting!

  Processing methods:
    cleanBeams : Deletes all Beam instances and resets list of
                 Beams.
         No input; Returns bool flag, True means all good.


  I/o methods:


  Exceptions:
    badBeam, badParameter


Created on Mon 28Feb24: Version history:
----------------------------------------
 1.0: 28Feb24: First implementation

@author: kennethlong
"""

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
        self._Location  = []
        self._s         = []
        
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
            with np.printoptions(linewidth=500,precision=5,suppress=True):
                print(self.getLocation()[iLoc], ": z, s, trace space:", \
                      self.getz()[iLoc], self.gets()[iLoc])


#--------  Processing methods:

    
#--------  Exceptions:
class noReferenceBeam(Exception):
    pass

class badBeam(Exception):
    pass

class badParameter(Exception):
    pass

