#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class Particle:
===============

  Instance of particle class is record of particle travelling through the
  beamm line.


  Class attributes:
  -----------------
    instances : List of instances of Particle class
  __Debug     : Debug flag

      
  Instance attributes:
  --------------------
   All instance attributes are initialised to Null
   _Location[] :   str   : Name of location where phase space recorded
   _z[]        : float   : z coordinate at which phase space recorded
   _s[]        : float   : s coordinate at which phase space recorded
   _PhsSpc[]   : ndarray : 6D phase space: x, x', y, y', t, E (m, s, MeV)

***   _SourcePhaseSpace: numpy array of 6-dimensional phase space
    
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

  resetParticleInsances:
               Sets cls.instances []

  setAll2None: Set all instance attributes to None.
        No input or return.

  setLocation: str : Set location string at which phase-space is stored.

         setz: float : Set z coordinate at which phase-space is stored.

         sets: float : Set s coordinate at which phase-space is stored.

setPhaseSpace: np.ndarray(6,) : phase space 6 floats

recortParticle: i/p: Location, s, z, PhaseSpace:
                calls, setLocation, setz, sets, setPhaseSpace in turn
                to store all variables.

  setSourcePhaseSpace: set phase space after source
           Input: numpy.array(6,); 6D phase to store
          Return: Success: bool, True if stored OK.


  Get methods:
      getDebug, getParticleInstances, getLocation, getz, gets, 
      getPhaseSpace
          -- thought to be self documenting!

  Processing method:
    cleanParticles : Deletes all particle instances and resets list of
                     particles.
         No input; Returns bool flag, True means all good.

 plotPhaseSpaceProgression: create plots showing standard summary of
                            progression through beam line
         No input or return

          printProgression: print progression through the beamline
         No input or return

  I/o methods:
     createParticleFile: create a file in which to store particle events.
          Input: datafilePATH: os PATH to directory containing datafile
                               TO BE WRITTEN
                 datafileNAME: file name for data file TO BE WRITTEN
         Return: ParticleFILE full path to NEW file to which events will be
                 written

    writeParticle: Write one particle to datafile.
          Input: particleFILE full path to file to which event will be
                 written

      flushNcloseParticleFile: Flush and close file.
          Input: ParticleFILE full path to NEW file to which events will be
                 written

      openParticleFile: Open file from which particle events will be
                               read

     readParticle: Read particle from ParticleFILE
          Input: particleFILE full path to file to which event will be
                 read
         Return: OK flag: True ==> event read fine

  closeParticleFile: Close particle file being read.
          Input: particleFILE full path to file from which events were
                 read


  Exceptions:
    badParticle, badParameter, noPATH, noNAME, noFILE


Created on Mon 03Jul23: Version history:
----------------------------------------
 1.0: 12Jun23: First implementation

