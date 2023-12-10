#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
To do:
======
 - Still to do:
   - KL: Add length to aperture: i.e. there can be a length to the plate
         or other collimator structure.
   - KL: Add rotation to Shift2Local and Shift2Global.  Need to update dvCtr
         to Euler angles, I think.
         Also, as coded, these methods are not correct, they do not account
         for position of element in global coordinates.


Class BeamLineElement:
======================

  Class to contain beam line elements.  Parent class defines principal
  coordinates of the beam-line element and transfer matrix.  Properties
  of the beam-line elements are derived classes.

  Classes derived from BeamLineElement:
             Drift, Aperture, FocusQuadrupole, DeFocusQuadrupole,
             SectorDipole, Octupole, Solenoid, RFCavity, Source


  Class attributes:
  -----------------
        instances : List of instances of BeamLineElement class
      __Debug     : Debug flag
constants_instance: Instance of PhysicalConstants class
    speed_of_light: Speed of light from PhysicalConstants

      
  Instance attributes:
  --------------------
  Calling arguments:
   _Name : string; name of element, should be identifiable, e.g., Drift1
   _rCtr : numpy array; x, y, z position (in m) of centre of element.
   _vCtr : numpy array; theta, phi of principal axis of element.
  _drCtr : "error", displacement of centre from nominal position (rad).
  _dvCtr : "error", deviation in theta and phy from nominal axis (rad).

  Instance attributes assigned in BeamLineElement parent class:
  _TrnsfMtrx: Transfer matrix (6x6).  Set to Null in __init__, initialised
              (to Null) in BeamLineElement.__init__, filled in derived
              classes.

    
  Methods:
  --------
  Built-in methods __init__, __repr__ and __str__.
      __init__ : Creates instance of beam-line element class.
      __repr__: One liner with call.
      __str__ : Dump of constants

      SummaryStr: returns summary string, presently just position of
                  element.
            Input: None
           Return: str="Pos: [x, y, z] = " + str(self.getrCtr())

  Set methods:
      setDebug  : Set debug flag
    setAll2None : Set all attributes to Null
       setName  : Set name of element
       setrCtr  : Set centre of element, x, y, z (m)
       setvCtr  : Set orientation of element, theta, phi (rad)
      setdrCtr  : Set offset of centre of element, x, y, z (m)
      setdvCtr  : Set offset orientation of element, theta, phi (rad)

  Get methods:
      getDebug  : get debug flag
  getinstances  : get list of instances
       getName  : Get name of element
       getrCtr  : Get centre of element, x, y, z (m)
       getvCtr  : Get orientation of element, theta, phi (rad)
      getdrCtr  : Get offset from nominal centre of element, x, y, z (m)
      getdvCtr  : Get offset of orientation of element, theta, phi (rad)
 getTransferMatrix : Get transfer matrix.

  Processing method:
      Transport : Applies transfer matrix to phase-space vector.
             Input: 6D phase-space vector, np.array.
            Return: 6D phase-space vector after element

    Shift2Local : Transform from global to local coordinates.
                 <---- Not correct yet!
             Input: 6D phase-space vector, np.array.
            Return: Transformed 6D phase-space vector

   Shift2Global : Transform from local to global coordinates
                 <---- Not correctyet!
             Input: 6D phase-space vector, np.array.
            Return: Transformed 6D phase-space vector


Created on Mon 12Jun23: Version history:
----------------------------------------
 1.0: 12Jun23: First implementation

@author: kennethlong
"""

import numpy  as np
import math   as mth
import random as rnd

import PhysicalConstants as PhysCnst
import Particle          as Prtcl

#.. Physical Constants
constants_instance = PhysCnst.PhysicalConstants()
speed_of_light     = constants_instance.SoL()
protonMASS         = constants_instance.mp()

alpha              = 0.0072973525693
electricCHARGE     = mth.sqrt(4.*mth.pi*alpha)
epsilon0           = 1.
Joule2MeV          = 6241509074000.
m2InvMeV           = 5067730717679.4

class BeamLineElement:

#-------- Class attributes  --------  --------

#.. List of instances and debug flag
    instances  = []
    __Debug    = False

#--------  "Built-in methods":
    def __init__(self, _Name=None, \
                 _rCtr=None, _vCtr=None, _drCtr=None, _dvCtr=None):
        if self.__Debug:
            print(' BeamLineElement.__init__: ', \
                  'creating the BeamLineElement object')
            print("     ---->               Name:", _rName)
            print("     ---->           Position:", _rCtr)
            print("     ---->        Orientation:", _vCtr)
            print("     ---->    Position offset:", _drCtr)
            print("     ----> Orientation offset:", _dvCtr)

        BeamLineElement.instances.append(self)

        self.setAll2None()
        
        if  not isinstance( _Name, str)        or \
            not isinstance( _rCtr, np.ndarray) or \
            not isinstance( _vCtr, np.ndarray) or \
            not isinstance(_drCtr, np.ndarray) or \
            not isinstance(_dvCtr, np.ndarray):
            raise badBeamLineElement( \
                  " BeamLineElement: no default beamline element!"
                                      )

        self.setName(_Name)
        self.setrCtr(_rCtr)
        self.setvCtr(_vCtr)
        self.setdrCtr(_drCtr)
        self.setdvCtr(_dvCtr)
        
        if self.__Debug:
            print("     ----> New BeamLineElement instance: \n", \
                  BeamLineElement.__str__(self))
            
    def __repr__(self):
        return "BeamLineElement()"

    def __str__(self):
        print(" BeamLineElement:")
        print(" ----------------")
        print("     ---->         Debug flag:", BeamLineElement.getDebug())
        print("     ---->               Name:", self.getName())
        print("     ---->           Position:", self.getrCtr())
        print("     ---->        Orientation:", self.getvCtr())
        print("     ---->    Position offset:", self.getdrCtr())
        print("     ----> Orientation offset:", self.getdvCtr())
        return " <---- BeamLineElement parameter dump complete."

    def SummaryStr(self):
        Str = "Pos: [x, y, z] = " + str(self.getrCtr())
        return Str

    
#--------  "Set method" only Debug
#.. Method believed to be self documenting(!)

    @classmethod
    def setDebug(self, Debug=False):
        if self.__Debug:
            print(" BeamLineElement.setdebug: ", Debug)
        self.__Debug = Debug

    def setAll2None(self):
        self._Name      = None
        self._rCtr      = None
        self._vCtr      = None
        self._drCtr     = None
        self._dvCtr     = None
        self._TrnsfMtrx = None
        
    def setName(self, _Name):
        if not isinstance(_Name, str):
            raise badParameter(" BeamLineElement.setrCtr: bad name:", \
                               _Name)
        self._Name = _Name
        
    def setrCtr(self, _rCtr):
        if not isinstance(_rCtr, np.ndarray):
            raise badParameter(" BeamLineElement.setrCtr: bad centre:", \
                               _rCtr)
        self._rCtr = _rCtr
        
    def setvCtr(self, _vCtr):
        if not isinstance(_vCtr, np.ndarray):
            raise badParameter(" BeamLineElement.setvCtr: bad orienttion:", \
                               _vCtr)
        self._vCtr = _vCtr
        
    def setdrCtr(self, _drCtr):
        if not isinstance(_drCtr, np.ndarray):
            raise badParameter(" BeamLineElement.setdrCtr:", \
                               " bad centre offset:", \
                               _drCtr)
        self._drCtr = _drCtr
        
    def setdvCtr(self, _dvCtr):
        if not isinstance(_dvCtr, np.ndarray):
            raise badParameter(" BeamLineElement.setdvCtr:", \
                               " bad orienttion offset:", \
                               _dvCtr)
        self._dvCtr = _dvCtr
        

#--------  "Get methods" only; version, reference, and constants
#.. Methods believed to be self documenting(!)

    @classmethod
    def getDebug(self):
        return self.__Debug

    @classmethod
    def getinstances(self):
        return self.instances

    def getName(self):
        return self._Name

    def getrCtr(self):
        return self._rCtr

    def getvCtr(self):
        return self._vCtr

    def getdrCtr(self):
        return self._drCtr

    def getdvCtr(self):
        return self._dvCtr

    def getTransferMatrix(self):
        return self._TrnsMtrx
    
    
#--------  Utilities:
    def Transport(self, _R):
        if not isinstance(_R, np.ndarray) or np.size(_R) != 6:
            raise badParameter( \
                        " BeamLineElement.Transport: bad input vector:", \
                                _R)
        return self.getTransferMatrix().dot(_R)

    def Shift2Local(self, _R):
        if not isinstance(_R, np.ndarray) or np.size(_R) != 6:
            raise badParameter( \
                        " BeamLineElement.Shift2Local: bad input vector:", \
                                _R)

        _Rprime    = _R
        _Rprime[0] -= self._drCtr[0]
        _Rprime[2] -= self._drCtr[1]

        return _Rprime

    def Shift2Global(self, _R):
        if not isinstance(_R, np.ndarray) or np.size(_R) != 6:
            raise badParameter( \
                        " BeamLineElement.Shift2Local: bad input vector:", \
                                _R)
        
        _Rprime    = _R
        _Rprime[0] += self._drCtr[0]
        _Rprime[2] += self._drCtr[1]
        
        return _Rprime


#--------  Derived classes  --------  --------  --------  --------  --------
"""
Derived class Facility:
=======================

  Facility class derived from BeamLineElement to contain paramters for a
  Facility space.  __init__ sets parameters of Facility.  Methods to
  apply transfer matix.


  Class attributes:
  -----------------
    instance : List of instances of Facility(BeamLineElement) class
  __Debug    : Debug flag


  Parent class attributes:
  ------------------------
   _rCtr : numpy array; x, y, z position (in m) of centre of element.
   _vCtr : numpy array; theta, phi of principal axis of element.
  _drCtr : "error", displacement of centre from nominal position.
  _dvCtr : "error", deviation in theta and phy from nominal axis.
  _TrnsMtrx : Transfer matrix.


  Instance attributes to define Facility:
  ------------------------------------
  _Name : str   : Name of facility
  _p0   : float : Reference particle momentum
    
  Methods:
  --------
  Built-in methods __init__, __repr__ and __str__.
      __init__ : Creates instance of beam-line element class.
      __repr__: One liner with call.
      __str__ : Dump of constants

  Set methods:
        setName  : 
          setp0  : 

  Get methods:
     getName, getp0

"""
class Facility(BeamLineElement):
    instance  = []
    __Debug   = False

    
#--------  "Built-in methods":
    def __init__(self, _Name=None, \
                 _rCtr=None, _vCtr=None, _drCtr=None, _dvCtr=None, \
                 _p0=None):
        if self.__Debug:
            print(' Facility.__init__: ', \
                  'creating the Facility object: Name=', _Name, \
                  'p0=', _p0)

        Facility.instance = self

        #.. BeamLineElement class initialisation:
        BeamLineElement.__init__(self, _Name, _rCtr, _vCtr, _drCtr, _dvCtr)

        if not isinstance(_p0, float):
            raise badBeamLineElement( \
                  " Facility: bad specification for length of Facility!"
                                      )
        self.setp0(_p0)
                
        if self.__Debug:
            print("     ----> New Facility instance: \n", \
                  self)
            
    def __repr__(self):
        return "Facility()"

    def __str__(self):
        print(" Facility:")
        print(" ------")
        print("     ----> Debug flag:", Facility.getDebug())
        print("     ----> Name      :", self.getName())
        print("     ----> p0 (MeV/c):", self.getp0())
        BeamLineElement.__str__(self)
        return " <---- Facility parameter dump complete."

    def SummaryStr(self):
        Str  = "Facility         : " + BeamLineElement.SummaryStr(self) + \
            "; Name = " + self.getName() + "; p0 = " + str(self.getp0())
        return Str


#--------  "Set methods"
#.. Methods believed to be self documenting(!)
    def setp0(self, _p0=None):
        if not isinstance(_p0, float):
            raise badParameter( \
                     " BeamLineElement.Facility.setLength: bad p0",
                                _p0)
        self._p0 = _p0

        
#--------  "get methods"
#.. Methods believed to be self documenting(!)
    def getp0(self):
        return self._p0
    
        
"""
Derived class Drift:
====================

  Drift class derived from BeamLineElement to contain paramters for a drift
  space.  __init__ sets parameters of drift.  Methods to apply transfer
  matix.


  Class attributes:
  -----------------
    instances : List of instances of Drift(BeamLineElement) class
  __Debug     : Debug flag


  Parent class attributes:
  ------------------------
   _rCtr : numpy array; x, y, z position (in m) of centre of element.
   _vCtr : numpy array; theta, phi of principal axis of element.
  _drCtr : "error", displacement of centre from nominal position.
  _dvCtr : "error", deviation in theta and phy from nominal axis.
  _TrnsMtrx : Transfer matrix.


  Instance attributes to define drift:
  ------------------------------------
  _Length : Length (in m) of drift length
  
    
  Methods:
  --------
  Built-in methods __init__, __repr__ and __str__.
      __init__ : Creates instance of beam-line element class.
      __repr__: One liner with call.
      __str__ : Dump of constants

  Set methods:
        setLength  : Set _Length
 setTransferMatrix : "Calculate" amd set transfer matrix.
                Input: _Length (m)

  Get methods:
     getLength  : get debug flag

"""
class Drift(BeamLineElement):
    instances  = []
    __Debug    = False

    
#--------  "Built-in methods":
    def __init__(self, _Name=None, \
                 _rCtr=None, _vCtr=None, _drCtr=None, _dvCtr=None, \
                 _Length=None):
        if self.__Debug:
            print(' Drift.__init__: ', \
                  'creating the Drift object: Length=', _Length)

        Drift.instances.append(self)

        #.. BeamLineElement class initialisation:
        BeamLineElement.__init__(self, _Name, _rCtr, _vCtr, _drCtr, _dvCtr)

        if not isinstance(_Length, float):
            raise badBeamLineElement( \
                  " Drift: bad specification for length of drift!"
                                      )
        self.setLength(_Length)
        self.setTransferMatrix(_Length)
                
        if self.__Debug:
            print("     ----> New drift instance: \n", \
                  self)
            
    def __repr__(self):
        return "Drift()"

    def __str__(self):
        print(" Drift:")
        print(" ------")
        print("     ----> Debug flag:", Drift.getDebug())
        print("     ----> Length (m):", self.getLength())
        print("     ----> Transfer matrix: \n", self.getTransferMatrix())
        BeamLineElement.__str__(self)
        return " <---- Drift parameter dump complete."

    def SummaryStr(self):
        Str  = "Drift            : " + BeamLineElement.SummaryStr(self) + \
            "; length = " + str(self.getLength())
        return Str


#--------  "Set methods"
#.. Methods believed to be self documenting(!)

    def setLength(self, _Length):
        if not isinstance(_Length, float):
            raise badParameter(" BeamLineElement.Drift.setLength: bad length:",
                               _Length)
        self._Length = _Length

    def setTransferMatrix(self, _Length):
        if not isinstance(_Length, float):
            raise badParameter( \
                    " BeamLineElement.Drift.setTransferMatrix: bad length:",
                               _Length)
        TrnsMtrx = np.array( [ \
                              [1., _Length, 0.,      0., 0., 0.], \
                              [0.,      1., 0.,      0., 0., 0.], \
                              [0.,      0., 1., _Length, 0., 0.], \
                              [0.,      0., 0.,      1., 0., 0.], \
                              [0.,      0., 0.,      0., 1., 0.], \
                              [0.,      0., 0.,      0., 0., 1.]  \
                             ] )
        self._TrnsMtrx = TrnsMtrx

        
#--------  "get methods"
#.. Methods believed to be self documenting(!)

    def getLength(self):
        return self._Length
    
        
"""
Derived class Aperture:
=======================

  Aperture class derived from BeamLineElement to contain paramters for an
  aperture.  __init__ sets parameters of the aperture.  Methods to apply
  transfer cuts in position and the transfer matix are provided.


  Class attributes:
  -----------------
    instances : List of instances of BeamLineElement class
  __Debug     : Debug flag


  Parent class instance attributes:
  ---------------------------------
  Calling arguments:
   _Name : Name
   _rCtr : numpy array; x, y, z position (in m) of centre of element.
   _vCtr : numpy array; theta, phi of principal axis of element.
  _drCtr : "error", displacement of centre from nominal position.
  _dvCtr : "error", deviation in theta and phy from nominal axis.
  _Param : Array, Type, then paramters for aperture.

  _TrnsMtrx : Transfer matrix.


  Instance attributes to define aperture:
  ---------------------------------------
  _Type      : Type of aperture:
               = 0: circular
               = 1: Elliptical
 _Params     : Circular:
               _Params[0]: Radius of circular aperture
               Elliptical:
               _Params[0]: Radius of ellipse in horizontal (x) direction
               _Params[1]: Radius of ellipse in horizontal (y) direction

    
  Methods:
  --------
  Built-in methods __init__, __repr__ and __str__.
      __init__ : Creates instance of beam-line element class.
      __repr__: One liner with call.
      __str__ : Dump of constants

    SummaryStr: No arguments, returns one-line string summarising aperture
                parameterrs.

  Set methods:
setAoertureParameters: Sets aperture parameters:
                 Input: _Param: same i/p arguments as Aperture __init__
 setTransferMatrix : "Calculate" amd set transfer matrix.
                Input: _Length (m)

  Get methods:
     getDebug: get debug flag, bool
      getType: Get type, return Type, int
    getParams: Return Params, list

  Utilities:


