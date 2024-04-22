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

import Particle as Prtcl

#--------  visualise class  --------
class visualise(object):
    __Debug     = False
    __instances = []


#--------  "Built-in methods":
    def __init__(self, _CoordSys=None, _Projection=None):
        if self.getDebug():
            print('visualise.__init__: creating the visualise instance')
            print('------------------')

        self.setAll2None()

        self.addinstance(self)

        self.setCoordSys(_CoordSys)
        self.setProjection(_Projection)

        if self.getDebug():
            self.print()

    def __repr__(self):
        return "visualise()"

    def __str__(self):
        self.__repr__()
        self.print()
        return(" <---- visualise.__str__ done.")
        

    def print(self):
        print(" visualise.print:")
        print(" ----------------")
        print("                          Debug:", \
              self.getDebug())
        print("            Number of instances:", \
              len(self.getinstances()))
        print("              Coordinate system:", \
              self.getCoordSys())
        print("                     Projection:", \
              self.getProjection())
        return(" <---- visualise.print done.")

        
#--------  "Set methods":
#.. Methods believed to be self documenting(!)
    @classmethod
    def setDebug(cls, _Debug=False):
        cls.__Debug = _Debug

    def setAll2None(self):
        self._CoordSys   = None
        self._Projection = None

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

    def setCoordSys(self, _CoordSys):
        if not isinstance(_CoordSys, str):
            raise badParameter()
        self._CoordSys = _CoordSys

    def setProjection(self, _Projection):
        if not isinstance(_Projection, str):
            raise badParameter()
        self._Projection = _Projection

        
#--------  "Get methods":
#.. Methods believed to be self documenting(!)
    @classmethod
    def getDebug(cls):
        return cls.__Debug

    @classmethod
    def getinstances(cls):
        return cls.__instances

    def getCoordSys(self):
        return self._CoordSys

    def getProjection(self):
        return self._Projection


#--------  Visualisation managers:
    def ReferenceParticle(self, axs):
        if self.getDebug():
            print(" visualise.ReferenceParticle: start")
            print("     ----> Coordinate system:", \
                  self.getCoordSys())
            print("     ----> Projection:", \
                  self.getProjection())

        irefPrtcl = Prtcl.ReferenceParticle.getinstance()
        
        sorz = []
        xory = []
        #..  Plotting as a function of s if RPLC or z if laboratory:
        if self.getCoordSys() == "RPLC":
            iCrd = 0
            axl  = "x"
            if self.getProjection() == "ys":
                iCrd = 2
                axl  = "y"
            sorz = irefPrtcl.getsOut()
            for TrcSpc in irefPrtcl.getTraceSpace():
                xory.append(TrcSpc[iCrd])

        if self.getDebug():
            print("     ----> sorz:", sorz)
            print("     ----> xory:", xory)
        
        axs.plot(sorz, xory, color='black', linewidth='1', \
                 linestyle='dashed')
        axs.set_xlabel('s (m)')
        axs.set_ylabel(axl + ' (m)')
        


#--------  Exceptions:
class badParameter(Exception):
    pass

