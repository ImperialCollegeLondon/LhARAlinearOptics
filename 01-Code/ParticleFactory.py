#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class ParticleFactory:
======================

  A Factory class which returns the constructor for either a Particle or
  and UnstableParticle


  Class attributes:
  -----------------
  __Debug     : Debug flag

      
  Instance attributes:
  --------------------
    
  Methods:
  --------
  Built-in methods createParticle.
      __init__: Factory class not expected to be instantiated - raises an exception
      __repr__: No instanvces so no __repr__
      __str__ : No instanvces so no __str__


      createParticle(species) : returns an instantiation call for a Particle or UnstableParticle.


  Set methods:
     setDebug: set class debug flag
          Input: bool, True/False
          Return: None

  Get methods:
      getDebug: get class debug flag

  Exceptions:
    unknownParticleSpecies

Created on Mon 11Aug25: Version history:
----------------------------------------
 1.0: 11Aug25: First implementation

@author: paulkyberd
"""

from Particle import Particle, UnstableParticle


class ParticleFactory:

    __Debug = False

    def __init__(self):

      raise donotInstantiate("The particle factory class should not be instantiated")


    @staticmethod
    def createParticle(species):
        stable_species = {"proton", "neutrino"}
        unstable_species = {"pion", "muon"}

        if species.lower() in stable_species:
            return Particle(species)
        elif species.lower() in unstable_species:
            return UnstableParticle(species)
        else:
            raise unknownParticleSpecies(f"Unknown species: {species}")

    @classmethod
    def getDebug(cls):
        return cls.__Debug

    @classmethod
    def setDebug(cls, Debug=False):
        if cls.__Debug:
            print(" ParticleFactory.setDebug: ", Debug)
        cls.__Debug = Debug


#--------  Exceptions:
class unknownParticleSpecies(Exception):
  pass

class donotInstantiate(Exception):
  pass

