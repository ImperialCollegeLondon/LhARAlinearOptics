#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class visualise
================

  Class to manage visualisatoin for LhARAlinearOptics package.

  Class attributes:
  -----------------
  __instances : Set on creation of instances.
  __Debug     : Debug flag


  Instance attributes:
  --------------------
            _NEvt : Number of events to generate

    
  Methods:
  --------
  Built-in methods __new__, __repr__ and __str__.
      __new__ : Creates singleton class and prints version, PDG
                reference, and values of constants used.
      __repr__: One liner with call.
      __str__ : Dump of contents

  Get/set methods:
      CdVrsn()     : Returns code version number.

       Utilities:
             print : Print summary of paramters


Created on Thu 22Apr24;11:04: Version history:
----------------------------------------------
 1.0: 22Apr24: First implementation

@author: kennethlong
"""


#--------  visualise class  --------
class visualise(object):
    __Debug     = False
    __instances = []


#--------  "Built-in methods":
    def __init__(self):
        if self.getDebug():
            print('visualise.__init__: creating the visualise instance')
            print('------------------')

        self.setAll2None()

        self.addinstance(self)

    def __repr__(self):
        return "visualise()"

    def __str__(self):
        self.__repr__()
        self.print()
        return(" <---- visualise.__str__ done.")
        

    def print(self):
        print(" visualise.print:")
        print(" ----------------")
        print("                          Debug:", self.getDebug())
        print("            Number of instances:", len(self.getinstances()))
        return(" <---- visualise.print done.")

        
#--------  "Set methods":
#.. Methods believed to be self documenting(!)
    @classmethod
    def setDebug(cls, _Debug=False):
        cls.__Debug = _Debug

    def setAll2None(self):
        pass

    @classmethod
    def setinstances(cls, instances):
        if not isinstance(instances, list):
            raise badParameter()
        cls.__instances = instances

    @classmethod
    def addinstance(cls, instance):
        if not isinstance(instance, visualise):
            raise badParameter()
        cls.__instances.append(instance)

        
#--------  "Get methods":
#.. Methods believed to be self documenting(!)
    @classmethod
    def getDebug(cls):
        return cls.__Debug

    @classmethod
    def getinstances(cls):
        return cls.__instances


#--------  Exceptions:
class badParameter(Exception):
    pass

