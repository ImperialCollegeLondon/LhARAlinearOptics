#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
To do:
------
23Jun23: Check if the "classmethods" really need to be class methods.

Class LhARASource:
==================

  Singleton class to initialise the source for LhARA.  Default is the
  laser-driven source.  Other source characteristics can be selected.


  Class attributes:
  -----------------
  __instance : Set on creation of first (and only) instance.
  __Debug    : Debug flag

  ModeList   : List of valid modes:
       [0] = 0 -- Parameterisation of laser-driven proton spectrum
       [1] = 1 -- Gaussian energy, flat angular (i.e. flat on unit sphere)
  ModeText   : Text avatar of valid modes:
       [0] = "Not coded" -- set for paramterisation of laser-driven source
       [1] = "Gaussian"
  ParamList  : List of lists.  Param[Mode][iParam] is "type" of parameter
               (e.g. float).
       [0] = [float, float]
       [1] = [float, float, float, float, float]
                 

  Instance attributes:
  --------------------
  _Mode  : Int, Mode
  _Param : List of parameters,
           Parameterised laser-driven source (Mode=0):
             [0] - Sigma of x gaussian - m
             [1] - Sigma of y gaussian - m
             [2] - Minimum cos theta to generate
             [3] - E_min: min energy to generate
             [4] - E_max: max energy to generate
             [5] - N_stp: number of steps for numerical integration
           Gaussian (Mode=1):
             [0] - Sigma of x gaussian - m
             [1] - Sigma of y gaussian - m
             [2] - Minimum cos theta to generate
             [3] - Kinetic energy - MeV
             [4] - Sigma of gaussian - MeV
           Drifts:
        [nSrc+1] - Length   of  first drift - m
        [nSrc+2] - z centre of  first drift - m
        [nSrc+3] - First aperture radius    - m
        [nSrc+4] - Length   of second drift - m
        [nSrc+5] - z centre of second drift - m
        [nSrc+6] - Second aperture radius   - m

  
    
  Methods:
  --------
  Built-in methods __new__, __repr__ and __str__.
      __new__ : Creates single instance of LhARASource class.
      __repr__: One liner with call.
      __str__ : Dump of constants

  Set methods:
      setDebug      : Set debug flag
      __setAll2None : Set all instance attributes to None
      __setMode     : Set Mode
      __setModetext : Set Mode text
      __setParam    : Set parameters

  Get/set methods:
      getDebug    : get debug flag
      getMode     : Set Mode
      getModetext : Set Mode text
      getParam    : Set parameters

  Processing method:
      cleanInstance : Delete singular instance and clear __instance
          CheckMode : Check mode is valid
                  Input: Mode
                Returns: Bool, true/false
         CheckParam : Check paramters are of correct type
                  Input: Param[ ... ]
                Returns: Bool, true/false

        getParticle : Generate particle from source, using Mode and Params
                Returns: KE, cosTheta, Phi
    getFlatThetaPhi : Generate Theta, phi flat on surface of sphere.

  
Created on Mon 19Jun23: Version history:
----------------------------------------
 1.0: 19Jun23: First implementation

