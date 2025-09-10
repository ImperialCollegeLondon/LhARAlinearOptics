#!/Usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Class BeamLine:
===============

  Singleton class to set up the beam line defined in the beam-line
  specification file.


  Class attributes:
  -----------------
   __Debug    : Debug flag
__BeamLineInst: Instance of BeamLine class.  Set on creation of first
                (and only) instance.

      
  Instance attributes:
  --------------------
    _Element[] : BeamLineElement : List of beam line elements making up the
                                   beam line.
   _BeamLineSpecificationCSVfile : Path to csv file in which beam line is
                                   specified.
            _BeamLineParamPandas : Pandas data frame instance containing
                                   parameters.
                      _SrcTrcSpc : 6D trace space at source (np.ndarray)
    
  Methods:
  --------
  Built-in methods __new__, __repr__ and __str__.
      __new__ : Creates single instance of BeamLine class.
      __repr__: One liner with call.
      __str__ : Dump of constants

  Set methods:
      setDebug  : Set debug flag

    setSrcTrcSpc: Set trace space at source.
             Input: np.array([6,]) containing 6D trace space vector.

  Get methods:
     getinstance: Get instance of beam class
      getDebug  : get debug flag
getBeamLineSpecificationCSVfile:
                  Get the path to the csv file specifying the beam line
getBeamLineParamPandas:
                  Get pandas instance specifying the beam line
      getElement: get list of instances of BeamLineElement objects that make
                  up the beam line
    getSrcTrcSpc: get source trace space nd.array(6,)

  Processing method:
      print()   : Dumps parameters
  
  I/o methods:
 getBeamLineParams: Creates pandas instance with values stored in
                    parameters stored in cvs file
              Input: fileneam: path to pandas file
             Return: Pandas instance

  Processing methods:
        csv2pandas: convert csv file to pandas data frame
               Input: filename, path: Path to complete pandas data frame
              Return: Pandas dataframe instance

           addSource: Parse source parameters from pandas dataframe
                    containing specification of the beam line
                Input: pandas source instance
               Return:
           Source mode, int: Mode for source generation as defined in
                             BeamLineElement.Source
               Source param: list, [x,]: list of parameters that specify
                             source as defined in BeamLineElement.Source

          addBeamline: Parse parameters from pandas dataframe
                       containing specification of the beam line
                Input: pandas source instance

   checkConsistency: Runs through beam line elements to make sure total
                     length is consistent with sum of element lengths and
                     position of final element
                Input: None
               Return: True/False: consistent/not consistent

          trackBeam: Tracks through the beam line.

  I/o methods:
To be added ...

Created on Mon 02Oct23: Version history:
----------------------------------------
 2.1: 08Apr25: Include electron temperature update from Sadur and Zakhir.
               Also, slim down input arguments required for laser-driven
               source.
 2.0: 11Dec23: Refactor to make code generate beamline based on input
               specificaiton file and not tie it to or another
               hard-coded facility.
 1.0: 02Oct23: First implementation

