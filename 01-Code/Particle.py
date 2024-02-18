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
      getDebug, getParticleInstances, getLocation, getz, gets, 
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
 plotParticleTrajectory_Lab: create plots showing the progression of particle in the lab frame.

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

@author: kennethlong
"""

from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.collections import LineCollection
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import struct as strct
import numpy as np
import math as mth
import os
import io
from Utilities import RotMat_x, RotMat_y, RotMat_z
import matplotlib.transforms as mt

import BeamLine as BL
import BeamLineElement as BLE

# -------- Physical Constants Instances and Methods ----------------
from PhysicalConstants import PhysicalConstants


constants_instance = PhysicalConstants()
protonMASS = constants_instance.mp()
speed_of_light = constants_instance.SoL()


class Particle:
    instances = []
    __Debug = False

    # --------  "Built-in methods":
    def __init__(self):
        if self.__Debug:
            print(" Particle.__init__: ", "creating the Particle object")

        # .. Must have reference particle as first in the instance list,
        #   ... so ...
        if not isinstance(ReferenceParticle.getinstance(), ReferenceParticle):
            raise noReferenceParticle(
                " Reference particle, ", "not first in particle list."
            )

        Particle.instances.append(self)

        # .. Particle instance created with phase-space at each
        #   interface being recorded as None
        self.setAll2None()

        if self.__Debug:
            print("     ----> New Particle instance: \n", Particle.__str__(self))
            print(" <---- Particle instance created.")

    def __repr__(self):
        return "Particle()"

    def __str__(self):
        self.print()
        return " Partcle __str__ done."

    def print(self):
        print("\n Particle:")
        print(" ---------")
        print("     ----> Debug flag:", self.getDebug())
        print("     ----> Number of phase-space records:", len(self.getLocation()))
        if len(self.getLocation()) > 0:
            print("     ----> Record of trace space:")
        for iLctn in range(len(self.getLocation())):
            print("         ---->", self.getLocation()[iLctn], ":")
            print("             ----> z, s", self.getz()[iLctn], self.gets()[iLctn])
            try:
                print(
                    "             ----> ",
                    BLE.BeamLineElement.getinstances()[iLctn + 1].getName(),
                    "; length ",
                    BLE.BeamLineElement.getinstances()[iLctn + 1].getLength(),
                )
            except:
                print(
                    "             ----> ",
                    BLE.BeamLineElement.getinstances()[iLctn + 1].getName(),
                    "; has no length",
                )
            with np.printoptions(linewidth=500, precision=7, suppress=True):
                print(
                    "             ---->     trace space:", self.getTraceSpace()[iLctn]
                )
            if len(self.getRPLCPhaseSpace()) == 0:
                print("             ---->     phase space: not yet filled")
            else:
                with np.printoptions(linewidth=500, precision=7, suppress=True):
                    print(
                        "             ---->     phase space:",
                        self.getRPLCPhaseSpace()[iLctn],
                    )
            if len(self.getLabPhaseSpace()) == 0:
                print("             ----> Lab phase space: not yet filled")
            else:
                with np.printoptions(linewidth=500, precision=7, suppress=True):
                    print(
                        "             ----> Lab phase space:",
                        self.getLabPhaseSpace()[iLctn],
                    )
        return " <---- Particle parameter dump complete."

    # --------  "Set method" only Debug
    # .. Method believed to be self documenting(!)

    @classmethod
    def setDebug(cls, Debug=False):
        if cls.__Debug:
            print(" Particle.setdebug: ", Debug)
        cls.__Debug = Debug

    @classmethod
    def resetParticleInstances(cls):
        if len(cls.instances) > 0:
            iRefPrtcl = cls.instances[0]
            cls.instances = []
            cls.instances.append(iRefPrtcl)

    def setAll2None(self):
        self._Location = []
        self._z = []
        self._s = []
        self._TrcSpc = []
        self._PhsSpc = []
        self._LabPhsSpc = []
        self._x = []

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
            Success = self.setz(0.0)
        if Success:
            Success = self.sets(0.0)
        if Success:
            Success = self.setTraceSpace(TraceSpace)
        return Success

    # --------  "Get methods" only; version, reference, and constants
    # .. Methods believed to be self documenting(!)

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

    def getTraceSpace(self):
        return self._TrcSpc

    def getRPLCPhaseSpace(self):
        return self._PhsSpc

    def getLabPhaseSpace(self):
        return self._LabPhsSpc

    # --------  Utilities:
    @classmethod
    def cleanParticles(cls):
        DoneOK = False

        for iPrtcl in cls.getParticleInstances():
            if not isinstance(iPrtcl, ReferenceParticle):
                del iPrtcl

        cls.resetParticleInstances()
        DoneOK = True

        return DoneOK

    @classmethod
    def plotTraceSpaceProgression(cls):
        font = {
            "family": "serif",
            "color": "darkred",
            "weight": "normal",
            "size": 16,
        }
        plt.rcParams["figure.figsize"] = (7.5, 10.0)

        nLoc = []
        xLoc = []
        xpLoc = []
        yLoc = []
        ypLoc = []
        ELoc = []
        ELab = []
        Scl = []

        nPrtcl = 0
        for iPrtcl in cls.getParticleInstances():
            nPrtcl += 1
            if isinstance(iPrtcl, ReferenceParticle):
                iRefPrtcl = iPrtcl
                continue
            iLoc = -1
            for iTrcSpc in iPrtcl.getTraceSpace():
                iLoc += 1
                if iLoc > (len(xLoc) - 1):
                    nLoc.append(iPrtcl.getLocation()[iLoc])
                    xLoc.append([])
                    xpLoc.append([])
                    yLoc.append([])
                    ypLoc.append([])
                    ELoc.append([])
                    ELab.append([])
                    Scl.append([])

                """
                print(" Here:", iLoc)
                print("     ---->", iPrtcl.getTraceSpace()[iLoc])
                print("     ---->", iRefPrtcl.getPrOut()[iLoc])
                """

                p0 = mth.sqrt(
                    np.dot(
                        iRefPrtcl.getPrOut()[iLoc][:3], iRefPrtcl.getPrOut()[iLoc][:3]
                    )
                )
                E0 = iRefPrtcl.getPrOut()[iLoc][3]
                b0 = p0 / E0
                E = E0 + iPrtcl.getTraceSpace()[iLoc][5] * p0
                p = mth.sqrt(E**2 - protonMASS**2)
                E -= protonMASS
                D = mth.sqrt(
                    1.0
                    + 2.0 * iPrtcl.getTraceSpace()[iLoc][5] / b0
                    + iPrtcl.getTraceSpace()[iLoc][5] ** 2
                )

                eps = (
                    iPrtcl.getTraceSpace()[iLoc][1] ** 2
                    + iPrtcl.getTraceSpace()[iLoc][3] ** 2
                ) / (2.0 * D**2)
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

        plotFILE = "99-Scratch/ParticleProgressionPlot.pdf"

        with PdfPages(plotFILE) as pdf:
            for iLoc in range(len(xLoc)):
                fig, axs = plt.subplots(
                    nrows=3, ncols=2, figsize=(6.0, 6.0), constrained_layout=True
                )

                Ttl = nLoc[iLoc]
                fig.suptitle(Ttl, fontdict=font)

                axs[0, 0].hist2d(xLoc[iLoc], yLoc[iLoc], bins=100)
                axs[0, 0].set_xlabel("x (m)")
                axs[0, 0].set_ylabel("y (m)")

                axs[0, 1].hist(ELoc[iLoc], 100)
                axs[0, 1].set_xlabel("delta")
                axs[0, 1].set_ylabel("Number")

                axs[1, 0].hist2d(xLoc[iLoc], xpLoc[iLoc], bins=100)
                axs[1, 0].set_xlabel("x (m)")
                axs[1, 0].set_ylabel("xprime (m)")

                axs[1, 1].hist2d(yLoc[iLoc], ypLoc[iLoc], bins=100)
                axs[1, 1].set_xlabel("y (m)")
                axs[1, 1].set_ylabel("yprime (m)")

                axs[2, 0].hist(ELab[iLoc], 100)
                axs[2, 0].set_xlabel("Kinetic energy (MeV)")
                axs[2, 0].set_ylabel("Number")

                axs[2, 1].hist(Scl[iLoc], 100)
                axs[2, 1].set_xlabel("Epsilon")
                axs[2, 1].set_ylabel("Number")
                print("Plotted:", nLoc[iLoc])

                pdf.savefig()
                plt.close()

    @classmethod
    def plotParticleTrajectory_Lab(cls, axyz=None, axxz=None):

        line_collection_list = []
        line_collection_list_term = []

        x_lab = []
        y_lab = []
        z_lab = []

        for nPrtcl, iPrtcl in enumerate(cls.getParticleInstances()):
            if isinstance(iPrtcl, ReferenceParticle):
                NInsts = len(cls.getParticleInstances())
                NLocs = len(iPrtcl.getRrOut())
                x_lab = np.full((NInsts, NLocs), np.nan)
                y_lab = np.full((NInsts, NLocs), np.nan)
                z_lab = np.full((NInsts, NLocs), np.nan)
                continue

            iPrtcl.fillPhaseSpace()

            iLabPhaseSpace = np.array(iPrtcl.getLabPhaseSpace())
            maxN = len(iLabPhaseSpace)

            x_lab[nPrtcl, :maxN] = iLabPhaseSpace[:, 0, 0]
            y_lab[nPrtcl, :maxN] = iLabPhaseSpace[:, 0, 1]
            z_lab[nPrtcl, :maxN] = iLabPhaseSpace[:, 0, 2]
        # print(x_lab)
        segmentsYZ = np.dstack((z_lab, y_lab))
        segmentsXZ = np.dstack((z_lab, x_lab))

        if axxz is not None:

            # Finding the elements that have nan at end:

            segments_terminated_XZ = segmentsXZ[np.isnan(segmentsXZ[:, -1, 1])]
            segments_end_XZ = segmentsXZ[~np.isnan(segmentsXZ[:, -1, 1])]
            # as it is not the same length for all, need a different method to see which one gets deleted, or need to put nan values in.
            line_collection_end = LineCollection(
                segments_end_XZ, linewidths=0.5, colors="green", linestyle="solid"
            )
            line_collection_terminated = LineCollection(
                segments_terminated_XZ, linewidths=0.5, color="red", linestyle="solid"
            )
            line_collection_list.append(line_collection_end)
            line_collection_list_term.append(line_collection_terminated)
            axxz.add_collection(line_collection_end)
            axxz.add_collection(line_collection_terminated)
            axxz.set_xlabel("z [m]")
            axxz.set_ylabel("x [m]")
            axxz.set_title("Particle Trajectory (Lab; x-z plane)")
            for row in segments_end_XZ[0, :, 0]:
                axxz.axvline(x=row, color="black", linestyle="--", linewidth=0.1)

        if axyz is not None:
            segments_terminated_YZ = segmentsYZ[np.isnan(segmentsXZ[:, -1, 1])]
            segments_end_YZ = segmentsYZ[~np.isnan(segmentsXZ[:, -1, 1])]
            line_collection_2 = LineCollection(
                segments_end_YZ, linewidths=0.5, colors="blue", linestyle="solid"
            )
            line_collection_terminated = LineCollection(
                segments_terminated_YZ,
                linewidths=0.5,
                color="purple",
                linestyle="solid",
            )

            line_collection_list.append(line_collection_2)
            line_collection_list_term.append(line_collection_terminated)
            axyz.add_collection(line_collection_2)
            axyz.add_collection(line_collection_terminated)
            axyz.set_xlabel("z [m]")
            axyz.set_ylabel("y [m]")
            axyz.set_title("Particle Trajectory (Lab; y-z plane)")
            for row in segments_end_YZ[0, :, 0]:
                axyz.axvline(x=row, color="black", linestyle="--", linewidth=0.1)

        return line_collection_list

    @classmethod
    def plotParticleTrajectory_RPLC(cls, axyz=None, axxz=None):

        line_collection_list = []
        line_collection_list_term = []

        x_RPLC = []
        y_RPLC = []
        z_RPLC = []

        nPrtcl = 0

        for nPrtcl, iPrtcl in enumerate(cls.getParticleInstances()):

            if isinstance(iPrtcl, ReferenceParticle):

                NInsts = len(cls.getParticleInstances())
                NLocs = len(iPrtcl.getRrOut())
                x_RPLC = np.full((NInsts, NLocs), np.nan)
                y_RPLC = np.full((NInsts, NLocs), np.nan)
                z_RPLC = np.full((NInsts, NLocs), np.nan)
                continue

            iTraceSpace = np.array(iPrtcl.getTraceSpace())
            icoords = np.array(iPrtcl.gets())

            maxN = len(iTraceSpace)

            x_RPLC[nPrtcl, :maxN] = iTraceSpace[:, 0]
            y_RPLC[nPrtcl, :maxN] = iTraceSpace[:, 2]
            z_RPLC[nPrtcl, :maxN] = icoords[:]

        segmentsYZ = np.dstack((z_RPLC, y_RPLC))
        segmentsXZ = np.dstack((z_RPLC, x_RPLC))

        if axxz is not None:

            # Finding the elements that have nan at end:
            segments_terminated_XZ = segmentsXZ[np.isnan(segmentsXZ[:, -1, 1])]
            segments_end_XZ = segmentsXZ[~np.isnan(segmentsXZ[:, -1, 1])]
            # print(segments_end_XZ[1])
            # as it is not the same length for all, need a different method to see which one gets deleted, or need to put nan values in.
            line_collection_end = LineCollection(
                segments_end_XZ, linewidths=0.5, colors="green", linestyle="solid"
            )
            line_collection_terminated = LineCollection(
                segments_terminated_XZ, linewidths=0.5, color="red", linestyle="solid"
            )
            line_collection_list.append(line_collection_end)
            line_collection_list_term.append(line_collection_terminated)
            axxz.add_collection(line_collection_end)
            axxz.add_collection(line_collection_terminated)
            axxz.set_xlabel("z [m]")
            axxz.set_ylabel("x [m]")
            axxz.set_title("Particle Trajectory (RPLC; x-z plane)")

            for row in segments_end_XZ[0, :, 0]:
                axxz.axvline(x=row, color="black", linestyle="--", linewidth=0.1)

        if axyz is not None:
            segments_terminated_YZ = segmentsYZ[np.isnan(segmentsXZ[:, -1, 1])]
            segments_end_YZ = segmentsYZ[~np.isnan(segmentsXZ[:, -1, 1])]
            line_collection_2 = LineCollection(
                segments_end_YZ, linewidths=0.5, colors="green", linestyle="solid"
            )
            line_collection_terminated = LineCollection(
                segments_terminated_YZ, linewidths=0.5, color="red", linestyle="solid"
            )

            line_collection_list.append(line_collection_2)
            line_collection_list_term.append(line_collection_terminated)
            axyz.add_collection(line_collection_2)
            axyz.add_collection(line_collection_terminated)
            axyz.set_xlabel("z [m]")
            axyz.set_ylabel("y [m]")

            axyz.set_title("Particle Trajectory (RPLC; y-z plane)")
            for row in segments_end_YZ[0, :, 0]:
                axyz.axvline(x=row, color="black", linestyle="--", linewidth=0.1)

        return line_collection_list

    def printProgression(self):
        for iLoc in range(len(self.getLocation())):
            with np.printoptions(linewidth=500, precision=5, suppress=True):
                print(
                    self.getLocation()[iLoc],
                    ": z, s, trace space:",
                    self.getz()[iLoc],
                    self.gets()[iLoc],
                    self.getTraceSpace()[iLoc],
                )

    # --------  Processing methods:
    @classmethod
    def fillPhaseSpaceAll(cls):  # doesn't seem to work
        Success = False
        if cls.getDebug():
            print(" Particle.fillPhaseSpaceAll, start:")
            print(
                "     ----> fill phase space for",
                len(cls.getParticleInstances()),
                "particle instances.",
            )

        nPrtcl = 0
        for iPrtcl in cls.getParticleInstances():
            nPrtcl += 1
            if cls.getDebug():
                print("     ----> Particle:", nPrtcl)

            if not isinstance(iPrtcl, ReferenceParticle):
                if Particle.getDebug():
                    print("         ----> Fill phase space for particle:", nPrtcl)
                    Success = iPrtcl.fillPhaseSpace()

        if cls.getDebug():
            print(
                "     ----> Particle.fillPhaseSpaceAll:",
                "fill phase space Success =",
                Success,
            )
            print(" <----  Particle.fillPhaseSpaceAll, compete.")

        return Success

    def fillPhaseSpace(self):
        Success = False
        if self.getDebug():
            print(" Particle.fillPhaseSpace, start:")
            print(
                "     ----> fill phase space for particle with",
                len(self.getLocation()),
                "records.",
            )

        iRefPrtcl = ReferenceParticle.getinstance()

        nLoc = 0
        for iLoc in self.getLocation():
            if self.getDebug():
                print("         ----> Convert at location:", iLoc)
            PhsSpc = self.calcRPLCPhaseSpace(nLoc)
            Success = self.setRPLCPhaseSpace(PhsSpc)

            RotMtrx = iRefPrtcl.getRot2LabOut()[nLoc]
            drLab = np.matmul(RotMtrx, PhsSpc[0])
            pLab = np.matmul(RotMtrx, PhsSpc[1])

            rLab = iRefPrtcl.getRrOut()[nLoc][0:3] + drLab

            LabPhsSpc = [rLab, pLab]
            Success = self.setLabPhaseSpace(LabPhsSpc)

            nLoc += 1

        if nLoc == len(self.getLocation()):
            Success = True

        if self.getDebug():
            with np.printoptions(linewidth=500, precision=7, suppress=True):
                print("     ----> Particle.fillPhaseSpace: RPLC phase space:", PhsSpc)
            with np.printoptions(linewidth=500, precision=7, suppress=True):
                print(
                    "     ----> Particle.fillPhaseSpace:  Lab phase space:", LabPhsSpc
                )
            print(" <----  Particle.fillPhaseSpace, compete.", "Success:", Success)

        return Success

    def calcRPLCPhaseSpace(self, nLoc=None):
        if self.getDebug():
            print(" Particle.calcRPLCPhaseSpace for nLoc:", nLoc, "start:")

        TrcSpc = self.getTraceSpace()[nLoc]
        if self.getDebug():
            with np.printoptions(linewidth=500, precision=7, suppress=True):
                print("     ----> trace space:", TrcSpc)

        rRPLC = np.array([TrcSpc[0], TrcSpc[2], 0.0])

        p0 = BL.BeamLine.getElement()[0].getp0()

        E0 = np.sqrt(protonMASS**2 + p0**2)
        Enrgy = E0 + (TrcSpc[5] * p0)
        # print(Enrgy, protonMASS)

        Enrgy = protonMASS**2 + (TrcSpc[5] * p0) ** 2  # what?
        # print(Enrgy, protonMASS)

        Mmtm = mth.sqrt(Enrgy**2 - protonMASS**2)
        zPrm = mth.sqrt(1.0 - TrcSpc[1] ** 2 - TrcSpc[3] ** 2)  #:)
        pRPLC = np.array([TrcSpc[1] * Mmtm, TrcSpc[3] * Mmtm, zPrm * Mmtm])  #:)

        if self.getDebug():
            with np.printoptions(linewidth=500, precision=7, suppress=True):
                print("     ----> position:", rRPLC)
                print("     ----> Mmtm    :", pRPLC)

        PhsSpc = [rRPLC, pRPLC]

        if self.getDebug():
            with np.printoptions(linewidth=500, precision=7, suppress=True):
                print(" <---- Return phase space:", PhsSpc)

        return PhsSpc

    # --------  I/o methods:
    #                     ----> Write instances:
    @classmethod
    def createParticleFile(cls, datafilePATH=None, datafileNAME=None):
        if cls.getDebug():
            print("Particle.createParticleFile:", datafilePATH, datafileNAME)

        if datafilePATH == None:
            raise noPATH(" Particle.createParticleFile: no path given.")

        if datafileNAME == None:
            raise noNAME(" Particle.createParticleFile: no file name given.")

        if not os.path.exists(datafilePATH):
            raise noPATH(" Particle.createParticleFile: path does not exist.")

        ParticleFILE = open(os.path.join(datafilePATH, datafileNAME), "wb")

        if cls.getDebug():
            print("     ----> File created:", ParticleFILE)

        return ParticleFILE

    def writeParticle(self, ParticleFILE=None):
        if self.getDebug():
            print("Particle.writeParticle starts.")

        if not isinstance(ParticleFILE, io.BufferedWriter):
            raise noFILE(" Particle.writeParticle: file does not exist.")

        nLoc = len(self.getLocation())
        if self.getDebug():
            print("     ----> Number of locations to store:", nLoc)
        record = strct.pack(">i", nLoc)
        ParticleFILE.write(record)

        for iLoc in range(len(self.getLocation())):
            bLocation = bytes(self.getLocation()[iLoc], "utf-8")

            record = strct.pack(">i", len(bLocation))
            ParticleFILE.write(record)
            if self.getDebug():
                print("         ----> Length of bLocation:", strct.unpack(">i", record))

            record = bLocation
            ParticleFILE.write(record)

            if self.getDebug():
                print("         ----> Location:", bLocation.decode("utf-8"))

            record = strct.pack(
                ">8d",
                self.getz()[iLoc],
                self.gets()[iLoc],
                self.getTraceSpace()[iLoc][0],
                self.getTraceSpace()[iLoc][1],
                self.getTraceSpace()[iLoc][2],
                self.getTraceSpace()[iLoc][3],
                self.getTraceSpace()[iLoc][4],
                self.getTraceSpace()[iLoc][5],
            )
            ParticleFILE.write(record)
            if self.getDebug():
                print("         ----> z, s, trace space:", strct.unpack(">8d", record))

        Cleaned = self.cleanParticles()

    @classmethod
    def flushNcloseParticleFile(cls, ParticleFILE=None):
        if cls.getDebug():
            print("Particle.flushNcloseParticleFile starts")

        if not isinstance(ParticleFILE, io.BufferedWriter):
            raise noFILE(" Particle.flushNcloseParticle: file does not exist.")

        ParticleFILE.flush()
        ParticleFILE.close()

    #                     ----> Write instances:
    @classmethod
    def openParticleFile(cls, datafilePATH=None, datafileNAME=None):
        if cls.getDebug():
            print("Particle.openParticleFile:", datafilePATH, datafileNAME)

        if datafilePATH == None:
            raise noPATH(" Particle.openParticleFile: no path given.")

        if datafileNAME == None:
            raise noNAME(" Particle.openParticleFile: no file name given.")

        if not os.path.exists(datafilePATH):
            raise noPATH(" Particle.openParticleFile: path does not exist.")

        ParticleFILE = open(os.path.join(datafilePATH, datafileNAME), "rb")

        if cls.getDebug():
            print("     ----> File opened:", ParticleFILE)

        return ParticleFILE

    @classmethod
    def readParticle(cls, ParticleFILE=None):
        if cls.getDebug():
            print("Particle.readParticle starts.")

        if not isinstance(ParticleFILE, io.BufferedReader):
            raise noFILE(" Particle.writeParticle: file does not exist.")

        brecord = ParticleFILE.read(4)
        if brecord == b"":
            if cls.getDebug():
                print(" <---- end of file, return.")
            return True

        record = strct.unpack(">i", brecord)
        nLoc = record[0]
        if cls.getDebug():
            print("     ----> Number of locations to read:", nLoc)
        if nLoc > 0:
            iPrtcl = Particle()

        for iLoc in range(nLoc):
            brecord = ParticleFILE.read(4)
            record = strct.unpack(">i", brecord)
            len = record[0]
            if cls.getDebug():
                print("         ----> Length of bLocation:", len)

            brecord = ParticleFILE.read(len)
            Location = brecord.decode("utf-8")
            if cls.getDebug():
                print("         ----> Location:", Location)

            brecord = ParticleFILE.read((8 * 8))
            record = strct.unpack(">8d", brecord)
            z = float(record[0])
            s = float(record[1])
            TrcSpc = np.array(
                [
                    float(record[2]),
                    float(record[3]),
                    float(record[4]),
                    float(record[5]),
                    float(record[6]),
                    float(record[7]),
                ]
            )
            if cls.getDebug():
                print("         ----> z, s, trace space:", z, s, TrcSpc)

            iPrtcl.recordParticle(Location, z, s, TrcSpc)

        if cls.getDebug():
            print("     <---- Particle instsance")
            print(iPrtcl)
            print(" <---- readParticle done.")
        cls.setDebug(False)
        return False

    @classmethod
    def closeParticleFile(cls, ParticleFILE=None):
        if cls.getDebug():
            print("Particle.closeParticleFile starts")

        if not isinstance(ParticleFILE, io.BufferedReader):
            raise noFILE(" Particle.closeParticle: file does not exist.")

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

 setReferenceParticleAtDrift: I/p: iBLE : BeamLineElement instance
                               Sets attributes for reference partice for a
                               drift space.  Also works for apertures,
                               quads, and any element that has length but
                               does not bend the beam, such as quadropole.

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
    __instance = None
    __RPDebug = False

    # --------  "Built-in methods":
    def __init__(self):
        if ReferenceParticle.getinstance() is None:
            if self.__RPDebug:
                print(
                    " ReferenceParticle(Particle).__init__: ",
                    "creating the ReferenceParticle object",
                )
            ReferenceParticle.setinstance(self)

            # .. Particle class initialisation:
            Particle.__init__(self)

            # .. Set ReferenceParticle attributes to None: (Switched position!)
            self.setAllRP2None()

            # Only constants; print values that will be used:
            if self.getRPDebug():
                print(self)

        else:
            print(
                " ReferenceParticle(Particle).__init__: ",
                " attempt to create second reference particle.",
                " Abort!",
            )
            raise secondReferenceParticle(" Second call not allowed.")

        return

    def __repr__(self):
        return "ReferenceParticle()"

    def __str__(self):
        print(" ReferenceParticle:")
        print(" ==================")
        print("     ----> Debug     :", self.getRPDebug())
        print("     ----> Location  :", self.getLocation())
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

    # --------  "Get methods" only; version, reference, and constants
    # .. Methods believed to be self documenting(!)

    @classmethod
    def getinstance(cls):
        return cls.__instance

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
        return mth.sqrt(np.dot(self.getPrIn()[iLoc][:3], self.getPrIn()[iLoc][:3]))

    def getPrOut(self):
        return self._PrOut

    def getMomentumOut(self, iLoc):
        return mth.sqrt(np.dot(self.getPrOut()[iLoc][:3], self.getPrOut()[iLoc][:3]))

    def getRot2LabIn(self):
        return self._Rot2LabIn

    def getRot2LabOut(self):
        return self._Rot2LabOut

    # --------  "Set methods";
    @classmethod
    def cleaninstance(cls):
        if isinstance(cls.__instance, ReferenceParticle):
            del cls.__instance
            cls.resetinstance()

    @classmethod
    def resetinstance(cls):
        cls.__instance = None

    @classmethod
    def setinstance(cls, inst):
        if isinstance(inst, ReferenceParticle):
            cls.__instance = inst
        else:
            raise badArgument()

    def setRPDebug(self, Debug):
        if isinstance(Debug, bool):
            self.__RPDebug = Debug
        else:
            raise badArgument()

    def setAllRP2None(self):
        self._sIn = []
        self._sOut = []
        self._RrIn = []
        self._PrIn = []
        self._RrOut = []
        self._PrOut = []
        self._Rot2LabIn = []
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

    # --------  Processing methods:
    def setReferenceParticle(self):
        Success = False
        if self.getRPDebug():
            print(" ReferenceParticle(Particle).setReferenceParticle", "starts.")

        # .. Loop over beam-line elements:
        for iBLE in BLE.BeamLineElement.getinstances():
            if isinstance(iBLE, BLE.Facility):
                continue
            if isinstance(iBLE, BLE.Source):
                Success = self.setReferenceParticleAtSource()
                if not Success:
                    raise fail2setReferenceParticle("setReferenceParticleAtSource")
            elif (
                isinstance(iBLE, BLE.Drift)
                or isinstance(iBLE, BLE.Aperture)
                or isinstance(iBLE, BLE.FocusQuadrupole)
                or isinstance(iBLE, BLE.DefocusQuadrupole)
            ):
                Success = self.setReferenceParticleAtDrift(iBLE)
                if not Success:
                    raise fail2setReferenceParticle("setReferenceParticleAtDrift")
            elif isinstance(iBLE, BLE.SectorDipole):
                Success = self.setReferenceParticleAtSectorDipole(iBLE)
                if not Success:
                    raise fail2setReferenceParticle(
                        "setReferenceParticleAtSectorDipole"
                    )

            Success = self.setLocation(iBLE.getName())
            if not Success:
                raise fail2setReferenceParticle("setLocation")

        if self.getRPDebug():
            print("     ----> Dump refence particle:")
            print(self)

        return Success

    def setReferenceParticleAtSource(self):
        nRcrds = len(self.getsIn())
        print(nRcrds)
        # Not sure about this? Assuming source is in position 1?

        Success = self.setLocation(
            BLE.BeamLineElement.getinstances()[nRcrds + 1].getName()
        )
        if not Success:
            raise fail2setReferenceParticle("Name")

        Success = self.setsIn(0.0)
        if not Success:
            raise fail2setReferenceParticle("sIn")
        Success = self.setsOut(0.0)
        if not Success:
            raise fail2setReferenceParticle("sOut")

        RrIn = np.array([0.0, 0.0, 0.0, 0.0])
        RrOut = np.array([0.0, 0.0, 0.0, 0.0])
        Success = self.setRrIn(RrIn)
        if not Success:
            raise fail2setReferenceParticle("RrIn")
        Success = self.setRrOut(RrOut)
        if not Success:
            raise fail2setReferenceParticle("RrOut")

        p0 = BL.BeamLine.getElement()[0].getp0()
        Ref4mmtm = np.array([0.0, 0.0, p0, mth.sqrt(p0**2 + protonMASS**2)])

        PrIn = Ref4mmtm
        PrOut = Ref4mmtm
        Success = self.setPrIn(PrIn)
        if not Success:
            raise fail2setReferenceParticle("PrIn")
        Success = self.setPrOut(PrOut)
        if not Success:
            raise fail2setReferenceParticle("PrOut")

        Rot2LabIn = np.array(
            [
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
            ]
        )
        Rot2LabOut = np.array(
            [
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
            ]
        )

        # Rotates in x and z by angle theta

        Success = self.setRot2LabIn(Rot2LabIn)
        if not Success:
            raise fail2setReferenceParticle("Rot2LabIn")
        Success = self.setRot2LabOut(Rot2LabOut)
        if not Success:
            raise fail2setReferenceParticle("Rot2LabOut")

        # .. Now particle position/trace space:
        Success = self.setz(self.getRrOut()[0][3])
        if not Success:
            raise fail2setReferenceParticle("setz")
        Success = self.sets(self.getsOut()[0])
        if not Success:
            raise fail2setReferenceParticle("sets")
        TrcSpc = np.array([0.0, 0.0, 0.0, 0.0, np.nan, np.nan])
        Success = self.setTraceSpace(TrcSpc)
        if not Success:
            raise fail2setReferenceParticle("setTraceSpace")

        return Success

    def setReferenceParticleAtDrift(self, iBLE=None):
        nRcrds = len(self.getsIn())

        # Changed to (nRcrds + 1) -> nRcds

        Success = self.setLocation(
            BLE.BeamLineElement.getinstances()[nRcrds + 1].getName()
        )
        if not Success:
            raise fail2setReferenceParticle("Name")

        Success = self.setsIn(self.getsOut()[nRcrds - 1])
        if not Success:
            raise fail2setReferenceParticle("sIn")
        Success = self.setsOut(self.getsOut()[nRcrds - 1] + iBLE.getLength())
        if not Success:
            raise fail2setReferenceParticle("sOut")

        RrIn = self.getRrOut()[nRcrds - 1]

        Mmtm = mth.sqrt(
            self.getPrOut()[nRcrds - 1][0] ** 2
            + self.getPrOut()[nRcrds - 1][1] ** 2
            + self.getPrOut()[nRcrds - 1][2] ** 2
        )
        cx = self.getPrOut()[nRcrds - 1][0] / Mmtm
        cy = self.getPrOut()[nRcrds - 1][1] / Mmtm
        cz = self.getPrOut()[nRcrds - 1][2] / Mmtm
        RrOut = np.array(
            [
                RrIn[0] + cx * iBLE.getLength(),
                RrIn[1] + cy * iBLE.getLength(),
                RrIn[2] + cz * iBLE.getLength(),
                0.0,
            ]
        )
        # Nothing done to time coordinate either?
        Success = self.setRrIn(RrIn)
        if not Success:
            raise fail2setReferenceParticle("RrIn")
        Success = self.setRrOut(RrOut)
        if not Success:
            raise fail2setReferenceParticle("RrOut")

        PrIn = self.getPrOut()[nRcrds - 1]
        PrOut = PrIn
        Success = self.setPrIn(PrIn)
        if not Success:
            raise fail2setReferenceParticle("PrIn")
        Success = self.setPrOut(PrOut)
        if not Success:
            raise fail2setReferenceParticle("PrOut")

        Rot2LabIn = self.getRot2LabOut()[nRcrds - 1]
        Rot2LabOut = Rot2LabIn
        Success = self.setRot2LabIn(Rot2LabIn)
        if not Success:
            raise fail2setReferenceParticle("Rot2LabIn")
        Success = self.setRot2LabOut(Rot2LabOut)
        if not Success:
            raise fail2setReferenceParticle("Rot2LabOut")

        # .. Now particle position/trace space:
        Success = self.setz(self.getRrOut()[nRcrds][2])
        if not Success:
            raise fail2setReferenceParticle("setz")
        Success = self.sets(self.getsOut()[nRcrds])
        if not Success:
            raise fail2setReferenceParticle("sets")
        TrcSpc = np.array([0.0, 0.0, 0.0, 0.0, np.nan, np.nan])
        Success = self.setTraceSpace(TrcSpc)
        if not Success:
            raise fail2setReferenceParticle("setTraceSpace")

        return Success

    def setReferenceParticleAtSectorDipole(self, iBLE=None):
        nRcrds = len(self.getsIn())

        Success = self.setLocation(
            BLE.BeamLineElement.getinstances()[nRcrds + 1].getName()
        )
        if not Success:
            raise fail2setReferenceParticle("Name")

        # For the dipole this should still be fine.
        # So just adding on the ``path length'' of the dipole. Check if this is set
        # Correctly

        Success = self.setsIn(self.getsOut()[nRcrds - 1])
        if not Success:
            raise fail2setReferenceParticle("sIn")
        Success = self.setsOut(self.getsOut()[nRcrds - 1] + iBLE.getLength())
        if not Success:
            raise fail2setReferenceParticle("sOut")

        # RrOut and RrIn are documented as lab frame!
        # Position coord in is taken as the last position out - still fine.

        RrIn = self.getRrOut()[nRcrds - 1]

        # Working out total momentum? (Lab Frame!)

        Mmtm = mth.sqrt(
            self.getPrOut()[nRcrds - 1][0] ** 2
            + self.getPrOut()[nRcrds - 1][1] ** 2
            + self.getPrOut()[nRcrds - 1][2] ** 2
        )

        # B field in y direction

        # if "AC"==True:
        # theta = iBLE.getAngle()  # only dipole here
        # thetap = theta / 2
        # else:
        # theta = -iBLE.getAngle()  # only dipole here
        # thetap = theta / 2

        # thetaZ = 0  # chooses the plane of bend
        # removed thetaz, as we are not dealing with intermediate planes

        # Default is an upward bend in YZ plane
        dipolePlane = iBLE.getPlane()
        theta = -iBLE.getAngle()
        thetap = theta / 2
        Rotation = RotMat_x(thetap)  # On momenta unit vector
        Rotation2 = RotMat_x(theta)  # On coordinates

        # Default is upward bend in YZ

        if "up" == True and "YZ" == True:
            theta = theta
            thetap = theta / 2
            Rotation = Rotation
            Rotation2 = Rotation2

        # Conditions for upward bend in XZ

        elif "up" == True and "YZ" == False:
            theta = iBLE.getAngle()
            thetap = theta / 2
            Rotation = RotMat_y(thetap)
            Rotation2 = RotMat_y(theta)

        # Conditions for downward bend in YZ

        elif "up" == False and "YZ" == True:
            theta = iBLE.getAngle()
            thetap = theta / 2
            Rotation = RotMat_x(thetap)
            Rotation2 = RotMat_x(theta)

        # Conditions for downward bend in XZ
        else:
            theta = theta
            thetap = theta / 2
            Rotation = RotMat_y(thetap)
            Rotation2 = RotMat_y(theta)

        cx = self.getPrOut()[nRcrds - 1][0] / Mmtm
        cy = self.getPrOut()[nRcrds - 1][1] / Mmtm
        cz = self.getPrOut()[nRcrds - 1][2] / Mmtm

        unit = np.array([cx, cy, cz])

        cx, cy, cz = Rotation @ unit

        Brho = (1 / (speed_of_light * 1.0e-9)) * Mmtm / 1000.0
        r = Brho / iBLE.getB()
        d = 2 * r * np.sin(theta / 2)

        print("d:", d)
        print("r:", r)

        # works out chord vector

        RrOut = np.array(
            [
                RrIn[0] + cx * np.abs(d),
                RrIn[1] + cy * np.abs(d),
                RrIn[2] + cz * np.abs(d),
                0.0,  # ignore time
            ]
        )
        Success = self.setRrIn(RrIn)
        if not Success:
            raise fail2setReferenceParticle("RrIn")
        Success = self.setRrOut(RrOut)
        if not Success:
            raise fail2setReferenceParticle("RrOut")

        # Momentum; rotate by theta

        PrIn = self.getPrOut()[nRcrds - 1]  # PrIn unchanged
        PrOut = np.zeros(4)
        PrOut[0:3] = Rotation2 @ PrIn[0:3]

        # PrOut[0:3] = (
        # RotMat_z(thetaZ) @ RotMat_x(theta) @ RotMat_z(thetaZ).T @ PrIn[0:3]
        # )  # Rotate PrOut

        PrOut[3] = PrIn[3]  # Energy unchanged
        Success = self.setPrIn(PrIn)
        if not Success:
            raise fail2setReferenceParticle("PrIn")
        Success = self.setPrOut(PrOut)
        if not Success:
            raise fail2setReferenceParticle("PrOut")

        # Now define coordinate axes rotation

        Rot2LabIn = self.getRot2LabOut()[nRcrds - 1]  # accumulated rotation
        Rot2LabOut = Rotation2 @ Rot2LabIn

        Success = self.setRot2LabIn(Rot2LabIn)
        if not Success:
            raise fail2setReferenceParticle("Rot2LabIn")
        Success = self.setRot2LabOut(Rot2LabOut)
        if not Success:
            raise fail2setReferenceParticle("Rot2LabOut")

        # .. Now particle position/trace space:

        # WRONG CHANGE!!!
        Success = self.setz(self.getRrOut()[nRcrds][2])
        if not Success:
            raise fail2setReferenceParticle("setz")
        Success = self.sets(self.getsOut()[nRcrds])
        if not Success:
            raise fail2setReferenceParticle("sets")

        # Not sure about this?
        TrcSpc = np.array([0.0, 0.0, 0.0, 0.0, np.nan, np.nan])
        Success = self.setTraceSpace(TrcSpc)
        if not Success:
            raise fail2setReferenceParticle("setTraceSpace")

        return Success


# --------  Exceptions:
class noReferenceParticle(Exception):
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