@author: kennethlong
"""

import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import struct            as strct
import numpy             as np
import os
import io

import BeamLineElement   as BLE

class Particle:
    instances  = []
    __Debug    = False


#--------  "Built-in methods":
    def __init__(self):
        if self.__Debug:
            print(' Particle.__init__: ', \
                  'creating the Particle object')

        Particle.instances.append(self)

        #.. Particle instance created with phase-space at each
        #   interface being recorded as None
        self.setAll2None()

        if self.__Debug:
            print("     ----> New Particle instance: \n", \
                  Particle.__str__(self))
            print(" <---- Particle instance created.")
            
    def __repr__(self):
        return "Particle()"

    def __str__(self):
        print(" Particle:")
        print(" ---------")
        print("     ----> Debug flag:", self.getDebug())
        print("     ----> Number of phase-space records:", \
              len(self.getLocation()))
        if len(self.getLocation()) > 0:
            print("     ----> Record of phase space:")
        for iLctn in range(len(self.getLocation())):
            print("         ---->", self.getLocation()[iLctn], ":")
            print("             ----> z, s", self.getz()[iLctn], \
                                             self.gets()[iLctn])
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print("             ----> Phase space:", \
                      self.getPhaseSpace()[iLctn])
        return " <---- Particle parameter dump complete."

    
#--------  "Set method" only Debug
#.. Method believed to be self documenting(!)

    @classmethod
    def setDebug(cls, Debug=False):
        if cls.__Debug:
            print(" Particle.setdebug: ", Debug)
        cls.__Debug = Debug

    @classmethod
    def resetParticleInstances(cls):
        cls.instances = []
        
    def setAll2None(self):
        self._Location = []
        self._z        = []
        self._s        = []
        self._PhsSpc   = []
        
    def setLocation(self, Location):
        Success = False
        if isinstance(Location, str):
            self._Location.append(Location)
            Success = True
        return Success

    def setz(self, z):
        Success = False
        if isinstance(z, float):
            self._z.append(z)
            Success = True
        return Success

    def sets(self, s):
        Success = False
        if isinstance(s, float):
            self._s.append(s)
            Success = True
        return Success

    def setPhaseSpace(self, PhaseSpace):
        Success = False
        if isinstance(PhaseSpace, np.ndarray):
            self._PhsSpc.append(PhaseSpace)
            Success = True
        return Success

    def recordParticle(self, Location, z, s, PhaseSpace):
        Success = self.setLocation(Location)
        if Success:
            Success = self.setz(z)
        if Success:
            Success = self.sets(s)
        if Success:
            Success = self.setPhaseSpace(PhaseSpace)
        return Success

    def setSourcePhaseSpace(self, PhaseSpace):
        Success = self.setLocation("Source")
        if Success:
            Success = self.setz(0.)
        if Success:
            Success = self.sets(0.)
        if Success:
            Success = self.setPhaseSpace(PhaseSpace)
        return Success

    
#--------  "Get methods" only; version, reference, and constants
#.. Methods believed to be self documenting(!)

    @classmethod
    def getDebug(cls):
        return cls.__Debug

    @classmethod
    def getParticleInstances(cls):
        return cls.instances

    def getLocation(self):
        return self._Location
    
    def getz(self):
        return self._z
    
    def gets(self):
        return self._s
    
    def getPhaseSpace(self):
        return self._PhsSpc
    
    
#--------  Utilities:
    @classmethod
    def cleanParticles(cls):
        DoneOK = False
        
        for iPrtcl in cls.getParticleInstances():
            del iPrtcl
            
        cls.resetParticleInstances()
        DoneOK = True

        return DoneOK
    
    @classmethod
    def plotPhaseSpaceProgression(cls):

        font = {'family': 'serif', \
                'color':  'darkred', \
                'weight': 'normal', \
                'size': 16, \
                }
        
        xLoc  = []
        xpLoc = []
        yLoc  = []
        ypLoc = []
        ELoc  = []
        for iPrtcl in cls.getParticleInstances():
            iLoc = -1
            for iPhsSpc in iPrtcl.getPhaseSpace():
                iLoc += 1
                if iLoc > (len(xLoc)-1):
                    xLoc.append([])
                    xpLoc.append([])
                    yLoc.append([])
                    ypLoc.append([])
                    ELoc.append([])

                xLoc[iLoc].append(iPrtcl.getPhaseSpace()[iLoc][0])
                xpLoc[iLoc].append(iPrtcl.getPhaseSpace()[iLoc][1])
                yLoc[iLoc].append(iPrtcl.getPhaseSpace()[iLoc][2])
                ypLoc[iLoc].append(iPrtcl.getPhaseSpace()[iLoc][3])
                ELoc[iLoc].append(iPrtcl.getPhaseSpace()[iLoc][5])

        for iLoc in range(len(xLoc)):
            fig, axs = plt.subplots(nrows=2, ncols=2)
            fig, axs = plt.subplots(ncols=2, nrows=2, figsize=(6., 6.), \
                                    layout="constrained")
            # add an artist, in this case a nice label in the middle...
            for row in range(2):
                for col in range(2):
                    axs[row, col].annotate( \
                            f'axs[{row}, {col}]', (0.5, 0.5),  \
                            transform=axs[row, col].transAxes, \
                            ha='center', va='center', fontsize=18, \
                            color='darkgrey')
            Ttl = BLE.BeamLineElement.getinstances()[iLoc].getName()
            fig.suptitle(Ttl, fontdict=font)

            #axs[0, 0].set_title('x,y')
            axs[0, 0].hist2d(xLoc[iLoc], yLoc[iLoc], bins=100)
            axs[0, 0].set_xlabel('x (m)')
            axs[0, 0].set_ylabel('y (m)')
            
            #axs[0, 1].set_title('Energy')
            axs[0, 1].hist(ELoc[iLoc], 100)
            axs[0, 1].set_xlabel('Energy (MeV)')
            axs[0, 1].set_ylabel('Number')
            
            #axs[1, 0].set_title('x, xprime')
            axs[1, 0].hist2d(xLoc[iLoc], xpLoc[iLoc], bins=100)
            axs[1, 0].set_xlabel('x (m)')
            axs[1, 0].set_ylabel('xprime (m)')

            #axs[1, 1].set_title('y, yprime')
            axs[1, 1].hist2d(yLoc[iLoc], ypLoc[iLoc], bins=100)
            axs[1, 1].set_xlabel('y (m)')
            axs[1, 1].set_ylabel('yprime (m)')

        
            plotFILE = '99-Scratch/ParticleProgressionPlot' + \
                str(iLoc) + '.pdf'
            plt.savefig(plotFILE)
            plt.close()
            

    def printProgression(self):
        for iLoc in range(len(self.getLocation())):
            with np.printoptions(linewidth=500,precision=5,suppress=True):
                print(self.getLocation()[iLoc], ": z, s, phase space:", \
                      self.getz()[iLoc], self.gets()[iLoc], \
                      self.getPhaseSpace()[iLoc])

    
#--------  I/o methods:
#                     ----> Write instances:
    @classmethod
    def createParticleFile(cls, datafilePATH=None, datafileNAME=None):
        if cls.getDebug():
            print("Particle.createParticleFile:", datafilePATH, datafileNAME)
            
        if datafilePATH == None:
            raise noPATH( \
                         " Particle.createParticleFile: no path given.")
        
        if datafileNAME == None:
            raise noNAME( \
                    " Particle.createParticleFile: no file name given.")

        if not os.path.exists(datafilePATH):
            raise noPATH( \
                    " Particle.createParticleFile: path does not exist.")
        
        ParticleFILE = open(os.path.join(datafilePATH, datafileNAME), "wb")

        if cls.getDebug():
            print("     ----> File created:", ParticleFILE)

        return ParticleFILE

    def writeParticle(self, ParticleFILE=None):
        if self.getDebug():
            print("Particle.writeParticle starts.")

        if not isinstance(ParticleFILE, io.BufferedWriter):
            raise noFILE( \
                    " Particle.writeParticle: file does not exist.")

        nLoc = len(self.getLocation())
        if self.getDebug():
            print("     ----> Number of locations to store:", nLoc)
        record = strct.pack(">i", nLoc)
        ParticleFILE.write(record)
        
        for iLoc in range(len(self.getLocation())):
            bLocation = bytes(self.getLocation()[iLoc], 'utf-8')
            
            record    = strct.pack(">i", len(bLocation))
            ParticleFILE.write(record)
            if self.getDebug():
                print("         ----> Length of bLocation:", \
                      strct.unpack(">i", record))
            
            record = bLocation
            ParticleFILE.write(record)
            
            if self.getDebug():
                print("         ----> Location:", bLocation.decode('utf-8'))

            
            record = strct.pack(">8d",                           \
                                self.getz()[iLoc],               \
                                self.gets()[iLoc],               \
                                self.getPhaseSpace()[iLoc][0],   \
                                self.getPhaseSpace()[iLoc][1],   \
                                self.getPhaseSpace()[iLoc][2],   \
                                self.getPhaseSpace()[iLoc][3],   \
                                self.getPhaseSpace()[iLoc][4],   \
                                self.getPhaseSpace()[iLoc][5])
            ParticleFILE.write(record)
            if self.getDebug():
                print("         ----> z, s, phase space:", \
                      strct.unpack(">8d",record))
        
        Cleaned = self.cleanParticles()
        
    @classmethod
    def flushNcloseParticleFile(cls, ParticleFILE=None):
        if cls.getDebug():
            print("Particle.flushNcloseParticleFile starts")

        if not isinstance(ParticleFILE, io.BufferedWriter):
            raise noFILE( \
                    " Particle.flushNcloseParticle: file does not exist.")

        ParticleFILE.flush()
        ParticleFILE.close()
#                     ----> Write instances:
    @classmethod
    def openParticleFile(cls, datafilePATH=None, datafileNAME=None):
        if cls.getDebug():
            print("Particle.openParticleFile:", datafilePATH, datafileNAME)
            
        if datafilePATH == None:
            raise noPATH( \
                         " Particle.openParticleFile: no path given.")
        
        if datafileNAME == None:
            raise noNAME( \
                    " Particle.openParticleFile: no file name given.")

        if not os.path.exists(datafilePATH):
            raise noPATH( \
                    " Particle.openParticleFile: path does not exist.")
        
        ParticleFILE = open(os.path.join(datafilePATH, datafileNAME), "rb")

        if cls.getDebug():
            print("     ----> File opened:", ParticleFILE)

        return ParticleFILE

    @classmethod
    def readParticle(cls, ParticleFILE=None):
        if cls.getDebug():
            print("Particle.readParticle starts.")

        if not isinstance(ParticleFILE, io.BufferedReader):
            raise noFILE( \
                    " Particle.writeParticle: file does not exist.")

        brecord = ParticleFILE.read(4)
        if brecord == b'':
            if cls.getDebug():
                print(" <---- end of file, return.")
            return True
        
        record  = strct.unpack(">i", brecord)
        nLoc    = record[0]
        if cls.getDebug():
            print("     ----> Number of locations to read:", nLoc)
        if nLoc > 0:
            iPrtcl = Particle()

        for iLoc in range(nLoc):
            brecord = ParticleFILE.read(4)
            record  = strct.unpack(">i", brecord)
            len     = record[0]
            if cls.getDebug():
                print("         ----> Length of bLocation:", len)
            
            brecord  = ParticleFILE.read(len)
            Location = brecord.decode('utf-8')
            if cls.getDebug():
                print("         ----> Location:", Location)

            brecord = ParticleFILE.read((8*8))
            record  = strct.unpack(">8d", brecord)
            z       = float(record[0])
            s       = float(record[1])
            PhsSpc = np.array([                  \
                               float(record[2]), \
                               float(record[3]), \
                               float(record[4]), \
                               float(record[5]), \
                               float(record[6]), \
                               float(record[7])] )
            if cls.getDebug():
                print("         ----> z, s, phase space:", z, s, PhsSpc)

            iPrtcl.recordParticle(Location, z, s, PhsSpc)

        if cls.getDebug():
            print("     <---- Particle instsance")
            print(iPrtcl)
            print(" <---- readParticle done.")
            
        return False        
        
    @classmethod
    def closeParticleFile(cls, ParticleFILE=None):
        if cls.getDebug():
            print("Particle.closeParticleFile starts")

        if not isinstance(ParticleFILE, io.BufferedReader):
            raise noFILE( \
                    " Particle.closeParticle: file does not exist.")

        ParticleFILE.close()

            
#--------  Exceptions:
class badParticle(Exception):
    pass

class badParameter(Exception):
    pass

class noPATH(Exception):
    pass

class noNAME(Exception):
    pass

class noFILE(Exception):
    pass