"""
class Aperture(BeamLineElement):
    instances  = []
    __Debug    = False

#--------  "Built-in methods":    
    def __init__(self, _Name=None, \
                 _rCtr=None, _vCtr=None, _drCtr=None, _dvCtr=None, \
                 _Param=[]):
        if self.getDebug():
            print(' Aperture.__init__: ', \
                  'creating the Aperture object')
            print("     ----> Parameters:", _Param)

        Aperture.instances.append(self)
        
        #.. BeamLineElement class initialisation:
        BeamLineElement.__init__(self, _Name, _rCtr, _vCtr, _drCtr, _dvCtr)

        if len(_Param) < 2:
            raise badBeamLineElement( \
                  " Aperture: bad specification for aperture!"
                                      )
        self.setApertureParameters(_Param)
        self.setTransferMatrix()
                
        if self.setDebug():
            print("     ----> New Aperture instance: \n", \
                  self)
            
    def __repr__(self):
        return "Aperture()"
    
    def __str__(self):
        print(" Aperture:")
        print(" ---------")
        print("     ----> Debug flag:", Aperture.getDebug())
        print("     ----> Type:", self.getType())
        if self.getType() == 0:
            print("     ----> Circular:")
            print("     ----> Radius (m)", self.getParams()[0])
        elif self.getType() == 1:
            print("     ----> Eliptical:")
            print("     ----> Radius x, y (m)", self.getParams())
        BeamLineElement.__str__(self)
        return " <---- Aperture parameter dump complete."

    def SummaryStr(self):
        Str  = "Aperture         : " + BeamLineElement.SummaryStr(self) + \
            "; Type = " + str(self.getType()) + \
            "; Parameters = " + str(self.getParams())
        return Str

    
#--------  "Set methods".
#.. Methods believed to be self documenting(!)
    def setApertureParameters(self, _Param):
        if self.getDebug():
            print(" Apperture.setApertureParamters; Parameters:", _Param)
        if not isinstance(_Param[0], int):
            raise badParameter( \
                        " BeamLineElement.Aperture.setApertureParameters:",\
                        " bad type:",
                        _Param[0])
        self._Type = _Param[0]

        self._Params = np.array([])
        if _Param[0] == 0:           #.. Circular aperture
            if not isinstance(_Param[1], float):
                raise badParameter( \
                        " BeamLineElement.Aperture.setApertureParameters:",\
                        " bad radius:",
                        _Param[1])
            self._Params = np.append(self._Params, _Param[1])
        elif _Param[0] == 1:           #.. Eliptical aperture
            if not isinstance(_Param[1], float) or \
               not isinstance(_Param[2], float):
                raise badParameter( \
                        " BeamLineElement.Aperture.setApertureParameters:",\
                        " bad radius:",
                        _Param[1], _Param[1])
            self._Params = np.append(self._Params, _Param[1])
            self._Params = np.append(self._Params, _Param[2])

    def setTransferMatrix(self):
        TrnsMtrx = np.array( [ \
                              [1., 0., 0., 0., 0., 0.], \
                              [0., 1., 0., 0., 0., 0.], \
                              [0., 0., 1., 0., 0., 0.], \
                              [0., 0., 0., 1., 0., 0.], \
                              [0., 0., 0., 0., 1., 0.], \
                              [0., 0., 0., 0., 0., 1.]  \
                             ] )
        self._TrnsMtrx = TrnsMtrx


#--------  "get methods"
#.. Methods believed to be self documenting(!)
    @classmethod
    def getDebug(cls):
        return cls.__Debug
    
    def getType(self):
        return self._Type
    
    def getParams(self):
        return self._Params

    def getLength(self):
        return 0.

    
#--------  Utilities:
    def Transport(self, _R):
        if not isinstance(_R, np.ndarray) or np.size(_R) != 6:
            raise badParameter( \
                        " BeamLineElement.Transport: bad input vector:", \
                                _R)
        NotCut = True
        #print(" Aperture(BeamLineElement).Transport:", \
        #      self.getType(), self.getParams())
        if self.getType() == 0:
            Rad = np.sqrt(_R[0]**2 + _R[2]**2)
            #print(" Aperture cut: R, Raptr:", Rad, self.getParams()[0])
            if Rad >= self.getParams()[0]:
                NotCut = False
        elif self.getType() == 1:
            RadX2 = (_R[0]/self.getParams()[0])**2
            RadY2 = (_R[2]/self.getParams()[1])**2
            #print(" Aperture cut: RadX2, RapY2:", RadX2, RadY2)
            if (RadX2+RadY2) >= 1.:
                NotCut = False

        _Rprime = None
        if NotCut:
            _Rprime = self.getTransferMatrix().dot(_R)
            
        return _Rprime

    
"""
Derived class FocusQuadrupole:
==============================

  FocusQuadrupole class derived from BeamLineElement to contain paramters
  for an F-quad.


  Class attributes:
  -----------------
    instances : List of instances of BeamLineElement class
  __Debug     : Debug flag


  Parent class instance attributes:
  ---------------------------------
  Calling arguments:
   _Name : Name
   _rCtr : numpy array; x, y, z position (in m) of centre of element.
   _vCtr : numpy array; theta, phi of principal axis of element.
  _drCtr : "error", displacement of centre from nominal position.
  _dvCtr : "error", deviation in theta and phy from nominal axis.


  _TrnsMtrx : Transfer matrix:
         Input: Brho: float ... B*rho (=3.3356E-3) * p (MeV)
                      at init in __init__ Brho=1. is used


  Instance attributes to define quadrupole:
  -----------------------------------------
  _Length  : Length of quad, m
  _Strength: Strength of quad in T/m

    
  Methods:
  --------
  Built-in methods __init__, __repr__ and __str__.
      __init__ : Creates instance of beam-line element class.
      __repr__: One liner with call.
      __str__ : Dump of constants

    SummaryStr: No arguments, returns one-line string summarising quad
                parameterrs.

  Set methods:
    setLength: set length:
          Input: _Length (float): length of quad (m)
  setStrength: -Strength (float): strength of quad (T/m)
          Input: _Length (float): length of quad

setTransferMatrix: Set transfer matrix; calculate using i/p brhop
          Input: Brho (T m)
         Return: np.array(6,6,) transfer matrix

  Get methods:
      getLength, getStrength

  Utilities:
    Transport: transport through focus quad.  Sets transfer matrix (using
               call to setTransferMatrix) given Brho
            Input:
                  R: 6D numpy array containing phase space at entry of
                      aperture
               Brho: Brho: float ... B*rho (~3.3356E-3) * p (MeV)
             Rprime: 6D phase space (numpy array) at exit of aperture
                     if the particle passes through the aperture ... or ...

"""
class FocusQuadrupole(BeamLineElement):
    instances = []
    __Debug = False

    def __init__(self, _Name=None, \
                 _rCtr=None, _vCtr=None, _drCtr=None, _dvCtr=None, \
                 _Length=None, _Strength=None):
        
        if self.getDebug():
            print(' FocusQuadrupole.__init__: ', \
                  'creating the FocusQuadrupole object: Length=', \
                  _Length, ', Strength=', _Strength)

        FocusQuadrupole.instances.append(self)

        # BeamLineElement class initialization:
        BeamLineElement.__init__(self, _Name, _rCtr, _vCtr, _drCtr, _dvCtr)

        if not isinstance(_Length, float):
            raise badBeamLineElement("FocusQuadrupole: bad specification", \
                                     " for length!")
        if not isinstance(_Strength, float):
            raise badBeamLineElement("FocusQuadrupole: bad specification", \
                                     " for quadrupole strength!")

        self.setLength(_Length)
        self.setStrength(_Strength)

        iRefPrtcl = Prtcl.ReferenceParticle.getinstance()
        self.setTransferMatrix(iRefPrtcl.getMomentumIn(0))

        if self.getDebug():
            print("     ----> New FocusQuadrupole instance: \n", self)

    def __repr__(self):
        return "FocusQuadrupole()"

    def __str__(self):
        print(" FocusQuadrupole:")
        print(" ----------------")
        print("     ----> Debug flag:", FocusQuadrupole.getDebug())
        print("     ----> Length (m):", self.getLength())
        print("     ----> Strength:", self.getStrength())
        with np.printoptions(linewidth=500,precision=7,suppress=True):
            print("     ----> Transfer matrix: \n", self.getTransferMatrix())
        BeamLineElement.__str__(self)
        return " <---- FocusQuadrupole parameter dump complete."

    def SummaryStr(self):
        Str  = "FocusQuadrupole  : " + BeamLineElement.SummaryStr(self) + \
            "; Length = " + str(self.getLength()) + \
            "; Strength = " + str(self.getStrength())
        return Str

    
# -------- "Set methods"
# Methods believed to be self-documenting(!)
    def setLength(self, _Length):
        if not isinstance(_Length, float):
            raise badParameter( \
                            "BeamLineElement.FocusQuadrupole.setLength:", \
                            " bad length:", _Length)
        self._Length = _Length

    def setStrength(self, _Strength):
        if not isinstance(_Strength, float):
            raise badParameter( \
                    "BeamLineElement.FocusQuadrupole.setStrength:", \
                    " bad quadrupole strength:", _Strength)
        self._Strength = _Strength

    def setTransferMatrix(self, _p0=None):
        if not isinstance(_p0, float):
            raise badParameter(\
                    "BeamLineElement.FocusQuadrupole.setTransferMatrix:", \
                               "bad reference particle momentum:", _p0)

        Brho = (1./(speed_of_light*1.E-9))*_p0/1000.
        k = self._Strength / Brho
        l = self._Length

        b = np.sqrt(k)
        a = l * b

        TrnsMtrx = np.array([                                             \
            [   np.cos(a), np.sin(a)/b, 0., 0.,                   0., 0.],\
            [-b*np.sin(a),   np.cos(a), 0., 0.,                   0., 0.],\
            [          0.,          0., np.cosh(a), np.sinh(a)/b, 0., 0.],\
            [          0.,          0., b*np.sinh(a), np.cosh(a), 0., 0.],\
            [0., 0., 0., 0., 1., 0.],\
            [0., 0., 0., 0., 0., 1.]\
        ])

        self._TrnsMtrx = TrnsMtrx

        
# -------- "Get methods"
# Methods believed to be self-documenting(!)
    def getLength(self):
        return self._Length

    def getStrength(self):
        return self._Strength

    
# -------- Utilities:
    def Transport(self, _R):
        if not isinstance(_R, np.ndarray) or np.size(_R) != 6:
            raise badParameter( \
                        " BeamLineElement.Transport: bad input vector:", \
                                _R)

        iRefPrtcl = Prtcl.ReferenceParticle.getinstance()
        
        mmtm = iRefPrtcl.getMomentumIn(0) + iRefPrtcl.getMomentumIn(0)*_R[5]

        self.setTransferMatrix(mmtm)
        
        return self.getTransferMatrix().dot(_R)
    

"""
Derived class DefocusQuadrupole:
================================

  DefocusQuadrupole class derived from BeamLineElement to contain paramters
  for a D-quad.


  Class attributes:
  -----------------
    instances : List of instances of BeamLineElement class
  __Debug     : Debug flag


  Parent class instance attributes:
  ---------------------------------
  Calling arguments:
   _Name : Name
   _rCtr : numpy array; x, y, z position (in m) of centre of element.
   _vCtr : numpy array; theta, phi of principal axis of element.
  _drCtr : "error", displacement of centre from nominal position.
  _dvCtr : "error", deviation in theta and phy from nominal axis.

  _TrnsMtrx : Transfer matrix:
         Input: Brho: float ... B*rho (=3.3356E-3) * p (MeV)
                      at init in __init__ Brho=1. is used


  Instance attributes to define quadrupole:
  -----------------------------------------
  _Length  : Length of quad, m
  _Strength: Strength of quad in T/m

    
  Methods:
  --------
  Built-in methods __init__, __repr__ and __str__.
      __init__ : Creates instance of beam-line element class.
      __repr__: One liner with call.
      __str__ : Dump of constants

    SummaryStr: No arguments, returns one-line string summarising quad
                parameterrs.

  Set methods:
    setLength: set length:
          Input: _Length (float): length of quad (m)
  setStrength: -Strength (float): strength of quad (T/m)
          Input: _Length (float): length of quad

