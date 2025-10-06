#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class Particle:
===============

  Instance of particle class is record of particle travelling through the
  beam line.

  Derived classes:
  ----------------
   ReferenceParticle: Reference particle derived class to record passage of
                      reference particle through the lattice.


  Class attributes:
  -----------------
    instances : List of instances of Particle class
 __Debug     : Debug flag

      
  Instance attributes:
  --------------------
   All instance attributes are initialised to Null
   _Species    :   str   : Species, has to be in list in PhysicalConstants.
   _Location[] :   str   : Name of location where trace space recorded
   _z[]        : float   : z coordinate at which trace space recorded
   _s[]        : float   : s coordinate at which trace space recorded
   _TrcSpc[]   : ndarray : 6D trace space: x, x', y, y', z, delta, all
                           in reference particle local coordinates
   _PhsSpc[]   : array   : RPLC 6D phase space: [(x, y, z), (px, py, pz)]
                           List ot two ndarrays.
   _LabPhsSpc[]: array   : Lab 6D phase space: [(x, y, z), (px, py, pz)]
                           List ot two ndarrays.

***   _SourceTraceSpace: numpy array of 6-dimensional trace space
    
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

setTraceSpace: np.ndarray(6,) : trace space 6 floats

setRPLCPhaseSpace: [np.ndarray(3,), np.ndarray(3,)]: two three vectors

setLabPhaseSpace: [np.ndarray(3,), np.ndarray(3,)]: two three vectors

recordParticle: i/p: Location, s, z, TraceSpace:
                calls, setLocation, setz, sets, setTraceSpace in turn
                to store all variables.

  setSourceTraceSpace: set trace space after source
           Input: numpy.array(6,); 6D phase to store
          Return: Success: bool, True if stored OK.


  Get methods:
      getDebug, getinstances, getLocation, getz, gets, 
      getTraceSpace, getRPLCPhaseSpace, getPhaseSpace
          -- thought to be self documenting!

  Processing methods:
    cleanParticles : Deletes all particle instances and resets list of
                     particles.
         No input; Returns bool flag, True means all good.

 plotTraceSpaceProgression: create plots showing standard summary of
                            progression through beam line
         No input or return

          printProgression: print progression through the beamline
         No input or return

   fillPhaseSpaceAll: Class method, no arguments.  Fills RPLC and Lab
          phase-space attrutes for all particle
               Returns: Success: Book=l, True if success.

      fillPhaseSpace: fill phase space (RPLC and Lab) for "self"
               Returns: Success: Book=l, True if success.

   calcRPLCPhaseSpace: Calculate RPLC phase space from trace space
          I/p: Location numner, starting from 0
      Returns: Success: Book=l, True if success.


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
 1.1: 21Mar24: Add particle species, can be proton, muon or pion. proton is default 

