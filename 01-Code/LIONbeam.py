#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
To do:
 - Add documentation for methods from trackLION
 - Document all class attributes

Class LIONbeam:
===============

  Singleton class to set up the beam lines that define the LION beam line
  facility.


  Class attributes:
  -----------------
   __Debug    : Debug flag
   __SrcTrcSpc: 6D trace space at source (np.ndarray)
__LIONbeamInst: Instance of LIONbeam class.  Set on creation of first
                (and only) instance.

      
  Instance attributes:
  --------------------
   _LIONbeamSpecificationCVSfile : Path to csv file in which beam line is
                                   specified.
            _LIONbeamParamPandas : Pandas data frame instance containing
                                   parameters.
    _Element[] : BeamLineElement : List of beam line elements making up the
                                   LION beam line.
    
  Methods:
  --------
  Built-in methods __new__, __repr__ and __str__.
      __new__ : Creates single instance of LIONbeam class.
      __repr__: One liner with call.
      __str__ : Dump of constants

  Set methods:
      setDebug  : Set debug flag

    setSrcTrcSpc: Set trace space at source.
             Input: np.array([6,]) containing 6D trace space vector.

  Get methods:
     getinstance: Get instance of LION beam class
      getDebug  : get debug flag
getLIONbeamSpecificationCVSfile:
                  Get the path to the csv file specifying the beam line
getLIONbeamParamPandas:
                  Get pandas instance specifying the beam line
      getElement: get list of instances of BeamLineElement objects that make
                  up the LION beam line
    getSrcTrcSpc: get source trace space nd.array(6,)

  Processing method:
      print()   : Dumps parameters
  
  I/o methods:
 getLIONbeamParams: Creates pandas instance with values stored in
                    LION parameters stored in cvs file
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

          trackLION: Tracks through the LION beam line.

Created on Mon 12Jun23: Version history:
----------------------------------------
 1.0: 12Jun23: First implementation