@author: kennethlong
"""

import math   as mth
import random as rnd
import numpy  as np

import BeamLineElement as BLE
import LhARAFacility as LhFclty

class LhARASource(object):
    __instance = None
    __Debug    = False

    LsrDrvnIni = False
    LsrDrvnG_E = None
    
    ModeList   = [0, 1]
    ModeText   = ["Parameterised laser driven", "Gaussian"]
    ParamList  = [ [float, float, float, float, float, int, \
                    float, float, float, \
                    float, float, float],
                   [float, float, float, float, float, \
                    float, float, float, \
                    float, float, float] ]


#--------  "Built-in methods":
    def __new__(cls, _Mode=None, _Param=None):
        if cls.__instance is None:
            if cls.__Debug:
                print(' LhARASource.__new__: ', \
                      'creating the LhARASource object')
            cls.__instance = super(LhARASource, cls).__new__(cls)

            cls.__setAll2None()

            #.. Set default parameters (to parameterisatio of laser driven)
            #   if none set:
            if _Mode == None and _Param==None:
                _Mode  = 0
                _Param = [0.000004, 0.000004, 0.998,    \
                          1., 25., 1000,                \
                          2.5E-2, 5.E-2, 2.5E-2, 5.E-2]
            
            if _Mode == None or _Param==None:
                print(" LhARASource.__init__: bad source paramters:", \
                      _Mode, _Param)
                raise badSourceSpecification( \
                    " LhARASource.__init__: bad source paramters. Exit", \
                                                 )
            nSrc = 5
            if _Mode == 1:
                nSrc = 4
            
            ValidSourceParam = BLE.Source.CheckSourceParam( \
                                            _Mode, _Param[:(nSrc+1)])
            if not ValidSourceParam:
                print(" LhARASource.__init__: bad source input; :", \
                      "_Mode, _Param:", _Mode, _Param)
                raise badSourceSpecification( \
                    " LhARASource.__init__: bad source paramters. Exit")
            
            cls.__setMode(_Mode)
            cls.__setModeText(cls.ModeText[_Mode])
            cls.__setParam(_Param)

            #.. Implement source:
            rCtr  = np.array([0.,0.,0.])
            vCtr  = np.array([0.,0.])
            drCtr = np.array([0.,0.,0.])
            dvCtr = np.array([0.,0.])
            cls._Source = BLE.Source("Source", \
                                     rCtr, vCtr, drCtr, dvCtr, \
                                     _Mode, _Param[:(nSrc+1)])

            if cls.getDebug():
                print(" Start setting drifts etc. nSrc:", nSrc)
                
            #.. Implement drifts:
            #        ----> First drift:
            vCtr = np.array([0.,0.])
            drCtr = np.array([0.,0.,0.])
            dvCtr = np.array([0.,0.])
            rCtr  = np.array([0.,0.,_Param[nSrc+2]])
            cls._Drift1 = BLE.Drift("Drift1", \
                                    rCtr, vCtr, drCtr, dvCtr, _Param[nSrc+1])

            #        ----> First aperture:
            rCtr = np.array([0.,0.,(_Param[nSrc+2]+_Param[nSrc+1]/2.)])
            AprtrParam = [0, _Param[nSrc+3]]
            cls._Aperture1 = BLE.Aperture("Aperture1", \
                                          rCtr, vCtr, drCtr, dvCtr, \
                                          AprtrParam)

            #        ----> Second drift:
            rCtr = np.array([0.,0.,_Param[nSrc+5]])
            cls._Drift2 = BLE.Drift("Drift2", \
                                    rCtr, vCtr, drCtr, dvCtr, _Param[nSrc+4])
                                          
            #        ----> Second aperture:
            rCtr = np.array([0.,0.,(_Param[nSrc+5]+_Param[nSrc+4]/2.)])
            AprtrParam = [0, _Param[nSrc+6]]
            cls._Aperture2 = BLE.Aperture("Aperture2", \
                                          rCtr, vCtr, drCtr, dvCtr, \
                                          AprtrParam)

            #.. Only constants; print values that will be used:
            if cls.__Debug:
                print("     ----> Debug flag: ", cls.getDebug())
                print("     ----> Mode      : ", cls.getMode(), \
                      "; ", cls.getModeText())
                print("     ----> Param     : ", cls.getParam())
                print("     ----> Drifts 1 and 2:")
                print(cls._Drift1)
                print(cls._Aperture1)
                print(cls._Drift2)
                print(cls._Aperture2)
        else:
            if cls.__Debug:
                print(' LhARASource.__new__: ', \
                      'attempt to create second instance.  Skipped!')
            
        if cls.__Debug:
            print(' <---- LhARASource.__new__, done. --------', \
                  '  --------  --------  --------  --------  --------')

        return cls.__instance

    def __repr__(self):
        return "LhARASource()"

    def __str__(self):
        print(" LhARA source set up as follows:")
        print(" ===============================")
        print("     ----> Debug flag:", LhARASource.getDebug())
        print("     ----> Mode      :", LhARASource.getMode(), \
              "; ", LhARASource.getModeText())
        print("     ----> Param     :", LhARASource.getParam())
        return " <---- LhARA source parameter dump complete."

    
#--------  "Set methods":
#.. Method believed to be self documenting(!)

    @classmethod
    def setDebug(cls, Debug=False):
        if cls.__Debug or Debug:
            print(" LhARASource.setdebug: ", Debug)
        cls.__Debug = Debug

    @classmethod
    def __setAll2None(self):
        self._Mode     = None
        self._ModeText = None
        self._Param    = None
        
    @classmethod
    def __setMode(cls, _Mode):
        cls._Mode = _Mode

    @classmethod
    def __setModeText(cls, _ModeText):
        cls._ModeText = _ModeText

    @classmethod
    def __setParam(cls, _Param):
        cls._Param = _Param


#--------  "Get methods" only; version, reference, and constants
#.. Methods believed to be self documenting(!)

    @classmethod
    def getDebug(cls):
        return cls.__Debug

    @classmethod
    def getMode(cls):
        return cls._Mode

    @classmethod
    def getModeText(cls):
        return cls._ModeText

    @classmethod
    def getParam(cls):
        return cls._Param

    @classmethod
    def getSource(cls):
        return cls._Source

    @classmethod
    def getDrift1(cls):
        return cls._Drift1

    @classmethod
    def getDrift2(cls):
        return cls._Drift2

    @classmethod
    def getAperture1(cls):
        return cls._Aperture1

    @classmethod
    def getAperture2(cls):
        return cls._Aperture2


#--------  Utilities:
    @classmethod
    def cleanInstance(cls):
        del cls.__instance
        cls.__instance = None
        if cls.__Debug:
            print(' LhARASource.cleanInstance: instance removed.')


#--------  Processing methods:
    def getParticleFromSource(self):
        if self.__Debug:
            print(" LhARASource.getParticleFromSource: start")

        #.. Generate initial particle:
        GotOne = False
        nTrys  = 0
        while not GotOne:
            nTrys += 1
            
            #.. Get particle:
            TrcSpc = self.getSource().getParticleFromSource()
            if self.__Debug:
                print("     ----> Trace space at source:", TrcSpc)

            #.. Apply drift 1:
            TrcSpc1 = self.getDrift1().Transport(TrcSpc)
            if self.__Debug:
                print("     ----> Trace space after drift 1:", TrcSpc1)

            #.. Apply apperture 1:
            TrcSpc2 = self.getAperture1().Transport(TrcSpc1)
            if self.__Debug:
                print("     ----> Trace space after aperture 1:", TrcSpc2)
            if not isinstance(TrcSpc2, np.ndarray):
                if self.__Debug:
                    print("     ----> Failed to pass aperture 1.")
                continue
                
            #.. Apply drift 1:
            TrcSpc3 = self.getDrift2().Transport(TrcSpc2)
            if self.__Debug:
                print("     ----> Trace space after drift 2:", TrcSpc3)

            #.. Apply apperture 2:
            TrcSpc4 = self.getAperture2().Transport(TrcSpc3)
            if self.__Debug:
                print("     ----> Trace space after aperture 2:", TrcSpc4)
            if not isinstance(TrcSpc4, np.ndarray):
                if self.__Debug:
                    print("     ----> Failed to pass aperture 2.")
                continue
                
            GotOne = True
            if self.__Debug:
                print("     <---- Finally got one after", nTrys, " trys.")
                
        if self.__Debug:
            print(" <---- LhARASource.getParticleFromSource, done.  --------", \
                  '  --------  --------  --------  --------  --------')

        return TrcSpc4


#--------  Exceptions:
class badSourceSpecification(Exception):
    pass

class badParameters(Exception):
    pass
