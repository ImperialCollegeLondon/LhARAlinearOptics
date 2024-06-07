#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Start with methods used in analysis main that should be standard for all
analyses.

"""

import UserFramework as UFw

"""
Class UserAnal:
===============

  Dummy class created to help user develop their own analysis.

  Out of the box provides three "user hooks":

   UserInit: called at instanitation to allow user to initialise.

   UserAnal: called in the event loop to allow user to do whatever is needed
             for their analysis.

    UserEnd: called at the end of execution before termination to allow
             user to dump summaries, statistics, plots etc.

  Class attributes:
  -----------------
    instances : List of instances of Particle class
  __Debug     : Debug flag

      
  Instance attributes:
  --------------------
    
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


Created on Tue 27Feb24: Version history:
----------------------------------------
 1.0: 27Feb24: First implementation

@author: kennethlong
"""

import io

import Particle as Prtcl
import BeamLine as BL

class UserAnal:

        
#--------  UserHooks:
    def UserInit(self):
        print(" UserAnal.UserInit: initialsation")
        print("     ----> Default UserInit.")

        if not UserAnal.InitCalled:
            print(BL.BeamLine.getinstance())

        print("\n <---- Default UserInit complete.")
        
    def UserEvent(self, iPrtcl): 
        print(" UserAnal.UserEvent: user particle-by-particle processing")
        print("     ----> Default UserEvent.")
       
        print("\n <---- Default UserEvent complete.")

    def UserEnd(self, d0_new=None, d1_new=None, sp_new=None, d4_new=None):
        print(" UserAnal.UserEnd: end of processing")
        print("     ----> Default UserEnd.")

        print("\n <---- Default UserEnd complete.")


#--------  "Standard" UserAnal: no need to edit ...

    instances  = []
    __Debug    = True
    InitCalled = False

    Iter = 0


#--------  "Built-in methods":
    def __init__(self, Debug=False):
        self.setDebug(Debug)
        if self.getDebug():
            print(' UserAnal.__init__: ', \
                  'creating the user analysis object object')

        UserAnal.instances.append(self)

        self.setAll2None()

        self.UserInit()

        if self.__Debug:
            print("     ----> New UserAnal instance: \n", \
                  UserAnal.__str__(self))
            print(" <---- UserAnal instance created.")
            
    def __repr__(self):
        return "UserAnal()"

    def __str__(self):
        self.print()
        return " UserAnal __str__ done."

    def print(self):
        print("\n UserAnal:")
        print(" ---------")
        print("     ----> Debug flag:", self.getDebug())
        return " <---- UserAnal parameter dump complete."

    
#--------  "Set method" only Debug
#.. Method believed to be self documenting(!)

    @classmethod
    def setDebug(cls, Debug=False):
        if cls.__Debug:
            print(" Particle.setdebug: ", Debug)
        cls.__Debug = Debug

    def setAll2None(self):
        pass

    
#--------  "Get methods" only; version, reference, and constants
#.. Methods believed to be self documenting(!)

    @classmethod
    def getDebug(cls):
        return cls.__Debug

    @classmethod
    def getUserAnalInstances(cls):
        return cls.instances

    @classmethod
    def getIter(cls):
        return cls.Iter


#--------  Processing methods:
    def EventLoop(self, ibmIOw):

        nPrtcl = 0
        for iPrtcl in Prtcl.Particle.getParticleInstances():
            nPrtcl += 1
            if isinstance(iPrtcl, Prtcl.ReferenceParticle):
                iRefPrtcl = iPrtcl
                continue
            iLoc = -1

            self.UserEvent(iPrtcl)

            if isinstance(ibmIOw, io.BufferedWriter):
                iPrtcl.writeParticle(ibmIOw)
        
        Prtcl.Particle.cleanParticles()
        

#--------  Exceptions:

