#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class PhysicalConstants
=======================

  Defines the physical constants that are required to carry out the linear
  optics calculations for the LhARA_beamlinenpackage.

  The values are taken from, for example, the PDG.  The constants packages is
  implemented as a singleton class so that there is no ambiguity about which
  values are in use. 

  Class attributes:
  -----------------
  __instance : Set on creation of first (and only) instance.
  __Debug    : Debug flag

      
  Instance attributes:
  --------------------
  None; all constants returned by "get" methods.


  Methods:
  --------
  Built-in methods __new__, __repr__ and __str__.
      __new__ : Creates single instance of PhysicalConstants class.
      __repr__: One liner with call.
      __str__ : Dump of constants

  Set methods:
      setDebug  : Set debug flag

  Get/set methods:
      getDebug  : get debug flag
      CdVrsn()  : Returns code version number.
      PDGref()  : Returns reference to version of PDG used for
                  constants.
         SoL()  : Speed of light (m/s)

  Processing method:
      print()   : Dumps parameters

  
Created on Mon 12Jun23: Version history:
----------------------------------------
 1.0: 12Jun23: First implementation
 1.1: 21Mar24: Add mass of the pion and mass of the muon
 1.2: 06Aug25: Add the lifetime of the pion, muon, proton and neutrino

@author: kennethlong
"""

import scipy           as sp
import scipy.constants
import math


class PhysicalConstants(object):
    __instance = None
    __Debug    = False
    _Species   = ["proton", "pion", "muon", "neutrino", "12c6"]

#--------  "Built-in methods":
    def __new__(cls):
        if cls.__instance is None:
            if cls.getDebug():
                print(' PhysicalConstants.__new__: ', \
                      'creating the PhysicalConstants object')
            cls.__instance = super(PhysicalConstants, cls).__new__(cls)

        # Only constants; print values that will be used:
        if cls.getDebug():
            print(" PhysicalConstants: version:", cls.CdVrsn(cls))
            print("PhysicalConstants: PDG reference:", cls.PDGref(cls))
            print("PhysicalConstants: speed of light:", cls.SoL(cls))
            
        return cls.getinstances()

    def __repr__(self):
        return "PhysicalConstants()"

    def __str__(self):
        print(" PhysicalConstants:")
        print(" ==================")
        print("      ----> version:", self.CdVrsn())
        print("      ----> PDG reference:", self.PDGref())
        print("      ----> speed of light (m/s):", self.SoL())
        print("      ----> electron mass (MeV/c2):", self.me())
        print("      ----> proton mass (MeV/c2):", self.mp())
        print("      ----> proton lifetime (s):", self.tauP())
        print("      ----> pion mass (MeV/c2):", self.mPion())
        print("      ----> pion lifetime (s):", self.tauPion())
        print("      ----> muon mass (MeV/c2):", self.mMuon())
        print("      ----> muon lifetime (s):", self.tauMuon())
        print("      ----> neutrino mass (MeV/c2):", self.mNeutrino())
        print("      ----> neutrino lifetime (s):", self.tauNeutrino())
        print("      ----> 12C6 mass (MeV/c2):", self.m12c6())
        print("      ----> 12C6 lifetime (s):", self.tau12c6())
        print("      ----> Permitivity of free space (N/A**2):", self.mu0())
        print("      ----> debug flag:", self.getDebug())
        return " <---- PhysicalConstants dump complete."

    
#--------  "Set method" only Debug
#.. Method believed to be self documenting(!)
    @classmethod
    def setAll2None(cls): 
        pass
       
    @classmethod
    def setDebug(cls, Debug=False):
        if cls.__Debug:
            print(" PhysicalConstants.setdebug: ", Debug)
        cls.__Debug = Debug
        

#--------  "Get methods" only; version, reference, and constants
#.. Methods believed to be self documenting(!)
    @classmethod
    def getDebug(cls):
        return cls.__Debug

    @classmethod
    def getinstances(cls):
        return cls.__instance

    def CdVrsn(self):
        return 1.0

    def PDGref(self):
        return "P.A. Zyla et al. (Particle Data Group), " \
            "Prog. Theor. Exp. Phys. 2020, 083C01 (2020)."

    def SoL(self):
        return sp.constants.c

    @classmethod
    def getSpecies(cls):
        return cls._Species

    @classmethod
    def getparticleCHARGE(cls, _Species):
        particleCHARGE = None
        if not isinstance(_Species, str):
            raise badParameter("PhysicalConstants.getParticleCHARGE:", \
                               " Species " + _Species + " not a string!")
        if _Species.lower() in PhysicalConstants.getSpecies():
            if   _Species.lower() == "proton":
                particleCHARGE = 1.
            elif _Species.lower() == "pion":
                particleCHARGE = 1.
            elif _Species.lower() == "muon":
                particleCHARGE = 1.
            elif _Species.lower() == "neutrino":
                particleCHARGE = 0.
            elif _Species.lower() == "12c6":
                particleCHARGE = 6.
        else:
            raise badParameter("PhysicalConstants.getParticleCHARGE:", \
                               "species " + _Species + " not allowed!")
        return particleCHARGE

    def getparticleMASS(self, _Species):
        particleMASS = None
        if not isinstance(_Species, str):
            raise badParameter("PhysicalConstants.getParticleMASS: " \
                               " Species " + _Species + " not a string!")
        if _Species.lower() in PhysicalConstants.getSpecies():
            if   _Species.lower() == "proton":
                particleMASS = self.mp()
            elif _Species.lower() == "pion":
                particleMASS = self.mPion()
            elif _Species.lower() == "muon":
                particleMASS = self.mMuon()
            elif _Species.lower() == "neutrino":
                particleMASS = self.mNeutrino()
            elif _Species.lower() == "12c6":
                particleMASS = self.m12c6()
        else:
            raise badParameter("PhysicalConstants.getParticleMASS: " \
                               "Species " + _Species + " not allowed!")
        return particleMASS
    
    def getparticleLifeTime(self, _Species):
        particleLifeTime = None
        if not isinstance(_Species, str):
            raise badParameter("PhysicalConstants.getParticleLifeTime:", \
                               " Species " + _Species + " not a string!")
        if _Species.lower() in PhysicalConstants.getSpecies():
            if   _Species.lower() == "proton":
                particleLifeTime = self.tauP()
            elif _Species.lower() == "pion":
                particleLifeTime = self.tauPion()
            elif _Species.lower() == "muon":
                particleLifeTime = self.tauMuon()
            elif _Species.lower() == "neutrino":
                particleLifeTime = self.tauNeutrino()
            elif _Species.lower() == "12c6":
                particleLifeTime = self.tau12c6()
        else:
            raise badParameter("PhysicalConstants.getParticleLifeTime: Species " + \
                               _Species + " not allowed!")
        return particleLifeTime

    def me(self):
        return 0.51099895000

    def meSI(self):
        return 9.1093837015E-31

    def mp(self):
        return 938.27208816

    def mpSI(self):
        return 1.67262192360E-27

    def mPion(self):
        return 139.57061

    def mMuon(self):
        return 105.6583745

    def mNeutrino(self):
        return 0.

    def m12c6(self):
        return 11174.8

    def tauPion(self):
        return 26.033E-9

    def tauMuon(self):
        return 2.1969811E-6

    def tauP(self):
        return math.inf

    def tau12c6(self):
        return math.inf

    def tauNeutrino(self):
        return math.inf

    def mu0(self):
        return sp.constants.mu_0

    def epsilon0(self):
        return 8.8541878128E-12

    def epsilon0SI(self):
        return 8.8541878128E-12

    def electricCHARGE(self):
        return 1.602176634E-19

    def alpha(self):
        return 1./137.035999084

    def Joule2MeV(self):
        return 6241509074000.

    def m2InvMeV(self):
        return 5067730717679.4


#--------  Utilities:


#--------  Exceptions:
class badParameter(Exception):
    pass