setTransferMatrix: Set transfer matrix; calculate using i/p brhop
          Input: Brho (T m)
         Return: np.array(6,6,) transfer matrix

  Get methods:
      getLength, getStrength

  Utilities:
    Transport: transport through focus quad.  Sets transfer matrix (using
               call to setTransferMatrix) given Brho
            Input:
                  R: 6D numpy array containing phase space at entry of
                      aperture
               Brho: Brho: float ... B*rho (~3.3356E-3) * p (MeV
             Rprime: 6D phase space (numpy array) at exit of aperture
                     if the particle passes through the aperture ... or ...

"""
class DefocusQuadrupole(BeamLineElement):
    instances = []
    __Debug = False

    def __init__(self, _Name=None, \
                 _rCtr=None, _vCtr=None, _drCtr=None, _dvCtr=None, \
                 _Length=None, _Strength=None):
        if self.__Debug:
            print(' DefocusQuadrupole.__init__: ', \
                  'creating the DefocusQuadrupole object: Length=', \
                  _Length, ', Strength=', _Strength)

        DefocusQuadrupole.instances.append(self)

        # BeamLineElement class initialization:
        BeamLineElement.__init__(self, _Name, _rCtr, _vCtr, _drCtr, _dvCtr)

        if not isinstance(_Length, float):
            raise badBeamLineElement("DefocusQuadrupole:",\
                                     " bad specification for length!")
        if not isinstance(_Strength, float):
            raise badBeamLineElement("DefocusQuadrupole:", \
                                     " bad specification for quadrupole", \
                                     " strength!")

        self.setLength(_Length)
        self.setStrength(_Strength)
        
        iRefPrtcl = Prtcl.ReferenceParticle.getinstance()
        self.setTransferMatrix(iRefPrtcl.getMomentumIn(0))

        if self.__Debug:
            print("     ----> New DefocusQuadrupole instance: \n", self)

    def __repr__(self):
        return "DefocusQuadrupole()"

    def __str__(self):
        print(" DefocusQuadrupole:")
        print(" -------------------")
        print("     ----> Debug flag:", DefocusQuadrupole.getDebug())
        print("     ----> Length (m):", self.getLength())
        print("     ----> Strength:", self.getStrength())
        with np.printoptions(linewidth=500,precision=7,suppress=True):
            print("     ----> Transfer matrix: \n", self.getTransferMatrix())
        BeamLineElement.__str__(self)
        return " <---- DefocusQuadrupole parameter dump complete."

    def SummaryStr(self):
        Str  = "DefocusQuadrupole: " + BeamLineElement.SummaryStr(self) + \
            "; Length = " + str(self.getLength()) + \
            "; Strength = " + str(self.getStrength())
        return Str

    
# -------- "Set methods"
# Methods believed to be self-documenting(!)
    def setLength(self, _Length):
        if not isinstance(_Length, float):
            raise badParameter( \
                "BeamLineElement.DefocusQuadrupole.setLength:", \
                " bad length:", _Length)
        self._Length = _Length

    def setStrength(self, _Strength):
        if not isinstance(_Strength, float):
            raise badParameter( \
                "BeamLineElement.DefocusQuadrupole.setStrength:", \
                " bad quadrupole strength:", _Strength)
        self._Strength = _Strength

    def setTransferMatrix(self, _p0=None):
        if not isinstance(_p0, float):
            raise badParameter(\
                    "BeamLineElement.DeocusQuadrupole.setTransferMatrix:", \
                               "bad reference particle momentum:", _p0)

        Brho = (1/(speed_of_light*1.E-9))*_p0/1000.
        k = self._Strength / Brho
        l = self._Length

        b = np.sqrt(k)
        a = l * b

        TrnsMtrx = np.array([                                               \
            [  np.cosh(a), np.sinh(a)/b,           0.,          0., 0., 0.],\
            [b*np.sinh(a),   np.cosh(a),           0.,          0., 0., 0.],\
            [          0.,           0.,    np.cos(a), np.sin(a)/b, 0., 0.],\
            [          0.,           0., -b*np.sin(a),   np.cos(a), 0., 0.],\
            [0., 0., 0., 0., 1., 0.],\
            [0., 0., 0., 0., 0., 1.] \
        ])

        self._TrnsMtrx = TrnsMtrx

    # -------- "Get methods"
    # Methods believed to be self-documenting(!)
    def getLength(self):
        return self._Length

    def getStrength(self):
        return self._Strength

# -------- Utilities:
    def Transport(self, _R):
        if not isinstance(_R, np.ndarray) or np.size(_R) != 6:
            raise badParameter( \
                        " BeamLineElement.Transport: bad input vector:", \
                                _R)
        
        iRefPrtcl = Prtcl.ReferenceParticle.getinstance()
        
        mmtm = iRefPrtcl.getMomentumIn(0) + iRefPrtcl.getMomentumIn(0)*_R[5]

        self.setTransferMatrix(mmtm)

        return self.getTransferMatrix().dot(_R)

"""
Derived class SectorDipole:
===========================

  SectorDipole class derived from BeamLineElement to contain parameters
  for a sector dipole


  Class attributes:
  -----------------
    instances : List of instances of BeamLineElement class
  __Debug     : Debug flag


  Parent class instance attributes:
  ---------------------------------
  Calling arguments:
   _Name : Name
   _rCtr : numpy array; x, y, z position (in m) of centre of element.
   _vCtr : numpy array; theta, phi of principal axis of element.
  _drCtr : "error", displacement of centre from nominal position.
  _dvCtr : "error", deviation in theta and phy from nominal axis.

  _TrnsMtrx : Transfer matrix


  Instance attributes to define quadrupole:
  -----------------------------------------
  _Angle  : Bending angle, degrees

    
  Methods:
  --------
  Built-in methods __init__, __repr__ and __str__.
      __init__ : Creates instance of beam-line element class.
      __repr__: One liner with call.
      __str__ : Dump of constants

    SummaryStr: No arguments, returns one-line string summarising dipole
                parameterrs.

  Set methods:
    setAngle: set length:
          Input: _Angle (float): angle through which dipole bends reference
                                 particle

setTransferMatrix: Set transfer matrix; calculate using i/p brhop
          Input: Brho (T m)
         Return: np.array(6,6,) transfer matrix

  Get methods:
      getAngle

  Utilities:

"""
class SectorDipole(BeamLineElement):
    instances = []
    __Debug = False

    def __init__(self, _Name=None, \
                 _rCtr=None, _vCtr=None, _drCtr=None, _dvCtr=None, \
                 _Angle=None, _B=None):
        if self.__Debug:
            print(' SectorDipole(BeamLineElement).__init__: ', \
                  'creating SectorDipole object: Angle=', _Angle)

        SectorDipole.instances.append(self)

        # BeamLineElement class initialization:
        BeamLineElement.__init__(self, _Name, _rCtr, _vCtr, _drCtr, _dvCtr)

        if not isinstance(_Angle, float):
            raise badBeamLineElement( \
                "SectorDipole: bad specification for bending angle (Angle)!")

        self.setAngle(_Angle)
        self.setB(_B)
        iRefPrtcl = Prtcl.ReferenceParticle.getinstance()
        self.setTransferMatrix(iRefPrtcl.getMomentumIn(0))

        if self.__Debug:
            print("     ----> New SectorDipole instance: \n", self)

    def __repr__(self):
        return "SectorDipole()"

    def __str__(self):
        print(" SectorDipole:")
        print(" -------")
        print("     ----> Debug flag:", SectorDipole.getDebug())
        print("     ----> Bending Angle (Angle):", self.getAngle())
        print("     ----> Magnetic field:", self.getB())
        print("     ----> Transfer matrix: \n", self.getTransferMatrix())
        BeamLineElement.__str__(self)
        return " <---- SectorDipole parameter dump complete."

# -------- "Set methods"
#..  Methods believed to be self-documenting(!)
    def setAngle(self, _Angle):
        if not isinstance(_Angle, float):
            raise badParameter(\
                               "BeamLineElement.SectorDipole.setAngle:", \
                               "bad bending angle (Angle):", _Angle)
        self._Angle = _Angle

    def setB(self, _B):
        if not isinstance(_B, float):
            raise badParameter(\
                               "BeamLineElement.SectorDipole.setB:", \
                               "bad B:", _B)
        self._B = _B

    def setTransferMatrix(self, _p0=None):
        if not isinstance(_p0, float):
            raise badParameter(\
                    "BeamLineElement.SectorDipole.setTransferMatrix:", \
                               "bad reference particle momentum:", _p0)
        
        Brho = (1/(speed_of_light*1.E-9))*_p0/1000.
        r    = Brho / self.getB()
        c    = np.cos(self.getAngle())
        s    = np.sin(self.getAngle())
        l    = r * self.getAngle()

        TrnsMtrx = np.array([
            [       c, r*s, 0., 0., 0., r*(1-c)],
            [-(1/r)*s,   c, 0., 0., 0.,       s],
            [      0.,  0., 1.,  l, 0.,      0.],
            [      0.,  0., 0., 1., 0.,      0.],
            [      0.,  0., 0., 0., 1.,      0.],
            [      0.,  0., 0., 0., 0.,      1.]
        ])

        self._TrnsMtrx = TrnsMtrx

# -------- "Get methods"
#..  Methods believed to be self-documenting(!)
    def getAngle(self):
        return self._Angle

    def getB(self):
        return self._B


class Octupole(BeamLineElement):
    instances = []
    __Debug = False

    def __init__(self, _Name=None, \
                 _rCtr=None, _vCtr=None, _drCtr=None, _dvCtr=None, \
                 _Length=None):
        if self.__Debug:
            print(' Octupole.__init__: ', 'creating the Octupole object: Length=', _Length)

        Octupole.instances.append(self)

        # BeamLineElement class initialization:
        BeamLineElement.__init__(self, _Name, _rCtr, _vCtr, _drCtr, _dvCtr)

        if not isinstance(_Length, float):
            raise badBeamLineElement("Octupole: bad specification for length!")

        self.setLength(_Length)
        self.setTransferMatrix()

        if self.__Debug:
            print("     ----> New Octupole instance: \n", self)

    def __repr__(self):
        return "Octupole()"

    def __str__(self):
        print(" Octupole:")
        print(" ---------")
        print("     ----> Debug flag:", Octupole.getDebug())
        print("     ----> Length (m):", self.getLength())
        print("     ----> Transfer matrix: \n", self.getTransferMatrix())
        BeamLineElement.__str__(self)
        return " <---- Octupole parameter dump complete."

    # -------- "Set methods"
    # Methods believed to be self-documenting(!)

    def setLength(self, _Length):
        if not isinstance(_Length, float):
            raise badParameter("BeamLineElement.Octupole.setLength: bad length:", _Length)
        self._Length = _Length

    def setTransferMatrix(self):
        l = self._Length

        TrnsMtrx = np.array([
            [1, l, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, l, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1]
        ])

        self._TrnsMtrx = TrnsMtrx

    # -------- "Get methods"
    # Methods believed to be self-documenting(!)

    def getLength(self):
        return self._Length
    
"""
Derived class Solenoid:
=======================

  Solenoid class derived from BeamLineElement to contain paramters
  for a solenoid.


  Class attributes:
  -----------------
    instances : List of instances of BeamLineElement class
  __Debug     : Debug flag


  Derived instance attributes:
  ----------------------------
  Calling arguments:
   _rCtr : numpy array; x, y, z position (in m) of centre of element.
   _vCtr : numpy array; theta, phi of principal axis of element.
  _drCtr : "error", displacement of centre from nominal position.
  _dvCtr : "error", deviation in theta and phy from nominal axis.


  _TrnsMtrx : Transfer matrix (6x6).  Set to Null in __init__, initialised
              (to Null) in BeamLineElement.__init__, filled in derived
              classes.
                

  Instance attributes to define quadrupole:
  -----------------------------------------
  _Length  : Length of quad, m
  _Strength: Strength of solenoid (B0) in T

    
  Methods:
  --------
  Built-in methods __init__, __repr__ and __str__.
      __init__ : Creates instance of beam-line element class.
      __repr__: One liner with call.
      __str__ : Dump of constants

    SummaryStr: No arguments, returns one-line string summarising quad
                parameterrs.

  Set methods:
    setLength: set length:
          Input: _Length (float)   : length of quad (m)
  setStrength: set primary field strength
          Input: _Streng=th (float): strength of solenoid (B0) (T)

setTransferMatrix: Set transfer matrix; calculate using i/p kinetic
                   energy for test particle and reference particle
          Input: Brho (T m)
         Return: np.array(6,6,) transfer matrix
         Return: np.array(6,6,) transfer matrix

  Get methods:
      getLength, getStrength

  Utilities:
    Transport: transport through solenoid.  Sets transfer matrix (using
               call to setTransferMatrix) given Brho
            Input:
                  R: 6D numpy array containing phase space at entry of
                      solenoid
               Brho: Brho (T m)
             Rprime: 6D phase space (numpy array) at exit of aperture
                     if the particle passes through the solenoid.

"""
class Solenoid(BeamLineElement):
    instances = []
    __Debug = False

    def __init__(self, _Name=None, \
                 _rCtr=None, _vCtr=None, _drCtr=None, _dvCtr=None, \
                 _Length=None, _Strength=None):

        if self.getDebug():
            print(" Solenoid.__init__:", \
                  " creating the Solenoid object: Length=", _Length, " m,"\
                  " strength=", _Strength, " T")

        Solenoid.instances.append(self)

        # BeamLineElement class initialization:
        BeamLineElement.__init__(self, _Name, _rCtr, _vCtr, _drCtr, _dvCtr)

        if not isinstance(_Length, float):
            raise badBeamLineElement( \
                            "Solenoid: bad specification for length!")
        if not isinstance(_Strength, float):
            raise badBeamLineElement( \
                            "Solenoid: bad specification for strength!")

        self.setLength(_Length)
        self.setStrength(_Strength)

        iRefPrtcl = Prtcl.ReferenceParticle.getinstance()
        self.setTransferMatrix(iRefPrtcl.getMomentumIn(0))

        if self.getDebug():
            print("     ----> New Solenoid instance: \n", self)

    def __repr__(self):
        return "Solenoid()"

    def __str__(self):
        print(" Solenoid:")
        print(" ---------")
        print("     ----> Debug flag:", Solenoid.getDebug())
        print("     ----> Length (m):", self.getLength())
        print("     ----> Strength:", self.getStrength())
        with np.printoptions(linewidth=500,precision=7,suppress=True):
            print("     ----> Transfer matrix: \n", self.getTransferMatrix())
        BeamLineElement.__str__(self)
        return " <---- Solenoid parameter dump complete."

    def SummaryStr(self):
        Str  = "Solenoid         : " + BeamLineElement.SummaryStr(self) + \
            "; Length = " + str(self.getLength()) + \
            "; Strength = " + str(self.getStrength())
        return Str

    
# -------- "Set methods"
# Methods believed to be self-documenting(!)
    @classmethod
    def setDebug(cls, Debug):
        cls.__Debug = Debug
        
    def setLength(self, _Length):
        if not isinstance(_Length, float):
            raise badParameter( \
                "BeamLineElement.Solenoid.setLength: bad length:", _Length)
        self._Length = _Length

    def setStrength(self, _Strength):
        if not isinstance(_Strength, float):
            raise badParameter("BeamLineElement.Solenoid.setStrength:" \
                               " bad strength value:", _Strength)
        self._Strength = _Strength

    def setTransferMatrix(self, _p0=None):
        if _p0 == None:
            raise badBeamLineElement( \
            " Solenoid(BeamLineElement).setTransferMatrix:", \
                               "bad reference particle momentum:", _p0)

        Brho = (1./(speed_of_light*1.E-9))*_p0/1000.
        l  = self.getLength()
        k     = self.getStrength() / (2.*Brho)
        
        ckl  = mth.cos(k*l)
        skl  = mth.sin(k*l)
        sckl = ckl*skl

        TrnsMtrx = np.array([                                      \
            [   ckl**2,    sckl/k,      sckl, (skl**2)/k, 0., 0.], \
            [  -k*sckl,    ckl**2, -k*skl**2,       sckl, 0., 0.], \
            [    -sckl, -skl**2/k,    ckl**2,     sckl/k, 0., 0.], \
            [ k*skl**2,     -sckl,   -k*sckl,     ckl**2, 0., 0.], \
            [0., 0., 0., 0., 1., 0.],                              \
            [0., 0., 0., 0., 0., 1.]                               \
                             ])

        self._TrnsMtrx = TrnsMtrx

        
# -------- Get methods:
#..   Methods believed to be self-documenting(!)
    def getLength(self):
        return self._Length

    def getStrength(self):
        return self._Strength
    

# -------- Utilities:
    def Transport(self, _R):
        if not isinstance(_R, np.ndarray) or np.size(_R) != 6:
            raise badParameter( \
                        " BeamLineElement.Transport: bad input vector:", \
                                _R)
        
        iRefPrtcl = Prtcl.ReferenceParticle.getinstance()
        
        mmtm = iRefPrtcl.getMomentumIn(0) + iRefPrtcl.getMomentumIn(0)*_R[5]

        self.setTransferMatrix(mmtm)

        return self.getTransferMatrix().dot(_R)

"""
Derived class GaborLens:
========================

  GaborLens class derived from BeamLineElement to contain paramters
  for a Gabor lens.


  Class attributes:
  -----------------
    instances : List of instances of BeamLineElement class
  __Debug     : Debug flag


  Derived instance attributes:
  ----------------------------
  Calling arguments:
   _rCtr : numpy array; x, y, z position (in m) of centre of element.
   _vCtr : numpy array; theta, phi of principal axis of element.
  _drCtr : "error", displacement of centre from nominal position.
  _dvCtr : "error", deviation in theta and phy from nominal axis.


  _TrnsMtrx : Transfer matrix (6x6).  Set to Null in __init__, initialised
              (to Null) in BeamLineElement.__init__, filled in derived
              classes.
                

  Instance attributes to define quadrupole:
  -----------------------------------------
  _Length  : Length of quad, m
  _Strength: Strength of solenoid (B0) in T

    
  Methods:
  --------
  Built-in methods __init__, __repr__ and __str__.
      __init__ : Creates instance of beam-line element class.
      __repr__: One liner with call.
      __str__ : Dump of constants

    SummaryStr: No arguments, returns one-line string summarising quad
                parameterrs.

  Set methods:
           setLength: set length:
                  Input: _Length (float)   : length of lens (m)
  setElectronDensity: set primary field strength
                  Input: _ne (float): electron density (m^{-3))

setTransferMatrix: Set transfer matrix; calculate using i/p kinetic
                   energy for test particle and reference particle
          Input: Brho (T m)
         Return: np.array(6,6,) transfer matrix
         Return: np.array(6,6,) transfer matrix

  Get methods:
      getLength, getElectronDensity

  Utilities:
    Transport: transport through solenoid.  Sets transfer matrix (using
               call to setTransferMatrix) given Brho
            Input:
                  R: 6D numpy array containing phase space at entry of
                      solenoid
               Brho: Brho (T m)
             Rprime: 6D phase space (numpy array) at exit of aperture
                     if the particle passes through the solenoid.

"""
class GaborLens(BeamLineElement):
    instances = []
    __Debug = True

    def __init__(self, _Name=None, \
                 _rCtr=None, _vCtr=None, _drCtr=None, _dvCtr=None, \
                 _Bz=None, _VA=None, _RA=None, _Rp=None, _Length=None):

        if self.getDebug():
            print(" GaborLens.__init__:", \
                  " creating the GaborLens object:")
            print("     ---->     Bz:",     _Bz, " T")
            print("     ---->     VA:",     _VA, " V")
            print("     ---->     RA:",     _RA, " m")
            print("     ---->     RP:",     _Rp, " m")
            print("     ----> Length:", _Length, " m")

        GaborLens.instances.append(self)

        # BeamLineElement class initialization:
        BeamLineElement.__init__(self, _Name, _rCtr, _vCtr, _drCtr, _dvCtr)

        OK = self.setAll2None()

        if not isinstance(_Bz, float):
            raise badBeamLineElement( \
                            "GaborLens: bad specification for Bz!")
        if not isinstance(_VA, float):
            raise badBeamLineElement( \
                            "GaborLens: bad specification for Bz!")
        if not isinstance(_RA, float):
            raise badBeamLineElement( \
                            "GaborLens: bad specification for Bz!")
        if not isinstance(_Rp, float):
            raise badBeamLineElement( \
                            "GaborLens: bad specification for Bz!")
        if not isinstance(_Length, float):
            raise badBeamLineElement( \
                            "GaborLens: bad specification for length!")

        self.setBz(_Length)
        self.setVA(_Length)
        self.setRA(_Length)
        self.setRp(_Length)
        self.setLength(_Length)
        self.setElectronDensity()

        iRefPrtcl = Prtcl.ReferenceParticle.getinstance()
        self.setTransferMatrix(iRefPrtcl.getMomentumIn(0))

        if self.getDebug():
            print("     ----> New GaborLens instance: \n", self)

    def __repr__(self):
        return "GaborLens()"

    def __str__(self):
        print(" GaborLens:")
        print(" ---------")
        print("     ----> Debug flag:", GaborLens.getDebug())
        print("     ----> Length (m):", self.getLength())
        print("     ----> n_e (/m^3):", self.getElectronDensity())
        with np.printoptions(linewidth=500,precision=7,suppress=True):
            print("     ----> Transfer matrix: \n", self.getTransferMatrix())
        BeamLineElement.__str__(self)
        return " <---- GaborLens parameter dump complete."

    def SummaryStr(self):
        Str  = "GaborLens         : " + BeamLineElement.SummaryStr(self) + \
            "; Length = " + str(self.getLength()) + \
            "; Electron density = " + str(self.getElectronDensity())
        return Str

    
# -------- "Set methods"
# Methods believed to be self-documenting(!)
    @classmethod
    def setDebug(cls, Debug):
        cls.__Debug = Debug

    def setAll2None(self):
        self._Bz    = None
        self._VA    = None
        self._RA    = None
        self._Rp    = None
        self._Lengh = None
        
    def setBz(self, _Bz):
        if not isinstance(_Bz, float):
            raise badParameter( \
                "BeamLineElement.GaborLens.setBz: bad length:", _Bz)
        self._Bz = _Bz

    def setVA(self, _VA):
        if not isinstance(_VA, float):
            raise badParameter( \
                "BeamLineElement.GaborLens.setVA: bad length:", _VA)
        self._VA = _VA

    def setRA(self, _RA):
        if not isinstance(_RA, float):
            raise badParameter( \
                "BeamLineElement.GaborLens.setRA: bad length:", _RA)
        self._RA = _RA

    def setRp(self, _Rp):
        if not isinstance(_Rp, float):
            raise badParameter( \
                "BeamLineElement.GaborLens.setRp: bad length:", _Rp)
        self._Rp = _Rp

    def setLength(self, _Length):
        if not isinstance(_Length, float):
            raise badParameter( \
                "BeamLineElement.GaborLens.setLength: bad length:", _Length)
        self._Length = _Length

    def setElectronDensity(self):
        if self.getBz() == None or              \
           self.getVA() == None or              \
           self.getRA() == None or              \
           self.getRp() == None:
            raise badParameter( \
                        "BeamLineElement.GaborLens.setElectronDensity:" \
                               " no parameters!")

        ne_trans = epsilon0 * self.getBz() / (2. * electronMASS)
        ne_longi = 4. * epsilon0 * self.getVA() / \
            (electronCHARGE * self.getRp()**2 * ( \
                        1. + 2.*mth.log(self.getRA()/self.getRp()) \
                                                 ))
        self._ElectronDensity = 1.
        
    def setTransferMatrix(self, p0=None):
        if p0 == None:
            raise badBeamLineElement( \
            " GaborLens(BeamLineElement).setTransferMatrix:", \
                               "bad reference particle momentum:", _p0)

        E0     = mth.sqrt(protonMASS**2 + p0**2)
        gamma0 = E0/protonMASS
        l      = self.getLength()
        ne     = self.getElectronDensity()

        print(" GaborLens.setTransferMatrix: l, ne:", l, ne)
        print("     ----> p0, E0:", p0, E0)
        print("         ----> gamma0:", gamma0)

        print("     ----> alpha, electricCHARGE, epsilon0:", \
              alpha, electricCHARGE, epsilon0)
        print("     ----> Joule2MeV:", Joule2MeV)
        print("     ----> m2InvMeV:", m2InvMeV)

        k      = (electricCHARGE**2 * protonMASS * gamma0) / \
                 (2.*epsilon0 * p0**2) * \
                 ne /m2InvMeV
        w      = mth.sqrt(k)
        print("     ----> k, w:", k, w)
        
        cwl  = mth.cos(w*l)
        swl  = mth.sin(w*l)

        TrnsMtrx = np.array([                                      \
            [    cwl, swl/w,     0.,    0., 0., 0.], \
            [ -w*swl,   cwl,     0.,    0., 0., 0.], \
            [     0.,    0.,    cwl, swl/w, 0., 0.], \
            [     0.,    0., -w*swl,   cwl, 0., 0.], \
            [0., 0., 0., 0., 1., 0.],                              \
            [0., 0., 0., 0., 0., 1.]                               \
                             ])

        self._TrnsMtrx = TrnsMtrx

        
# -------- Get methods:
#..   Methods believed to be self-documenting(!)
    @classmethod
    def getDebug(self):
        return self.__Debug
    
    def getBz(self):
        return self._Bz

    def getVA(self):
        return self._VA

    def getRA(self):
        return self._RA

    def getRp(self):
        return self._Rp

    def getLength(self):
        return self._Length

    def getElectronDensity(self):
        return self._ElectronDensity
    

# -------- Utilities:
    def Transport(self, _R):
        if not isinstance(_R, np.ndarray) or np.size(_R) != 6:
            raise badParameter( \
                        " BeamLineElement.Transport: bad input vector:", \
                                _R)
        
        iRefPrtcl = Prtcl.ReferenceParticle.getinstance()
        
        mmtm = iRefPrtcl.getMomentumIn(0) + iRefPrtcl.getMomentumIn(0)*_R[5]

        self.setTransferMatrix(mmtm)

        return self.getTransferMatrix().dot(_R)

# -------- New, undebugged classes ...
class RFCavity(BeamLineElement):
    instances = []
    __Debug = False

    def __init__(self, _Name=None, \
                 _rCtr=None, _vCtr=None, _drCtr=None, _dvCtr=None, \
                 _AngFreq=None, _Voltage=None, _RFKick=None, _Time=None):
        if self.__Debug:
            print(' RFCavity.__init__: ', 'creating the RFCavity object: Time=', _Time)

        RFCavity.instances.append(self)

        # BeamLineElement class initialization:
        BeamLineElement.__init__(self, _Name, _rCtr, _vCtr, _drCtr, _dvCtr)

        if not isinstance(_AngFreq, float) or not isinstance(_Voltage, float) or not isinstance(_RFKick, float) or not isinstance(_Time, float):
            raise badBeamLineElement("RFCavity: bad specification for AngFreq, Voltage, RFKick, or Time!")

        self.setAngularFrequency(_AngFreq)
        self.setVoltage(_Voltage)
        self.setRFKick(_RFKick)
        self.setTime(_Time)
        self.setTransferMatrix()

        if self.__Debug:
            print("     ----> New RFCavity instance: \n", self)

    def __repr__(self):
        return "RFCavity()"

    def __str__(self):
        print(" RFCavity:")
        print(" ---------")
        print("     ----> Debug flag:", RFCavity.getDebug())
        print("     ----> Angular frequency (AngFreq):", self.getAngularFrequency())
        print("     ----> Voltage:", self.getVoltage())
        print("     ----> RF Kick (RFKick):", self.getRFKick())
        print("     ----> Time:", self.getTime())
        print("     ----> Transfer matrix: \n", self.getTransferMatrix())
        BeamLineElement.__str__(self)
        return " <---- RFCavity parameter dump complete."

    # -------- "Set methods"
    # Methods believed to be self-documenting(!)

    def setAngularFrequency(self, _AngFreq):
        if not isinstance(_AngFreq, float):
            raise badParameter("BeamLineElement.RFCavity.setAngularFrequency: bad angular frequency:", _AngFreq)
        self._AngFreq = _AngFreq

    def setVoltage(self, _Voltage):
        if not isinstance(_Voltage, float):
            raise badParameter("BeamLineElement.RFCavity.setVoltage: bad voltage:", _Voltage)
        self._Voltage = _Voltage

    def setRFKick(self, _RFKick):
        if not isinstance(_RFKick, float):
            raise badParameter("BeamLineElement.RFCavity.setRFKick: bad RF kick:", _RFKick)
        self._RFKick = _RFKick

    def setTime(self, _Time):
        if not isinstance(_Time, float):
            raise badParameter("BeamLineElement.RFCavity.setTime: bad time:", _Time)
        self._Time = _Time

    def setTransferMatrix(self):
        AngFreq = self._AngFreq
        Voltage = self._Voltage
        RFKick = self._RFKick
        Time = self._Time

        phi = AngFreq * Time
        c = speed_of_light

        TrnsMtrx = np.array([
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, -(AngFreq / c) * (Voltage / (RFKick * c)) * np.cos(phi), 1]
        ])

        self._TrnsMtrx = TrnsMtrx

    # -------- "Get methods"
    # Methods believed to be self-documenting(!)

    def getAngularFrequency(self):
        return self._AngFreq

    def getVoltage(self):
        return self._Voltage

    def getRFKick(self):
        return self._RFKick

    def getTime(self):
        return self._Time

############################################################################   
     
#--------  Utilities:
    def Transport(self, _R):
        if self.__Debug:
            print(" Aperture.Transport: Type, params:", \
                  self._Type, self._Params)
            
        if not isinstance(_R, np.ndarray) or np.size(_R) != 6:
            raise badParameter( \
                        " Aperture.Transport: bad input vector:", \
                                _R)

        Rprime = self.getTransferMatrix().dot(_R)

        if self._Type == 0:
            r  = mth.sqrt( _R[0]**2 + _R[2]**2 )
            if self.__Debug:
                print("     ----> Particle at r =", r, \
                      " aperture R =", self._Params[0])

            if r > self._Params[0]:
                Rprime = None

            if self.__Debug:
                print(" <---- Return phase space =", Rprime)
                
        return Rprime

    
"""
Derived class Source:
=====================

  Source class derived from BeamLineElement to contain paramters for the
  source.  __init__ sets parameters of the source.  


  Class attributes:
  -----------------
    instances : List of instances of BeamLineElement class
  __Debug     : Debug flag


  Parent class instance attributes:
  ---------------------------------
   _Name : Name
   _rCtr : numpy array; x, y, z position (in m) of centre of element.
   _vCtr : numpy array; theta, phi of principal axis of element.
  _drCtr : "error", displacement of centre from nominal position.
  _dvCtr : "error", deviation in theta and phy from nominal axis.


  Instance attributes to define source:
  -------------------------------------
  _Mode  : Int, Mode
  _Param : List of parameters,
           Parameterised laser-driven source (Mode=0):
             [0] - Sigma of x gaussian - m
             [1] - Sigma of y gaussian - m
             [2] - Minimum cos theta to generate
             [3] - E_min: min energy to generate
             [4] - E_max: max energy to generate
             [5] - N_stp: number of steps for numerical integration
           Gaussian (Mode=1):
             [0] - Sigma of x gaussian - m
             [1] - Sigma of y gaussian - m
             [2] - Minimum cos theta to generate
             [3] - Kinetic energy - MeV
             [4] - Sigma of gaussian - MeV

    
  Methods:
  --------
  Built-in methods __init__, __repr__ and __str__.
      __init__ : Creates instance of beam-line element class.
      __repr__: One liner with call.
      __str__ : Dump of constants

    SummaryStr: No arguments, returns one-line string summarising quad
                parameters.

  Set methods:
        setAll2None : Set all instance attributes to None
            setMode : Set mode (int)
        setModeText : Set mode text--string identifying source
      setParameters : Source parameters, fitting with Mode

  Get methods:
        getAll2None : Set all instance attributes to None
            getMode : Set mode (int)
        getModeText : Set mode text--string identifying source

  Utilities and processing methods:
     cleanInstances : Deletes source instance(s) and empties list of sources.

    CheckSoureParam : Checks source parameters are self consistent.  Calls
                      CheckMode and CheckParam
                  Input : Mode (Int), Parameters (list, as defined for Mode)
                 Return : True/False

          CheckMode : Checks mode
                  Input : Mode (Int)
                 Return : True/False

         CheckParam : Check parameters are consistent with Mode
                  Input : Mode (Int), Parameters (list, as defined for Mode)
                 Return : True/False

getParticleFromSource : Generate one particle at source.  Check that particle
                        meets cos(theta) requirement programmed in source
                        parameters.
                  Input : None
                 Return : np.ndarray : 6D phase space of particle at source.

        getParticle : Generate one particle at source using Mode.
                  Input : None
                 Return : np.ndarray : 6D phase space of particle at source.

    getFlatThetaPhi : Generate direction of particle at source flat in
                      cos(theta) and phi
                  Input : None
                 Return : cos(theta) [float], phi [Float]

getLaserDrivenProtonEnergy: Generate proton energy at source using
                            parameterised TNSA spectrum.
                  Input : None
                 Return : Energy [float]

      getTraceSpace : Convert x, y, energy, cos(theta), phi [input] to
                      trace space.

                  Input : x, y, energy, cos(theta), phi [floats]
                 Return : np.ndarray : 6D phase space of particle at source.


"""
class Source(BeamLineElement):
    instances  = []
    __Debug    = False

    ModeList   = [0, 1]
    ModeText   = ["Parameterised laser driven", "Gaussian"]
    ParamList  = [ [float, float, float, float, float, int], \
                   [float, float, float, float, float] ]

    LsrDrvnG_E = None
    LsrDrvnIni = False
    
    def __init__(self, _Name=None, \
                 _rCtr=None, _vCtr=None, _drCtr=None, _dvCtr=None, \
                 _Mode=None, _Param=[]):
        if self.__Debug:
            print(' Source.__init__: ', \
                  'creating the Source object')
            print("     ----> Parameters:", _Param)

        Source.instances.append(self)

        self.setAll2None()
        
        #.. BeamLineElement class initialisation:
        BeamLineElement.__init__(self, _Name, _rCtr, _vCtr, _drCtr, _dvCtr)

        #.. Check valid mode and parameters:
        if _Mode==None or _Param==None:
            print(" BeamLineElement(Source).__init__:", \
                  " bad source paramters:", \
                      _Mode, _Param)
            raise badBeamLineElement( \
                  " Source: bad specification for source!"
                                      )
        ValidSourceParam = self.CheckSourceParam(_Mode, _Param)
        if not ValidSourceParam:
            print(" BeamLineElement(Source).__init__:", \
                  " bad source input; :", \
                  "_Mode, _Param:", _Mode, _Param)
            raise badSourceSpecification( \
                        " BeamLineElement(Source).__init__:", \
                        " bad source paramters. Exit", \
                        _Name
                                                            )

        self.setMode(_Mode)
        self.setModeText(Source.ModeText[_Mode])
        self.setParameters(_Param)
                
        if self.__Debug:
            print("     ----> New Source instance: \n", \
                  self)
            print(" <---- BeamLineElement(Source) instance created.")
            
    def __repr__(self):
        return "Source()"

    def __str__(self):
        print(" BeamLineElement(Source):")
        print(" ------------------------")
        print("     ----> Debug flag:", Source.getDebug())
        print("     ----> Mode      :", self.getMode())
        print("     ----> Mode text :", self.getModeText())
        print("     ----> Parameters:", self.getParameters())
        return " <---- Source parameter dump complete."

    def SummaryStr(self):
        Str  = "Source           : " + BeamLineElement.SummaryStr(self) + \
            "; Mode = " + str(self.getMode()) + "; paramters = " + \
            str(self.getParameters())
        return Str
    

#--------  "Set methods".
#.. Methods believed to be self documenting(!)
    def setAll2None(self):
        self._Mode     = None
        self._ModeText = None
        self._Param    = None
        
    def setMode(self, _Mode):
        if self.getDebug():
            print(" Source.setMode; Mode:", _Mode)
        self._Mode = _Mode

    def setModeText(self, _ModeText):
        if self.getDebug():
            print(" Source.setParamters; Mode:", _ModeText)
        self._ModeText = _ModeText

    def setParameters(self, _Param):
        if self.getDebug():
            print(" Source.setParamters; Parameters:", _Param)
        self._Param = _Param
         
        
#--------  "get methods"
#.. Methods believed to be self documenting(!)
    def getMode(self):
        return self._Mode
    
    def getModeText(self):
        return self._ModeText
    
    def getParameters(self):
        return self._Param
    
        
#--------  Utilities:
    @classmethod
    def cleanInstances(cls):
        for inst in cls.instances:
            del inst
        cls.instances = []
        if cls.getDebug():
            print(' BeamLineElement(Source).cleanInstance: instances removed.')

    @classmethod
    def CheckSourceParam(cls, _Mode, _Param):
        if cls.getDebug():
            print(' BeamLineElement(Source).CheckSourceParam:', \
                  ' mode, params:', \
                  _Mode, _Param)

        ValidMode  = False
        ValidParam = False
        
        ValidMode  = cls.CheckMode(_Mode)
        if ValidMode:
            ValidParam = cls.CheckParam(_Mode, _Param)

        ValidSourceParam = ValidMode and ValidParam
        if cls.getDebug():
            print("     <---- ValidMode, ValidParam, ValidSourcParam:", \
                  ValidMode, ValidParam, ValidSourceParam)

        if cls.getDebug():
            print(' <---- BeamLineElement(Source).CheckSourceParam,', \
                  ' done.  --------', \
                  '  --------  --------  --------  --------  --------')
            
        return ValidSourceParam

    @classmethod
    def CheckMode(cls, _Mode):
        if cls.getDebug():
            print(' BeamLineElement(Source).CheckMode: mode:', _Mode)
            
        #.. Do this with a loop, detault fail
        ValidMode = False
        for iMode in cls.ModeList:
            if cls.getDebug():
                print("     ----> iMode:", iMode, "cf _Mode", _Mode)
            
            if _Mode == iMode:
                ValidMode = True
                break
            
        if cls.getDebug():
            print("     <---- iMode, _Mode, ValidMode:", \
                  iMode, _Mode, ValidMode)
            
        if cls.getDebug():
            print(' <---- BeamLineElement(Source).CheckMode: done.', \
            '  --------  --------  --------  --------  --------  ')

        return ValidMode
    
    @classmethod
    def CheckParam(cls, _Mode, _Param):
        if cls.getDebug():
            print(' BeamLineElement(Source).CheckParam: mode, params:', \
                  _Mode, _Param)

        #.. Detault fail
        ValidParam = False
        if cls.getDebug():
            print("     ----> len(_Param):", len(_Param))
            print("         ----> cf     :", len(cls.ParamList[_Mode]))

        if len(_Param) == len(cls.ParamList[_Mode]):
            iMtch = 0
            for i in range(len(_Param)):
                if cls.getDebug():
                    print("         ----> i, ParamList, _Param:", \
                          i, cls.ParamList[_Mode][i], _Param[i])
                if isinstance(_Param[i], cls.ParamList[_Mode][i]):
                    iMtch += 1
                else:
                    if cls.getDebug():
                        print("             ----> No match for", \
                              "i, ParamList, _Param:", \
                              i, cls.ParamList[_Mode][i], _Param[i])
                    
            if cls.getDebug():
                print("     ----> iMtch:", iMtch)
        else:
            raise badParameters( \
                                 " BeamLineElement(Source).CheckParam:", \
                                 " bad source paramters. Exit")

        if iMtch == len(_Param):
            ValidParam = True
        if cls.getDebug():
            print("     <---- ValidParam:", ValidParam)
        if cls.getDebug():
            print(" <---- BeamLineElement(Source).CheckParam, done.", \
                  "  --------", \
                  '  --------  --------  --------  --------  --------')

        return ValidParam

    def getParticleFromSource(self):
        if self.__Debug:
            print(" BeamLineElement(Source).getParticleFromSource: start")

        #.. Generate initial particle:
        GotOne = False
        nTrys  = 0
        while not GotOne:
            nTrys += 1
            x, y, K, cTheta, Phi = self.getParticle()
            if self.__Debug:
                print("     ----> x, y, K, cTheta, Phi:", \
                      x, y, K, cTheta, Phi)

            #.. Convert to trace space:
            TrcSpc = self.getTraceSpace(x, y, K, cTheta, Phi)
            if self.__Debug:
                print("     ----> Trace space:", TrcSpc)

            if not isinstance(TrcSpc, np.ndarray):
                if self.__Debug:
                    print("     ----> Failed to pass aperture cut.")
                continue
                
            GotOne = True
            if self.__Debug:
                print("     <---- Finally got one after", nTrys, " trys.")

        if self.__Debug:
            print(" <---- BeamLineElement(Source).getParticleFromSource,", \
                  " done.", \
                  '  --------  --------  --------  --------  --------')

        return TrcSpc

    def getParticle(self):
        if self.getDebug():
            print(" BeamLineElement(Source).getParticle: start")
            print("     ----> Mode, paramters:", \
                  self.getMode(), self.getParameters())

        if self._Mode == 0:
            X             = rnd.gauss(0., self.getParameters()[0])
            Y             = rnd.gauss(0., self.getParameters()[1])
            cosTheta, Phi = self.getFlatThetaPhi()
            KE            = self.getLaserDrivenProtonEnergy()

        elif self._Mode == 1:
            X             = rnd.gauss(0., self.getParameters()[0])
            Y             = rnd.gauss(0., self.getParameters()[1])
            cosTheta, Phi = self.getFlatThetaPhi()
            KE            = rnd.gauss(self.getParameters()[3], \
                                      self.getParameters()[4])

        if self.__Debug:
            print("     ----> X, Y, KE, cosTheta, Phi:", \
                  X, Y, KE, cosTheta, Phi)
            
        if self.__Debug:
            print(" <---- BeamLineElement(Source).getParticle, done.", \
                  '  --------  --------  --------  --------  --------')
            
        return X, Y, KE, cosTheta, Phi
    
    def getFlatThetaPhi(self):
        cosTheta = rnd.uniform(self.getParameters()[2], 1.)
        Phi      = rnd.uniform( 0., 2.*mth.pi)
        return cosTheta, Phi

    def getLaserDrivenProtonEnergy(self):
        if not Source.LsrDrvnIni:
            if self.__Debug:
                print(" BeamLineElement(Source).getLaserDrivenProtonEnergy:", \
                      " initialise")
            Source.LsrDrvnIni = True
            E_min = self._Param[3]
            E_max = self._Param[4]
            N_stp = self._Param[5]
            E_stp = (E_max - E_min) / float(N_stp)
            Ei, E_stp1 = np.linspace(E_min, E_max, N_stp, False, True, float)
            g_E = np.exp(-np.sqrt(Ei)) / np.sqrt(Ei)
            g_E /= np.sum(g_E)    # normalize the probability distribution
            G_E  = np.cumsum(g_E) # cumulative probability distribution
            if self.__Debug:
                print("     ----> E_min, E_max, N_stp, E_stp, E_stp1:", \
                      E_min, E_max, N_stp, E_stp, E_stp1)
            Source.LsrDrvnG_E = G_E
    
        #.. Generate random numbers from the distribution using
        #   inverse transform sampling

        G_E = Source.LsrDrvnG_E
        iE  = np.searchsorted(G_E, rnd.uniform(0., 1.))
        E   = self._Param[3] + \
            float(iE) * (self._Param[4] - self._Param[3]) / \
            float(self._Param[5])
        if self.__Debug:
            print("     ----> iE, E:", iE, E)
        
        return E

    def getTraceSpace(self, x, y, K, cTheta, Phi):
        sTheta = mth.sqrt(1.-cTheta**2)
        xPrime = sTheta * mth.cos(Phi)
        yPrime = sTheta * mth.sin(Phi)

        iRefPrtcl = Prtcl.ReferenceParticle.getinstance()
        p0        = iRefPrtcl.getMomentumIn(0)
        mmtm      = mth.sqrt( (protonMASS+K)**2 - protonMASS**2)
        dp        = mmtm - p0
        
        TrcSpc = np.array([x, xPrime, y, yPrime, 0., dp/p0])
        return TrcSpc

    
#--------  Exceptions:
class badBeamLineElement(Exception):
    pass

class badParameter(Exception):
    pass