@author: kennethlong
"""

from copy import deepcopy
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import struct            as strct
import random            as rnd
import numpy             as np
import math              as mth
import os
import io
import sys

import Particle          as Prtcl
import BeamLine          as BL
import BeamLineElement   as BLE
import PhysicalConstants as PhysCnstnts

#-------- Physical Constants Instances and Methods ----------------
from PhysicalConstants import PhysicalConstants

iPhysclCnstnts = PhysicalConstants()


class Particle:
    instances  = []
    __Debug    = False

    stable_species   = {"proton", "neutrino"}
    unstable_species = {"pion", "muon"}
            
#--------  "Built-in methods":
    def __init__(self, _species="proton"):
        #.. Must have reference particle as first in the instance list,
        #   ... so ...
        if not isinstance(ReferenceParticle.getinstances("All")[0], \
                          ReferenceParticle):
            raise noReferenceParticle(" Reference particle, ", \
                                      "not first in particle list.")

        Particle.instances.append(self)
        
        #.. Particle instance created with phase-space at each
        #   interface being recorded as None
        self.setAll2None()

        self.setSpecies(_species)
        
        if self.__Debug:
            print("     ----> New Particle instance: \n", \
                  Particle.__str__(self))
            print(" <---- Particle instance created.")
            
    def __repr__(self):
        return "Particle()"

    def __str__(self):
        self.print()
        return " Particle __str__ done."

    def print(self):
        try:
            tst = self.getLocation()
        except:
            print("\n Particle: type:", type(self), \
                  "Particle attributes not yet initialsed.")
            return " <---- Particle parameter dump complete."
            
        print("\n Particle: ", self.getSpecies(), "  mass: ", \
              iPhysclCnstnts.getparticleMASS(self.getSpecies()))
        print(" ---------")
        print("     ----> Debug flag:", self.getDebug())
        print("     ---->    Species:", self.getSpecies())
        print("     ----> Number of phase-space records:", \
              len(self.getLocation()))
        if len(self.getLocation()) > 0:
            print("     ----> Record of trace space:")
        for iLctn in range(len(self.getLocation())):
            print("         ---->", self.getLocation()[iLctn], ":")
            print("             ----> z, s", self.getz()[iLctn], \
                                             self.gets()[iLctn])
            try:
                print("             ----> ", \
              BLE.BeamLineElement.getinstances()[iLctn+1].getName(), \
                      "; length ", \
              BLE.BeamLineElement.getinstances()[iLctn+1].getLength())
            except:
                print("             ----> ", \
                    BLE.BeamLineElement.getinstances()[iLctn+1].getName(), \
                      "; has no length ")
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print("             ---->     trace space:", \
                      self.getTraceSpace()[iLctn])
            if len(self.getRPLCPhaseSpace()) == 0:
                print("             ---->     phase space: not yet filled")
            else:
                with np.printoptions(linewidth=500,precision=7,\
                                     suppress=True):
                    print("             ---->     phase space:", \
                          self.getRPLCPhaseSpace()[iLctn])
            if len(self.getLabPhaseSpace()) == 0:
                print("             ----> Lab phase space: not yet filled")
            else:
                with np.printoptions(linewidth=500,precision=7,\
                                     suppress=True):
                    print("             ----> Lab phase space:", \
                          self.getLabPhaseSpace()[iLctn])
        return " <---- Particle parameter dump complete."

    
#--------  "Set method" only Debug
#.. Method believed to be self documenting(!)

    @classmethod
    def setDebug(cls, Debug=False):
        if cls.__Debug:
            print(" Particle.setDebug: ", Debug)
        cls.__Debug = Debug

    @classmethod
    def resetParticleInstances(cls):
        if len(cls.instances) > 0:
            iRefPrtcl     = cls.instances[0]
            cls.instances = []
            cls.instances.append(iRefPrtcl)
        
    def setAll2None(self):
        self._Species           = None
        self._Location          = []
        self._z                 = []
        self._s                 = []
        self._TrcSpc            = []
        self._PhsSpc            = []
        self._LabPhsSpc         = []
        self._RemainingLifetime = mth.inf

    def setRemainingLifetime(self, _RemainingLifetime):
        self._RemainingLifetime = _RemainingLifetime

    def setSpecies(self, _Species):
        if not isinstance(_Species, str):
            raise badParameter("Particle.__init__: Species " + \
                               _Species + " not a string!")
        if _Species.lower() in iPhysclCnstnts.getSpecies():
            self._Species = _Species.lower()
            pass
        else:
            raise badParameter("Particle.__init__: Species " + \
                               _Species + " not allowed!")

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

    def setTraceSpace(self, TraceSpace):
        Success = False
        if isinstance(TraceSpace, np.ndarray):
            self._TrcSpc.append(TraceSpace)
            Success = True
        return Success

    def setRPLCPhaseSpace(self, PhaseSpace):
        Success = False
        self._PhsSpc.append(PhaseSpace)
        Success = True

        return Success

    def setLabPhaseSpace(self, PhaseSpace):
        Success = False
        self._LabPhsSpc.append(PhaseSpace)
        Success = True

        return Success

    def recordParticle(self, Location, z, s, TraceSpace):
        Success = self.setLocation(Location)
        if Success:
            Success = self.setz(z)
        if Success:
            Success = self.sets(s)
        if Success:
            Success = self.setTraceSpace(TraceSpace)
        return Success

    def setSourceTraceSpace(self, TraceSpace):
        Success = self.setLocation("Source")
        if Success:
            Success = self.setz(0.)
        if Success:
            Success = self.sets(0.)
        if Success:
            Success = self.setTraceSpace(TraceSpace)
        return Success

    
#--------  "Get methods" only; version, reference, and constants
#.. Methods believed to be self documenting(!)

    @classmethod
    def getDebug(cls):
        return cls.__Debug

    @classmethod
    def getinstances(cls):
        return cls.instances

    def getRemainingLifetime(self):
        return self._RemainingLifetime
    
    def getSpecies(self):
        return self._Species
            
    def getLocation(self):
        return self._Location
    
    def getz(self):
        return self._z
    
    def gets(self):
        return self._s
    
    def getTraceSpace(self):
        return self._TrcSpc
    
    def getRPLCPhaseSpace(self):
        return self._PhsSpc
    
    def getLabPhaseSpace(self):
        return deepcopy(self._LabPhsSpc)

            
#--------  Processing methods:
    @staticmethod
    def createParticle():
        if Particle.getDebug():
            print(" Particle.createParticle:", \
                  "start.")
            print("     ----> Primary particle species:", 
                  BL.BeamLine.getcurrentReferenceParticle().getSpecies())

        species = BL.BeamLine.getcurrentReferenceParticle().getSpecies()
        if   species == "proton":     iPrtcl = proton()
        elif species == "pion":       iPrtcl = pion()
        elif species == "muon":       iPrtcl = muon()
        elif species == "neutrino":   iPrtcl = neutrino()
        else:
            iPrtcl = Particle( \
                BL.BeamLine.getcurrentReferenceParticle().getSpecies() \
                              )
        
        if Particle.getDebug():
            print(" <---- Done.")

        return iPrtcl
    
    @classmethod
    def fillPhaseSpaceAll(cls):
        Success = False
        if cls.getDebug():
            print(" Particle.fillPhaseSpaceAll, start:")
            print("     ----> fill phase space for", \
                  len(cls.getinstances()), \
                  "particle instances.")

        nPrtcl = 0
        for iPrtcl in cls.getinstances():
            nPrtcl += 1
            if cls.getDebug():
                print("     ----> Particle:", nPrtcl)
            
            #if not isinstance(iPrtcl, ReferenceParticle):
            if Particle.getDebug():
                print("         ----> Fill phase space for particle:", \
                      nPrtcl)
            Success = iPrtcl.fillPhaseSpace()

        if cls.getDebug():
            print("     ----> Particle.fillPhaseSpaceAll:", \
                  "fill phase space Success =", Success)
            print(" <----  Particle.fillPhaseSpaceAll, compete.")
            
        return Success
    
    def fillPhaseSpace(self):
        if self.getDebug():
            print(" Particle.fillPhaseSpace, start:")
            print("     ----> fill phase space for particle with", \
                  len(self.getLocation()), "records.")

        iRefPrtcl = BL.BeamLine.getcurrentReferenceParticle()

        nLoc = 0
        for iLoc in self.getLocation():
            if self.getDebug():
                print("         ----> Convert at location:", \
                      iLoc)
            PhsSpc  = self.calcRPLCPhaseSpace(nLoc)
            Success = self.setRPLCPhaseSpace(PhsSpc)

            RotMtrx = iRefPrtcl.getRot2LabOut()[nLoc]
            if self.getDebug():
                print("         ----> Rotation matrix:", \
                      RotMtrx)
            
            drLab   = np.matmul(RotMtrx, PhsSpc[0])
            if PhsSpc[1][2] != None:
                pLab    = np.matmul(RotMtrx, PhsSpc[1])
            else:
                pLab    = np.array([None, None, None])

            rLab    = iRefPrtcl.getRrOut()[nLoc][0:3] + drLab

            LabPhsSpc = [rLab, pLab]
            Success   = self.setLabPhaseSpace(LabPhsSpc)

            nLoc  += 1

        if nLoc == len(self.getLocation()):
            Success = True
        
        if self.getDebug():
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print("     ----> Particle.fillPhaseSpace: RPLC phase space:", \
                      PhsSpc)
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print("     ----> Particle.fillPhaseSpace:  Lab phase space:", \
                      LabPhsSpc)
            print(" <----  Particle.fillPhaseSpace, compete.", \
                  "Success:", Success)

        return Success

    def calcRPLCPhaseSpace(self, nLoc=None):
        if self.getDebug():
            print(" Particle.calcRPLCPhaseSpace for nLoc:", \
                  nLoc, self.getLocation()[nLoc], "start:")
            
        PhsSpc = self.RPLCTraceSpace2PhaseSpace(self.getTraceSpace()[nLoc])

        if self.getDebug():
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print(" <---- Return phase space:", PhsSpc)

        return PhsSpc

    @classmethod
    def RPLCTraceSpace2PhaseSpace(cls, TrcSpc):
        if cls.getDebug():
            print(" Particle.RPLCTraceSpace2PhaseSpace:")
            
        if cls.getDebug():
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print("     ----> trace space:", TrcSpc)

        species      = BL.BeamLine.getcurrentReferenceParticle().getSpecies()
        particleMASS = iPhysclCnstnts.getparticleMASS(species)

        p0  = BL.BeamLine.getcurrentReferenceParticle().getMomentumOut(0)
        E0  = np.sqrt(particleMASS**2 + p0**2)
        b0  = p0/E0
        E   = E0 + TrcSpc[5]*p0

        D   = mth.sqrt(1. + \
                       2.*TrcSpc[5]/b0 +
                       TrcSpc[5]**2)
        eps = ( TrcSpc[1]**2 + TrcSpc[3]**2  ) / (2.*D**2)
        
        if cls.getDebug():
            print("     ---->       p0, E0, b0, E:", p0, E0, b0, E)
            K0 = E0 - particleMASS
            K  = E  - particleMASS
            print("     ----> particleMASS, K0, K:", particleMASS, K0, K)
            print("     ---->          D, epsilon:", D, eps)
        
        p = mth.sqrt(E**2 - particleMASS**2)
        
        #rRPLC = np.array([ TrcSpc[0], TrcSpc[2], TrcSpc[4]*b0 ]) #.. Here!
        rRPLC = np.array([ TrcSpc[0], TrcSpc[2], 0. ]) #.. Here!

        px = TrcSpc[1]*p0
        py = TrcSpc[3]*p0
        p2 = p**2 - px**2 - py**2
        
        if p2 < 0.:
            #.. Report issue and expansion parameter:
            print(" Particle.RPLCTraceSpace2PhaseSpace:", \
                  " unphysical phase space, set pz=None:")
            print("     ----> p0, E0, b0, E:", p0, E0, b0, E)
            K0 = E0 - particleMASS
            K  = E  - particleMASS
            print("     ----> particleMASS, K0, K:", particleMASS, K0, K)
            print("     ----> p2, px, py, p:", p2, px, py, p)
            print("     ----> species, particleMASS, p0, E0, b0:", \
                  species, particleMASS, p0, E0, b0)
            print("     ---->          D, epsilon:", D, eps)
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print("     ----> TrcSpc:", TrcSpc)
                
            pz    = None

        else:
            pz    = mth.sqrt(p2)
            
        pRPLC = np.array([px, py, pz])
                
        if cls.getDebug():
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print("     ----> position:", rRPLC)
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print("     ----> Mmtm    :", pRPLC)
            if pRPLC[2] != None:
                Etmp = mth.sqrt(particleMASS**2 + np.dot(pRPLC, pRPLC))
            else:
                Etmp = None
            print("     ----> Energy  :", Etmp)

        PhsSpc = np.array([rRPLC, pRPLC])

        if cls.getDebug():
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print(" <---- Return phase space:", PhsSpc)

        return PhsSpc


    @classmethod
    def RPLCPhaseSpace2TraceSpace(cls, PhsSpc):
        if cls.getDebug():
            print(" Particle.RPLCPhaseSpace2TraceSpace: start.")
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print("     ----> PhsSpx:", PhsSpc)
            
        species      = Prtcl.ReferenceParticle.getinstances("All").getSpecies()
        particleMASS = iPhysclCnstnts.getparticleMASS(species)

        p0        = BL.BeamLine.getElement()[0].getp0()
        E0        = mth.sqrt( particleMASS**2 + p0**2)
        b0        = p0/E0
        if cls.getDebug():
            print("     ----> p0, E0, b0, ( K0 ):", p0, E0, b0, \
                  "(", E0-particleMASS, ")")

        E = mth.sqrt(particleMASS**2 + np.dot(PhsSpc[3:],PhsSpc[3:]))
        if cls.getDebug():
            print("     ----> E:", E)
        
        x      = PhsSpc[0]
        y      = PhsSpc[1]
        
        xPrime = PhsSpc[3] / p0
        yPrime = PhsSpc[4] / p0

        if cls.getDebug():
            print("     ----> xPrime, yPrime:", 
                  xPrime, yPrime)

        z      = PhsSpc[2] / b0
        delta  = (E - E0) / p0
        
        if cls.getDebug():
            print("     ----> z, E, delta:", z, E, delta)

        TrcSpc = np.array([x, xPrime, y, yPrime, z, delta])

        if cls.getDebug():
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print("     ----> Trace space:", TrcSpc)

        return TrcSpc

    def visualise(self, CoordSys, Projection, axs):
        if self.getDebug():
            print(" Particle.visualise: start")
            print("     ----> Coordinate system:", CoordSys)
            print("     ----> Projection:", Projection)

        sorz = []
        xory = []
        #..  Plotting as a function of s if RPLC or z if laboratory:
        if CoordSys == "RPLC":
            iCrd = 0
            axl  = "x"
            if Projection == "ys":
                iCrd = 2
                axl  = "y"
            sorz = BL.BeamLine.getcurrentReferenceParticle().getsOut()
            for TrcSpc in self.getTraceSpace():
                xory.append(TrcSpc[iCrd])

        elif CoordSys == "Lab":
            iCrd = 0
            axl  = "x"
            if Projection == "yz":
                iCrd = 1
                axl  = "y"

            iAddr = -1
            for RrOut in self.getLabPhaseSpace():
                xory.append(RrOut[0][iCrd])
                sorz.append(RrOut[0][2])

        if self.getDebug():
            print("     ----> len, sorz:", len(sorz), sorz)
            print("     ----> len, xory:", len(xory), xory)
            print("     ----> len ref. prtcl.:", \
                  len(ReferenceParticle.getinstances("All").getsOut()))

        if len(BL.BeamLine.getcurrentReferenceParticle().getsOut()) > len(xory):
            axs.plot(sorz[0:len(xory)], xory, color='salmon', linewidth='0.5')
        else:
            axs.plot(sorz, xory, color='darkgray', linewidth='0.5', zorder=2)

        if CoordSys == "RPLC":
            axs.set_xlabel('s (m)')
        elif CoordSys == "Lab":
            axs.set_xlabel('z (m)')
        axs.set_ylabel(axl + ' (m)')

        
#--------  Utilities:
    @classmethod
    def cleanAllParticles(cls):
        DoneOK = False
        
        for iPrtcl in cls.getinstances():
            del iPrtcl
            
        cls.instances = []

        ReferenceParticle.cleaninstances()
        
        DoneOK = True

        return DoneOK
    
    @classmethod
    def cleanParticles(cls):
        DoneOK = False
        
        for iPrtcl in cls.getinstances():
            if not isinstance(iPrtcl, ReferenceParticle):
                del iPrtcl
            
        cls.resetParticleInstances()
        DoneOK = True

        return DoneOK
    
    @classmethod
    def plotTraceSpaceProgression(cls):
        font = {'family': 'serif', \
                'color':  'darkred' \
                }
        """
                'weight': 'normal', \
                'size': 16, \
        """

        plt.rcParams["figure.figsize"] = (7.5, 10.)
        
        nLoc   = []
        xLoc   = []
        xpLoc  = []
        yLoc   = []
        ypLoc  = []
        ELoc   = []
        ELab   = []
        Scl    = []

        iSrc = BLE.Source.getinstances()[0]
        logE = False
        if iSrc.getMode() == 0:
            logE = True
                
        nPrtcl = 0
        for iPrtcl in cls.getinstances():
            particleMASS = \
                iPhysclCnstnts.getparticleMASS(iPrtcl.getSpecies())
            nPrtcl += 1
            if isinstance(iPrtcl, ReferenceParticle):
                iRefPrtcl = iPrtcl
                continue
            iLoc = -1
            for iTrcSpc in iPrtcl.getTraceSpace():
                iLoc += 1
                if iLoc > (len(xLoc)-1):
                    nLoc.append(iPrtcl.getLocation()[iLoc])
                    xLoc.append([])
                    xpLoc.append([])
                    yLoc.append([])
                    ypLoc.append([])
                    ELoc.append([])
                    ELab.append([])
                    Scl.append([])

                p0 = mth.sqrt(np.dot(iRefPrtcl.getPrOut()[iLoc][:3], \
                                     iRefPrtcl.getPrOut()[iLoc][:3]))
                E0  = iRefPrtcl.getPrOut()[iLoc][3]
                b0  = p0/E0
                E   = E0 + iPrtcl.getTraceSpace()[iLoc][5] * p0
                p   = mth.sqrt(E**2 - particleMASS**2)
                E  -= particleMASS
                D   = mth.sqrt(1. + \
                               2.*iPrtcl.getTraceSpace()[iLoc][5]/b0 +
                               iPrtcl.getTraceSpace()[iLoc][5]**2)

                eps = ( iPrtcl.getTraceSpace()[iLoc][1]**2 +    \
                        iPrtcl.getTraceSpace()[iLoc][3]**2  ) / \
                        (2.*D**2)
                """
                eps = (p - p0) / p0
                """
                
                xLoc[iLoc].append(iPrtcl.getTraceSpace()[iLoc][0])
                xpLoc[iLoc].append(iPrtcl.getTraceSpace()[iLoc][1])
                yLoc[iLoc].append(iPrtcl.getTraceSpace()[iLoc][2])
                ypLoc[iLoc].append(iPrtcl.getTraceSpace()[iLoc][3])
                ELoc[iLoc].append(iPrtcl.getTraceSpace()[iLoc][5])
                ELab[iLoc].append(E)
                Scl[iLoc].append(eps)
                
        plotFILE = '99-Scratch/ParticleProgressionPlot.pdf'
        with PdfPages(plotFILE) as pdf:
            for iLoc in range(len(xLoc)):
                fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(6., 6.), \
                                        layout="constrained")
                # add an artist, in this case a nice label in the middle...
                Ttl = nLoc[iLoc]
                fig.suptitle(Ttl, fontdict=font)

                #axs[0, 0].set_title('x,y')
                axs[0, 0].hist2d(xLoc[iLoc], yLoc[iLoc], bins=100)
                axs[0, 0].set_xlabel('x (m)')
                axs[0, 0].set_ylabel('y (m)')
            
                #axs[0, 1].set_title('delta')
                
                axs[0, 1].hist(ELoc[iLoc], 100)
                axs[0, 1].set_yscale('linear')
                if logE:
                    axs[0, 1].set_yscale('log')
                axs[0, 1].set_xlabel('delta')
                axs[0, 1].set_ylabel('Number')
            
                #axs[1, 0].set_title('x, xprime')
                axs[1, 0].hist2d(xLoc[iLoc], xpLoc[iLoc], bins=100)
                axs[1, 0].set_xlabel('x (m)')
                axs[1, 0].set_ylabel('xprime (m)')

                #axs[1, 1].set_title('y, yprime')
                axs[1, 1].hist2d(yLoc[iLoc], ypLoc[iLoc], bins=100)
                axs[1, 1].set_xlabel('y (m)')
                axs[1, 1].set_ylabel('yprime (m)')

                axs[2, 0].hist(ELab[iLoc], 100)
                axs[2, 0].set_yscale('linear')
                if logE:
                    axs[2, 0].set_yscale('log')
                axs[2, 0].set_xlabel('Kinetic energy (MeV)')
                axs[2, 0].set_ylabel('Number')

                axs[2, 1].hist(Scl[iLoc], 100)
                axs[2, 1].set_yscale('linear')
                if logE:
                    axs[2, 1].set_yscale('log')
                axs[2, 1].set_xlabel('Epsilon')
                axs[2, 1].set_ylabel('Number')

        
                pdf.savefig()
                plt.close()

    def printProgression(self):
        for iLoc in range(len(self.getLocation())):
            with np.printoptions(linewidth=500,precision=5,suppress=True):
                print(self.getLocation()[iLoc], ": z, s, trace space:", \
                      self.getz()[iLoc], self.gets()[iLoc], \
                      self.getTraceSpace()[iLoc])

    @classmethod
    def plotLongitudinalTraceSpaceProgression(cls):

        font = {'family': 'serif', \
                'color':  'darkred', \
                }
        plt.rcParams["figure.figsize"] = (7.5, 10.)
        
        nLoc   = []
        zLoc   = []
        delLoc  = []
        tLoc   = []
        ELoc   = []

        iSrc = BLE.Source.getinstances()[0]
        logE = False
        if iSrc.getMode() == 0:
            logE = True
       
        speed_of_light = \
            iPhysclCnstnts.SoL()
        
        nPrtcl = 0
        for iPrtcl in cls.getinstances():
            particleMASS = \
                iPhysclCnstnts.getparticleMASS(iPrtcl.getSpecies())
                
            nPrtcl += 1
            if isinstance(iPrtcl, ReferenceParticle):
                iRefPrtcl = iPrtcl
                continue
            iLoc = -1
            for iTrcSpc in iPrtcl.getTraceSpace():
                iLoc += 1
                if iLoc > (len(zLoc)-1):
                    nLoc.append(iPrtcl.getLocation()[iLoc])
                    zLoc.append([])
                    delLoc.append([])
                    tLoc.append([])
                    ELoc.append([])

                p0 = mth.sqrt(np.dot(iRefPrtcl.getPrOut()[iLoc][:3], \
                                     iRefPrtcl.getPrOut()[iLoc][:3]))
                E0  = iRefPrtcl.getPrOut()[iLoc][3]
                b0  = p0/E0
                E   = E0 + iPrtcl.getTraceSpace()[iLoc][5] * p0
                p   = mth.sqrt(E**2 - particleMASS**2)
                b   = p/E
                E  -= particleMASS

                t = iPrtcl.getTraceSpace()[iLoc][4]*b0 / (b*speed_of_light)
                
                zLoc[iLoc].append(iPrtcl.getTraceSpace()[iLoc][4]*b0)
                delLoc[iLoc].append(iPrtcl.getTraceSpace()[iLoc][5])
                tLoc[iLoc].append(t)
                ELoc[iLoc].append(E)
                
        plotFILE = '99-Scratch/ParticleLongiProgressionPlot.pdf'
        with PdfPages(plotFILE) as pdf:
            for iLoc in range(len(zLoc)):
                fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(6., 6.), \
                                        layout="constrained")
                # add an artist, in this case a nice label in the middle...
                Ttl = nLoc[iLoc]
                fig.suptitle(Ttl, fontdict=font)

                axs[0, 0].hist2d(zLoc[iLoc], delLoc[iLoc], bins=100)
                axs[0, 0].set_xlabel('z (m)')
                axs[0, 0].set_ylabel('delta')
            
                axs[0, 1].hist(delLoc[iLoc], 100)
                axs[0, 1].set_yscale('linear')
                if logE:
                    axs[0, 1].set_yscale('log')
                axs[0, 1].set_xlabel('Delta')
                axs[0, 1].set_ylabel('Number')

                axs[1, 0].hist(zLoc[iLoc], 100)
                axs[1, 0].set_xlabel('z (m)')
                axs[1, 0].set_ylabel('Number')
            
                axs[1, 1].hist(tLoc[iLoc], 100)
                axs[1, 1].set_xlabel('t (s)')
                axs[1, 1].set_ylabel('Number')

                axs[2, 0].hist(ELoc[iLoc], 100)
                axs[2, 0].set_yscale('linear')
                if logE:
                    axs[2, 0].set_yscale('log')
                axs[2, 0].set_xlabel('Kinetic energy (MeV)')
                axs[2, 0].set_ylabel('Number')

                axs[2, 1].hist2d(tLoc[iLoc], ELoc[iLoc], bins=100)
                axs[2, 1].set_xlabel('t (s)')
                axs[2, 1].set_ylabel('Kinetic energy (MeV)')

        
                pdf.savefig()
                plt.close()
            

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

    def writeParticle(self, ParticleFILE=None, CleanAfterWrite=True):
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
                                self.getTraceSpace()[iLoc][0],   \
                                self.getTraceSpace()[iLoc][1],   \
                                self.getTraceSpace()[iLoc][2],   \
                                self.getTraceSpace()[iLoc][3],   \
                                self.getTraceSpace()[iLoc][4],   \
                                self.getTraceSpace()[iLoc][5])
            ParticleFILE.write(record)
            if self.getDebug():
                print("         ----> z, s, trace space:", \
                      strct.unpack(">8d",record))
        
        if CleanAfterWrite:
            Cleaned = self.cleanParticles()
        
    def writeParticleBDSIM(self, ParticleFILE=None, iLoc=1, \
                           CleanAfterWrite=True):
        if self.getDebug():
            print("Particle.writeParticleBDSIM starts.")

        if not isinstance(ParticleFILE, io.TextIOWrapper):
            raise noFILE( \
                    " Particle.writeParticle: file does not exist.")

        if self.getDebug():
            print("     ----> Location to store:", iLoc)

        iAddr = iLoc - 1
        
        species      = BL.BeamLine.getcurrentReferenceParticle().getSpecies()
        particleMASS = iPhysclCnstnts.getparticleMASS(species)

        p0  = BL.BeamLine.getElement()[0].getp0()[0]
        E0  = np.sqrt(particleMASS**2 + p0**2)

        b0  = p0/E0
        z   = self.gets()[iAddr] + self.getTraceSpace()[iAddr][4]*b0

        E   = E0 + self.getTraceSpace()[iAddr][5]*p0

        if self.getDebug():
            with np.printoptions(linewidth=500,precision=5,suppress=True):
                print("     ----> iAddr, iLoc, name:", iAddr, iLoc, \
                      BLE.BeamLineElement.getinstances()[iLoc].getName())
                print("     ----> Trace space:", self.getTraceSpace()[iAddr])

        """
        reportString = "distrFileFormat = " +\
            "x[m]:xp[rad]:y[m]:yp[rad]:z[m]:E[MeV]";
        """
        
        Line = str(self.getTraceSpace()[iAddr][0]) + ' ' + \
               str(self.getTraceSpace()[iAddr][2]) + ' ' + \
               str(z)                              + ' ' + \
               str(self.getTraceSpace()[iAddr][1]) + ' ' + \
               str(self.getTraceSpace()[iAddr][3]) + ' ' + \
               str(E) + "\n"
            
        ParticleFILE.write(Line)
        if self.getDebug():
                print("         ----> Line:", Line)
        
        if CleanAfterWrite:
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
            print("Particle.openParticleFile: dir: ", \
                  datafilePATH, " name: ", datafileNAME)
            
        if os.path.exists(datafilePATH):
            if datafilePATH == None:
                raise noPATH( \
                         " Particle.openParticleFile: no path given.")
            if datafileNAME == None:
                raise noNAME( \
                    " Particle.openParticleFile: no file name given.")

            ParticleFILE1 = os.path.join(datafilePATH, datafileNAME)
        else:
            ParticleFILE1 = os.path.normpath(datafileNAME)

        if not os.path.exists(ParticleFILE1):
            raise noPATH( \
                    " Particle.openParticleFile: data file does not exist.")

        ParticleFILE = open(ParticleFILE1, "rb")
        if cls.getDebug():
            print("     ----> File opened:", ParticleFILE)

        return ParticleFILE

    @classmethod
    def readParticle(cls, ParticleFILE=None):
        if cls.getDebug():
            print("Particle.readParticle starts.")

        if not isinstance(ParticleFILE, io.BufferedReader):
            raise noFILE( \
                    " Particle.readParticle: file does not exist.")

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
            TrcSpc = np.array([                  \
                               float(record[2]), \
                               float(record[3]), \
                               float(record[4]), \
                               float(record[5]), \
                               float(record[6]), \
                               float(record[7])] )
            if cls.getDebug():
                print("         ----> z, s, trace space:", z, s, TrcSpc)

            iPrtcl.recordParticle(Location, z, s, TrcSpc)

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


"""
Derived class ReferenceParticle(Particle):
==========================================

  Provides reference particle.  Derived from Particle class.


  Class attributes:
  -----------------
  __instance : Instances of ReferenceParticle class
    : Debug flag

      
  Instance attributes:
  --------------------
   Particle instance attributes.

   ReferencePartricle attributes:
         _sIn[]: float   : Path lenth at entrance to beamline element. 
        _sOut[]: float   : Path lenth at exit from beamline element. 
        _RrIn[]: ndarray : In laboratory frame, four-vector position at
                           entrance to beamline element. 
          _Pr[]: ndarray : In laboratory frame, four-vector momentum at
                           entrance to beamline element. 
       _RrOut[]: ndarray : In laboratory frame, four-vector position at
                           exit from beamline element. 
       _PrOut[]: ndarray : In laboratory frame, four-vector momentum at
                           exit from beamline element.
   _Rot2LabIn[]: ndarray : Rotation matrix from RPLC to lab at entry to
                           beamline element.
  _Rot2LabOut[]: ndarray : Rotation matrix from RPLC to lab at exit from
                           beamline element.

   All instance attributes are initialised to Null


  Methods:
  --------
  Built-in methods __init__, __repr__ and __str__.
      __init__ : Creates instance of beam-line element class.
      __repr__: One liner with call.
      __str__ : Dump of constants

  Get methods:
   getinstance: Class method, returns instance of ReferencePartcicle class.

    getRPDebug: Get ReferenceParticle class debug flag.

     getsIn, getsOut, getRrIn, getRrOut, getPrIn, getPrOut, getRot2LabIn,
     getRot2LabOut all believed to be self documenting.

  Set methods:
   setinstance: Class method, sets ReferencePartcicle instance.
           Input: ReferenceParticle
          Return: None
       Exception: Raised if i/p not instance of ReferenceParticle

    setRPDebug: Set ReferenceParticle class debug flag.
           Input: bool, True/False
          Return: None
       Exception: Raised if i/p not bool.

   setAll2RPNone: set all instance attributes to None or []

          setsIn : i/p float              : Sets _sIn
         setsOut : i/p float              : Sets _sOut

         setRrIn : i/p 4 param, ndarray   : Sets _RrIn
        setRrOut : i/p 4 param, ndarray   : Sets _RrOut

         setPrIn : i/p 4 param, ndarray   : Sets _PrIn
        setPrOut : i/p 4 param, ndarray   : Sets _PrOut

    setRot2LabIn : i/p 3x3 param, ndarray : Sets _Rot2LabIn
   setRot2LabOut : i/p 3x3 param, ndarray : Sets _Rot2LabOut

  Processing method:
         setReferenceParticle: No input, runs through beam line elements
                               (instances of BeamLineElement class) to
                               set parameters of reference particle at each
                               element.

 setReferenceParticleAtSource: I/p: iBLE : BeamLineElement instance
                               Sets attributes for reference partice at
                               source.

 setReferenceParticle: I/p: iBLE : BeamLineElement instance
                               Sets attributes for reference partice for a
                               drift space.  Also works for apertures,
                               quads, and any element that has length but
                               does not bend the beam, sich as a dipole.

  I/o methods:
     None so far.

  Exceptions:
     badArgument(Exception), secondReferenceParticle
    

