#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
To do:
 - Add documentation for methods from trackLhARA
 LhARAcument all class attributes

Class BeamLine:
===============

  Singleton class to set up the beam line defined in the beam-line
  specification file.


  Class attributes:
  -----------------
   __Debug    : Debug flag
   __SrcPhsSpc: 6D phase space at source (np.ndarray)
__BeamLineInst: Instance of BeamLine class.  Set on creation of first
                (and only) instance.

      
  Instance attributes:
  --------------------
   _BeamLineSpecificationCVSfile : Path to csv file in which beam line is
                                   specified.
            _BeamLineParamPandas : Pandas data frame instance containing
                                   parameters.
    _Element[] : BeamLineElement : List of beam line elements making up the
                                   LhARA beam line.
    
  Methods:
  --------
  Built-in methods __new__, __repr__ and __str__.
      __new__ : Creates single instance of BeamLine class.
      __repr__: One liner with call.
      __str__ : Dump of constants

  Set methods:
      setDebug  : Set debug flag

    setSrcPhsSpc: Set phase space at source.
             Input: np.array([6,]) containing 6D phase space vector.

  Get methods:
     getinstance: Get instance of LhARA beam class
      getDebug  : get debug flag
getBeamLineSpecificationCVSfile:
                  Get the path to the csv file specifying the beam line
getBeamLineParamPandas:
                  Get pandas instance specifying the beam line
      getElement: get list of instances of BeamLineElement objects that make
                  up the LhARA beam line
    getSrcPhsSpc: get source phase space nd.array(6,)

  Processing method:
      print()   : Dumps parameters
  
  I/o methods:
 getBeamLineParams: Creates pandas instance with values stored in
                    LhARA parameters stored in cvs file
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

          trackLhARA: Tracks through the LhARA beam line.

Created on Mon 02Oct23: Version history:
----------------------------------------
 2.0: 11Dec23: Refactor to make code generate beamline based on input
               specificaiton file and not tie it to LhARA or another
               hard-coded facility.
 1.0: 02Oct23: First implementation

@author: rehanahrazak
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

class BeamLine(object):
    __BeamLineInst = None
    __Debug        = False
    __SrcPhsSpc    = None
    __BeamLineInst = None


#--------  "Built-in methods":
    def __new__(cls, _BeamLineSpecificationCVSfile=None):
        if cls.getinstance() is None:
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

#    ----> Beam line:  --------  --------  --------  --------
        if cls.getDebug():
            print("         ----> Beam line: ")

        cls.addBeamline()
        
        if cls.getDebug():
            print("        <---- Beam line done.")
#    <---- Done beam line  --------  --------  --------  --------

        return cls.getinstance()

    def __repr__(self):
        return "BeamLine()"

    def __str__(self):
        print(" LhARA beam line set up as follows:")
        print(" =================================")
        print("     ----> Debug flag:", BeamLine.getDebug())
        print("     ----> Source and beam line:")
        for iBLE in BLE.BeamLineElement.getinstances():
            print("               ", iBLE.SummaryStr())            
        print("     ----> LhARA beam line is self consistent = ", \
              self.checkConsistency())
        return " <---- LhARA beam line parameter dump complete."
                
    
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
    def setSrcPhsSpc(cls, SrcPhsSpc=np.array([])):
        if cls.getDebug():
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print(" BeamLine.setSrcPhsSpc: ", SrcPhsSpc)
        
        if not isinstance(SrcPhsSpc, np.ndarray):
            raise badPhaseSpaceVector( \
                        " BeamLine.setSrcPhsSpc:", SrcPhsSpc)

        if len(SrcPhsSpc) == 0:
            SrcPhsSpc = None
        elif not SrcPhsSpc.size == 6:
            raise badPhaseSpaceVector( \
                        " BeamLine.setSrcPhsSpc:", SrcPhsSpc)

        cls.__SrcPhsSpc = SrcPhsSpc
        
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
    def getSrcPhsSpc(cls):
        return cls.__SrcPhsSpc
    
        
