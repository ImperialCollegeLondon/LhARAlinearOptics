#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
To do:
 - Add documentation for methods from trackBeam
 LhARAcument all class attributes

Class BeamLine:
===============

  Singleton class to set up the beam line defined in the beam-line
  specification file.


  Class attributes:
  -----------------
   __Debug    : Debug flag
   __SrcTrcSpc: 6D trace space at source (np.ndarray)
__BeamLineInst: Instance of BeamLine class.  Set on creation of first
                (and only) instance.

      
  Instance attributes:
  --------------------
   _BeamLineSpecificationCVSfile : Path to csv file in which beam line is
                                   specified.
            _BeamLineParamPandas : Pandas data frame instance containing
                                   parameters.
    _Element[] : BeamLineElement : List of beam line elements making up the
                                   beam line.
    
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
getBeamLineSpecificationCVSfile:
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

Created on Mon 02Oct23: Version history:
----------------------------------------
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
import pandas as pnds

import Particle        as Prtcl
import BeamLineElement as BLE

#-------- Physical Constants Instances and Methods ----------------
from PhysicalConstants import PhysicalConstants

constants_instance = PhysicalConstants()

protonMASS         = constants_instance.mp()
speed_of_light     = constants_instance.SoL()
mu0                = constants_instance.mu0()

class BeamLine(object):
    __BeamLineInst = None
    __Debug        = False
    __SrcTrcSpc    = None
    __BeamLineInst = None


#--------  "Built-in methods":
    def __new__(cls, _BeamLineSpecificationCVSfile=None):
        if cls.getinstance() == None:
            if cls.getDebug():
                print(' BeamLine.__new__: ', \
                      'creating the BeamLine object')
            cls.__BeamLineInst = super(BeamLine, cls).__new__(cls)

            #.. Only constants; print values that will be used:
            if cls.getDebug():
                print("     ----> Debug flag: ", cls.getDebug())

                #.. Check and load parameter file
            if _BeamLineSpecificationCVSfile == None:
                raise Exception( \
                            " BeamLine.__new__: no parameter file given.")
        
            if not os.path.exists(_BeamLineSpecificationCVSfile):
                print(" BeamLine.__New__: _BeamLineSpecificationCVSfile:", \
                      _BeamLineSpecificationCVSfile)
                raise Exception( \
                    " BeamLine.__new__: parameter file does not exist.")
        
            cls._BeamLineSpecificationCVSfile = \
                               _BeamLineSpecificationCVSfile
            cls._BeamLineParamPandas = BeamLine.csv2pandas( \
                               _BeamLineSpecificationCVSfile)
            if not isinstance(cls._BeamLineParamPandas, pnds.DataFrame):
                raise Exception( \
                    " BeamLine.__new__: pandas data frame invalid.")

            cls._Element = []
                                                                      
            if cls.getDebug():
                print("     ----> Parameter file: ", \
                      cls.getBeamLineSpecificationCVSfile())
                print("     ----> Dump of pandas paramter list: \n", \
                      cls.getBeamLineParamPandas())

#.. Build facility:
            if cls.getDebug():
                print("     ----> Build facility:")

#    ----> Create reference particle:  --------  --------  --------  --------
#..  Instance only at this stage:
            if cls.getDebug():
                print("        ----> Create reference particle instance: ")
            
            refPrtcl  = Prtcl.ReferenceParticle()
            
            if cls.getDebug():
                print("        <---- Reference particle created. ")
#    <---- Done reference particle  --------  --------  --------  --------

#    ----> Facility:  --------  --------  --------  --------
            if cls.getDebug():
                print("         ----> Facility: ")

            cls.addFacility()
        
            if cls.getDebug():
                print("         <---- Facility done.")
#    <---- Done facility  --------  --------  --------  --------

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
            
            #refPrtclSet = refPrtcl.setReferenceParticle()

            if cls.getDebug():
                print("            ----> Reference particle set, success:")
                print("        <---- Reference particle done. ")
#    <---- Done reference particle -----  --------  --------  --------

        else:
            if cls.getDebug():
                print(' BeamLine.__new__: ', \
                      'existing BeamLine object will be used')

        return cls.getinstance()

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
                
    
#--------  I/o methods:
    def getBeamLineParams(_filename):
        BeamLineParams = pnds.read_csv(_filename)
        return BeamLineParams
    