Created on Mon 15Nov23: Version history:
----------------------------------------
 1.0: 15Nov23: First implementation

@author: kennethlong
"""
class ReferenceParticle(Particle):
    __instances   = []
    __RPDebug     = False
    __speciesLIST = []

#--------  "Built-in methods":
    def __new__(cls, _species="proton"):
        if cls.getRPDebug():
            print(' ReferenceParticle(Particle).__new__:', \
                  'start; checking if already an instance for', \
                  'species:', _species)
            
        if not _species in cls.getspeciesLIST():
            cls.setspecies(_species)
            if cls.getRPDebug():
                print('     ----> Not yet created; create!')

            inst = super(ReferenceParticle, cls).__new__(cls)

            cls.setinstance(inst)

        else:
            inst = cls.getinstance(_species)

        return inst
        
    def __init__(self, _species="proton"):
        if ReferenceParticle.getRPDebug():
            print(' ReferenceParticle(Particle).__init__:', \
                  'creating the ReferenceParticle object', \
                  'for species:', _species)
        
        #.. Set ReferenceParticle attributes to None:
        self.setAllRP2None()

        #.. Particle class initialisation:
        self.callSPECIEScreator(_species)
        
        # Only constants; print values that will be used:
        if ReferenceParticle.getRPDebug():
            print(self)
                
        return

    def __repr__(self):
        return "ReferenceParticle()"

    def __str__(self):
        print(" ReferenceParticle:")
        print(" ==================")
        print("     ----> Debug     :", self.getRPDebug())
        print("     ----> sIn       :", self.getsIn())
        print("     ----> sOut      :", self.getsOut())
        print("     ----> RrIn      :", self.getRrIn())
        print("     ----> PrIn      :", self.getPrIn())
        print("     ----> RrOut     :", self.getRrOut())
        print("     ----> PrOut     :", self.getPrOut())
        print("     ----> Rot2LabIn : \n", self.getRot2LabIn())
        print("     ----> Rot2LabOut: \n", self.getRot2LabOut())
        print("     <---- Reference particle dump complete.")
        print("     Particle:")
        print("     =========")
        print(self.print())
        return " <---- ReferenceParticle __str__ done."

    @staticmethod
    def createReferenceParticles():
        if ReferenceParticle.getRPDebug():
            print(" ReferenceParticle(Particle).createReferenceParticles:", \
                  "start.")
            print("     ----> Number of reference particles:", \
                  len(BLE.Facility.getinstances().getp0()))
            
        for id in range(len(BLE.Facility.getinstances().getp0())):
            if ReferenceParticle.getRPDebug():
                print("     ---->", \
                      BLE.Facility.getinstances().getspecies0()[id], \
                      BLE.Facility.getinstances().getp0()[id] \
                      )
            ReferenceParticle(BLE.Facility.getinstances().getspecies0()[id])
            
        if ReferenceParticle.getRPDebug():
            print(" <---- Done.")

        return ReferenceParticle.getinstances("All")

    def callSPECIEScreator(self, species):
        if ReferenceParticle.getRPDebug():
            print(" ReferenceParticle(Particle).callSPECIEScreator:", \
                  "species:", species)
            
        if species == "proton":
            proton.__init__(self)
        elif species == "pion":
            pion.__init__(self)
        elif species == "muon":
            muon.__init__(self)
        elif species == "neutrino":
            neutrino.__init__(self)
        else:
            print(" <---- Species,", species, "not recognised, abort.")
            raise badParameter()

        if ReferenceParticle.getRPDebug():
            print(" <---- Done.")

            
#--------  "Get methods" only; version, reference, and constants
#.. Methods believed to be self documenting(!)

    @classmethod
    def getinstances(cls, which="First"):
        #.. By default return only "First", primary, reference particle.
        #   This is for backward compatibility.
        if not which == "First":
            return cls.__instances
        return cls.__instances[0]

    @classmethod
    def getspeciesLIST(cls):
        return cls.__speciesLIST

    @classmethod
    def getinstance(cls, species):
        id = cls.__speciesLIST.index(species)
        return cls.__instances[id]

    @classmethod
    def getRPDebug(self):
        return self.__RPDebug

    def getsIn(self):
        return self._sIn
        
    def getsOut(self):
        return self._sOut
        
    def getRrIn(self):
        return self._RrIn
        
    def getRrOut(self):
        return self._RrOut
        
    def getPrIn(self):
        return self._PrIn

    def getMomentumIn(self, iLoc):
        return mth.sqrt(np.dot(self.getPrIn()[iLoc][:3], \
                               self.getPrIn()[iLoc][:3]))
        
    def getPrOut(self):
        return self._PrOut
    
    def getMomentumOut(self, iLoc):
        return mth.sqrt(np.dot(self.getPrOut()[iLoc][:3], \
                               self.getPrOut()[iLoc][:3]))
        
    def getRot2LabIn(self):
        return self._Rot2LabIn
        
    def getRot2LabOut(self):
        return self._Rot2LabOut

    def getb0(self, iLoc):
        p0  = mth.sqrt(np.dot(self.getPrOut()[iLoc][:3], \
                              self.getPrOut()[iLoc][:3]))
        E0  = self.getPrOut()[iLoc][3]
        b0 = p0/E0
        return b0
        
    def getg0b0(self, iLoc):
        p0   = mth.sqrt(np.dot(self.getPrOut()[iLoc][:3], \
                              self.getPrOut()[iLoc][:3]))
        g0b0 = p0 / \
            iPhysclCnstnts.getparticleMASS(self.getSpecies())
        return g0b0
        

#--------  "Set methods";
    @classmethod
    def cleaninstances(cls):
        for inst in cls.getinstances("All"):
            del inst
        cls.resetinstances()

    @classmethod
    def resetinstances(cls):
        cls.__instances   = []
        cls.__speciesLIST = []

    @classmethod
    def setspecies(cls, species):
        if isinstance(species, str):
            cls.__speciesLIST.append(species)
        else:
            raise badArgument()

    @classmethod
    def setinstance(cls, inst):
        if isinstance(inst, ReferenceParticle):
            cls.__instances.append(inst)
        else:
            raise badArgument()

    @classmethod
    def setRPDebug(self, Debug):
        if isinstance(Debug, bool):
            self.__RPDebug = Debug
        else:
            raise badArgument()

    def setAllRP2None(self):
        self._sIn        = []
        self._sOut       = []
        self._RrIn       = []
        self._PrIn       = []
        self._RrOut      = []
        self._PrOut      = []
        self._Rot2LabIn  = []
        self._Rot2LabOut = []

    def setsIn(self, sIn):
        Success = False
        if isinstance(sIn, float):
            self._sIn.append(sIn)
            Success = True
        return Success

    def setsOut(self, sOut):
        Success = False
        if isinstance(sOut, float):
            self._sOut.append(sOut)
            Success = True
        return Success

    def setRrIn(self, RrIn):
        Success = False
        if isinstance(RrIn, np.ndarray):
            self._RrIn.append(RrIn)
            Success = True
        return Success

    def setRrOut(self, RrOut):
        Success = False
        if isinstance(RrOut, np.ndarray):
            self._RrOut.append(RrOut)
            Success = True
        return Success

    def setPrIn(self, PrIn):
        Success = False
        if isinstance(PrIn, np.ndarray):
            self._PrIn.append(PrIn)
            Success = True
        return Success

    def setPrOut(self, PrOut):
        Success = False
        if isinstance(PrOut, np.ndarray):
            self._PrOut.append(PrOut)
            Success = True
        return Success

    def setRot2LabIn(self, Rot2LabIn):
        Success = False
        if isinstance(Rot2LabIn, np.ndarray):
            self._Rot2LabIn.append(Rot2LabIn)
            Success = True
        return Success

    def setRot2LabOut(self, Rot2LabOut):
        Success = False
        if isinstance(Rot2LabOut, np.ndarray):
            self._Rot2LabOut.append(Rot2LabOut)
            Success = True
        return Success

        
#--------  Processing methods:
    def setReferenceParticleAtSource(self):
        particleMASS = iPhysclCnstnts.getparticleMASS(self.getSpecies())
        
        nRcrds  = len(self.getsIn())

        Success = self.setLocation(BLE.BeamLineElement.getinstances()\
                                   [nRcrds+1].getName())
        if not Success:
            raise fail2setReferenceParticle("Name")

        Success = self.setsIn(0.)
        if not Success:
            raise fail2setReferenceParticle("sIn")
        Success = self.setsOut(0.)
        if not Success:
            raise fail2setReferenceParticle("sOut")

        RrIn  = np.array([0., 0., 0., 0.])
        RrOut = np.array([0., 0., 0., 0.])
        Success = self.setRrIn(RrIn)
        if not Success:
            raise fail2setReferenceParticle("RrIn")
        Success = self.setRrOut(RrOut)
        if not Success:
            raise fail2setReferenceParticle("RrOut")

        p0       = BL.BeamLine.getElement()[0].getp0()[0]
        Ref4mmtm = np.array([0., 0., p0,
                             mth.sqrt(p0**2 + particleMASS**2)])
        
        PrIn  = Ref4mmtm
        PrOut = Ref4mmtm
        Success = self.setPrIn(PrIn)
        if not Success:
            raise fail2setReferenceParticle("PrIn")
        Success = self.setPrOut(PrOut)
        if not Success:
            raise fail2setReferenceParticle("PrOut")

        Rot2LabIn  = np.array([                  \
                               [1., 0., 0.],      \
                               [0., 1., 0.],      \
                               [0., 0., 1.]       \
                                      ])
        Rot2LabOut = np.array([                   \
                               [1., 0., 0.],      \
                               [0., 1., 0.],      \
                               [0., 0., 1.]       \
                              ])
        Success = self.setRot2LabIn(Rot2LabIn)
        if not Success:
            raise fail2setReferenceParticle("Rot2LabIn")
        Success = self.setRot2LabOut(Rot2LabOut)
        if not Success:
            raise fail2setReferenceParticle("Rot2LabOut")

        #.. Now particle position/trace space:
        Success = self.setz(self.getRrOut()[0][3])
        if not Success:
            raise fail2setReferenceParticle("setz")
        Success = self.sets(self.getsOut()[0])
        if not Success:
            raise fail2setReferenceParticle("sets")
        TrcSpc  = np.array([0., 0., 0., 0., 0., 0.])
        Success = self.setTraceSpace(TrcSpc)
        if not Success:
            raise fail2setReferenceParticle("setTraceSpace")

        return Success

    def setReferenceParticle(self, iBLE=None):
        nRcrds  = len(self.getsIn())
        if self.getDebug():
            print(" --------  --------  --------  //", \
                  "  --------  --------  --------")
            print( \
            " ReferenceParticle(Particle).setReferenceParticle ", \
                   "starts; \n", \
                   "    ----> Number of previous records:", nRcrds)
        
        Success = self.setLocation(BLE.BeamLineElement.getinstances()\
                                   [nRcrds+1].getName())
        if not Success:
            raise fail2setReferenceParticle("Name")
        if self.getDebug():
            print( \
                   "     ----> Processing location:", self.getLocation()[-1])

        Success = self.setsIn(self.getsOut()[nRcrds-1])
        if not Success:
            raise fail2setReferenceParticle("sIn")
        Success = self.setsOut(self.getsOut()[nRcrds-1] + iBLE.getLength())
        if not Success:
            raise fail2setReferenceParticle("sOut")
        if self.getDebug():
            print( \
                   "         ---->   sIn:", self.getsIn()[-1])
                
        RrIn  = self.getRrOut()[nRcrds-1]
        delR = BLE.BeamLineElement.getinstances()[nRcrds+1].getStrt2End()
        delR = np.append(delR, 0.)
        RrOut = RrIn + delR
        Success = self.setRrIn(RrIn)
        if not Success:
            raise fail2setReferenceParticle("RrIn")
        Success = self.setRrOut(RrOut)
        if not Success:
            raise fail2setReferenceParticle("RrOut")
        if self.getDebug():
            print( \
                   "         ---->  RrIn:", self.getRrIn()[-1])
            print( \
                   "         ----> RrOut:", self.getRrOut()[-1])
        
        PrIn    = self.getPrOut()[nRcrds-1]
        rot2lab = BLE.BeamLineElement.getinstances()[nRcrds+1].getRot2LbEnd()
        PrOut   = np.matmul(rot2lab, PrIn[0:3])
        PrOut   = np.append(PrOut, PrIn[3])
        Success = self.setPrIn(PrIn)
        if not Success:
            raise fail2setReferenceParticle("PrIn")
        Success = self.setPrOut(PrOut)
        if not Success:
            raise fail2setReferenceParticle("PrOut")
        if self.getDebug():
            print( \
                   "         ---->  PrIn:", self.getPrIn()[-1])
            print( \
                   "         ----> PrOut:", self.getPrOut()[-1])
        
        Rot2LabIn  = \
            BLE.BeamLineElement.getinstances()[nRcrds+1].getRot2LbStrt()
        Rot2LabOut = \
            BLE.BeamLineElement.getinstances()[nRcrds+1].getRot2LbEnd()
        Success = self.setRot2LabIn(Rot2LabIn)
        if not Success:
            raise fail2setReferenceParticle("Rot2LabIn")
        Success = self.setRot2LabOut(Rot2LabOut)
        if not Success:
            raise fail2setReferenceParticle("Rot2LabOut")
        if self.getDebug():
            print( \
                   "         ---->  Rot2LabIn: \n", \
                   self.getRot2LabIn()[-1])
            print( \
                   "         ----> Rot2LabOut: \n", \
                   self.getRot2LabOut()[-1])
        
        #.. Now particle position/trace space:
        Success = self.setz(self.getRrOut()[nRcrds][2])
        if not Success:
            raise fail2setReferenceParticle("setz")
        Success = self.sets(self.getsOut()[nRcrds])
        if not Success:
            raise fail2setReferenceParticle("sets")
        TrcSpc  = np.array([0., 0., 0., 0., 0., 0.])
        Success = self.setTraceSpace(TrcSpc)
        if not Success:
            raise fail2setReferenceParticle("setTraceSpace")
        
        if self.getDebug():
            print( \
                   "         ----> particle z:", self.getz()[-1])
            print( \
                   "         ----> particle s:", self.gets()[-1])
            print( \
                   "         ----> particle TrcSpc:", \
                   self.getTraceSpace()[-1])
            print(" --------  --------  --------  //", \
                  "  --------  --------  --------")
        
        return Success

    def visualise(self, CoordSys, Projection, axs):
        if self.getDebug():
            print(" ReferenceParticle.visualise: start")
            print("     ----> Coordinate system:", CoordSys)
            print("     ----> Projection:", Projection)

        sorz = []
        xory = []
        
        #..  Plotting as a function of s if RPLC or z if laboratory:
        if CoordSys == "RPLC":
            iCrd = 0
            axl  = "x"
            if Projection == "ys":
                iCrd = 2
                axl  = "y"
                
            sorz = self.getsOut()
            for TrcSpc in self.getTraceSpace():
                xory.append(TrcSpc[iCrd])

        elif CoordSys == "Lab":
            iCrd = 0
            axl  = "x"
            if Projection == "yz":
                iCrd = 1
                axl  = "y"
                
            for RrOut in self.getRrOut():
                xory.append(RrOut[iCrd])
                sorz.append(RrOut[2])
            
        if self.getDebug():
            print("     ----> sorz:", sorz)
            print("     ----> xory:", xory)
        
        axs.plot(sorz, xory, color='black', linewidth='0.5', \
                 linestyle='dashed', zorder=3)
        axs.set_xlabel('s (m)')
        axs.set_ylabel(axl + ' (m)')
 
"""
Derived class UnstableParticle(Particle):
==========================================

  Provides unstable particle.  Derived from Particle class.

  Class attributes:
  -----------------

      
  Instance attributes:
  --------------------
   Particle instance attributes.

   _meanLife        : mean life time in seconds
   _remainingPath   : path left before the particle decays, in the lab frame

   _meanLife initilised from value in PhysicalConstants.py


  Methods:
  --------
  Built-in methods __init__, __repr__ and __str__.
      __init__ : Creates instance of UnstableParticle class.
      __repr__: One liner with call.
      __str__ : Dump of constants

  Get methods:
    getmeanLife:        Returns the mean lifetime of the particle.
    getremainingPath:   gets path left before the particle decays
    initremainingPath:  sets initial value of the remaining path, given the mean life time and the particle
                        momentum. Value in the laboratory frame.

  Set methods:

    setremainingPath : sets remainingPath to a new value
    setmeanLife      : set the value of the mean lifetime from PhysicalConstants unless
                    a value is given to override it

    print:  prints out the subclass variables and calls super.print to print out the values in
            the base class

  I/o methods:
     None so far.

  Exceptions:
    unKnownUnstableParticle(Exception)
    
