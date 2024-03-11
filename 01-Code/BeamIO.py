#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class BeamIO:
=============

  Class provides management of file handling and i/o for the Beam
  package.

"""

class BeamIO:
    instances = []
    __Debug   = False

#--------  "Built-in methods":
    def __init__(self):
        if self.__Debug:
            print(' BeamIO.__init__: ', \
                  'creating BeamIO object')

        BeamIO.instances.append(self)

        self.setAll2None()

        if self.__Debug:
            print("     ----> New BeamIO instance: \n", \
                  BeamIO.__str__(self))
            print(" <---- BeamIO instance created.")
            
    def __repr__(self):
        return "BeamIO() repr"

    def __str__(self):
        self.print()
        return " <---- BeamIO __str__ done. \n"

    def print(self):
        print("\n BeamIO:")
        print(" -------")
        print("     ----> Debug flag:", self.getDebug())

        
#--------  "Set method" only Debug
#.. Method believed to be self documenting(!)

    @classmethod
    def setDebug(cls, Debug=False):
        if cls.__Debug:
            print(" Particle.setdebug: ", Debug)
        cls.__Debug = Debug

    def setAll2None(self):
        self._Location  = []

        
#--------  "Get methods" only; version, reference, and constants
#.. Methods believed to be self documenting(!)
    @classmethod
    def getDebug(cls):
        return cls.__Debug

    @classmethod
    def getParticleInstances(cls):
        return cls.instances

        