@author: rehanahrazak
"""

import sys

import os
import io
import math   as mth
import numpy  as np
import scipy  as sp
import pandas as pnds
import struct as strct

import PhysicalConstants as PhysCnsts
import Particle          as Prtcl
import BeamLine          as BL
import BeamLineElement   as BLE
import Simulation        as Smltn

#-------- Physical Constants Instances and Methods ----------------
from PhysicalConstants import PhysicalConstants

constants_instance = PhysicalConstants()

electronMASS       = constants_instance.me()
SIelectronMASS     = constants_instance.meSI()
protonMASS         = constants_instance.mp()
speed_of_light     = constants_instance.SoL()

mu0                = constants_instance.mu0()
eps0               = constants_instance.epsilon0()
electricCHRG       = constants_instance.electricCHARGE()

class BeamLine(object):
    __BeamLineInst = None
    __Debug        = False
    _SrcTrcSpc     = None

    _currentReferenceParticle = None


#--------  "Built-in methods":
    def __new__(cls, _BeamLineSpecificationCSVfile=None, readDataFile=False):
        if cls.getinstances() == None:
            cls.setAll2None()
                                                                      
            if cls.getDebug():
                print(' BeamLine.__new__: ', \
                      'creating the BeamLine object')
            cls.__BeamLineInst = super(BeamLine, cls).__new__(cls)

            #.. Only constants; print values that will be used:
            if cls.getDebug():
                print("     ----> Debug flag: ", cls.getDebug())

            if cls.getDebug():
                print("     ----> readDataFile = ", readDataFile)
            if readDataFile:
                if cls.getDebug():
                    print(" <---- return after init.")
                return cls.getinstances()
              
            #.. Check and load parameter file
            if _BeamLineSpecificationCSVfile == None:
                raise Exception( \
                            " BeamLine.__new__: no parameter file given.")
        
            if not os.path.exists(_BeamLineSpecificationCSVfile):
                print(" BeamLine.__New__: _BeamLineSpecificationCSVfile:", \
                      _BeamLineSpecificationCSVfile)
                raise Exception( \
                    " BeamLine.__new__: parameter file does not exist.")
        
            cls._BeamLineSpecificationCSVfile = \
                               _BeamLineSpecificationCSVfile
            cls._BeamLineParamPandas = BeamLine.csv2pandas( \
                               _BeamLineSpecificationCSVfile)
            if not isinstance(cls._BeamLineParamPandas, pnds.DataFrame):
                raise Exception( \
                    " BeamLine.__new__: pandas data frame invalid.")

            if cls.getDebug():
                print("     ----> Parameter file: ", \
                      cls.getBeamLineSpecificationCSVfile())
                print("     ----> Dump of pandas paramter list: \n", \
                      cls.getBeamLineParamPandas())

#.. Build facility:
            if cls.getDebug():
                print("     ----> Build facility:")

#    ----> Facility:  --------  --------  --------  --------
            if cls.getDebug():
                print("         ----> Facility: ")

            cls.addFacility()
        
            if cls.getDebug():
                print("         <---- Facility done.")
#    <---- Done facility  --------  --------  --------  --------

#    ----> Create reference particle:  --------  --------  --------  --------
#..  Instance only at this stage:
            if cls.getDebug():
                print("        ----> Create reference particle instance: ")
            
            refPrtcl  = Prtcl.ReferenceParticle.createReferenceParticles()[0]
            cls.setcurrentReferenceParticle(refPrtcl)
            
            if cls.getDebug():
                print("        <---- Reference particle created. ")
#    <---- Done reference particle  --------  --------  --------  --------

#    ----> Source:  --------  --------  --------  --------
            if cls.getDebug():
                print("         ----> Source: ")

            cls.addSource()
        
            if cls.getDebug():
                print("        <---- Source done.")
#    <---- Done source  --------  --------  --------  --------

#    ----> Beam line:  --------  --------  --------  --------
            if cls.getDebug():
                print("        ----> Beam line: ")

            cls.addBeamline()
        
            if cls.getDebug():
                print("        <---- Beam line done.")
#    <---- Done beam line  --------  --------  --------  --------

#    ----> Reference particle:  --------  --------  --------  --------
            if cls.getDebug():
                print("        ----> Reference particle: ")
            
            if cls.getDebug():
                print("            ----> Reference particle set, success:")
                print("        <---- Reference particle done. ")
#    <---- Done reference particle -----  --------  --------  --------

        else:
            if cls.getDebug():
                print(' BeamLine.__new__: ', \
                      'existing BeamLine object will be used')

        return cls.getinstances()

    def __repr__(self):
        return "BeamLine()"

    def __str__(self):
        print(" Beam line set up as follows:")
        print(" ============================")
        print("     ----> Debug flag:", BeamLine.getDebug())
        print("     ----> Source and beam line:")
        Section = ""
        iCnt = -1
        for iBLE in BLE.BeamLineElement.getinstances():
            iCnt += 1
            NameStrs = iBLE.getName().split(":")
            if len(NameStrs) == 1:
                Section = NameStrs[0]
                print("        ---->", NameStrs[0])
            elif NameStrs[2] != Section:
                Section = NameStrs[2]
                print("        ---->", NameStrs[2])
            print("            ---->", iCnt, ":", iBLE.SummaryStr())        
        print("     ----> Beam line is self consistent = ", \
              self.checkConsistency())
        return " <---- Beam line parameter dump complete."
                
    
#--------  "Set methods"
#.. Method believed to be self documenting(!)
    @classmethod
    def setAll2None(cls):
        cls._Element                       = []
        cls.__BeamLineSpecificationCSVfile = None
        cls._BeamLineParamPandas           = None
        cls._SrcTrcSpc                     = []

    @classmethod
    def setDebug(cls, Debug=False):
        if Debug or cls.getDebug():
            print(" BeamLine.setdebug: ", Debug)
        cls.__Debug = Debug

    @classmethod
    def setcurrentReferenceParticle(cls, _currentRefPrtcl):
        if not isinstance(_currentRefPrtcl, Prtcl.ReferenceParticle):
            raise badParameter()
        cls._currentReferenceParticle = _currentRefPrtcl
        
    @classmethod
    def setSrcTrcSpc(cls, SrcTrcSpc=np.array([])):
        if cls.getDebug():
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print(" BeamLine.setSrcTrcSpc: ", SrcTrcSpc)
        
        if not isinstance(SrcTrcSpc, np.ndarray):
            raise badTraceSpaceVector( \
                        " BeamLine.setSrcTrcSpc:", SrcTrcSpc)

        if len(SrcTrcSpc) == 0:
            SrcTrcSpc = None
        elif not SrcTrcSpc.size == 6:
            raise badTraceSpaceVector( \
                        " BeamLine.setSrcTrcSpc:", SrcTrcSpc)

        cls._SrcTrcSpc = SrcTrcSpc
        
#--------  "Get methods"
#.. Method believed to be self documenting(!)
    @classmethod
    def getinstances(cls):
        return cls.__BeamLineInst

    @classmethod
    def getDebug(cls):
        return cls.__Debug

    @classmethod
    def getcurrentReferenceParticle(cls):
        return cls._currentReferenceParticle

    @classmethod
    def getBeamLineSpecificationCSVfile(cls):
        return cls._BeamLineSpecificationCSVfile

    @classmethod
    def getBeamLineParamPandas(cls):
        return cls._BeamLineParamPandas

    @classmethod
    def getElement(cls):
        return cls._Element
    
    @classmethod
    def getSrcTrcSpc(cls):
        return cls._SrcTrcSpc
    
        
#--------  Processing methods:
    @classmethod
    def addFacility(cls):
        if cls.getDebug():
            print("             ----> BeamLine.addFacility starts:")

        #.. Parse the dataframe to get Facility parameters:
        Name, K0, species0, VCMVr = cls.parseFacility()

        #.. Create the Facility beam line element:
        rStrt = np.array([0.,0.,0.])
        vStrt = np.array([[np.pi/2.,np.pi/2.],[0.,0.]])
        drStrt = np.array([0.,0.,0.])
        dvStrt = np.array([0.,0.,0.])

        p0 = []
        for id in range(len(species0)):
            mass   = PhysCnsts.PhysicalConstants().getparticleMASS(  \
                                                        species0[id] \
                                                                   )
            p0.append(mth.sqrt( (mass+K0[id])**2 - mass**2))

        FacilityBLE = BLE.Facility(Name, rStrt, vStrt, drStrt, dvStrt, \
                                   p0, VCMVr, species0)
        cls.addBeamLineElement(FacilityBLE)

        if cls.getDebug():
            print("             <----", Name, \
                  "facility initialised.")
            
    @classmethod
    def addSource(cls):
        if cls.getDebug():
            print("             BeamLine.addSource starts:")
            
        #.. Parse the dataframe to get source parameters:
        Name, SrcMode, SrcParam = cls.parseSource()
        if Name == None and SrcMode == None:
            return

        #.. Create the source beam line element:
        rStrt = np.array([0.,0.,0.])
        vStrt = np.array([[np.pi/2.,np.pi/2.],[0.,0.]])
        drStrt = np.array([0.,0.,0.])
        dvStrt = np.array([0.,0.,0.])
        SourceBLE = BLE.Source(Name, rStrt, vStrt, drStrt, dvStrt, \
                               SrcMode, SrcParam)

        cls.addBeamLineElement(SourceBLE)

        refPrtcl    = Prtcl.ReferenceParticle.getinstances()[0]
        refPrtclSet = refPrtcl.setReferenceParticleAtSource()

        if cls.getDebug():
            print("                 ---->", Name, \
                  "beam line element created.")
            print("                     ----> reference particle:")
            print("                         Position:", \
                  refPrtcl.getRrIn()[0])
            print("                         Momentum:", \
                  refPrtcl.getPrIn()[0])
            print(SourceBLE)
            print("                 <---- Done.")

    @classmethod
    def parseFacility(cls):
        Name  = None

        K0       = []
        p0       = []
        species0 = []
        if cls.getDebug():
            print("                 ----> BeamLine.parseFacility starts:")
            
        #.. Get "sub" pandas data frame with facility parameters only:
        pndsFacility = cls.getBeamLineParamPandas()[ \
                  (cls.getBeamLineParamPandas()["Section"] == "Facility") & \
                  (cls.getBeamLineParamPandas()["Element"] == "Global") \
                                                  ]
        Name = str(pndsFacility[ \
                        (pndsFacility["Type"]=="Name") & \
                        (pndsFacility["Parameter"]=="Name") ]. \
                            iloc[0]["Value"] \
                    )
        VCMVr = float(pndsFacility[ \
                    (pndsFacility["Type"]=="Vacuum chamber") & \
                    (pndsFacility["Parameter"]=="Mother volume radius") ]. \
                    iloc[0]["Value"] \
                    )

        K0.append(float(pndsFacility[ \
                        (pndsFacility["Type"]=="Reference particle") &   \
                        (pndsFacility["Parameter"]=="Kinetic energy") ]. \
                        iloc[0]["Value"]) \
                  )
        species0list = pndsFacility[ \
                        (pndsFacility["Type"]=="Reference particle") & \
                        (pndsFacility["Parameter"]=="Species") ]
        if len(species0list) == 0:
            species0.append("proton")
        else:
            species0.append(pndsFacility[ \
                        (pndsFacility["Type"]=="Reference particle") & \
                        (pndsFacility["Parameter"]=="Species") ]. \
                        iloc[0]["Value"] \
                            )
                  
        K0list = pndsFacility[ \
                        (pndsFacility["Type"]=="Reference particle") & \
                        (pndsFacility["Parameter"]=="Kinetic energy 1") ]
        species0list = pndsFacility[ \
                        (pndsFacility["Type"]=="Reference particle") & \
                        (pndsFacility["Parameter"]=="Species 1") ]

        for id in range(1, len(K0list)):
            print(" id", id)
            K0.append(float(pndsFacility[ \
                        (pndsFacility["Type"]=="Reference particle") & \
                        (pndsFacility["Parameter"]=="Kinetic energy 1") ]. \
                            iloc[id]["Value"] \
                            ) \
                      )
            species0.append(str(pndsFacility[ \
                        (pndsFacility["Type"]=="Reference particle") & \
                        (pndsFacility["Parameter"]=="Species 1") ]. \
                            iloc[id]["Value"] \
                            ) \
                                )

        if cls.getDebug():
            print("                     ----> Name:", Name, \
                  "; reference particle kinetic energy(ies):", K0, "MeV")
            print("                     ----> Name:", Name, \
                  "; reference particle species:", species0)
            print( \
        "                     ----> Vacuum chamber mother volume radius:", \
                   VCMVr, "m")
            print("                 <---- Done.")
            
        return Name, K0, species0, VCMVr

    @classmethod
    def parseSource(cls):
        SrcMode  = None
        SrcParam = None
        SigmaX   = None
        SigmaY   = None
        if cls.getDebug():
            print(" BeamLine.parseSource starts:")

        #.. Get "sub" pandas data frame with source parameters only:
        pndsSource = cls.getBeamLineParamPandas()[ \
                     cls.getBeamLineParamPandas()["Section"] == "Source" \
                                                  ]

        if pndsSource.empty:
            if cls.getDebug():
                print(" Beamline.parseSource: empty source, return.")
            return None, None, None

        SrcMode = int( \
           pndsSource[pndsSource["Parameter"] == \
                      "SourceMode"]["Value"].iloc[0] \
                       )
        if cls.getDebug():
            print("     ----> Mode:", SrcMode)
            
        if SrcMode == 0:               #.. Laser driven:
            #.. Scan and report legacy parameters:
            cleanedSource = BLE.Source.scanLEGACY(pndsSource)

            
            #.. Set defaults:
            wavelength, power, strhlRATIO, r0, Duration, Te, Kmin, Kmax, \
                Thickness, DivAngle, SigmaThetaS0, SlopeThetaS, rpmax = \
                    BLE.Source.setDEFAULTparams()

            #.. Wavelength:
            val = BLE.Source.parseSINGLEparam(cleanedSource, "Wavelength", \
                                                           wavelength    )
            if val != None: wavelength = val/1000000.
            
            #.. Power
            val = BLE.Source.parseSINGLEparam(cleanedSource, "Power", \
                                                           power    )
            if val != None: power = val

            #.. Strehl ratio
            val = BLE.Source.parseSINGLEparam(cleanedSource, \
                                              "Strehl ratio", \
                                                           strhlRATIO    )
            if val != None: strhlRATIO = val

            #.. Laser spot radius
            val = BLE.Source.parseSINGLEparam(cleanedSource, "r0", \
                                                           r0    )
            if val != None: r0 = val
            
            #.. Laser pulse length
            val = BLE.Source.parseSINGLEparam(cleanedSource, "Duration", \
                                                           Duration    )
            if val != None: Duration = val
            
            #.. Hot electron temperature:
            Te  = -99.
            val = BLE.Source.parseSINGLEparam(cleanedSource, "Te", \
                                                           Te    )
            if val != None:
                if val == -99.:
                    Te = None

                    print("     ---->", \
                          "Hot electron temperature is not defined;", \
                          "it will be calculated.")

                    Te = BLE.Source.calculateTe(wavelength, r0, \
                                                power, strhlRATIO)
                    
                    if cls.getDebug():
                        print("         ----> Te:", Te)
                else:
                    Te = val
            
            #.. Kmin:
            val = BLE.Source.parseSINGLEparam(cleanedSource, "Kmin", \
                                                           Kmin    )
            if val != None: Kmin = val
            
            #.. Kmax:
            val = BLE.Source.parseSINGLEparam(cleanedSource, "Kmax", \
                                                           Kmax    )
            if val != None: Kmax = val
            
            #.. Target thickness and electron divergence angle:
            val = BLE.Source.parseSINGLEparam(cleanedSource, \
                                              "Thickness", \
                                               Thickness    )
            if val != None: Thickness = val
            val = BLE.Source.parseSINGLEparam(cleanedSource, \
                                              "DivAngle", \
                                               DivAngle    )
            if val != None: DivAngle = val
            
            if Kmax == None:
                #.. Calculate t0:
                t0, Kinfnty = BLE.Source.calculatet0(power, strhlRATIO, r0, \
                                                     Thickness, DivAngle)

                # Solve for "X" to get Kmax:
                initial_guess = 0.5
                solution = sp.optimize.fsolve( \
                                BLE.Source.DurationBYt0equation, \
                                    initial_guess, args=(Duration, t0) )

                if cls.getDebug():
                    print("     ----> initial_guess, solution:", \
                          initial_guess, solution)

                X     = float(solution[0])
                KmaxJ = Kinfnty*(X**2)
                Kmax  = KmaxJ / (electricCHRG * 1.E6)

                if cls.getDebug():
                    print("     ----> X, Kmax, KmaxJ:", X, Kmax, KmaxJ)
            
            #.. Parameters determining angular distribution:
            val = BLE.Source.parseSINGLEparam(cleanedSource, \
                                              "SigmaThetaS0", \
                                               SigmaThetaS0    )
            if val != None: SigmaThetaS0 = val
            
            val = BLE.Source.parseSINGLEparam(cleanedSource, \
                                              "SlopeThetaS", \
                                               SlopeThetaS    )
            if val != None: SlopeThetaS = val
            
            val = BLE.Source.parseSINGLEparam(cleanedSource, \
                                              "rpmax", rpmax)
            if val != None: rpmax = val
            
        elif SrcMode == 1:               #.. Gaussian:
            MeanE  = float( \
             pndsSource[pndsSource["Parameter"]=="MeanEnergy"] \
                            ["Value"].iloc[0])
            SigmaE = float( \
             pndsSource[pndsSource["Parameter"]== \
                        "SigmaEnergy"]["Value"].iloc[0])
            MinCTheta = float(\
             pndsSource[pndsSource["Parameter"]=="MinCTheta"] \
                              ["Value"].iloc[0])
        elif SrcMode == 2:               #.. Flat
            Kmin  = float( \
             pndsSource[pndsSource["Parameter"]=="Kmin"]["Value"].iloc[0])
            Emax = float( \
             pndsSource[pndsSource["Parameter"]=="Emax"]["Value"].iloc[0])
            MinCTheta = float( \
             pndsSource[pndsSource["Parameter"]=="MinCTheta"] \
                               ["Value"].iloc[0])
        elif SrcMode == 4:               #.. Uniform disc
            MeanE  = float( \
             pndsSource[pndsSource["Parameter"]=="MeanEnergy"] \
                            ["Value"].iloc[0])
            SigmaE = float( \
             pndsSource[pndsSource["Parameter"]== \
                        "SigmaEnergy"]["Value"].iloc[0])
            MaxRadius = float( \
             pndsSource[pndsSource["Parameter"]=="Radius"]["Value"].iloc[0])
        elif SrcMode == 3:               #.. Read from file
            pass

        if SrcMode != 0 and SrcMode != 3 and SrcMode !=4:
            SigmaX  = float( \
                pndsSource[pndsSource["Parameter"]=="SigmaX"] \
                             ["Value"].iloc[0])
            SigmaY  = float( \
                pndsSource[pndsSource["Parameter"]=="SigmaY"] \
                             ["Value"].iloc[0])
        
        if cls.getDebug():
            if SrcMode != 0 and SrcMode != 3 and SrcMode !=4:
                print("     ----> SigmaX, SigmaY:", \
                      SigmaX, SigmaY)
            if SrcMode == 0:
                print("     ----> wavelength, power, strhlRATIO, r0, Te,", \
                      "Kmin, Kmax, Thickness, DivAngle:", \
                      wavelength, power, strhlRATIO, r0, Duration, Te, \
                      Kmin, Kmax, Thickness, DivAngle)
                print("           SigmaThetaS0, SlopeThetaS, rpmax:", \
                      SigmaThetaS0, SlopeThetaS, rpmax)
            elif SrcMode == 1 or SrcMode == 4:
                print("                         ----> Mean and sigma:", \
                      MeanE, SigmaE)
            elif SrcMode == 2:
                print("                         ----> MinE and MaxE:", \
                      MinE, MaxE)

        if SrcMode == 0:
            SrcParam = [wavelength, power, strhlRATIO, r0, Duration, Te, \
                        Kmin, Kmax, SigmaThetaS0, SlopeThetaS, rpmax]

        elif SrcMode == 1:
            SrcParam = [SigmaX, SigmaY, MinCTheta, MeanE, SigmaE]

        elif SrcMode == 2:
            SrcParam = [SigmaX, SigmaY, MinCTheta, Kmin, Emax]
        elif SrcMode == 4:
            SrcParam = [MeanE, SigmaE, MaxRadius]

        elif SrcMode == 3:
            SrcParam = []

        Name = BLE.BeamLineElement.getinstances()[0].getName() + ":" \
                       + str(pndsSource["Stage"].iloc[0]) + ":" \
                       + pndsSource["Section"].iloc[0]    + ":" \
                       + pndsSource["Element"].iloc[0]

        if cls.getDebug():
            print(" <---- Name, SrcMode, SrcParam:", \
                  Name, SrcMode, SrcParam)
            
        return Name, SrcMode, SrcParam

    @classmethod
    def addBeamline(cls):
        if cls.getDebug():
            print("            BeamLine.addBeamline starts:")
            
        #.. Get "sub" pandas data frame with beamline parameters only:
        pndsBeamline = cls.getBeamLineParamPandas()[ \
                    (cls.getBeamLineParamPandas()["Section"] != "Source") & \
                    (cls.getBeamLineParamPandas()["Section"] != "Facility") \
                                                  ]

        if pndsBeamline.empty:
            if cls.getDebug():
                print(" BeamLine.addBeamline: empty beam line, return.")
            return
            
        Section    = ""
        NewElement = True
        s         = 0.

        iRefPrtcl = Prtcl.ReferenceParticle.getinstances()[0]
        if not isinstance(iRefPrtcl, Prtcl.ReferenceParticle):
            raise ReferenceParticleNotSpecified()
        p0        = mth.sqrt(np.dot(iRefPrtcl.getPrIn()[0][:3], \
                                    iRefPrtcl.getPrIn()[0][:3]))

        iBLE  = None
        nShft = 0
        nTlt  = 0
        for iLine in pndsBeamline.itertuples():
            Name = BLE.BeamLineElement.getinstances()[0].getName() + ":" \
                           + str(iLine.Stage) + ":"  \
                           + iLine.Section    + ":" \
                           + iLine.Element    + ":"

            iLst  = BLE.BeamLineElement.getinstances()[ \
                            len(BLE.BeamLineElement.getinstances()) - 1 \
                                                        ]
            if cls.getDebug():
                print("     ----> Name, iLst.Name:", \
                      Name, iLst.getName())

            elementKEY = iLine.Element

            if cls.getDebug():
                if iBLE != None: print("     ----> Just before Shift/Tilt", \
                                       "handling:", \
                                   iBLE.getName(),
                                   iLine.Type, Name, Name0)
            if iBLE != None:
                if cls.getDebug():
                    print("         ----> Name0, Name:", Name0, Name)
                if Name0 == Name and isinstance(iLine.Type, str):
                    if cls.getDebug():
                        print("             ---->", \
                              iLine.Type.lower())
                    if "shift" in iLine.Type.lower() or \
                       "tilt"  in iLine.Type.lower():
                        if cls.getDebug():
                            print("                 ---->", \
                                  iLine.Parameter)
                        if iLine.Parameter == "dx":
                            nShft += 1
                            iBLE.getdrStrt()[0] = float(iLine.Value)
                            if cls.getDebug():
                                print("                ----> Shift",
                                      Name, ", nShft =", nShft, \
                                      ": dr =", iBLE.getdrStrt())
                            continue
                        elif iLine.Parameter == "dy":
                            nShft += 1
                            iBLE.getdrStrt()[1] = float(iLine.Value)
                            if cls.getDebug():
                                print("                 <---- Shift",
                                      Name, ", nShft =", nShft, \
                                      ": dr =", iBLE.getdrStrt())
                            continue
                        elif "tilt"  in iLine.Type.lower():
                            if iLine.Parameter == "alphaE":
                                nTlt += 1
                                iBLE.getdvStrt()[0] = float(iLine.Value)
                                if cls.getDebug():
                                    print("                ----> Tilt",
                                          Name, ", nTlt =", nTlt, \
                                          ": dv =", iBLE.getdvStrt())
                                continue
                            elif iLine.Parameter == "betaE":
                                nTlt += 1
                                iBLE.getdvStrt()[1] = float(iLine.Value)
                                if cls.getDebug():
                                    print("                ----> Tilt",
                                          Name, ", nTlt =", nTlt, \
                                          ": dv =", iBLE.getdvStrt())
                                continue
                            elif iLine.Parameter == "gammaE":
                                nTlt += 1
                                iBLE.getdvStrt()[2] = float(iLine.Value)
                                if cls.getDebug():
                                    print("                ----> Tilt",
                                          Name, ", nTlt =", nTlt, \
                                          ": dv =", iBLE.getdvStrt())
                                continue
                else:
                    if np.linalg.norm(iBLE.getdvStrt()) != 0:
                        iBLE.setdvStrt(iBLE.getdvStrt())
                    if cls.getDebug():
                        print("     <---- Tilt:", iBLE.getdvStrt())
                        print(iBLE.getdRotStrt())
                        print(iBLE.getdRotStrtINV())
                                    
            if NewElement:
                nShft = 0
                nTlt = 0
                Name0 = Name
                rStrt = iLst.getrStrt() + iLst.getStrt2End()
                vStrt = iLst.getvEnd()
                drStrt = np.array([0.,0.,0.])
                dvStrt = np.array([0.,0.,0.])
            
            if cls.getDebug():
                print("                ---->  rStrt:", rStrt)
                print("                ---->  vStrt:", vStrt)
                print("                ----> drStrt:", drStrt)
                print("                ----> dvStrt:", dvStrt)

            if iLine.Section != Section:
                Section   = iLine.Section
                nRPLCswtch = 0
                nDrift     = 0
                nAperture  = 0
                nFquad     = 0
                nDquad     = 0
                nSlnd      = 0
                nGbrLns    = 0
                nDpl       = 0
                nCvty      = 0

            refPrtcl = cls.getcurrentReferenceParticle()
            if elementKEY == "RPLCswitch":
                if cls.getDebug():
                    print("               ----> Start on RPLCswitch.")
                if NewElement:
                    jtheta = None
                    jphi   = None
                    ktheta = None
                    kphi   = None
                if iLine.Type == "j":
                    if iLine.Parameter == "theta":
                        jtheta = float(iLine.Value)
                    elif iLine.Parameter == "phi":
                        jphi   = float(iLine.Value)
                elif iLine.Type == "k":
                    if iLine.Parameter == "theta":
                        ktheta = float(iLine.Value)
                    elif iLine.Parameter == "phi":
                        kphi   = float(iLine.Value)
                if jtheta != None and \
                   jphi   != None and \
                   ktheta != None and \
                   kphi   != None:
                    NewElement = True
                    if cls.getDebug():
                        print("                   <---- ", \
                              "jtheta, jphi, ktheta, kphi:", \
                              jtheta, jphi, ktheta, kphi)
                else:
                    if cls.getDebug():
                        print("                   ----> ", \
                              "jtheta, jphi, ktheta, kphi:", \
                              jtheta, jphi, ktheta, kphi)
                    NewElement = False
                    continue
                nRPLCswtch += 1
                Name      = Name + str(nRPLCswtch)
                if cls.getDebug():
                    print("           ----> Add", Name)
                vStrt = np.array([ [jtheta, jphi], [ktheta, kphi] ])
                iBLE = BLE.RPLCswitch(Name, rStrt, vStrt, drStrt, dvStrt)
                cls.addBeamLineElement(iBLE)
                s += iBLE.getLength()
                refPrtclSet = refPrtcl.setReferenceParticle(iBLE)
            elif elementKEY == "Drift":
                nDrift   += 1
                Name      = Name + str(nDrift)
                Length    = float(iLine.Value)
                if cls.getDebug():
                    print("             ----> Add", Name)
                iBLE = BLE.Drift(Name, 
                             rStrt, vStrt, drStrt, dvStrt, Length)
                cls.addBeamLineElement(iBLE)
                s += Length
                refPrtclSet = refPrtcl.setReferenceParticle(iBLE)
            elif elementKEY == "Aperture":
                localType = iLine.Type.replace(" ", "")
                typeLIST  = localType.split(',')
                if cls.getDebug():
                    print(" Aperture: localType, typeLIST:",
                          localType, typeLIST)
            
                if NewElement:
                    iMode   = 0
                    iLnsApp = 0
                    nLnsApp = 1
                    Param   = [0, 0., 0.]
                    if typeLIST[0] == "Elliptical" or \
                       typeLIST[0] == "Rectangular":
                        iMode   = 1
                        nLnsApp = 2
                        if typeLIST[0] == "Rectangular": iMode = 2

                Param[0] = iMode
                iLnsApp += 1
                if cls.getDebug():
                    print("     ----> iMode, iLnsApp, nLnsApp, NewElement:",\
                          iMode, iLnsApp, nLnsApp, NewElement)

                if typeLIST[0] == "Circular":
                    if iLine.Parameter == "Radius":
                        Param[1] = float(iLine.Value)
                elif typeLIST[0] == "Elliptical" or \
                    typeLIST[0] == "Rectangular":
                    if iLine.Parameter == "RadiusX":
                        Param[1] = float(iLine.Value)
                    elif iLine.Parameter == "RadiusY":
                        Param[2] = float(iLine.Value)

                if cls.getDebug():
                    print("     ----> Param, drStrt:", \
                          Param, drStrt)
                    print("     ----> NewElement, iLnsApp, nLnsApp:", \
                          NewElement, iLnsApp, nLnsApp)
                    
                if iLnsApp < nLnsApp:
                    NewElement = False
                    continue
                else:
                    NewElement = True
                    
                nAperture += 1
                Name       = Name + typeLIST[0] + ":" + str(nAperture)
                if cls.getDebug():
                    print("     ----> NewElement:", NewElement)
                    print("     ----> Add", Name)
                iBLE = BLE.Aperture(Name, \
                                    rStrt, vStrt, drStrt, dvStrt, Param)
                cls.addBeamLineElement(iBLE)
                s += 0.
                refPrtclSet = refPrtcl.setReferenceParticle(iBLE)

            elif elementKEY == "Fquad":
                if cls.getDebug():
                    print(" Fquad: NewElement:", NewElement)
                if NewElement:
                    nLnsFQ = 2
                    iLnsFQ = 0
                iLnsFQ += 1
                
                if iLine.Parameter == "Length":
                    FqL = float(iLine.Value)
                elif iLine.Parameter == "Strength":
                    FqS = float(iLine.Value)
                elif iLine.Parameter == "kq":
                    kq   = float(iLine.Value)
                    Brho = (1./(speed_of_light*1.E-9))*p0/1000.
                    FqS  = kq * Brho

                if iLnsFQ < nLnsFQ:
                    NewElement = False
                    continue
                else:
                    NewElement = True
                    
                nFquad += 1
                Name       = Name + str(nFquad)
                if cls.getDebug():
                    print("             ----> Add", Name)
                iBLE = BLE.FocusQuadrupole(Name, \
                                    rStrt, vStrt, drStrt, dvStrt, FqL, FqS)
                cls.addBeamLineElement(iBLE)
                s += FqL
                refPrtclSet = refPrtcl.setReferenceParticle(iBLE)
            elif elementKEY == "Dquad":
                if NewElement:
                    nLnsDQ = 2
                    iLnsDQ = 0
                iLnsDQ += 1
                
                if iLine.Parameter == "Length":
                    DqL = float(iLine.Value)
                elif iLine.Parameter == "Strength":
                    DqS = float(iLine.Value)
                elif iLine.Parameter == "kq":
                    kq   = float(iLine.Value)
                    Brho = (1/(speed_of_light*1.E-9))*p0/1000.
                    DqS  = kq * Brho
                    
                if NewElement or iLnsDQ < nLnsDQ:
                    NewElement = False
                    continue
                else:
                    NewElement = True
                    
                nDquad += 1
                Name       = Name + str(nDquad)
                if cls.getDebug():
                    print("             ----> Add", Name)
                iBLE = BLE.DefocusQuadrupole(Name, \
                                    rStrt, vStrt, drStrt, dvStrt, DqL, DqS)
                cls.addBeamLineElement(iBLE)
                s += DqL
                refPrtclSet = refPrtcl.setReferenceParticle(iBLE)
            elif elementKEY == "Solenoid":
                if NewElement:
                    if iLine.Type == "Length, layers and turns":
                        nLnsSlnd = 4
                        iLnSlnd  = 1
                    elif iLine.Type == "Length, strength":
                        nLnsSlnd = 2
                        iLnSlnd  = 1
                    else:
                        raise badParameter(" BeamLine.addbeam: Solenoid", \
                                           " Type=", iLine.Type, \
                                           " invalid.")
                if iLine.Parameter == "Length":
                    SlndL = float(iLine.Value)
                elif iLine.Parameter == "Current":
                    SlndI = float(iLine.Value)
                elif iLine.Parameter == "Layers":
                    SlndLy = float(iLine.Value)
                elif iLine.Parameter == "Turns":
                    SlndT = float(iLine.Value)
                elif iLine.Parameter == "Strength":
                    Slndks = float(iLine.Value)
                if iLnSlnd < nLnsSlnd:
                    iLnSlnd += 1
                    NewElement = False
                    continue
                else:
                    NewElement = True
                """
                rStrt = np.array([0.,0.,s])
                vStrt = np.array([[np.pi/2.,np.pi/2.],[0.,0.]])
                drStrt = np.array([0.,0.,0.])
                dvStrt = np.array([0.,0.,0.])
                """
                nSlnd += 1
                Name  += str(nSlnd)
                if iLine.Type == "Length, layers and turns":
                    nTrns  = float(SlndLy) * float(SlndT)
                    B0     = mu0*nTrns*SlndI/SlndL
                elif iLine.Type == "Length, strength":
                    Brho = (1./(speed_of_light*1.E-9))*p0/1000.
                    B0 = Slndks * Brho
                else:
                    raise badParameter(" BeamLine.addbeam: Solenoid", \
                                       " Type=", iLine.Type, \
                                       " invalid.")
                if cls.getDebug():
                    print("             ----> Add", Name)
                iBLE = BLE.Solenoid(Name, \
                                rStrt, vStrt, drStrt, dvStrt, SlndL, B0)
                cls.addBeamLineElement(iBLE)
                s += SlndL
                refPrtclSet = refPrtcl.setReferenceParticle(iBLE)
            elif elementKEY == "Gabor lens":
                if NewElement:
                    if iLine.Type == "Length, strength":
                        nLnsGbrLns = 2
                        iLnGbrLns  = 1
                    else:
                        raise badParameter(" BeamLine.addbeam: Gabor lens", \
                                           " Type=", iLine.Type, \
                                           " invalid.")
                if iLine.Parameter == "Length":
                    GbrLnsL = float(iLine.Value)
                elif iLine.Parameter == "Strength":
                    GbrLnsks = float(iLine.Value)
                if iLnGbrLns < nLnsGbrLns:
                    iLnGbrLns += 1
                    NewElement = False
                    continue
                else:
                    NewElement = True
                """
                rStrt = np.array([0.,0.,s])
                vStrt = np.array([[np.pi/2.,np.pi/2.],[0.,0.]])
                drStrt = np.array([0.,0.,0.])
                dvStrt = np.array([0.,0.,0.])
                """
                nGbrLns += 1
                Name  += str(nGbrLns)
                if iLine.Type == "Length, strength":
                    Brho = (1./(speed_of_light*1.E-9))*p0/1000.
                    B0 = GbrLnsks * Brho
                else:
                    raise badParameter(" BeamLine.addbeam: Gabor lens", \
                                       " Type=", iLine.Type, \
                                       " invalid.")
                if cls.getDebug():
                    print("             ----> Add", Name)
                iBLE = BLE.GaborLens(Name, \
                                rStrt, vStrt, drStrt, dvStrt, \
                                None, None, None, None, GbrLnsL, B0)
                cls.addBeamLineElement(iBLE)
                s += GbrLnsL
                refPrtclSet = refPrtcl.setReferenceParticle(iBLE)
            elif elementKEY == "Dipole":
                if NewElement:
                    if iLine.Type == "Sector (Length, angle)":
                        nLnsDpl = 2
                        iLnDpl  = 1
                    else:
                        raise badParameter(" BeamLine.addbeam: Dipole", \
                                           " Type=", iLine.Type, \
                                           " invalid.")
                if iLine.Parameter == "Length":
                    DplL = float(iLine.Value)
                elif iLine.Parameter == "Angle":
                    DplA = float(iLine.Value)
                    DplA = DplA * mth.pi / 180.
                if iLnDpl < nLnsDpl:
                    iLnDpl += 1
                    NewElement = False
                    continue
                else:
                    NewElement = True
                """
                rStrt = np.array([0.,0.,s])
                vStrt = np.array([[np.pi/2.,np.pi/2.],[0.,0.]])
                drStrt = np.array([0.,0.,0.])
                dvStrt = np.array([0.,0.,0.])
                """
                nDpl   += 1
                Name   += str(nDpl)
                rho     = DplL/DplA
                B       = (1/(speed_of_light*1.E-9))*p0/rho/1000.
                cls.addBeamLineElement(BLE.SectorDipole(Name, \
                                rStrt, vStrt, drStrt, dvStrt, DplA, B))
                s += cls._Element[len(cls._Element)-1].getLength()
                refPrtclSet = refPrtcl.setReferenceParticle(iBLE)
            elif elementKEY == "Cavity":
                if NewElement:
                    if iLine.Type == "Cylindrical":
                        nLnsCvty = 3
                        iLnCvty  = 1
                    else:
                        raise badParameter(" BeamLine.addbeam: Cavity", \
                                           " Type=", iLine.Type, \
                                           " invalid.")
                if iLine.Parameter == "Gradient":
                    CylCvtyGrdnt  = float(iLine.Value)
                elif iLine.Parameter == "Frequency":
                    CylCvtyFrqncy = float(iLine.Value)
                elif iLine.Parameter == "Phase":
                    CylCvtyPhs    = float(iLine.Value)
                    CylCvtyPhs    = CylCvtyPhs * mth.pi / 180.
                if iLnCvty < nLnsCvty:
                    iLnCvty += 1
                    NewElement = False
                    continue
                else:
                    NewElement = True
                nCvty   += 1
                Name    += str(nCvty)
                iBLE    = BLE.CylindricalRFCavity(Name, \
                                    rStrt, vStrt, drStrt, dvStrt, \
                                    CylCvtyGrdnt, CylCvtyFrqncy, CylCvtyPhs)
                cls.addBeamLineElement(iBLE)
                s += cls._Element[len(cls._Element)-1].getLength()
                refPrtclSet = refPrtcl.setReferenceParticle(iBLE)

            if cls.getDebug():
                print("     ---->", Name, \
                      "beam line element created.")
                print("         ----> reference particle:")
                print("               Position:", \
                      refPrtcl.getRrIn()[0])
                print("               Momentum:", \
                      refPrtcl.getPrIn()[0])
                print("     <---- Done.")

    @classmethod
    def addBeamLineElement(cls, iBLE=False):
        if not isinstance(iBLE, BLE.BeamLineElement):
            raise badBeamLineElement()
        cls._Element.append(iBLE)
        
    def checkConsistency(self):
        if self.getDebug():
            print(" BeamLine.checkConsistency: start")
            
        ConsChk = False

        #.. Check length is consistent:
        iBLE = BLE.BeamLineElement.getinstances()[-1]
        iRfP = BL.BeamLine.getcurrentReferenceParticle()
        if self.getDebug():
            print("     ----> BLE name:", \
                  iBLE.getName(), \
                  iBLE.getrStrt()[2])
            if len(iRfP.getRrIn()) > 0:
                print("     ----> Ref prtcl RrIn[-1][2]:", \
                      iRfP.getRrIn()[-1][2])

        if len(iBLE.getrStrt()) == 3 and \
           isinstance(iRfP.getRrIn(), list) and \
           len(iRfP.getRrIn()) > 0:
            dif = iBLE.getrStrt()[2] - iRfP.getRrIn()[-1][2]
        
            if self.getDebug():
                print("     ----> BLE name:", \
                      iBLE.getName(), \
                      iBLE.getrStrt()[2])
                print("     ----> Ref prtcl RrIn[-1][2]:", \
                      iRfP.getRrIn()[-1][2])
                print("     ----> dif:", dif)

            if abs(dif) > 1E-6:
                return ConsChk
        else:
            return ConsChk

        #.. Check no beam-line-element names are unique:
        Names = []
        for iBLE in BLE.BeamLineElement.getinstances():
            Names.append(iBLE.getName())

        if self.getDebug():
            print("     ----> Names:", Names)

        for iBLE in BLE.BeamLineElement.getinstances():
            nName = Names.count(iBLE.getName())
            if self.getDebug():
                print("         ---->", nName, iBLE.getName())
                
            if nName != 1: return ConsChk

        return True

    @classmethod
    def trackBeam(cls, NEvts=0, ParticleFILE=None, \
                  iParticle=None, LocStrt=None, CleanAfterWrite=True):
        if cls.getDebug():
            print(" BeamLine.trackBeam start")
            print("     ----> NEvts:", NEvts)
            print("     ----> ParticleFILE:", ParticleFILE)
            if iParticle == None:
                print("     ----> iParticle:", iParticle)
            else:
                print("     ----> iParticle:", id(iParticle))
            print("     ----> LocStrt:", LocStrt)
            print("     ----> CleanAfterWrite:", CleanAfterWrite)

        if isinstance(iParticle, Prtcl.Particle): NEvts = 1
        if (cls.getDebug() or NEvts > 1) and \
           Smltn.Simulation.getProgressPrint():
            print("     ----> BeamLine.trackBeam for", NEvts, " events.")
        Scl  = 10
        iCnt = 1

        iRefPrtcl = BL.BeamLine.getcurrentReferenceParticle()

        for iEvt in range(0, NEvts):
            if (iEvt % Scl) == 0:
                if (cls.getDebug() or NEvts > 1) and \
                   Smltn.Simulation.getProgressPrint():
                    print("         ----> Generating event ", iEvt)
                if iCnt == 10:
                    iCnt = 1
                    Scl  = Scl * 10
                iCnt += 1
                
            #.. Create particle instance to store progression through
            #   beam line
            if iParticle != None:
                PrtclInst   = iParticle

                if cls.getDebug():
                    print("            ----> LocStrt:", LocStrt)
                    print("                   Length:", \
                          len(PrtclInst.getTraceSpace()))
                iLoc = 1
                if LocStrt != None: iLoc = LocStrt
                if iLoc-1 >= len(PrtclInst.getTraceSpace()):
                    continue
                
                del PrtclInst.getLocation() \
                    [iLoc:len(PrtclInst.getLocation())]
                del PrtclInst.getz()[iLoc:len(PrtclInst.getz())]
                del PrtclInst.gets()[iLoc:len(PrtclInst.gets())]
                del PrtclInst.getTraceSpace() \
                    [iLoc:len(PrtclInst.getTraceSpace())]
                del PrtclInst.getRPLCPhaseSpace()\
                    [iLoc:len(PrtclInst.getRPLCPhaseSpace())]
                del PrtclInst.getLabPhaseSpace()\
                    [iLoc:len(PrtclInst.getLabPhaseSpace())]
                SrcTrcSpc = PrtclInst.getTraceSpace()[iLoc-1]
            else:
                PrtclInst   = Prtcl.Particle.createParticle()
                if cls.getDebug():
                    print("     ----> Created new Particle instance")

                #.. Generate particle:
                if isinstance(cls.getSrcTrcSpc(), np.ndarray):
                    if cls.getDebug():
                        print("     ----> Start using:", iEvt)
                    Name = BLE.BeamLineElement.getinstances()[0].getName()+\
                        ":Source:User"
                    SrcTrcSpc = cls.getSrcTrcSpc()
                else:
                    if cls.getDebug():
                        print("     ----> Start by calling", \
                              "getSourceTraceSpace")
                    Name = cls.getElement()[1].getName()
                    SrcTrcSpc = \
                        cls.getElement()[1].getParticleFromSource()
                Success = PrtclInst.recordParticle(Name, 0., 0., SrcTrcSpc)
                if cls.getDebug():
                    print("     ----> Event", iEvt)
                    with np.printoptions(linewidth=500,precision=7,\
                                         suppress=True):
                        print("         ----> trace space at source     :", \
                              SrcTrcSpc)

            #.. Track through beam line:
            TrcSpc_i = SrcTrcSpc
            TrcSpc   = SrcTrcSpc
            if cls.getDebug():
                print("     ----> Transport through beam line")
            iLoc = -1
            nLocStrt = -1
            if LocStrt != None: nLocStrt = LocStrt
            for iBLE in BLE.BeamLineElement.getinstances():
                iLoc += 1
                if iLoc <= nLocStrt or \
                   isinstance(iBLE, BLE.Source) or \
                   isinstance(iBLE, BLE.Facility):
                    continue
                if cls.getDebug():
                    print("         ---->", iBLE.getName())

                TrcSpc     = iBLE.Transport(TrcSpc_i)
                if cls.getDebug():
                    with np.printoptions(\
                                linewidth=500,precision=7,suppress=True):
                        print("             ----> Updated trace space   :", \
                              TrcSpc)
                        
                if not isinstance(TrcSpc, np.ndarray):
                    if cls.getDebug():
                        print("              ---->", \
                              " partice outside acceptance(1)")
                    break

                elif cls.checkDecay(iBLE, iRefPrtcl, PrtclInst, iLoc, TrcSpc):
                    break
                
                else:
                    if iBLE.ExpansionParameterFail(TrcSpc):
                        if cls.getDebug():
                            print("              ---->", \
                                " Particle fails expansion parameter test")
                        TrcSpc = None
                        break
                    else:
                        zEnd    = -999999.
                        sEnd    = iBLE.getrStrt()[2] + iBLE.getLength()
                        Success = PrtclInst.recordParticle(iBLE.getName(), \
                                                           zEnd, \
                                                           sEnd, \
                                                           TrcSpc)
                TrcSpc_i = TrcSpc

            if cls.getDebug():
                print("         ----> Reached end of beam line.")

            #.. Write event:
            if isinstance(ParticleFILE, io.BufferedWriter):
                if cls.getDebug():
                    print("     ----> Write particle to file:", ParticleFILE)
                PrtclInst.writeParticle(ParticleFILE, CleanAfterWrite)
                if CleanAfterWrite:
                    Prtcl.Particle.cleanParticles()
                #del PrtclInst
            
            if cls.getDebug():
                print("     <---- Finished handling beam line.")
                
        if (cls.getDebug() or NEvts > 1) and \
        Smltn.Simulation.getProgressPrint():
            print("     <---- End of this simulation, ", NEvts, \
                  " events generated")

    @classmethod
    def checkDecay(cls, iBLE, iRefPrtcl, PrtclInst, iLoc, TrcSpc):
        decayed = False

        if cls.getDebug():
            print(" BeamLine.checkDecay: handle unstable particle:")
            print("             ----> Time left to live:", \
                  PrtclInst.getRemainingLifetime())
        
        if PrtclInst.getRemainingLifetime() != mth.inf:
            if cls.getDebug():
                print("     ----> Time left to live:", \
                      PrtclInst.getRemainingLifetime())
                print("     ----> Length of element:", \
                      iBLE.getLength())
                        
            m = \
        PhysCnsts.PhysicalConstants().getparticleMASS(PrtclInst.getSpecies())
            E = iRefPrtcl.getPrOut()[iLoc-1][3] + \
                         TrcSpc[5] * iRefPrtcl.getMomentumOut(iLoc-1)
            p = mth.sqrt(E**2 - m**2)
            if cls.getDebug():
                print(" iLoc, E, p, mass:", iLoc, E, p, m)
                        
            scl = m / p / speed_of_light
            dt  = iBLE.getLength() * scl
            if cls.getDebug():
                print("     ----> Proper time increment:", dt)
                    
            if dt > PrtclInst.getRemainingLifetime():
                if cls.getDebug():
                    print(" <---- Particle decayed!")
                decayed = True
            else:
                PrtclInst.setRemainingLifetime( \
                            PrtclInst.getRemainingLifetime() - dt \
                                               )
                if cls.getDebug():
                    print("         <---- Particle survived!")

        return decayed
                                    
#--------  I/o methods:
    def csv2pandas(_filename):
        ParamsPandas = pnds.read_csv(_filename)
        return ParamsPandas

    def pandasBeamLine(self):
        if self.getDebug():
            print(" BeamLine.pandasBeamLine starts.")

        """
        if not os.path.isdir(os.path.dirname(csvFILE)):
            raise noFILE( \
                    " BeamLine.pandasBeamLine: Directory for CSV file", \
                    os.path.dirname(CSVfile), "does not exist.")
        """
        
        Lines = []
            
        if self.getDebug():
            nBLE = len(BLE.BeamLineElement.getinstances())
            print("     ----> Number of locations to store:", nBLE)

        Lines.append(self.getHeader())
        if self.getDebug():
            print("     ----> Header:", Lines[0])
        
        for iBLE in BLE.BeamLineElement.getinstances():
            if self.getDebug():
                print("         ----> Write element:", iBLE.getName())
            iBLElines = iBLE.getLines()
            for Line in iBLElines:
                Lines.append(Line)
                if self.getDebug():
                    print("             ", Lines[-1])
                
        DataFrame = pnds.DataFrame(Lines, \
                                   columns=self.getHeader())
        if self.getDebug():
            print("     ----> Dump data frame:")
            print(DataFrame)
        
        if self.getDebug():
            print(" <---- BeamLine.writeBeamLine done.")
        
        return DataFrame

    def getHeader(self):
        HeaderList = ["Stage", "Section", "Element", "Type", "Parameter", \
	              "Value", "Unit", "Comment"]
        return HeaderList

        
    def writeBeamLine(self, beamlineFILE=None):
        if self.getDebug():
            print(" BeamLine.writeBeamLine starts.")

        if not isinstance(beamlineFILE, io.BufferedWriter):
            raise noFILE( \
                    " BeamLine.writeBeamLine: file not BufferedWriter.")

        nBLE = len(BLE.BeamLineElement.getinstances())
        if self.getDebug():
            print("     ----> Number of locations to store:", nBLE)
        record = strct.pack(">i", nBLE)
        beamlineFILE.write(record)
        
        for iBLE in BLE.BeamLineElement.getinstances():
            if self.getDebug():
                print("         ----> Write element:", iBLE.getName())
            iBLE.writeElement(beamlineFILE)
        
        if self.getDebug():
            print(" <---- BeamLine.writeBeamLine done.")

    @classmethod
    def readBeamLine(cls, beamlineFILEinst=None):
        if cls.getDebug():
            print(" BeamLine.readBeamLine starts.")

        #.. Initialise BeamLine instance:
        cls.__new__(cls, None, True)

        beamlineFILE = beamlineFILEinst.getdataFILE()
        if not isinstance(beamlineFILE, io.BufferedReader):
            raise noFILE( \
                    " BeamLine.readBeamLine: file does not exist.")

        EoF = False

        if Prtcl.ReferenceParticle.getinstances() == []:
            refPrtcl  = BL.BeamLine.getcurrentReferenceParticle()

        brecord = beamlineFILE.read(4)
        if brecord == b'':
            if cls.getDebug():
                print(" <---- end of file, return.")
            return True
            
        record = strct.unpack(">i", brecord)
        nBLE   = record[0]
        if cls.getDebug():
            print("     ----> Number of beam line elements:", nBLE)
                
        for iBLE in range(nBLE):
            if cls.getDebug():
                print("         ----> Read element:", iBLE)

            dr = np.array([0., 0., 0.])
            dv = np.array([0., 0., 0.])
                
            brecord = beamlineFILE.read(4)
            if brecord == b'':
                if cls.getDebug():
                    print(" <---- end of file, return.")
                return True
            
            record = strct.unpack(">i", brecord)
            nChr   = record[0]
            if cls.getDebug():
                print("             ----> Number of characters:", nChr)
        
            brecord      = beamlineFILE.read(nChr)
            derivedCLASS = brecord.decode('utf-8')
            if cls.getDebug():
                print("                   Derived class:", derivedCLASS)

            if derivedCLASS == "Facility":
                EoF, p0, VCMVr = BLE.Facility.readElement(beamlineFILEinst)
                if EoF:
                    return EoF
            elif derivedCLASS == "Source":
                EoF, Mode, Params = BLE.Source.readElement(beamlineFILEinst)
                if EoF:
                    return EoF
            elif derivedCLASS == "Drift":
                EoF, Length = BLE.Drift.readElement(beamlineFILEinst)
                if EoF:
                    return EoF
            elif derivedCLASS == "Aperture":
                EoF, Type, Params = BLE.Aperture.readElement(beamlineFILEinst)
                if EoF:
                    return EoF
            elif derivedCLASS == "GaborLens":
                EoF, Bz, VA, RA, Rp, Ln, St = \
                    BLE.GaborLens.readElement(beamlineFILEinst)
                if EoF:
                    return EoF
            elif derivedCLASS == "Solenoid":
                EoF, Ln, St, kSol = \
                    BLE.Solenoid.readElement(beamlineFILEinst)
                if EoF:
                    return EoF
            elif derivedCLASS == "CylindricalRFCavity":
                EoF, Grdnt, Frqncy, Phs = \
                    BLE.CylindricalRFCavity.readElement(beamlineFILEinst)
                if EoF:
                    return EoF
            elif derivedCLASS == "SectorDipole":
                EoF, Angl, B = \
                    BLE.SectorDipole.readElement(beamlineFILEinst)
                if EoF:
                    return EoF
            elif derivedCLASS == "DefocusQuadrupole":
                EoF, Ln, St, kDQ = \
                    BLE.DefocusQuadrupole.readElement(beamlineFILEinst)
                if EoF:
                    return EoF
            elif derivedCLASS == "FocusQuadrupole":
                EoF, Ln, St, kFQ = \
                    BLE.FocusQuadrupole.readElement(beamlineFILEinst)
                if EoF:
                    return EoF
            elif derivedCLASS == "RPLCswitch":
                EoF = BLE.RPLCswitch.readElement(beamlineFILEinst)
                if EoF:
                    return EoF
            else:
                print("Next derived class:", derivedCLASS, " not coded.", \
                      "  Abort.")
                sys.exit(1)

            EoF, Loc, r, v, dr, dv = \
                BLE.BeamLineElement.readElement(beamlineFILEinst)
            
            if derivedCLASS == "Facility":
                instBLE = BLE.Facility(Loc, r, v, dr, dv, p0, VCMVr)
                if cls.getDebug():
                    print(instBLE)
                refPrtcl  = \
                    Prtcl.ReferenceParticle.createReferenceParticles()[0]
                cls.setcurrentReferenceParticle(refPrtcl)
            elif derivedCLASS == "Source":
                instBLE = BLE.Source(Loc, r, v, dr, dv, Mode, Params)
                if cls.getDebug():
                    print(instBLE)
                refPrtclSet = refPrtcl.setReferenceParticleAtSource()
            elif derivedCLASS == "Drift":
                instBLE = BLE.Drift(Loc, r, v, dr, dv, Length)
                refPrtclSet = refPrtcl.setReferenceParticle(instBLE)
                if cls.getDebug():
                    print(instBLE)
            elif derivedCLASS == "Aperture":
                Param = [Type, Params[0]]
                if len(Params) > 1:
                    Param.append(Params[1])
                instBLE = BLE.Aperture(Loc, r, v, dr, dv, Param)
                refPrtclSet = refPrtcl.setReferenceParticle(instBLE)
                if cls.getDebug():
                    print(instBLE)
            elif derivedCLASS == "GaborLens":
                instBLE = BLE.GaborLens(Loc, r, v, dr, dv, \
                                        Bz, VA, RA, Rp, Ln, St)
                refPrtclSet = refPrtcl.setReferenceParticle(instBLE)
                if cls.getDebug():
                    print(instBLE)
            elif derivedCLASS == "Solenoid":
                instBLE = BLE.Solenoid(Loc, r, v, dr, dv, \
                                        Ln, St, kSol)
                refPrtclSet = refPrtcl.setReferenceParticle(instBLE)
                if cls.getDebug():
                    print(instBLE)
            elif derivedCLASS == "CylindricalRFCavity":
                instBLE = BLE.CylindricalRFCavity(Loc, r, v, dr, dv, \
                                                  Grdnt, Frqncy, Phs)
                refPrtclSet = refPrtcl.setReferenceParticle(instBLE)
                if cls.getDebug():
                    print(instBLE)
            elif derivedCLASS == "SectorDipole":
                instBLE = BLE.SectorDipole(Loc, r, v, dr, dv, \
                                           Angl, B)
                refPrtclSet = refPrtcl.setReferenceParticle(instBLE)
                if cls.getDebug():
                    print(instBLE)
            elif derivedCLASS == "DefocusQuadrupole":
                instBLE = BLE.DefocusQuadrupole(Loc, r, v, dr, dv, \
                                                Ln, St, kDQ)
                refPrtclSet = refPrtcl.setReferenceParticle(instBLE)
                if cls.getDebug():
                    print(instBLE)
            elif derivedCLASS == "FocusQuadrupole":
                instBLE = BLE.FocusQuadrupole(Loc, r, v, dr, dv, \
                                                Ln, St, kFQ)
                refPrtclSet = refPrtcl.setReferenceParticle(instBLE)
                if cls.getDebug():
                    print(instBLE)
            elif derivedCLASS == "RPLCswitch":
                instBLE = BLE.RPLCswitch(Loc, r, v, dr, dv)
                refPrtclSet = refPrtcl.setReferenceParticle(instBLE)
                if cls.getDebug():
                    print(instBLE)
            else:
                print("Derived class:", derivedCLASS, " not coded.", \
                      "  Abort.")
                sys.exit(1)
            cls.addBeamLineElement(instBLE)

                    
        if cls.getDebug():
            print(" <---- BeamLine.writeBeamLine done.")

        return EoF

#--------  Utilities:
    @classmethod
    def cleaninstance(cls):
        
        del cls.__BeamLineInst
        cls.__BeamLineInst = None

        cls._currentReferenceParticle = None
        
        if cls.getDebug():
            print(' BeamLine.cleaninstance: instance removed.')

    @classmethod
    def fixsz(self):
        PosEnd = np.array([0., 0., 0.])
        for iLoc in range(1, len(BLE.BeamLineElement.getinstances())):
            lastBLE = BLE.BeamLineElement.getinstances()[iLoc-1]
            iBLE    = BLE.BeamLineElement.getinstances()[iLoc]
            PosEnd  = lastBLE.getrStrt() + lastBLE.getStrt2End()
            if iBLE.getrStrt()[2] != PosEnd[2]:
                if self.getDebug():
                    print(iBLE.getName(), " \n", \
                      "     ---->            PosEnd:", PosEnd, \
                      "     ---->   iBLE.getrStrt():", iBLE.getrStrt(), \
                      "     ----> iBLE.getStrt2End():", lastBLE.getStrt2End())
                    
                PosStrt = lastBLE.getrStrt() + lastBLE.getStrt2End()
                iBLE.setrStrt(PosStrt)
                
                if self.getDebug():
                    print("     Corrected: \n", \
                      "     ---->   iBLE.getrStrt():", iBLE.getrStrt())


#--------  Exceptions:
class badParameter(Exception):
    pass
                
class badTraceSpaceVector(Exception):
    pass
                
class noFILE(Exception):
    pass

class BLEnotvalid(Exception):
    pass

class badSHIFT(Exception):
    pass
