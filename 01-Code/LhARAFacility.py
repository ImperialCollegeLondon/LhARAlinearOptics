#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class LhARAFacility:
====================

  Singleton class to set up the beam lines that define the LhARA facilit.


  Class attributes:
  -----------------
  __instance : Set on creation of first (and only) instance.
  __Debug    : Debug flag

      
  Instance attributes:
  --------------------
  
    
  Methods:
  --------
  Built-in methods __new__, __repr__ and __str__.
      __new__ : Creates single instance of LhARAFacility class.
      __repr__: One liner with call.
      __str__ : Dump of constants

  Set methods:
      setDebug  : Set debug flag

  Get/set methods:
      getDebug  : get debug flag

  Processing method:
      print()   : Dumps parameters
  
Created on Mon 12Jun23: Version history:
----------------------------------------
 1.0: 12Jun23: First implementation

@author: kennethlong
"""

import os
import pandas as pnds

import Particle    as Prtcl
import LhARASource as LhSrc

class LhARAFacility(object):
    __instance  = None
    __Debug     = False
    __LhSrcInst = None
    
#--------  "Built-in methods":
    def __new__(cls, _LhARAFacilitySpecificationCVSfile=None):
        if cls.__instance is None:
            if cls.__Debug:
                print(' LhARAFacility.__new__: ', \
                      'creating the LhARAFacility object')
            cls.__instance = super(LhARAFacility, cls).__new__(cls)

        #.. Only constants; print values that will be used:
        if cls.__Debug:
            print("     ----> Debug flag: ", cls.getDebug())

        #.. Check and load parameter file
        if _LhARAFacilitySpecificationCVSfile == None:
            raise Exception( \
                    " LhARAFacility.__new__: no parameter file given.")
        
        if not os.path.exists(_LhARAFacilitySpecificationCVSfile):
            raise Exception( \
                    " LhARAFacility.__new__: parameter file does not exist.")
        
        cls._LhARAFacilitySpecificationCVSfile = \
                               _LhARAFacilitySpecificationCVSfile
        cls._LhARAFacilityParamPandas = LhARAFacility.csv2pandas( \
                               _LhARAFacilitySpecificationCVSfile)
        if not isinstance(cls._LhARAFacilityParamPandas, pnds.DataFrame):
            raise Exception( \
                    " LhARAFacility.__new__: pandas data frame invalid.")
                                                                      
        if cls.__Debug:
            print("     ----> Parameter file: ", \
                  cls.getLhARAFacilitySpecificationCVSfile())
            print("     ----> Dump of pandas paramter list: \n", \
                  cls.getLhARAFacilityParamPandas())

#.. Build facility:
        if cls.__Debug:
            print("     ----> Build facility:")

#    ----> Source:
        if cls.__Debug:
            print("       ----> Source: ")

        pndsSource = cls._LhARAFacilityParamPandas[ \
                        cls._LhARAFacilityParamPandas["Section"] == "Source" \
                                                    ]
        SrcMode = int( \
                pndsSource[pndsSource["Name"]=="SourceMode"].loc[0]["Value"] \
                       )
        if cls.__Debug:
            print("         ----> Mode:", SrcMode)
            
        if SrcMode == 0:               #.. Laser driven:
            Emin  = \
             pndsSource[pndsSource["Name"]=="Emin"].iloc[0]["Value"]
            Emax = \
             pndsSource[pndsSource["Name"]=="Emax"].iloc[0]["Value"]
            nPnts = \
             int(pndsSource[pndsSource["Name"]=="nPnts"].iloc[0]["Value"])
            MinCTheta = \
             pndsSource[pndsSource["Name"]=="MinCTheta"].iloc[0]["Value"]
        elif SrcMode == 1:               #.. Gaussian:
            SigmaX  = \
             pndsSource[pndsSource["Name"]=="SigmaX"].iloc[0]["Value"]
            SigmaY  = \
             pndsSource[pndsSource["Name"]=="SigmaY"].iloc[0]["Value"]
            MeanE  = \
             pndsSource[pndsSource["Name"]=="MeanEnergy"].iloc[0]["Value"]
            SigmaE = \
             pndsSource[pndsSource["Name"]=="SigmaEnergy"].iloc[0]["Value"]
            MinCTheta = \
             pndsSource[pndsSource["Name"]=="MinCTheta"].iloc[0]["Value"]

        SigmaX  = \
            pndsSource[pndsSource["Name"]=="SigmaX"].iloc[0]["Value"]
        SigmaY  = \
            pndsSource[pndsSource["Name"]=="SigmaY"].iloc[0]["Value"]
        Drft1L = \
             pndsSource[pndsSource["Name"]=="Drift1Length"].iloc[0]["Value"]
        Drft1Z = Drft1L/2.
        Drft2L = \
             pndsSource[pndsSource["Name"]=="Drift2Length"].iloc[0]["Value"]
        Drft2Z = Drft1L + Drft1L/2.

        Aprtr1 = \
             pndsSource[pndsSource["Name"]=="Radius1"].iloc[0]["Value"]
        Aprtr2 = \
             pndsSource[pndsSource["Name"]=="Radius2"].iloc[0]["Value"]

        if cls.__Debug:
            print("             ----> SigmaX, SigmaY:", SigmaX, SigmaY)
            if SrcMode == 0:
                print("             ----> Emin, Emax, nPnts:", \
                      Emin, Emax, nPnts)
            elif SrcMode == 1:
                print("             ----> Mean and sigma:", MeanE, SigmaE)
            print("             ----> Min cos(Theta):", MinCTheta)
            print("             ----> Drift 1: length, centre:", \
                  Drft1L, Drft1Z)
            print("             ----> Drift 2: length, centre:", \
                  Drft2L, Drft2Z)
            print("             ----> Nozzle: inner radius at start and end", \
                  Aprtr1, Aprtr2)
            
        if SrcMode == 0:
            SrcParam = [SigmaX, SigmaY, MinCTheta, Emin, Emax, nPnts, \
                        Drft1L, Drft1Z, Aprtr1, \
                        Drft2L, Drft2Z, Aprtr2]
        elif SrcMode == 1:
            SrcParam = [SigmaX, SigmaY, MinCTheta, MeanE, SigmaE, \
                        Drft1L, Drft1Z, Aprtr1, \
                        Drft2L, Drft2Z, Aprtr2]

        cls.__LhSrcInst = LhSrc.LhARASource(SrcMode, SrcParam)
        print(cls.__LhSrcInst)
            
        return cls.__instance

    def __repr__(self):
        return "LhARAFacility()"

    def __str__(self):
        print(" LhARA facility set up as follows:")
        print(" =================================")
        print("     ----> Debug flag:", LhARAFacility.getDebug())
        return " <---- LhARA parameter dump complete."

    
#--------  I/o methods:
    def getLhARAFacilityParams(_filename):
        LhARAFacilityParams = pnds.read_csv(_filename)
        return LhARAFacilityParams
    

#--------  "Set method" only Debug
#.. Method believed to be self documenting(!)

    @classmethod
    def setDebug(cls, Debug=False):
        if cls.__Debug:
            print(" LhARAFacility.setdebug: ", Debug)
        cls.__Debug = Debug
        
    @classmethod
    def getLhARAFacilitySpecificationCVSfile(cls):
        return cls._LhARAFacilitySpecificationCVSfile

    @classmethod
    def getLhARAFacilityParamPandas(cls):
        return cls._LhARAFacilityParamPandas

    def csv2pandas(_filename):
        ParamsPandas = pnds.read_csv(_filename)
        return ParamsPandas
        
    @classmethod
    def getLhARASourceInstance(cls):
        return cls.__LhSrcInst

#--------  "Get methods" only; version, reference, and constants
#.. Methods believed to be self documenting(!)

    @classmethod
    def getDebug(cls):
        return cls.__Debug

#--------  Processing methods:
    @classmethod
    def trackLhARA(cls, NEvts=0):
        
        print(" trackLhARA for", NEvts, " events.")
        Scl  = 1
        iCnt = 1
        prt  = 0

        for iEvt in range(NEvts):
            if (iEvt % Scl) == 0:
                print("     ----> Generating event ", iEvt)
                prt   = 1
                iCnt += 1
                if iCnt == 10:
                    Scl  = Scl * 10
                    iCnt = 1
                
            #.. Create particle instance to store progression through
            #   beam line
            PrtclInst = Prtcl.Particle()
            if cls.__Debug:
                print("     ----> Created new Particle instance: \n", \
                      PrtclInst)
            
            #.. Generate initial particle:
            SrcPhsSpc = \
                cls.getLhARASourceInstance().getParticleFromSource()
            Success = PrtclInst.setSourcePhaseSpace(SrcPhsSpc)
            if cls.__Debug:
                print("     ----> Event", iEvt)
                print("         ----> Phase space at source:", SrcPhsSpc)
                print("         ----> Stored successfully:", Success)

        if prt == 1:
            prt = 0
            print("     <---- End of this event simulation")
