#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
To do:
 - Add documentation for methods from trackDRACO
 - Document all class attributes

Class DRACObeam:
================

  Singleton class to set up the beam lines that define the DRACO beam line
  facility.


  Class attributes:
  -----------------
    __Debug    : Debug flag
    __SrcTrcSpc: 6D trace space at source (np.ndarray)
__DRACObeamInst: Instance of DRACObeam class.  Set on creation of first
                 (and only) instance.

      
  Instance attributes:
  --------------------
   _DRACObeamSpecificationCVSfile : Path to csv file in which beam line is
                                   specified.
            _DRACObeamParamPandas : Pandas data frame instance containing
                                   parameters.
    _Element[] : BeamLineElement : List of beam line elements making up the
                                   DRACO beam line.
    
  Methods:
  --------
  Built-in methods __new__, __repr__ and __str__.
      __new__ : Creates single instance of DRACObeam class.
      __repr__: One liner with call.
      __str__ : Dump of constants

  Set methods:
      setDebug  : Set debug flag

    setSrcTrcSpc: Set trace space at source.
             Input: np.array([6,]) containing 6D trace space vector.

  Get methods:
     getinstance: Get instance of DRACO beam class
      getDebug  : get debug flag
getDRACObeamSpecificationCVSfile:
                  Get the path to the csv file specifying the beam line
getDRACObeamParamPandas:
                  Get pandas instance specifying the beam line
      getElement: get list of instances of BeamLineElement objects that make
                  up the DRACO beam line
    getSrcTrcSpc: get source trace space nd.array(6,)

  Processing method:
      print()   : Dumps parameters
  
  I/o methods:
 getDRACObeamParams: Creates pandas instance with values stored in
                     DRACO parameters stored in cvs file
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

          trackDRACO: Tracks through the DRACO beam line.

Created on Mon 12Jun23: Version history:
----------------------------------------
 1.0: 28Sep23: First implementation

