#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class BeamIO:
=============

  Class provides management of file handling and i/o for the Beam
  package.

  Class attributes:
  -----------------
    instances : List of instances of Particle class
  __Debug     : Debug flag

      
      Input arguments:
      ----------------
        _datafilePATH : Path to directory containing (or to contain, if
                        _create is True) data file
        _datafileNAME : Full path to data file, or, name of data file in
                        directory defined by _datafilePATH
              _create : If True, file to be created.
           _BDSIMfile : If True, read file in BDSIM format.


  Instance attributes:
  --------------------
   All instance attributes are initialised to Null

            _dataFile : Data file to be read or written;
           _Rd1stRcrd : Boolean, True, if first record has been read from
                        _dataFile.
     _dataFILEversion : _dataFILEversion version of data file being read:
                  = 1 : First version, does not have geometry record as
                        first record in file.
                 >= 2 : Has geometry as first record in file.
                 >= 3 : Also has repo version stored in _repoVERSION
                 >= 4 : Include drStrt and dvStrt for beam line elements
                 >= 5 : Convert dvStrt to Euler angles
         _repoVERSION : [ [tagNAME, tagDATETIME],
                          [commitSTRING, commitDATETIME] ]
           _BDSIMfile : If True, read file in BDSIM format.

  Methods:
  --------
  Built-in methods __init__, __repr__ and __str__.
      __init__ : Creates instance of beam-line element class.
      __repr__: One liner with call.
      __str__ : Dump of constants

        print: Print all attributes.

  setAll2None: Set all instance attributes to None.
        No input or return.

  Set methods:
     setDebug: set class debug flag
           Input: bool, True/False
          Return: None

     setpathFILE, setdataFILE, setReadFirstRecord, setdataFILEversion,
     setcreate, setBDSIMfile

  Get methods:
     getDebug: returns class debug flag
          Return: Boolean

 getinstances: return list of instances of BeamIO class.

     getpathFILE, getdataFILE, getReadFirstRecord, getdataFILEversion,
     getcreate, getBDSIMfile

  Processing methods:
    readBeamDataRecord: Read a record from the file.
              No input; returns Boolean "end of file"

         readVersion: Read version from file, returns version (string)

   flushNclosedataFile: Flush data in buffer not yet written and close
                        data file.
          Input: dataFILE : io.BufferedWriter : file being written

  Utilities:
    resetBeamInsances:
               Sets cls.instances []

     cleanBeamIOfiles:
                Removes instances of class.