Created on Mon 05Aug25: Version history:
----------------------------------------
 1.0: 05Aug25: First implementation

@author: paulkyberd
"""
class UnstableParticle(Particle):
    def __init__(self, species):
        UnstableSpecies = {"pion", "muon","proton"}

        if species.lower() in UnstableSpecies:
            super().__init__(species)
            self._meanLife = iPhysclCnstnts.getparticleLifeTime(species)
            self._remainingPath = None
        else:
            raise unKnownUnstableParticle(Exception)

    def __repr__(self):
        return "UnstableParticle()"

    def __str__(self):
        super().__str__()
#        super().print()
        print(f"     ----> Mean Life: {self._meanLife}")
        print(f"     ----> Remaining Path: {self._remainingPath}") 
        return " UnstableParticle __str__ done."

    # Getters
    def getmeanLife(self):
        return self._meanLife

    def getremainingPath(self):
        return self._remainingPath

    def initremainingPath(self, p):
        #   Get a decay time which is an exponential with the mean life as constant
        decayTime = np.random.exponential(self._meanLife)
        #   Turn the decay time in the rest frame, into a path length in the laboratory frame
        self._remainingPath = p*iPhysclCnstnts.SoL()*decayTime/iPhysclCnstnts.getparticleMASS(self.getSpecies())

    # Setters
    def setmeanLife(self, meanLife=None):
        if meanLife != None:
            self._meanLife = iPhysclCnstnts.getparticleLifeTime(species)
        else:
            self._meanLife = meanLife

    def setremainingPath(self, remainingPath):
        self._remainingPath = remainingPath

    
#--------  Exceptions:
class noReferenceParticle(Exception):
    pass

class unKnownReferenceParticle(Exception):
    pass

class unKnownUnstableParticle(Exception):
    pass

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

class badArgument(Exception):
    pass

class secondReferenceParticle(Exception):
    pass

class fail2setReferenceParticle(Exception):
    pass


class proton(Particle):
    __instance     = []

#--------  "Built-in methods":
    def __init__(self):
        if self.getDebug():
            print(' proton(Particle).__init__:', \
                  'creating the proton object')

        proton.__instance.append(self)
        
        #.. Particle class initialisation:
        Particle.__init__(self, "proton")
        
        # Only constants; print values that will be used:
        if self.getDebug():
            print(" <---- Done:", type(self), "instanciated.")

        return


class pion(Particle):
    __instance     = []

#--------  "Built-in methods":
    def __init__(self):
        if self.getDebug():
            print(' pion(Particle).__init__:', \
                  'creating the pion object')

        pion.__instance.append(self)
        
        #.. Particle class initialisation:
        Particle.__init__(self, "pion")

        iPhysCnstnts = PhysCnstnts.PhysicalConstants()
        lifetime     = iPhysCnstnts.tauPion()
        
        RemainingLifetime = -lifetime * mth.log(1. - rnd.random())
        #np.random.exponential(lifetime)
        self.setRemainingLifetime(RemainingLifetime)
        
        # Only constants; print values that will be used:
        if self.getDebug():
            print("     ----> pion lifetime:", lifetime, "s")
            print(" <---- remaining lifetime:", self.getRemainingLifetime())

        return


class muon(Particle):
    __instance     = []

#--------  "Built-in methods":
    def __init__(self):
        
        if self.getDebug():
            print(' muon(Particle).__init__:', \
                  'creating the muon object')

        muon.__instance.append(self)
        
        #.. Particle class initialisation:
        Particle.__init__(self, "muon")
        
        iPhysCnstnts = PhysCnstnts.PhysicalConstants()
        lifetime     = iPhysCnstnts.tauMuon()
        
        RemainingLifetime = np.random.exponential(lifetime)
        self.setRemainingLifetime(RemainingLifetime)
        
        # Only constants; print values that will be used:
        if self.getDebug():
            print("     ----> muon lifetime:", lifetime, "s")
            print(" <---- remaining lifetime:", self.getRemainingLifetime())

        return


class neutrino(Particle):
    __instance     = []
    __Debug      = False

#--------  "Built-in methods":
    def __init__(self):
        
        print(' neutrino(Particle).__init__:', \
                  'creating the neutrino object')

        neutrino.__instance.append(self)
        
        #.. Particle class initialisation:
        Particle.__init__(self, "neutrino")
        
        # Only constants; print values that will be used:
        print("     ----> Type::", type(self))
        
        return