@author: kennethlong
"""

import os
import io
import numpy  as np
import pandas as pnds

import Particle        as Prtcl
import BeamLineElement as BLE

#-------- Physical Constants Instances and Methods ----------------

from PhysicalConstants import PhysicalConstants

constants_instance = PhysicalConstants()
speed_of_light     = constants_instance.SoL()

class LIONbeam(object):
    __LIONbeamInst     = None
    __Debug        = False
    __SrcTrcSpc    = None
    __LIONbeamInst = None


#--------  "Built-in methods":
    def __new__(cls, _LIONbeamSpecificationCVSfile=None):
        if cls.getinstance() is None:
            if cls.getDebug():
                print(' LIONbeam.__new__: ', \
                      'creating the LIONbeam object')
            cls.__LIONbeamInst = super(LIONbeam, cls).__new__(cls)

        #.. Only constants; print values that will be used:
        if cls.getDebug():
            print("     ----> Debug flag: ", cls.getDebug())

        #.. Check and load parameter file
        if _LIONbeamSpecificationCVSfile == None:
            raise Exception( \
                    " LIONbeam.__new__: no parameter file given.")
        
        if not os.path.exists(_LIONbeamSpecificationCVSfile):
            raise Exception( \
                    " LIONbeam.__new__: parameter file does not exist.")
        
        cls._LIONbeamSpecificationCVSfile = \
                               _LIONbeamSpecificationCVSfile
        cls._LIONbeamParamPandas = LIONbeam.csv2pandas( \
                               _LIONbeamSpecificationCVSfile)
        if not isinstance(cls._LIONbeamParamPandas, pnds.DataFrame):
            raise Exception( \
                    " LIONbeam.__new__: pandas data frame invalid.")

        cls._Element = []
                                                                      
        if cls.getDebug():
            print("     ----> Parameter file: ", \
                  cls.getLIONbeamSpecificationCVSfile())
            print("     ----> Dump of pandas paramter list: \n", \
                  cls.getLIONbeamParamPandas())

#.. Build facility:
        if cls.getDebug():
            print("     ----> Build facility:")

#    ----> Source:  --------  --------  --------  --------
        if cls.getDebug():
            print("         ----> Source: ")

        cls.addSource()
        
        if cls.getDebug():
            print("        <---- Source done.")
#    <---- Done source  --------  --------  --------  --------

#    ----> Create reference particle:  --------  --------  --------  --------
#..  Set Name and reference-particle momentum only at this stage:
        cls.setDebug(True)
        if cls.getDebug():
            print("        ----> Create reference particle instance: ")
            
        refPrtcl  = Prtcl.ReferenceParticle()
        p0 = np.array([0., 0., 194.7585262, 1000.])
        refPrtcl.setPrIn(p0)

        if cls.getDebug():
            print("            ----> Reference particle 4-momentum:", \
                  p0)
            print("        <---- Reference particle created. ")
        cls.setDebug(False)
#    <---- Done source  --------  --------  --------  --------

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
                  refPrtclSet)
            print("        <---- Reference particle done. ")
#    <---- Done reference particle -----  --------  --------  --------

        return cls.getinstance()

    def __repr__(self):
        return "LIONbeam()"

    def __str__(self):
        print(" LION beam line set up as follows:")
        print(" =================================")
        print("     ----> Debug flag:", LIONbeam.getDebug())
        print("     ----> Source and beam line:")
        for iBLE in BLE.BeamLineElement.getinstances():
            print("               ", iBLE.SummaryStr())            
        print("     ----> LION beam line is self consistent = ", \
              self.checkConsistency())
        return " <---- LION beam line parameter dump complete."
                
    
#--------  I/o methods:
    def getLIONbeamParams(_filename):
        LIONbeamParams = pnds.read_csv(_filename)
        return LIONbeamParams
    

#--------  "Set methods"
#.. Method believed to be self documenting(!)
    @classmethod
    def setDebug(cls, Debug=False):
        if cls.getDebug():
            print(" LIONbeam.setdebug: ", Debug)
        cls.__Debug = Debug
        
    @classmethod
    def setSrcTrcSpc(cls, SrcTrcSpc=np.array([])):
        if cls.getDebug():
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print(" LIONbeam.setSrcTrcSpc: ", SrcTrcSpc)
        
        if not isinstance(SrcTrcSpc, np.ndarray):
            raise badTraceSpaceVector( \
                        " LIONbeam.setSrcTrcSpc:", SrcTrcSpc)

        if len(SrcTrcSpc) == 0:
            SrcTrcSpc = None
        elif not SrcTrcSpc.size == 6:
            raise badTraceSpaceVector( \
                        " LIONbeam.setSrcTrcSpc:", SrcTrcSpc)

        cls.__SrcTrcSpc = SrcTrcSpc
        
#--------  "Get methods"
#.. Method believed to be self documenting(!)
    @classmethod
    def getinstance(cls):
        return cls.__LIONbeamInst

    @classmethod
    def getDebug(cls):
        return cls.__Debug

    @classmethod
    def getLIONbeamSpecificationCVSfile(cls):
        return cls._LIONbeamSpecificationCVSfile

    @classmethod
    def getLIONbeamParamPandas(cls):
        return cls._LIONbeamParamPandas

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
    def addSource(cls):
        if cls.getDebug():
            print("         LIONbeam.addSource starts:")
            
        #.. Get "sub" pandas data frame with source parameters only:
        pndsSource = cls.getLIONbeamParamPandas()[ \
                       cls.getLIONbeamParamPandas()["Section"] == "Source" \
                                                  ]

        #.. Parse the dataframe to get source parameters:
        SrcMode, SrcParam = cls.parseSource(pndsSource)

        #.. Create the source beam line element:
        rCtr = np.array([0.,0.,0.])
        vCtr = np.array([0.,0.])
        drCtr = np.array([0.,0.,0.])
        dvCtr = np.array([0.,0.])
        Name = "LION:" + str(pndsSource.iloc[0]["Stage"]) + ":"  \
                       + pndsSource.iloc[0]["Section"]    + ":" \
                       + pndsSource.iloc[0]["Element"]
        SourceBLE = BLE.Source(Name, rCtr, vCtr, drCtr, dvCtr, \
                               SrcMode, SrcParam)
        if cls.getDebug():
            print("             <----", Name, \
                  "beam line element created.")

        cls._Element.append(SourceBLE)

    @classmethod
    def parseSource(cls, pndsSource):
        SrcMode  = None
        SrcParam = None
        if cls.getDebug():
            print("             ----> LIONbeam.parseSource starts:")

        SrcMode = int( \
           pndsSource[pndsSource["Parameter"]=="SourceMode"].loc[0]["Value"] \
                       )
        if cls.getDebug():
            print("                 ----> Mode:", SrcMode)
            
        if SrcMode == 0:               #.. Laser driven:
            Emin  = \
             pndsSource[pndsSource["Parameter"]=="Emin"].iloc[0]["Value"]
            Emax = \
             pndsSource[pndsSource["Parameter"]=="Emax"].iloc[0]["Value"]
            nPnts = \
             int(pndsSource[pndsSource["Parameter"]=="nPnts"].iloc[0]["Value"])
            MinCTheta = \
             pndsSource[pndsSource["Parameter"]=="MinCTheta"].iloc[0]["Value"]
        elif SrcMode == 1:               #.. Gaussian:
            MeanE  = \
             pndsSource[pndsSource["Parameter"]=="MeanEnergy"].iloc[0]["Value"]
            SigmaE = \
             pndsSource[pndsSource["Parameter"]=="SigmaEnergy"].iloc[0]["Value"]
            MinCTheta = \
             pndsSource[pndsSource["Parameter"]=="MinCTheta"].iloc[0]["Value"]

        SigmaX  = \
            pndsSource[pndsSource["Parameter"]=="SigmaX"].iloc[0]["Value"]
        SigmaY  = \
            pndsSource[pndsSource["Parameter"]=="SigmaY"].iloc[0]["Value"]

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
            print("         LIONbeam.addBeamline starts:")
            
        #.. Get "sub" pandas data frame with beamline parameters only:
        pndsBeamline = cls.getLIONbeamParamPandas()[ \
                       cls.getLIONbeamParamPandas()["Section"] != "Source" \
                                                  ]
        Section    = ""
        NewElement = True
        s         = 0.
        for iLine in pndsBeamline.itertuples():
            Name = "LION:" + str(iLine.Stage) + ":"  \
                           + iLine.Section    + ":" \
                           + iLine.Element    + ":"

            if iLine.Section != Section:
                Section   = iLine.Section
                nDrift    = 0
                nAperture = 0
                nFquad    = 0
                nDquad    = 0

            if iLine.Element == "Drift":
                nDrift   += 1
                Name      = Name + str(nDrift)
                Length    = iLine.Value
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
                    Param = [0, iLine.Value]
                elif iLine.Type == "Elliptical":
                    if NewElement:
                        Param      = [1, iLine.Value]
                        NewElement = False
                        continue
                    else:
                        Param.append(iLine.Value)
                        NewElement = True
                nAperture += 1
                Name       = Name + iLine.Type + ":" + str(nAperture)
                if cls.getDebug():
                    print("             ----> Add", Name)
                cls._Element.append(BLE.Aperture(Name, \
                                    rCtr, vCtr, drCtr, dvCtr, Param) )
                s += 0.
            elif iLine.Element == "Fquad":
                if iLine.Parameter == "Length":
                    FqL = iLine.Value
                elif iLine.Parameter == "Strength":
                    FqS = iLine.Value
                if NewElement:
                    NewElement = False
                    continue
                else:
                    NewElement = True
                rCtr  = np.array([0.,0.,s+FqL/2.])
                vCtr  = np.array([0.,0.])
                drCtr = np.array([0.,0.,0.])
                dvCtr = np.array([0.,0.])
                nFquad += 1
                Name       = Name + str(nFquad)
                if cls.getDebug():
                    print("             ----> Add", Name)
                cls._Element.append(BLE.FocusQuadrupole(Name, \
                                    rCtr, vCtr, drCtr, dvCtr, FqL, FqS) )
                s += FqL
            elif iLine.Element == "Dquad":
                if iLine.Parameter == "Length":
                    DqL = iLine.Value
                elif iLine.Parameter == "Strength":
                    DqS = iLine.Value
                if NewElement:
                    NewElement = False
                    continue
                else:
                    NewElement = True
                rCtr  = np.array([0.,0.,s+DqL/2.])
                vCtr  = np.array([0.,0.])
                drCtr = np.array([0.,0.,0.])
                dvCtr = np.array([0.,0.])
                nDquad += 1
                Name       = Name + str(nDquad)
                if cls.getDebug():
                    print("             ----> Add", Name)
                cls._Element.append(BLE.DefocusQuadrupole(Name, \
                                    rCtr, vCtr, drCtr, dvCtr, DqL, DqS) )
                s += DqL
        
    def checkConsistency(self):
        ConsChk = False
        s       = 0.
        if self._Element[0].getrCtr()[2] != 0.:
            return
        for iBLE in BLE.BeamLineElement.getinstances():
            if isinstance(iBLE, BLE.Drift):
                s += iBLE.getLength()
            elif isinstance(iBLE, BLE.FocusQuadrupole):
                s += iBLE.getLength()
            elif isinstance(iBLE, BLE.DefocusQuadrupole):
                s += iBLE.getLength()

        iBLElast = BLE.BeamLineElement.getinstances() \
                            [len(BLE.BeamLineElement.getinstances())-1]
        dif = (iBLElast.getrCtr()[2] + iBLElast.getLength()/2.) - s

        if abs(dif) > 1E-6:
            return ConsChk

        return True

    @classmethod
    def trackLION(cls, NEvts=0, ParticleFILE=None):
        if cls.getDebug() or NEvts > 1:
            print(" trackLION for", NEvts, " events.")
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
                Name = "LION:0:Source:User"
                SrcTrcSpc = cls.getSrcTrcSpc()
            else:
                if cls.getDebug():
                    print("     ----> Start by calling getSourceTraceSpace")
                Name = cls.getElement()[0].getName()
                SrcTrcSpc = \
                    cls.getElement()[0].getParticleFromSource()
            Success = PrtclInst.recordParticle(Name, 0., 0., SrcTrcSpc)
            if cls.getDebug():
                print("     ----> Event", iEvt)
                with np.printoptions(linewidth=500,precision=7,suppress=True):
                    print("         ----> trace space at source     :", \
                          SrcTrcSpc)

            Mmtm = np.sqrt(2.*938.27208816*SrcTrcSpc[5])
            Brho = (1/(speed_of_light*1.E-9))*Mmtm/1000.

            #.. Track through beam line:
            TrcSpc_i = SrcTrcSpc
            TrcSpc   = SrcTrcSpc
            HlfLngth = 0.
            if cls.getDebug():
                print("     ----> Transport through beam line")
            for iBLE in BLE.BeamLineElement.getinstances():
                if isinstance(iBLE, BLE.Source):
                    continue
                if cls.getDebug():
                    print("         ---->", iBLE.getName())
                HlfLngth = iBLE.getLength() / 2.
                if isinstance(iBLE, BLE.FocusQuadrupole) or \
                   isinstance(iBLE, BLE.DefocusQuadrupole):
                    TrcSpc     = iBLE.Transport(TrcSpc_i, Brho)
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
                
class badTraceSpaceVector(Exception):
    pass
                