@author: kennethlong
"""

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
speed_of_light     = constants_instance.SoL()
mu0                = constants_instance.mu0()
protonMASS         = constants_instance.mp()

class DRACObeam(object):
    __DRACObeamInst     = None
    __Debug        = False
    __SrcTrcSpc    = None
    __DRACObeamInst = None


#--------  "Built-in methods":
    def __new__(cls, _DRACObeamSpecificationCVSfile=None):
        if cls.getinstance() is None:
            if cls.getDebug():
                print(' DRACObeam.__new__: ', \
                      'creating the DRACObeam object')
            cls.__DRACObeamInst = super(DRACObeam, cls).__new__(cls)

        #.. Only constants; print values that will be used:
        if cls.getDebug():
            print("     ----> Debug flag: ", cls.getDebug())

        #.. Check and load parameter file
        if _DRACObeamSpecificationCVSfile == None:
            raise Exception( \
                    " DRACObeam.__new__: no parameter file given.")
        
        if not os.path.exists(_DRACObeamSpecificationCVSfile):
            raise Exception( \
                    " DRACObeam.__new__: parameter file does not exist.")
        
        cls._DRACObeamSpecificationCVSfile = \
                               _DRACObeamSpecificationCVSfile
        cls._DRACObeamParamPandas = DRACObeam.csv2pandas( \
                               _DRACObeamSpecificationCVSfile)
        if not isinstance(cls._DRACObeamParamPandas, pnds.DataFrame):
            raise Exception( \
                    " DRACObeam.__new__: pandas data frame invalid.")

        cls._Element = []
                                                                      
        if cls.getDebug():
            print("     ----> Parameter file: ", \
                  cls.getDRACObeamSpecificationCVSfile())
            print("     ----> Dump of pandas paramter list: \n", \
                  cls.getDRACObeamParamPandas())

#.. Build facility:
        if cls.getDebug():
            print("     ----> Build facility:")

#    ----> Facility:  --------  --------  --------  --------
        if cls.getDebug():
            print("         ----> Facility: ")

        cls.addFacility()
        
        if cls.getDebug():
            print("        <---- Facility done.")
#    <---- Done facility  --------  --------  --------  --------

#    ----> Source:  --------  --------  --------  --------
        if cls.getDebug():
            print("         ----> Source: ")

        cls.addSource()
        
        if cls.getDebug():
            print("        <---- Source done.")
#    <---- Done source  --------  --------  --------  --------

#    ----> Create reference particle:  --------  --------  --------  --------
#..  Set Name and reference-particle momentum only at this stage:
        if cls.getDebug():
            print("        ----> Create reference particle instance: ")
            
        refPrtcl  = Prtcl.ReferenceParticle()
        p0        = cls.getElement()[0].getp0()
        Ref4mmtm  = np.array([0., 0., p0,
                       mth.sqrt(p0**2 + protonMASS**2)])
        Success = refPrtcl.setPrIn(Ref4mmtm)
        if not Success:
            raise fail2createfacility()
        
        if cls.getDebug():
            print("            ----> Reference particle 4-momentum:", \
                  p0, Success)
            print("        <---- Reference particle created. ")
        cls.setDebug(False)
#    <---- Done reference particle  --------  --------  --------  --------

#    ----> Beam line:  --------  --------  --------  --------
        if cls.getDebug():
            print("         ----> Beam line: ")

        cls.addBeamline()
        
        if cls.getDebug():
            print("        <---- Beam line done.")
#    <---- Done beam line  --------  --------  --------  --------

#    ----> Reference particle:  --------  --------  --------  --------
        if cls.getDebug():
            print("        ----> Reference particle: ")

        refPrtclSet = refPrtcl.setReferenceParticle()

        if cls.getDebug():
            print("            ----> Reference particle set, success:", \
                  refPrtcl)
            print("        <---- Reference particle done. ")
#    <---- Done reference particle -----  --------  --------  --------

        return cls.getinstance()

    def __repr__(self):
        return "DRACObeam()"

    def __str__(self):
        print(" DRACO beam line set up as follows:")
        print(" =================================")
        print("     ----> Debug flag:", DRACObeam.getDebug())
        print("     ----> Source and beam line:")
        for iBLE in BLE.BeamLineElement.getinstances():
            print("               ", iBLE.SummaryStr())            
        print("     ----> DRACO beam line is self consistent = ", \
              self.checkConsistency())
        return " <---- DRACO beam line parameter dump complete."
                
    
#--------  I/o methods:
    def getDRACObeamParams(_filename):
        DRACObeamParams = pnds.read_csv(_filename)
        return DRACObeamParams
    

#--------  "Set methods"
#.. Method believed to be self documenting(!)
    @classmethod
    def setDebug(cls, Debug=False):
        if cls.getDebug():
            print(" DRACObeam.setdebug: ", Debug)
        cls.__Debug = Debug
        
    @classmethod
    def setSrcTrcSpc(cls, SrcTrcSpc=np.array([])):
        if cls.getDebug():
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print(" DRACObeam.setSrcTrcSpc: ", SrcTrcSpc)
        
        if not isinstance(SrcTrcSpc, np.ndarray):
            raise badPhaseSpaceVector( \
                        " DRACObeam.setSrcTrcSpc:", SrcTrcSpc)

        if len(SrcTrcSpc) == 0:
            SrcTrcSpc = None
        elif not SrcTrcSpc.size == 6:
            raise badPhaseSpaceVector( \
                        " DRACObeam.setSrcTrcSpc:", SrcTrcSpc)

        cls.__SrcTrcSpc = SrcTrcSpc
        
#--------  "Get methods"
#.. Method believed to be self documenting(!)
    @classmethod
    def getinstance(cls):
        return cls.__DRACObeamInst

    @classmethod
    def getDebug(cls):
        return cls.__Debug

    @classmethod
    def getDRACObeamSpecificationCVSfile(cls):
        return cls._DRACObeamSpecificationCVSfile

    @classmethod
    def getDRACObeamParamPandas(cls):
        return cls._DRACObeamParamPandas

    @classmethod
    def getElement(cls):
        return cls._Element
    
    @classmethod
    def getSrcTrcSpc(cls):
        return cls.__SrcTrcSpc
    
        
#--------  Processing methods:
    def csv2pandas(_filename):
        ParamsPandas = pnds.read_csv(_filename)
        return ParamsPandas
        
    @classmethod
    def addFacility(cls):
        if cls.getDebug():
            print("         DRACObeam.addFacility starts:")
            
        #.. Get "sub" pandas data frame with Facility parameters only:
        pndsFacility = cls.getDRACObeamParamPandas()[ \
                       cls.getDRACObeamParamPandas()["Section"] == "Facility" \
                                                  ]

        #.. Parse the dataframe to get Facility parameters:
        Name, K0 = cls.parseFacility(pndsFacility)

        #.. Create the Facility beam line element:
        rCtr  = np.array([0., 0., 0.])
        vCtr  = np.array([0., 0., 0.])
        drCtr = np.array([0., 0., 0.])
        dvCtr = np.array([0., 0., 0.])

        p0    = mth.sqrt( (protonMASS+K0)**2 - protonMASS**2)

        FacilityBLE = BLE.Facility(Name, rCtr, vCtr, drCtr, dvCtr, \
                                   p0)
        if cls.getDebug():
            print("             <----", Name, \
                  "beam line element created.")


        cls._Element.append(FacilityBLE)

    @classmethod
    def addSource(cls):
        if cls.getDebug():
            print("         DRACObeam.addSource starts:")
            
        #.. Get "sub" pandas data frame with source parameters only:
        pndsSource = cls.getDRACObeamParamPandas()[ \
                       cls.getDRACObeamParamPandas()["Section"] == "Source" \
                                                  ]

        #.. Parse the dataframe to get source parameters:
        SrcMode, SrcParam = cls.parseSource(pndsSource)

        #.. Create the source beam line element:
        rCtr = np.array([0.,0.,0.])
        vCtr = np.array([0.,0.])
        drCtr = np.array([0.,0.,0.])
        dvCtr = np.array([0.,0.])
        Name = "DRACO:" + str(pndsSource.iloc[0]["Stage"]) + ":"  \
                       + pndsSource.iloc[0]["Section"]    + ":" \
                       + pndsSource.iloc[0]["Element"]
        SourceBLE = BLE.Source(Name, rCtr, vCtr, drCtr, dvCtr, \
                               SrcMode, SrcParam)
        if cls.getDebug():
            print("             <----", Name, \
                  "beam line element created.")

        cls._Element.append(SourceBLE)

    @classmethod
    def parseFacility(cls, pndsSource):
        cls.setDebug(True)
        if cls.getDebug():
            print("         DRACObeam.addFacility starts:")
            
        #.. Get "sub" pandas data frame with facility parameters only:
        pndsFacility = cls.getDRACObeamParamPandas()[ \
                       cls.getDRACObeamParamPandas()["Section"] == "Facility" \
                                                  ]
        print(pndsFacility)
        
        Name  = None
        p0    = None
        if cls.getDebug():
            print("             ----> DRACObeam.parseFacility starts:")

        Name = str( \
            pndsFacility[pndsFacility["Parameter"]=="Name"].loc[0]["Value"] \
                   )
        K0   = float( \
                      pndsFacility[pndsFacility["Parameter"]== \
                     "Kinetic energy"].iloc[0]["Value"] \
                   )
        
        if cls.getDebug():
            print("                 ----> Name, K0:", Name, K0)

        return Name, K0

    @classmethod
    def parseSource(cls, pndsSource):
        SrcMode  = None
        SrcParam = None
        if cls.getDebug():
            print("             ----> DRACObeam.parseSource starts:")

        SrcMode = int( \
           pndsSource[pndsSource["Parameter"]=="SourceMode"].iloc[0]["Value"] \
                       )
        if cls.getDebug():
            print("                 ----> Mode:", SrcMode)
            
        if SrcMode == 0:               #.. Laser driven:
            Emin  = float( \
             pndsSource[pndsSource["Parameter"]=="Emin"].iloc[0]["Value"])
            Emax = float( \
             pndsSource[pndsSource["Parameter"]=="Emax"].iloc[0]["Value"])
            nPnts = \
             int(pndsSource[pndsSource["Parameter"]=="nPnts"].iloc[0]["Value"])
            MinCTheta = float( \
             pndsSource[pndsSource["Parameter"]=="MinCTheta"].iloc[0]["Value"])
        elif SrcMode == 1:               #.. Gaussian:
            MeanE  = float( \
             pndsSource[pndsSource["Parameter"]=="MeanEnergy"].iloc[0]["Value"])
            SigmaE = float( \
             pndsSource[pndsSource["Parameter"]=="SigmaEnergy"].iloc[0]["Value"])
            MinCTheta = float( \
             pndsSource[pndsSource["Parameter"]=="MinCTheta"].iloc[0]["Value"])

        SigmaX  = float( \
            pndsSource[pndsSource["Parameter"]=="SigmaX"].iloc[0]["Value"])
        SigmaY  = float( \
            pndsSource[pndsSource["Parameter"]=="SigmaY"].iloc[0]["Value"])

        if cls.getDebug():
            print("                     ----> SigmaX, SigmaY:", SigmaX, SigmaY)
            if SrcMode == 0:
                print("                     ----> Emin, Emax, nPnts:", \
                      Emin, Emax, nPnts)
            elif SrcMode == 1:
                print("                     ----> Mean and sigma:", \
                      MeanE, SigmaE)
            print("                     ----> Min cos(Theta):", MinCTheta)
            
        if SrcMode == 0:
            SrcParam = [SigmaX, SigmaY, MinCTheta, Emin, Emax, nPnts]

        elif SrcMode == 1:
            SrcParam = [SigmaX, SigmaY, MinCTheta, MeanE, SigmaE]

        return SrcMode, SrcParam

    @classmethod
    def addBeamline(cls):
        if cls.getDebug():
            print("         DRACObeam.addBeamline starts:")
            
        #.. Get "sub" pandas data frame with beamline parameters only:
        pndsBeamline = cls.getDRACObeamParamPandas()[ \
                       cls.getDRACObeamParamPandas()["Section"] != "Source" \
                                                  ]
        Section    = ""
        NewElement = True
        s         = 0.
        for iLine in pndsBeamline.itertuples():
            Name = "DRACO:" + str(iLine.Stage) + ":"  \
                           + iLine.Section    + ":" \
                           + iLine.Element    + ":"

            if iLine.Section != Section:
                Section   = iLine.Section
                nDrift    = 0
                nAperture = 0
                nSlnd     = 0

            if iLine.Element == "Drift":
                nDrift   += 1
                Name     += str(nDrift)
                Length    = float(iLine.Value)
                rCtr      = np.array([0.,0.,s+Length/2.])
                vCtr      = np.array([0.,0.])
                drCtr     = np.array([0.,0.,0.])
                dvCtr     = np.array([0.,0.])
                if cls.getDebug():
                    print("             ----> Add", Name)
                cls._Element.append(BLE.Drift(Name, \
                             rCtr, vCtr, drCtr, dvCtr, Length))
                s += Length
            elif iLine.Element == "Aperture":
                rCtr  = np.array([0.,0.,s])
                vCtr  = np.array([0.,0.])
                drCtr = np.array([0.,0.,0.])
                dvCtr = np.array([0.,0.])
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
                Name      += iLine.Type + ":" + str(nAperture)
                if cls.getDebug():
                    print("             ----> Add", Name)
                cls._Element.append(BLE.Aperture(Name, \
                                    rCtr, vCtr, drCtr, dvCtr, Param) )
                s += 0.
            elif iLine.Element == "Solenoid":
                if NewElement:
                    if iLine.Type == "Length, layers and turns":
                        nLnsSlnd = 4
                        iLnSlnd  = 1
                if iLine.Parameter == "Length":
                    SlndL = float(iLine.Value)
                elif iLine.Parameter == "Current":
                    SlndI = float(iLine.Value)
                elif iLine.Parameter == "Layers":
                    SlndLy = float(iLine.Value)
                elif iLine.Parameter == "Turns":
                    SlndT = float(iLine.Value)
                if iLnSlnd < nLnsSlnd:
                    iLnSlnd += 1
                    NewElement = False
                    continue
                else:
                    NewElement = True
                rCtr   = np.array([0.,0.,s+SlndL/2.])
                vCtr   = np.array([0.,0.])
                drCtr  = np.array([0.,0.,0.])
                dvCtr  = np.array([0.,0.])
                nSlnd += 1
                Name  += str(nSlnd)
                nTrns  = float(SlndLy) * float(SlndT)
                B0     = mu0*nTrns*SlndI/SlndL
                nSlnd += 1
                if cls.getDebug():
                    print("             ----> Add", Name)
                cls._Element.append(BLE.Solenoid(Name, \
                                     rCtr, vCtr, drCtr, dvCtr, SlndL, B0) )
                s += SlndL
        
    def checkConsistency(self):
        ConsChk = False
        s       = 0.
        if self._Element[0].getrCtr()[2] != 0.:
            return
        for iBLE in BLE.BeamLineElement.getinstances():
            if isinstance(iBLE, BLE.Drift):
                s += iBLE.getLength()
            elif isinstance(iBLE, BLE.Solenoid):
                s += iBLE.getLength()

        iBLElast = BLE.BeamLineElement.getinstances() \
                            [len(BLE.BeamLineElement.getinstances())-1]
        dif = (iBLElast.getrCtr()[2] + iBLElast.getLength()/2.) - s

        if abs(dif) > 1E-6:
            return ConsChk

        return True

    @classmethod
    def trackDRACO(cls, NEvts=0, ParticleFILE=None):
        if cls.getDebug() or NEvts > 1:
            print(" trackDRACO for", NEvts, " events.")
        Scl  = 1
        iCnt = 1

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
                Name = "DRACO:0:Source:User"
                SrcTrcSpc = cls.getSrcTrcSpc()
            else:
                if cls.getDebug():
                    print("     ----> Start by calling getSourcePhaseSpace")
                Name = cls.getElement()[0].getName()
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
            HlfLngth = 0.
            if cls.getDebug():
                print("     ----> Transport through beam line")
            for iBLE in BLE.BeamLineElement.getinstances():
                if isinstance(iBLE, BLE.Source) or \
                   isinstance(iBLE, BLE.Facility):
                    continue
                if cls.getDebug():
                    print("         ---->", iBLE.getName())
                HlfLngth = iBLE.getLength() / 2.
                if isinstance(iBLE, BLE.Solenoid):
                    TrcSpc     = iBLE.Transport(TrcSpc_i)
                else:
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
                    zEnd    = iBLE.getrCtr()[2] + HlfLngth
                    Success = PrtclInst.recordParticle(iBLE.getName(), \
                                                       zEnd, \
                                                       zEnd, \
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
                
class badPhaseSpaceVector(Exception):
    pass
                