#--------  Processing methods:
    def csv2pandas(_filename):
        ParamsPandas = pnds.read_csv(_filename)
        return ParamsPandas
        
    @classmethod
    def addFacility(cls):
        if cls.getDebug():
            print("         BeamLine.addFacility starts:")

        #.. Get "sub" pandas data frame with Facility parameters only:
        pndsFacility = cls.getBeamLineParamPandas()[ \
                       cls.getBeamLineParamPandas()["Section"] == "Facility" \
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
            print("         BeamLine.addSource starts:")
            
        #.. Get "sub" pandas data frame with source parameters only:
        pndsSource = cls.getBeamLineParamPandas()[ \
                       cls.getBeamLineParamPandas()["Section"] == "Source" \
                                                  ]

        #.. Parse the dataframe to get source parameters:
        SrcMode, SrcParam = cls.parseSource(pndsSource)

        #.. Create the source beam line element:
        rCtr = np.array([0.,0.,0.])
        vCtr = np.array([0.,0.])
        drCtr = np.array([0.,0.,0.])
        dvCtr = np.array([0.,0.])
        Name = "LhARA:" + str(pndsSource.iloc[0]["Stage"]) + ":"  \
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
            print("         BeamLine.addFacility starts:")
            
        #.. Get "sub" pandas data frame with facility parameters only:
        pndsFacility = cls.getBeamLineParamPandas()[ \
                       cls.getBeamLineParamPandas()["Section"] == "Facility" \
                                                  ]
        print(pndsFacility)
        
        Name  = None
        p0    = None
        if cls.getDebug():
            print("             ----> BeamLine.parseFacility starts:")

        Name = str( \
            pndsFacility[pndsFacility["Parameter"]=="Name"].loc[0]["Value"] \
                   )
        K0   = float( \
                      pndsFacility[ \
                        (pndsFacility["Parameter"]=="Reference particle") & \
                        (pndsFacility["Name"]=="Kinetic energy") ]. \
                            iloc[0]["Value"] \
                    )
        
        if cls.getDebug():
            print("                 ----> Name, K0:", Name, K0)

        return Name, K0

    @classmethod
    def parseSource(cls, pndsSource):
        SrcMode  = None
        SrcParam = None
        if cls.getDebug():
            print("             ----> BeamLine.parseSource starts:")

        SrcMode = int( \
           pndsSource[pndsSource["Name"]=="SourceMode"].loc[0]["Value"] \
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
            print("         BeamLine.addBeamline starts:")
            
        #.. Get "sub" pandas data frame with beamline parameters only:
        pndsBeamline = cls.getBeamLineParamPandas()[ \
                       cls.getBeamLineParamPandas()["Section"] != "Source" \
                                                  ]
        Section    = ""
        NewElement = True
        s         = 0.
        for iLine in pndsBeamline.itertuples():
            Name = "LhARA:" + str(iLine.Stage) + ":"  \
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
    def trackLhARA(cls, NEvts=0, ParticleFILE=None):
        if cls.getDebug() or NEvts > 1:
            print(" trackLhARA for", NEvts, " events.")
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
            if isinstance(cls.getSrcPhsSpc(), np.ndarray):
                if cls.getDebug():
                    print("     ----> Start using:", iEvt)
                Name = "LhARA:0:Source:User"
                SrcPhsSpc = cls.getSrcPhsSpc()
            else:
                if cls.getDebug():
                    print("     ----> Start by calling getSourcePhaseSpace")
                Name = cls.getElement()[0].getName()
                SrcPhsSpc = \
                    cls.getElement()[0].getParticleFromSource()
            Success = PrtclInst.recordParticle(Name, 0., 0., SrcPhsSpc)
            if cls.getDebug():
                print("     ----> Event", iEvt)
                with np.printoptions(linewidth=500,precision=7,suppress=True):
                    print("         ----> Phase space at source     :", \
                          SrcPhsSpc)

            Mmtm = np.sqrt(2.*938.27208816*SrcPhsSpc[5])
            Brho = (1/(speed_of_light*1.E-9))*Mmtm/1000.

            #.. Track through beam line:
            PhsSpc_i = SrcPhsSpc
            PhsSpc   = SrcPhsSpc
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
                    PhsSpc     = iBLE.Transport(PhsSpc_i, Brho)
                else:
                    PhsSpc     = iBLE.Transport(PhsSpc_i)
                if cls.getDebug():
                    with np.printoptions(\
                                linewidth=500,precision=7,suppress=True):
                        print("             ----> Updated phase space   :", \
                              PhsSpc)
                if not isinstance(PhsSpc, np.ndarray):
                    if cls.getDebug():
                        print("              ---->", \
                              " partice outside acceptance(1)")
                    break
                else:
                    zEnd    = iBLE.getrCtr()[2] + HlfLngth
                    Success = PrtclInst.recordParticle(iBLE.getName(), \
                                                       zEnd, \
                                                       zEnd, \
                                                       PhsSpc)
                PhsSpc_i = PhsSpc

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
                