"""

import io
import os
import struct as strct
import numpy  as np
import math   as mth

import BeamLine as BL
import Particle as Prtcl
import PhysicalConstants as PhysCnst
import LhARALinearOptics as LLO

constants_instance = PhysCnst.PhysicalConstants()
protonMASS         = constants_instance.mp()

class BeamIO:
    instances = []
    __Debug   = False

#--------  "Built-in methods":
    def __init__(self, _datafilePATH=None, _datafileNAME=None, \
                 _create=False, _BDSIMfile=False):
        if self.getDebug():
            print(' BeamIO.__init__: ', \
                  'creating BeamIO object')

        BeamIO.instances.append(self)

        self.setAll2None()

        #.. Sanity checks on i/p arguments:
        if not isinstance(_create, bool):
            raise badCreate( \
                         " BeamIO.__init__: bad create flag")

        if _datafilePATH == None and _datafileNAME == None:
            raise noPATH( \
                         " BeamIO.__init__: neither path or file name set.")
        
        elif _datafileNAME == None: 
            raise noNAME( \
                    " BeamIO.__init__: file name not set.")

        #.. Check path and, if necessary, join to file:
        if _datafilePATH != None:
            if not os.path.exists(_datafilePATH):
                raise noPATH( \
                    " Particle.createParticleFile: path does not exist.")

            pathFILE = os.path.join(_datafilePATH, _datafileNAME)

        else:
            pathFILE = _datafileNAME
            
        self.setpathFILE(pathFILE)

        if self.getDebug():
            print("     ----> Proceed with data file:", pathFILE)

        #.. open file; if file doesnt exist and _create is true, create it:
        #if not os.path.isfile(pathFILE) or _create:
        self.setcreate(_create)
        self.setBDSIMfile(_BDSIMfile)
        if _create:
            if not self.getBDSIMfile():
                dataFILE = open(pathFILE, "wb")
                self.setdataFILE(dataFILE)
                if self.getDebug():
                    print("         ----> File opened for write.")
                
                self.writeFIRSTword()
                self.writeVersion("BeamIO v5")
                self.writeREPOversion()
                
            else:
                dataFILE = open(pathFILE, "w")
                self.setdataFILE(dataFILE)
                if self.getDebug():
                    print("         ----> File opened for write.")

        else:
            if self.getBDSIMfile():
                dataFILE = open(pathFILE, "r")
            else:
                dataFILE = open(pathFILE, "rb")
            if self.getDebug():
                print("         ----> File opened for read.")
            self.setdataFILE(dataFILE)

        if self.getDebug():
            print("     <---- File ready.")

        
        if self.__Debug:
            print("     ----> New BeamIO instance: \n", \
                  BeamIO.__str__(self))
            print(" <---- BeamIO instance created.")
            
    def __repr__(self):
        return "BeamIO(<data file path>, <data file name>)"

    def __str__(self):
        self.print()
        return " <---- BeamIO __str__ done. \n"

    def print(self):
        print("\n BeamIO:")
        print(" -------")
        print("     ----> Debug flag:", self.getDebug())
        print("     ----> Data file:", self.getdataFILE())
        print("     ---->    Create:", self.getcreate())
        print("     ----> BDSIMfile:", self.getBDSIMfile())

        
#--------  "Set method" only Debug
#.. Method believed to be self documenting(!)

    @classmethod
    def setDebug(cls, Debug=False):
        if cls.__Debug:
            print(" BeamIO.setdebug: ", Debug)
        cls.__Debug = Debug
        
    def setAll2None(self):
        self._dataFile        = None
        self._Rd1stRcrd       = False
        self._dataFILEversion = None
        self._create          = None
        self._BDSIMfile       = None

    def setpathFILE(self, _pathFILE):
        self._pathFILE = _pathFILE

    def setdataFILE(self, _dataFILE):
        self._dataFILE = _dataFILE

    def setReadFirstRecord(self, _Rd1stRcrd):
        if not isinstance(_Rd1stRcrd, bool):
            raise badArgument()
        self._Rd1stRcrd = _Rd1stRcrd 

    def setdataFILEversion(self, dataFILEversion):
        if not isinstance(dataFILEversion, int):
            raise badArgument()
        self._dataFILEversion = dataFILEversion

    def setcreate(self, _create):
        if not isinstance(_create, bool):
            raise badArgument()
        self._create = _create

    def setBDSIMfile(self, _BDSIMfile):
        if not isinstance(_BDSIMfile, bool):
            raise badArgument()
        self._BDSIMfile = _BDSIMfile

        
#--------  "Get methods" only; version, reference, and constants
#.. Methods believed to be self documenting(!)
    @classmethod
    def getDebug(cls):
        return cls.__Debug

    @classmethod
    def getinstances(cls):
        return cls.instances

    def getpathFILE(self):
        return self._pathFILE

    def getdataFILE(self):
        return self._dataFILE

    def getReadFirstRecord(self):
        return self._Rd1stRcrd

    def getdataFILEversion(self):
        return self._dataFILEversion

    def getcreate(self):
        return self._create

    def getBDSIMfile(self):
        return self._BDSIMfile

    
#--------  Processing methods:


#--------  I/o methods:
#.. Manage read:
    def readBeamDataRecord(self):
        if self.getDebug():
            print(" BeamIO.readBeamDataRecord starts.")
            print("     ----> Read first record:", \
                  self.getReadFirstRecord())

        if not isinstance(self.getdataFILE(), io.BufferedReader) and \
           not isinstance(self.getdataFILE(), io.TextIOWrapper):
            raise noFILE( \
                          " BeamIO.readBeamDataRecord: " + \
                          str(self.getdataFILE()) + \
                          " file does not exist.")

        EoF = False

        #.. Deal with BDSIM file read first:
        if self.getBDSIMfile():
            record = self.getdataFILE().readline()
            if record == '':
                EoF = True
                return EoF
            
            record = record.lstrip()
            record = record.rstrip('\n')
            TrcSpc = np.asarray(record.split(' '), dtype=float)
            iRefPrtcl = Prtcl.ReferenceParticle.getinstances()
            E0        = iRefPrtcl.getPrOut()[0][3]
            p0        = mth.sqrt(E0**2 - protonMASS**2)
            TrcSpc[5] = (1000.*TrcSpc[5] - E0) / p0
            
            iPrtcl = Prtcl.Particle()
            iPrtcl.recordParticle('Source', 0., 0., TrcSpc)
            if self.getDebug():
                print("     <---- ", \
                      "BeamIO.readBeamDataRecord BDSIM particle read.")
                print(" <---- BeamIO.readBeamDataRecord Done.")

            return EoF

        #.. First record identifies first version of data format:
        if not self.getReadFirstRecord():
            brecord = self.getdataFILE().read(4)
            if brecord == b'':
                if self.getDebug():
                    print(" <---- end of file, return.")
                return True
            
            self.setReadFirstRecord(True)
            record = strct.unpack(">i", brecord)
            nId    = record[0]
            if self.getDebug():
                print("     ----> Id number:", nId)
                
            Version = "Version 1"
            self.setdataFILEversion(1)
            if nId == 9999:
                if self.getDebug():
                    print("           Not version 1!")
                Version  = self.readVersion()
                nVersion = int(Version[-1])
                self.setdataFILEversion(nVersion)
                if self.getDebug():
                    print("           Version:", \
                          self.getdataFILEversion())
                if nVersion >= 3:
                    repoVERSION = self.readREPOversion()

                if self.getDebug():
                    print(" BeamIO.readBeamDataRecord:", \
                          "reading data file version", Version)
                    
                BL.BeamLine.readBeamLine(self.getdataFILE())

            else:
                if self.getDebug():
                    print("           Handle version 1!")
                self.getdataFILE().seek(0)
                #EoF = Prtcl.Particle.readParticle(self.getdataFILE())
                
            if self.getDebug():
                print("     <---- Data file format version:", \
                      self.getdataFILEversion())
        else:
            EoF = Prtcl.Particle.readParticle(self.getdataFILE())
            if self.getDebug():
                print("     <---- BeamIO.readBeamDataRecord particle read.")
            
        if self.getDebug():
            print(" <---- BeamIO.readBeamDataRecord Done.")

        return EoF

    def writeFIRSTword(self):
        dataFILE = self.getdataFILE()
        
        record = strct.pack(">i", 9999)
        dataFILE.write(record)
        if self.getDebug():
            print("         ----> First word:", \
                  strct.unpack(">i", record), \
                  " is a large integer to distinguish v2, v3... from v1")

    def writeVersion(self, versionSTR=None):
        if not isinstance(versionSTR, str):
            raise badArgument()

        dataFILE = self.getdataFILE()
        
        bversionSTR = bytes(versionSTR, 'utf-8')
        
        record      = strct.pack(">i", len(versionSTR))
        dataFILE.write(record)
        if self.getDebug():
            print("         ----> Length of version record:", \
                  strct.unpack(">i", record))
            
        record   = bversionSTR
        dataFILE.write(record)
        if self.getDebug():
            print("         ----> Version:", \
                  bversionSTR.decode('utf-8'))
            
    def readVersion(self):
        if self.getDebug():
            print(" BeamIO.readVersion start.")

        brecord = self.getdataFILE().read(4)
        record  = strct.unpack(">i", brecord)
        len     = record[0]
        if self.getDebug():
            print("         ----> Length of version:", len)
            
        brecord  = self.getdataFILE().read(len)
        Version = brecord.decode('utf-8')
        if self.getDebug():
            print(" <---- Version:", Version)

        return Version

    def writeREPOversion(self):
        dataFILE = self.getdataFILE()

        repoVRSN = LLO.version()
        if self.getDebug():
            print("         ----> BeamIO.writeREPOversion: \n",
                   "              Version list:", repoVRSN)

        bTAG = bytes(repoVRSN[0][0], 'utf-8')
        bTIM = bytes(repoVRSN[0][1], 'utf-8')

        record = strct.pack(">i", len(repoVRSN[0][0]))
        dataFILE.write(record)
        if self.getDebug():
            print("             ----> Length of tag:", \
                  strct.unpack(">i", record))

        record = bTAG
        dataFILE.write(record)
        if self.getDebug():
            print("             ----> Tag:", \
                  bTAG.decode('utf-8'))
            
        record  = strct.pack(">i", len(repoVRSN[0][1]))
        dataFILE.write(record)
        if self.getDebug():
            print("             ----> Length of time string:", \
                  strct.unpack(">i", record))
        
        record = bTIM
        dataFILE.write(record)
        if self.getDebug():
            print("             ----> Time:", \
                  bTIM.decode('utf-8'))
            
        bCMMT = bytes(repoVRSN[1][0], 'utf-8')
        bTIM  = bytes(repoVRSN[1][1], 'utf-8')
        
        record  = strct.pack(">i", len(repoVRSN[1][0]))
        dataFILE.write(record)
        if self.getDebug():
            print("             ----> Length of commit record:", \
                  strct.unpack(">i", record))
        
        record = bCMMT
        dataFILE.write(record)
        if self.getDebug():
            print("             ----> Commit:", \
                  bCMMT.decode('utf-8'))
            
        record  = strct.pack(">i", len(repoVRSN[1][1]))
        dataFILE.write(record)
        if self.getDebug():
            print("             ----> Length of time string:", \
                  strct.unpack(">i", record))
        
        record = bTIM
        dataFILE.write(record)
        if self.getDebug():
            print("             ----> Time:", \
                  bTIM.decode('utf-8'))
            
        if self.getDebug():
            print("         <---- BeamIO.writeREPOversion: Done.")

    def readREPOversion(self):
        if self.getDebug():
            print(" BeamIO.readrepoVERSION start.")
            
        dataFILE = self.getdataFILE()

        brecord = dataFILE.read(4)
        record  = strct.unpack(">i", brecord)
        len     = record[0]
        if self.getDebug():
            print("     ----> Length of Tag:", len)
            
        brecord = dataFILE.read(len)
        TAG     = brecord.decode('utf-8')
        if self.getDebug():
            print("         ----> Tag:", TAG)

        brecord = dataFILE.read(4)
        record  = strct.unpack(">i", brecord)
        len     = record[0]
        if self.getDebug():
            print("     ----> Length of time:", len)
            
        brecord = dataFILE.read(len)
        TAGtim     = brecord.decode('utf-8')
        if self.getDebug():
            print("         ----> Time:", TAGtim)

        brecord = dataFILE.read(4)
        record  = strct.unpack(">i", brecord)
        len     = record[0]
        if self.getDebug():
            print("     ----> Length of commit:", len)
            
        brecord = dataFILE.read(len)
        CMMT     = brecord.decode('utf-8')
        if self.getDebug():
            print("         ----> Commit:", CMMT)

        brecord = dataFILE.read(4)
        record  = strct.unpack(">i", brecord)
        len     = record[0]
        if self.getDebug():
            print("     ----> Length of time:", len)
            
        brecord = dataFILE.read(len)
        CMMTtim = brecord.decode('utf-8')
        if self.getDebug():
            print("         ----> Time:", CMMTtim)

        repoVERSION = [ \
                        [TAG, TAGtim], [CMMT, CMMTtim] \
                       ]
        
        if self.getDebug():
            print(" <----> repoVERSION:", repoVERSION)

        return repoVERSION

#.. Flush and close
    def flushNclosedataFile(self, dataFILE=None):
        if self.getDebug():
            print(" BeamIO.flushNclosedataFile starts")
            print("     ----> File:", dataFILE)

        if not isinstance(dataFILE, io.BufferedWriter):
            raise noFILE( \
                    " BeamIO.flushNcloseParticle: file does not exist.")

        dataFILE.flush()
        dataFILE.close()


#--------  Utilities:
    @classmethod
    def resetinstances(cls):
        cls.instances = []
        
    @classmethod
    def cleanBeamIOfiles(cls):
        DoneOK = False
        
        for iIOfl in cls.getinstances():
            del iIOfl
            
        cls.resetinstances()
        DoneOK = True

        return DoneOK

    
#--------  Exceptions:
class noPATH(Exception):
    pass

class noNAME(Exception):
    pass

class noFILE(Exception):
    pass
        
class badCreate(Exception):
    pass

class badArgument(Exception):
    pass
        
