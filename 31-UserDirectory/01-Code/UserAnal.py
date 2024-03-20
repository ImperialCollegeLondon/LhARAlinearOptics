#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class UserAnal:
===============

  Dummy class created to help user develop their own analysis.

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

import Particle as Prtcl

class UserAnal:
    instances  = []
    __Debug    = False


#--------  "Built-in methods":
    def __init__(self):
        if self.__Debug:
            print(' UserAnal.__init__: ', \
                  'creating the user analysis object object')

        UserAnal.instances.append(self)

        self.setAll2None()

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

            
#--------  Utilities:
    @classmethod
    def plotSomething(cls):

        nPrtcl = 0
        for iPrtcl in Prtcl.Particle.getParticleInstances():
            nPrtcl += 1
            if isinstance(iPrtcl, Prtcl.ReferenceParticle):
                iRefPrtcl = iPrtcl
                continue
            iLoc = -1

            if nPrtcl < 10:
                iPrtcl.printProgression()

        print(" UserAnal done, number of particles read:", nPrtcl)

#--------  Exceptions:
class noReferenceParticle(Exception):
    pass