#--------  "Set methods"
#.. Method believed to be self documenting(!)
    @classmethod
    def setDebug(cls, Debug=False):
        if cls.getDebug():
            print(" BeamLine.setdebug: ", Debug)
        cls.__Debug = Debug
        
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

        cls.__SrcTrcSpc = SrcTrcSpc
        
#--------  "Get methods"
#.. Method believed to be self documenting(!)
    @classmethod
    def getinstance(cls):
        return cls.__BeamLineInst

    @classmethod
    def getDebug(cls):
        return cls.__Debug

    @classmethod
    def getBeamLineSpecificationCVSfile(cls):
        return cls._BeamLineSpecificationCVSfile

    @classmethod
    def getBeamLineParamPandas(cls):
        return cls._BeamLineParamPandas

    @classmethod
    def getElement(cls):
        return cls._Element
    
    @classmethod
    def getSrcTrcSpc(cls):
        return cls.__SrcTrcSpc
    
    @classmethod
    def addBeamLineElement(self, iBLE=False):
        if self.getDebug():
            print(" BeamLineElement.addBeamLineElement: ", iBLE.getName())
        if not isinstance(iBLE, BeamLineElement):
            raise badBeamLineElement()
        self._Element.append(FacilityBLE)
        
        
#--------  Processing methods:
    def csv2pandas(_filename):
        ParamsPandas = pnds.read_csv(_filename)
        return ParamsPandas
        
    @classmethod
    def addFacility(cls):
        if cls.getDebug():
            print("             ----> BeamLine.addFacility starts:")

        #.. Parse the dataframe to get Facility parameters:
        Name, K0, VCMVr = cls.parseFacility()

        #.. Create the Facility beam line element:
        rStrt  = np.array([0., 0., 0.])
        vStrt  = np.array([0., 0., 0.])
        drStrt = np.array([0., 0., 0.])
        dvStrt = np.array([0., 0., 0.])

        p0     = mth.sqrt( (protonMASS+K0)**2 - protonMASS**2)

        FacilityBLE = BLE.Facility(Name, rStrt, vStrt, drStrt, dvStrt, \
                                   p0, VCMVr)
        cls._Element.append(FacilityBLE)

        if cls.getDebug():
            print("             <----", Name, \
                  "facility initialise.")

    @classmethod
    def addSource(cls):
        if cls.getDebug():
            print("             BeamLine.addSource starts:")
            
        #.. Parse the dataframe to get source parameters:
        Name, SrcMode, SrcParam = cls.parseSource()
        if Name == None and SrcMode == None and SrcMode == None:
            return

        #.. Create the source beam line element:
        rStrt = np.array([0.,0.,0.])
        vStrt = np.array([0.,0.])
        drStrt = np.array([0.,0.,0.])
        dvStrt = np.array([0.,0.])
        SourceBLE = BLE.Source(Name, rStrt, vStrt, drStrt, dvStrt, \
                               SrcMode, SrcParam)

        cls._Element.append(SourceBLE)

        refPrtcl    = Prtcl.ReferenceParticle.getinstance()
        refPrtclSet = refPrtcl.setReferenceParticleAtSource()

        if cls.getDebug():
            print("                 ---->", Name, \
                  "beam line element created.")
            print("                     ----> reference particle:")
            print("                         Position:", refPrtcl.getRrIn()[0])
            print("                         Momentum:", refPrtcl.getPrIn()[0])
            print("                 <---- Done.")

    @classmethod
    def parseFacility(cls):
        Name  = None
        p0    = None
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
        K0   = float(pndsFacility[ \
                        (pndsFacility["Type"]=="Reference particle") & \
                        (pndsFacility["Parameter"]=="Kinetic energy") ]. \
                            iloc[0]["Value"] \
                    )

        VCMVr = float(pndsFacility[ \
                        (pndsFacility["Type"]=="Vacuum chamber") & \
                        (pndsFacility["Parameter"]=="Mother volume radius") ]. \
                            iloc[0]["Value"] \
                    )
        
        if cls.getDebug():
            print("                     ----> Name:", Name, \
                  "; reference particle kinetic energy:", K0, "MeV")
            print( \
        "                     ----> Vacuum chamber mother volume radius:", \
                   VCMVr, "m")
            print("                 <---- Done.")
            
        return Name, K0, VCMVr

    @classmethod
    def parseSource(cls):
        SrcMode  = None
        SrcParam = None
        if cls.getDebug():
            print("                 ----> BeamLine.parseSource starts:")

        #.. Get "sub" pandas data frame with source parameters only:
        pndsSource = cls.getBeamLineParamPandas()[ \
                     cls.getBeamLineParamPandas()["Section"] == "Source" \
                                                  ]

        if pndsSource.empty:
            print(" Beamline.parseSource: empty source, return.")
            return None, None, None
            
        SrcMode = int( \
           pndsSource[pndsSource["Parameter"]=="SourceMode"]["Value"].iloc[0] \
                       )
        if cls.getDebug():
            print("                     ----> Mode:", SrcMode)
            
        if SrcMode == 0:               #.. Laser driven:
            Emin  = float( \
             pndsSource[pndsSource["Parameter"]=="Emin"]["Value"].iloc[0])
            Emax = float( \
             pndsSource[pndsSource["Parameter"]=="Emax"]["Value"].iloc[0])
            nPnts = \
             int(pndsSource[pndsSource["Parameter"]=="nPnts"]["Value"].iloc[0])
            MinCTheta = float( \
             pndsSource[pndsSource["Parameter"]=="MinCTheta"]["Value"].iloc[0])
            Power = float( \
             pndsSource[pndsSource["Parameter"]=="Power"]["Value"].iloc[0])
            Energy = float( \
             pndsSource[pndsSource["Parameter"]=="Energy"]["Value"].iloc[0])
            Wavelength = float( \
             pndsSource[pndsSource["Parameter"]=="Wavelength"]["Value"].iloc[0])
            Duration = float( \
             pndsSource[pndsSource["Parameter"]=="Duration"]["Value"].iloc[0])
            Thickness = float( \
             pndsSource[pndsSource["Parameter"]=="Thickness"]["Value"].iloc[0])
            Intensity = float( \
             pndsSource[pndsSource["Parameter"]=="Intensity"]["Value"].iloc[0])
            DivAngle = float( \
             pndsSource[pndsSource["Parameter"]=="DivAngle"]["Value"].iloc[0])
            
        elif SrcMode == 1:               #.. Gaussian:
            MeanE  = float( \
             pndsSource[pndsSource["Parameter"]=="MeanEnergy"]["Value"].iloc[0])
            SigmaE = float( \
             pndsSource[pndsSource["Parameter"]=="SigmaEnergy"]["Value"].iloc[0])
            MinCTheta = float(\
             pndsSource[pndsSource["Parameter"]=="MinCTheta"]["Value"].iloc[0])
        elif SrcMode == 2:               #.. Gaussian:
            Emin  = float( \
             pndsSource[pndsSource["Parameter"]=="Emin"]["Value"].iloc[0])
            Emax = float( \
             pndsSource[pndsSource["Parameter"]=="Emax"]["Value"].iloc[0])
            MinCTheta = float( \
             pndsSource[pndsSource["Parameter"]=="MinCTheta"]["Value"].iloc[0])

        SigmaX  = float( \
            pndsSource[pndsSource["Parameter"]=="SigmaX"]["Value"].iloc[0])
        SigmaY  = float( \
            pndsSource[pndsSource["Parameter"]=="SigmaY"]["Value"].iloc[0])

        if cls.getDebug():
            print("                         ----> SigmaX, SigmaY:", \
                  SigmaX, SigmaY)
            if SrcMode == 0:
                print("                         ----> Emin, Emax, nPnts, Power, Energy, Wavelength, Duration, Thickness, Intensity, DivAngle:", \
                      Emin, Emax, nPnts, Power, Energy, Wavelength, Duration, Thickness, Intensity, DivAngle)
            elif SrcMode == 1:
                print("                         ----> Mean and sigma:", \
                      MeanE, SigmaE)
            elif SrcMode == 2:
                print("                         ----> MinE and MaxE:", \
                      MinE, MaxE)

        if SrcMode == 0:
            SrcParam = [SigmaX, SigmaY, MinCTheta, Emin, Emax, nPnts, Power, Energy, Wavelength, Duration, Thickness, Intensity, DivAngle]

        elif SrcMode == 1:
            SrcParam = [SigmaX, SigmaY, MinCTheta, MeanE, SigmaE]

        elif SrcMode == 2:
            SrcParam = [SigmaX, SigmaY, MinCTheta, Emin, Emax]

        Name = BLE.BeamLineElement.getinstances()[0].getName() + ":" \
                       + str(pndsSource["Stage"].iloc[0]) + ":" \
                       + pndsSource["Section"].iloc[0]    + ":" \
                       + pndsSource["Element"].iloc[0]

        if cls.getDebug():
            print("                 <---- Name, SrcMode, SrcParam:", \
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
            print(" BeamLine.addBeamline: empty beam line, return.")
            return
            
        Section    = ""
        NewElement = True
        s         = 0.

        iRefPrtcl = Prtcl.ReferenceParticle.getinstance()
        if not isinstance(iRefPrtcl, Prtcl.ReferenceParticle):
            raise ReferenceParticleNotSpecified()
        p0        = mth.sqrt(np.dot(iRefPrtcl.getPrIn()[0][:3], \
                                    iRefPrtcl.getPrIn()[0][:3]))
        
        for iLine in pndsBeamline.itertuples():
            Name = BLE.BeamLineElement.getinstances()[0].getName() + ":" \
                           + str(iLine.Stage) + ":"  \
                           + iLine.Section    + ":" \
                           + iLine.Element    + ":"

            if iLine.Section != Section:
                Section   = iLine.Section
                nDrift    = 0
                nAperture = 0
                nFquad    = 0
                nDquad    = 0
                nSlnd     = 0
                nGbrLns   = 0
                nDpl      = 0
                nCvty     = 0

            if iLine.Element == "Drift":
                nDrift   += 1
                Name      = Name + str(nDrift)
                Length    = float(iLine.Value)
                rStrt      = np.array([0.,0.,s])
                vStrt      = np.array([0.,0.])
                drStrt     = np.array([0.,0.,0.])
                dvStrt     = np.array([0.,0.])
                if cls.getDebug():
                    print("             ----> Add", Name)
                iBLE = BLE.Drift(Name, \
                             rStrt, vStrt, drStrt, dvStrt, Length)
                cls._Element.append(iBLE)
                s += Length
                refPrtcl    = Prtcl.ReferenceParticle.getinstance()
                refPrtclSet = refPrtcl.setReferenceParticleAtDrift(iBLE)
            elif iLine.Element == "Aperture":
                rStrt  = np.array([0.,0.,s])
                vStrt  = np.array([0.,0.])
                drStrt = np.array([0.,0.,0.])
                dvStrt = np.array([0.,0.])
                if iLine.Type == "Circular":
                    Param = [0, float(iLine.Value)]
                elif iLine.Type == "Elliptical":
                    if NewElement:
                        Param      = [1, float(iLine.Value)]
                        NewElement = False
                        continue
                    else:
                        Param.append(float(iLine.Value))
                        NewElement = True
                nAperture += 1
                Name       = Name + iLine.Type + ":" + str(nAperture)
                if cls.getDebug():
                    print("             ----> Add", Name)
                iBLE = BLE.Aperture(Name, \
                                    rStrt, vStrt, drStrt, dvStrt, Param)
                cls._Element.append(iBLE)
                s += 0.
                refPrtcl    = Prtcl.ReferenceParticle.getinstance()
                refPrtclSet = refPrtcl.setReferenceParticleAtDrift(iBLE)
            elif iLine.Element == "Fquad":
                if iLine.Parameter == "Length":
                    FqL = float(iLine.Value)
                elif iLine.Parameter == "Strength":
                    FqS = float(iLine.Value)
                elif iLine.Parameter == "kq":
                    kq   = float(iLine.Value)
                    Brho = (1/(speed_of_light*1.E-9))*p0/1000.
                    FqS  = kq * Brho
                if NewElement:
                    NewElement = False
                    continue
                else:
                    NewElement = True
                rStrt  = np.array([0.,0.,s])
                vStrt  = np.array([0.,0.])
                drStrt = np.array([0.,0.,0.])
                dvStrt = np.array([0.,0.])
                nFquad += 1
                Name       = Name + str(nFquad)
                if cls.getDebug():
                    print("             ----> Add", Name)
                iBLE = BLE.FocusQuadrupole(Name, \
                                    rStrt, vStrt, drStrt, dvStrt, FqL, FqS)
                cls._Element.append(iBLE)
                s += FqL
                refPrtcl    = Prtcl.ReferenceParticle.getinstance()
                refPrtclSet = refPrtcl.setReferenceParticleAtDrift(iBLE)
            elif iLine.Element == "Dquad":
                if iLine.Parameter == "Length":
                    DqL = float(iLine.Value)
                elif iLine.Parameter == "Strength":
                    DqS = float(iLine.Value)
                elif iLine.Parameter == "kq":
                    kq   = float(iLine.Value)
                    Brho = (1/(speed_of_light*1.E-9))*p0/1000.
                    DqS  = kq * Brho
                if NewElement:
                    NewElement = False
                    continue
                else:
                    NewElement = True
                rStrt  = np.array([0.,0.,s])
                vStrt  = np.array([0.,0.])
                drStrt = np.array([0.,0.,0.])
                dvStrt = np.array([0.,0.])
                nDquad += 1
                Name       = Name + str(nDquad)
                if cls.getDebug():
                    print("             ----> Add", Name)
                iBLE = BLE.DefocusQuadrupole(Name, \
                                    rStrt, vStrt, drStrt, dvStrt, DqL, DqS)
                cls._Element.append(iBLE)
                s += DqL
                refPrtcl    = Prtcl.ReferenceParticle.getinstance()
                refPrtclSet = refPrtcl.setReferenceParticleAtDrift(iBLE)
            elif iLine.Element == "Solenoid":
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
                rStrt   = np.array([0.,0.,s])
                vStrt   = np.array([0.,0.])
                drStrt  = np.array([0.,0.,0.])
                dvStrt  = np.array([0.,0.])
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
                cls._Element.append(BLE.Solenoid(Name, \
                                rStrt, vStrt, drStrt, dvStrt, SlndL, B0) )
                s += SlndL
                refPrtcl    = Prtcl.ReferenceParticle.getinstance()
                refPrtclSet = refPrtcl.setReferenceParticleAtDrift(iBLE)
            elif iLine.Element == "Gabor lens":
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
                rStrt   = np.array([0.,0.,s])
                vStrt   = np.array([0.,0.])
                drStrt  = np.array([0.,0.,0.])
                dvStrt  = np.array([0.,0.])
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
                cls._Element.append(BLE.GaborLens(Name, \
                                rStrt, vStrt, drStrt, dvStrt, \
                                None, None, None, None, GbrLnsL, B0) )
                s += GbrLnsL
                refPrtcl    = Prtcl.ReferenceParticle.getinstance()
                refPrtclSet = refPrtcl.setReferenceParticleAtDrift(iBLE)
            elif iLine.Element == "Dipole":
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
                rStrt   = np.array([0.,0.,s])
                vStrt   = np.array([0.,0.])
                drStrt  = np.array([0.,0.,0.])
                dvStrt  = np.array([0.,0.])
                nDpl   += 1
                Name   += str(nDpl)
                rho     = DplL/DplA
                B       = (1/(speed_of_light*1.E-9))*p0/rho/1000.
                cls._Element.append(BLE.SectorDipole(Name, \
                                rStrt, vStrt, drStrt, dvStrt, DplA, B))
                s += cls._Element[len(cls._Element)-1].getLength()
                refPrtcl    = Prtcl.ReferenceParticle.getinstance()
                refPrtclSet = refPrtcl.setReferenceParticleAtDrift(iBLE)
            elif iLine.Element == "Cavity":
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
                rStrt   = np.array([0.,0.,s])
                vStrt   = np.array([0.,0.])
                drStrt  = np.array([0.,0.,0.])
                dvStrt  = np.array([0.,0.])
                nCvty   += 1
                Name    += str(nCvty)
                cls._Element.append(BLE.CylindricalRFCavity(Name, \
                                    rStrt, vStrt, drStrt, dvStrt, \
                                    CylCvtyGrdnt, CylCvtyFrqncy, CylCvtyPhs))
                s += cls._Element[len(cls._Element)-1].getLength()
                refPrtcl    = Prtcl.ReferenceParticle.getinstance()
                refPrtclSet = refPrtcl.setReferenceParticleAtDrift(iBLE)

            if cls.getDebug():
                print("                 ---->", Name, \
                      "beam line element created.")
                print("                     ----> reference particle:")
                print("                         Position:", \
                      refPrtcl.getRrIn()[0])
                print("                         Momentum:", \
                      refPrtcl.getPrIn()[0])
                print("                 <---- Done.")
        
    def checkConsistency(self):
        ConsChk = False
        s       = 0.
        if self._Element[0].getrStrt()[2] != 0.:
            return
        for iBLE in BLE.BeamLineElement.getinstances():
            if isinstance(iBLE, BLE.Drift):
                s += iBLE.getLength()
            elif isinstance(iBLE, BLE.FocusQuadrupole):
                s += iBLE.getLength()
            elif isinstance(iBLE, BLE.DefocusQuadrupole):
                s += iBLE.getLength()
            elif isinstance(iBLE, BLE.Solenoid):
                s += iBLE.getLength()
            elif isinstance(iBLE, BLE.GaborLens):
                s += iBLE.getLength()
            elif isinstance(iBLE, BLE.SectorDipole):
                s += iBLE.getLength()

        iBLElast = BLE.BeamLineElement.getinstances() \
                            [len(BLE.BeamLineElement.getinstances())-1]
        dif = iBLElast.getrStrt()[2] + iBLElast.getLength() - s

        if abs(dif) > 1E-6:
            return ConsChk

        return True

    @classmethod
    def trackBeam(cls, NEvts=0, ParticleFILE=None):
        if cls.getDebug() or NEvts > 1:
            print(" trackBeam for", NEvts, " events.")
        Scl  = 1
        iCnt = 1

        iRefPrtcl = Prtcl.ReferenceParticle.getinstance()

        for iEvt in range(1, NEvts+1):
            if (iEvt % Scl) == 0:
                if cls.getDebug() or NEvts > 1:
                    print("     ----> Generating event ", iEvt)
                iCnt += 1
                if iCnt == 10:
                    iCnt = 1
                    Scl  = Scl * 10

                
            #.. Create particle instance to store progression through
            #   beam line
            PrtclInst   = Prtcl.Particle()
            if cls.getDebug():
                print("     ----> Created new Particle instance")

            #.. Generate particle:
            if isinstance(cls.getSrcTrcSpc(), np.ndarray):
                if cls.getDebug():
                    print("     ----> Start using:", iEvt)
                Name = BLE.BeamLineElement.getinstances()[0].getName() + ":" \
                       + "Source:User"
                SrcTrcSpc = cls.getSrcTrcSpc()
            else:
                if cls.getDebug():
                    print("     ----> Start by calling getSourceTraceSpace")
                Name = cls.getElement()[1].getName()
                SrcTrcSpc = \
                    cls.getElement()[1].getParticleFromSource()
            Success = PrtclInst.recordParticle(Name, 0., 0., SrcTrcSpc)
            if cls.getDebug():
                print("     ----> Event", iEvt)
                with np.printoptions(linewidth=500,precision=7,suppress=True):
                    print("         ----> trace space at source     :", \
                          SrcTrcSpc)

            #.. Track through beam line:
            TrcSpc_i = SrcTrcSpc
            TrcSpc   = SrcTrcSpc
            if cls.getDebug():
                print("     ----> Transport through beam line")
            iLoc = -1
            for iBLE in BLE.BeamLineElement.getinstances():
                iLoc += 1
                if isinstance(iBLE, BLE.Source) or \
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
                PrtclInst.writeParticle(ParticleFILE)
                Prtcl.Particle.cleanParticles()
                #del PrtclInst
            
            if cls.getDebug():
                print("     <---- Finished handling beam line.")
                
        if cls.getDebug() or NEvts > 1:
            print(" <---- End of this simulation, ", iEvt, \
                  " events generated")


#--------  Exceptions:
class badParameter(Exception):
    pass
                
class badTraceSpaceVector(Exception):
    pass
                
