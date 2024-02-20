#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
To do:
======
 - Still to do:
   - Editing/checking pass through BLEs to make sure up to date with
     documentation.
   - Constants
   - KL: Add length to aperture: i.e. there can be a length to the plate
         or other collimator structure.
   - KL: Add rotation to Shift2Local and Shift2Global.  Need to update dvStrt
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
             SectorDipole, Octupole, Solenoid, CylindricalRFCavity, Source


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
   _rStrt : numpy array; x, y, z position (in m) of start of element.
   _vStrt : numpy array; theta, phi of principal axis of element.
  _drStrt : "error", displacement of start from nominal position (rad).
  _dvStrt : "error", deviation in theta and phy from nominal axis (rad).

  Instance attributes assigned in BeamLineElement parent class:
  _TrnsMtrx: Transfer matrix (6x6).  Set to Null in __init__, initialised
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
           Return: str="Pos: [x, y, z] = " + str(self.getrStrt())

  Set methods:
      setDebug  : Set debug flag
    setAll2None : Set all attributes to Null
       setName  : Set name of element
       setrStrt  : Set start of element, x, y, z (m)
       setvStrt  : Set orientation of element, theta, phi (rad)
      setdrStrt  : Set offset of start of element, x, y, z (m)
      setdvStrt  : Set offset orientation of element, theta, phi (rad)

  Get methods:
      getDebug  : get debug flag
  getinstances  : get list of instances
       getName  : Get name of element
       getrStrt  : Get start of element, x, y, z (m)
       getvStrt  : Get orientation of element, theta, phi (rad)
      getdrStrt  : Get offset from nominal start of element, x, y, z (m)
      getdvStrt  : Get offset of orientation of element, theta, phi (rad)
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
 1.1: 10Jan24: Update setTraceSpaceAtSource to make it match documented
               definititions.
 1.0: 12Jun23: First implementation

@author: kennethlong
"""

import scipy  as sp
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

epsilon0SI       = 8.8541878128E-12
electronCHARGESI = 1.602176634E-19
electronMASSSI   = 9.1093837015E-31
protonMASSSI     = 1.67262192369E-27


class BeamLineElement:

#-------- Class attributes  --------  --------

#.. List of instances and debug flag
    instances  = []
    __Debug    = False

#--------  "Built-in methods":
    def __init__(self, _Name=None, \
                 _rStrt=None, _vStrt=None, _drStrt=None, _dvStrt=None):
        if self.__Debug:
            print(' BeamLineElement.__init__: ', \
                  'creating the BeamLineElement object')
            print("     ---->               Name:", _Name)
            print("     ---->           Position:", _rStrt)
            print("     ---->        Orientation:", _vStrt)
            print("     ---->    Position offset:", _drStrt)
            print("     ----> Orientation offset:", _dvStrt)

        BeamLineElement.instances.append(self)

        self.setAll2None()
        
        if  not isinstance( _Name, str)        or \
            not isinstance( _rStrt, np.ndarray) or \
            not isinstance( _vStrt, np.ndarray) or \
            not isinstance(_drStrt, np.ndarray) or \
            not isinstance(_dvStrt, np.ndarray):
            raise badBeamLineElement( \
                  " BeamLineElement: no default beamline element!"
                                      )

        self.setName(_Name)
        self.setrStrt(_rStrt)
        self.setvStrt(_vStrt)
        self.setdrStrt(_drStrt)
        self.setdvStrt(_dvStrt)
        
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
        print("     ---->           Position:", self.getrStrt())
        print("     ---->        Orientation:", self.getvStrt())
        print("     ---->    Position offset:", self.getdrStrt())
        print("     ----> Orientation offset:", self.getdvStrt())
        return " <---- BeamLineElement parameter dump complete."

    def SummaryStr(self):
        Str = "Pos: [x, y, z] = " + str(self.getrStrt())
        return Str

    
#--------  "Set method" only Debug
#.. Method believed to be self documenting(!)
    @classmethod
    def cleanInstances(cls):
        for inst in cls.instances:
            del inst
        cls.instances = []
        if cls.getDebug():
            print(' BeamLineElement.cleanInstance: instances removed.')

    @classmethod
    def removeInstance(cls, inst):
        if inst in cls.getinstances():
            if cls.getDebug():
                print(" BeamLineElement.removeInstance: remove", \
                      inst.getName(), "from beamline instances list")
            cls.getinstances().remove(inst)
        else:
            if cls.getDebug():
                print(" BeamLineElement.removeInstance: instance", \
                      inst.Name, "not in BeamLineElement.Instances!")

    @classmethod
    def setDebug(self, Debug=False):
        if self.__Debug:
            print(" BeamLineElement.setdebug: ", Debug)
        self.__Debug = Debug

    def setAll2None(self):
        self._Name      = None
        self._rStrt      = None
        self._vStrt      = None
        self._drStrt     = None
        self._dvStrt     = None
        self._TrnsMtrx = None
        
    def setName(self, _Name):
        if not isinstance(_Name, str):
            raise badParameter(" BeamLineElement.setName: bad name:", \
                               _Name)
        self._Name = _Name
        
    def setrStrt(self, _rStrt):
        if not isinstance(_rStrt, np.ndarray):
            raise badParameter(" BeamLineElement.setrStrt: bad start:", \
                               _rStrt)
        self._rStrt = _rStrt
        
    def setvStrt(self, _vStrt):
        if not isinstance(_vStrt, np.ndarray):
            raise badParameter(" BeamLineElement.setvStrt: bad orienttion:", \
                               _vStrt)
        self._vStrt = _vStrt
        
    def setdrStrt(self, _drStrt):
        if not isinstance(_drStrt, np.ndarray):
            raise badParameter(" BeamLineElement.setdrStrt:", \
                               " bad start offset:", \
                               _drStrt)
        self._drStrt = _drStrt
        
    def setdvStrt(self, _dvStrt):
        if not isinstance(_dvStrt, np.ndarray):
            raise badParameter(" BeamLineElement.setdvStrt:", \
                               " bad orienttion offset:", \
                               _dvStrt)
        self._dvStrt = _dvStrt

        
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

    def getrStrt(self):
        return self._rStrt

    def getvStrt(self):
        return self._vStrt

    def getdrStrt(self):
        return self._drStrt

    def getdvStrt(self):
        return self._dvStrt

    def getTransferMatrix(self):
        return self._TrnsMtrx
    
    def OutsideBeamPipe(self, _R):
        Outside = False
        Rad = np.sqrt(_R[0]**2 + _R[2]**2)
        if Rad >= Facility.getInstance().getVCMVr():
            Outside = True
        return Outside

#--------  Utilities:
    def Transport(self, _R):
        if not isinstance(_R, np.ndarray) or np.size(_R) != 6:
            raise badParameter( \
                        " BeamLineElement.Transport: bad input vector:", \
                                _R)

        if self.getDebug():
            print(" BeamLineElement.Transport:", \
                  Facility.getInstance().getName(), \
                  Facility.getInstance().getVCMVr())
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print("     ----> _R:", _R)
            print("     ----> Outside:", self.OutsideBeamPipe(_R))
            
        if self.OutsideBeamPipe(_R):
            _Rprime = None
        else:
            if isinstance(self, DefocusQuadrupole) or \
               isinstance(self, FocusQuadrupole)   or \
               isinstance(self, Solenoid)          or \
               isinstance(self, SectorDipole)      or \
               isinstance(self, GaborLens)         or \
               isinstance(self, QuadDoublet)       or \
               isinstance(self, QuadTriplet):
                self.setTransferMatrix(_R)
            _Rprime = self.getTransferMatrix().dot(_R)

        if self.getDebug():
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print(" <---- Rprime:", _Rprime)

        if not isinstance(_Rprime, np.ndarray):
            pass

        return _Rprime

    def Shift2Local(self, _R):
        if not isinstance(_R, np.ndarray) or np.size(_R) != 6:
            raise badParameter( \
                        " BeamLineElement.Shift2Local: bad input vector:", \
                                _R)

        _Rprime    = _R
        _Rprime[0] -= self._drStrt[0]
        _Rprime[2] -= self._drStrt[1]

        return _Rprime

    def Shift2Global(self, _R):
        if not isinstance(_R, np.ndarray) or np.size(_R) != 6:
            raise badParameter( \
                        " BeamLineElement.Shift2Local: bad input vector:", \
                                _R)
        
        _Rprime    = _R
        _Rprime[0] += self._drStrt[0]
        _Rprime[2] += self._drStrt[1]
        
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
   _rStrt : numpy array; x, y, z position (in m) of start of element.
   _vStrt : numpy array; theta, phi of principal axis of element.
  _drStrt : "error", displacement of start from nominal position.
  _dvStrt : "error", deviation in theta and phy from nominal axis.
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
    instance  = None
    __Debug   = False

    
#--------  "Built-in methods":
    def __init__(self, _Name=None, \
                 _rStrt=None, _vStrt=None, _drStrt=None, _dvStrt=None, \
                 _p0=None, _VCMVr=None):

        if Facility.instance == None:
            Facility.instance = self
            
            if self.__Debug:
                print(' Facility.__init__: ', \
                      'creating the Facility object:')
                print("     ----> Name:", _Name)
                print("     ----> Reference particle momentum:", _p0)
                print("     ----> Vacuum chamber mother volume radius", \
                      _VCMVr)

            Facility.instance = self

            #.. BeamLineElement class initialisation:
            BeamLineElement.__init__(self, \
                                     _Name, _rStrt, _vStrt, _drStrt, _dvStrt)

            if not isinstance(_p0, float):
                raise badBeamLineElement( \
                " Facility: bad specification for reference particle mometnum!"
                                         )
            if not isinstance(_VCMVr, float):
                raise badBeamLineElement( \
            " Facility: bad specification for vacuum chamber mother volume!"
                                         )
            
            self.setp0(_p0)
            self.setVCMVr(_VCMVr)
                
            if self.__Debug:
                print("     ----> New Facility instance: \n", \
                      self)
        else:
            print(' Facility(BeamLineElement).__init__: ',       \
                  " attempt to create facility.", \
                  " Abort!")
            raise secondFacility(" Second call not allowed.")
                
            
    def __repr__(self):
        return "Facility()"

    def __str__(self):
        print(" Facility:")
        print(" ------")
        print("     ----> Debug flag:", Facility.getDebug())
        print("     ----> Name      :", self.getName())
        print("     ----> p0 (MeV/c):", self.getp0())
        print("     ----> Vacuum chamber mother volume radius (m):", \
              self.getVCMVr())
        BeamLineElement.__str__(self)
        return " <---- Facility parameter dump complete."

    def SummaryStr(self):
        Str  = "Facility         : " + BeamLineElement.SummaryStr(self) + \
            "; Name = " + self.getName() + "; p0 = " + str(self.getp0()) + \
            "; VCMVr = " + str(self.getVCMVr())
        return Str


#--------  "Set methods"
#.. Methods believed to be self documenting(!)
    def setp0(self, _p0=None):
        if not isinstance(_p0, float):
            raise badParameter( \
                     " BeamLineElement.Facility.setp0: bad p0",
                                _p0)
        self._p0 = _p0

    def setVCMVr(self, _VCMVr=None):
        if not isinstance(_VCMVr, float):
            raise badParameter( \
                     " BeamLineElement.Facility.setVCMVr: bad VCMVr",
                                _VCMVr)
        self._VCMVr = _VCMVr

        
#--------  "get methods"
#.. Methods believed to be self documenting(!)
    @classmethod
    def getInstance(cls):
        return cls.instance
    
    def getp0(self):
        return self._p0
    
    def getVCMVr(self):
        return self._VCMVr
    
        
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
   _rStrt : numpy array; x, y, z position (in m) of start of element.
   _vStrt : numpy array; theta, phi of principal axis of element.
  _drStrt : "error", displacement of start from nominal position.
  _dvStrt : "error", deviation in theta and phy from nominal axis.
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
                 _rStrt=None, _vStrt=None, _drStrt=None, _dvStrt=None, \
                 _Length=None):
        if self.__Debug:
            print(' Drift.__init__: ', \
                  'creating the Drift object: Length=', _Length)

        Drift.instances.append(self)

        #.. BeamLineElement class initialisation:
        BeamLineElement.__init__(self, _Name, _rStrt, _vStrt, _drStrt, _dvStrt)

        if not isinstance(_Length, float):
            raise badBeamLineElement( \
                  " Drift: bad specification for length of drift!"
                                      )
        self.setLength(_Length)
        
        self.setTransferMatrix()
                
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

    def setTransferMatrix(self):
        iRefPrtcl = Prtcl.ReferenceParticle.getinstance()
        if not isinstance(iRefPrtcl, Prtcl.ReferenceParticle):
            raise ReferenceParticleNotSpecified()

        iPrev = len(iRefPrtcl.getPrOut()) - 1

        p0        = mth.sqrt(np.dot(iRefPrtcl.getPrOut()[iPrev][:3], \
                                    iRefPrtcl.getPrOut()[iPrev][:3]))
        E0        = iRefPrtcl.getPrOut()[iPrev][3]
        b02       = (p0/E0)**2
        g02       = 1./(1.-b02)
        
        if self.getDebug():
            print(" Drift(BeamLineElement).setTransferMatrix:")
            print("     ----> Reference particle 4-mmtm:", \
                  iRefPrtcl.getPrIn()[0])
            print("         ----> p0, E0:", p0, E0)
            print("     <---- b02, g02:", b02, g02)

        l = self.getLength()

        TrnsMtrx = np.array( [ \
                              [1.,  l, 0., 0., 0.,        0.], \
                              [0., 1., 0., 0., 0.,        0.], \
                              [0., 0., 1.,  l, 0.,        0.], \
                              [0., 0., 0., 1., 0.,        0.], \
                              [0., 0., 0., 0., 1., l/b02/g02], \
                              [0., 0., 0., 0., 0.,        1.]  \
                             ] )

        if self.getDebug():
            print("     ----> Drift transfer matrix:")
            print(TrnsMtrx)

        self._TrnsMtrx = TrnsMtrx
        
        if self.getDebug():
            print(" <---- Done.")
        
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
   _rStrt : numpy array; x, y, z position (in m) of start of element.
   _vStrt : numpy array; theta, phi of principal axis of element.
  _drStrt : "error", displacement of start from nominal position.
  _dvStrt : "error", deviation in theta and phy from nominal axis.
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
                 _rStrt=None, _vStrt=None, _drStrt=None, _dvStrt=None, \
                 _Param=[]):
        if self.getDebug():
            print(' Aperture.__init__: ', \
                  'creating the Aperture object')
            print("     ----> Parameters:", _Param)

        Aperture.instances.append(self)
        
        #.. BeamLineElement class initialisation:
        BeamLineElement.__init__(self, _Name, _rStrt, _vStrt, _drStrt, _dvStrt)

        if len(_Param) < 2:
            raise badBeamLineElement( \
                  " Aperture: bad specification for aperture!"
                                      )
        self.setApertureParameters(_Param)
        
        self.setTransferMatrix()
                
        if self.getDebug():
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

        if self.getDebug():
            print(" Aperture(BeamLineElement).Transport:", \
                  self.getType(), self.getParams())
            
        NotCut = True
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
   _rStrt : numpy array; x, y, z position (in m) of start of element.
   _vStrt : numpy array; theta, phi of principal axis of element.
  _drStrt : "error", displacement of start from nominal position.
  _dvStrt : "error", deviation in theta and phy from nominal axis.


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
  setStrength: _Strength (float): strength (gradient) of quad (T/m)
          Input: _Strength (float)
       setkFQ: _kFQ (float): quad focusing, k (m**-2)
          Input: _kFQ (float)

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
    __Debug   = False

    def __init__(self, _Name=None, \
                 _rStrt=None, _vStrt=None, _drStrt=None, _dvStrt=None, \
                 _Length=None, _Strength=None, _kFQ=None):
        
        if self.getDebug():
            print(' FocusQuadrupole.__init__: ', \
                  'creating the FocusQuadrupole object: Length=', \
                  _Length, ', Strength=', _Strength)

        FocusQuadrupole.instances.append(self)

        self.setAll2None()

        #.. Hard wired:
        #   - FQmode = 0 ==> use particle momentum in calculation of k
        #            = 1 ==> use reference particle momentum and dispersion
        #                    calculation.
        self._FQmode = 0

        # BeamLineElement class initialization:
        BeamLineElement.__init__(self, _Name, _rStrt, _vStrt, _drStrt, _dvStrt)

        if not isinstance(_Length, float):
            raise badBeamLineElement("FocusQuadrupole: bad specification", \
                                     " for length!")
        if not isinstance(_Strength, float) and \
           not isinstance(_kFQ, float):
            raise badBeamLineElement("FocusQuadrupole: bad specification", \
                                     " for quadrupole strength!")

        self.setLength(_Length)
        if isinstance(_Strength, float):
            self.setStrength(_Strength)
            self.setkFQ(self.calckFQ())
        if isinstance(_kFQ, float):
            self.setkFQ(_kFQ)
            self.setStrength(self.calcStrength())
                
        if self.getDebug():
            print("     ----> New FocusQuadrupole instance: \n", self)
            print(" <---- Done.")

    def __repr__(self):
        return "FocusQuadrupole()"

    def __str__(self):
        print(" FocusQuadrupole:")
        print(" ----------------")
        print("     ---->     Debug flag:", FocusQuadrupole.getDebug())
        print("     ---->     Length (m):", self.getLength())
        print("     ----> Strength (T/m):", self.getStrength())
        print("     ---->       kFQ (/m):", self.getkFQ())
        with np.printoptions(linewidth=500,precision=7,suppress=True):
            print("     ----> Transfer matrix: \n", self.getTransferMatrix())
        BeamLineElement.__str__(self)
        return " <---- FocusQuadrupole parameter dump complete."

    def SummaryStr(self):
        Str  = "FocusQuadrupole  : " + BeamLineElement.SummaryStr(self) + \
            "; Length = " + str(self.getLength()) + \
            "; Strength (gradient) = " + str(self.getStrength()) + \
            "; kFQ = " + str(self.getkFQ())
        return Str

    
# -------- "Set methods"
# Methods believed to be self-documenting(!)
    @classmethod
    def setDebug(cls, Debug):
        cls.__Debug = Debug
        
    def setAll2None(self):
        self._Length   = None
        self._Strength = None
        self._kFQ      = None
        self._TrnsMtrx = None
        self._FQmode   = None
        
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

    def setkFQ(self, _kFQ):
        if not isinstance(_kFQ, float):
            raise badParameter( \
                    "BeamLineElement.FocusQuadrupole.setStrength:", \
                                " bad quadrupole k constant:", _kFQ)
        self._kFQ = _kFQ

    def setTransferMatrix(self, _R):
        iRefPrtcl = Prtcl.ReferenceParticle.getinstance()
        if not isinstance(iRefPrtcl, Prtcl.ReferenceParticle):
            raise ReferenceParticleNotSpecified()

        iPrev = len(iRefPrtcl.getPrOut()) - 1

        p0        = mth.sqrt(np.dot(iRefPrtcl.getPrOut()[iPrev][:3], \
                                    iRefPrtcl.getPrOut()[iPrev][:3]))
        E0        = iRefPrtcl.getPrOut()[iPrev][3]
        b0        = p0/E0
        b02       = b0**2
        g02       = 1./(1.-b02)
        
        if self.getDebug():
            print(" FocusQuadrupole(BeamLineElement).setTransferMatrix:")
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print("     ----> Reference particle 4-mmtm:", \
                      iRefPrtcl.getPrOut()[iPrev])
            print("         ----> p0, E0:", p0, E0)
            print("     <---- b0, b02, g02:", b0, b02, g02)

        if self.getDebug():
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print("     ----> Trace space:", _R)

        D   = 1.
        Scl = 1.
        if self.getFQmode() == 1:
            D = mth.sqrt(1. + 2.*_R[5]/b0 + _R[5]**2)
        else:
            E   = E0 + _R[5]*p0
            p   = mth.sqrt(E**2 - protonMASS**2)
            Scl = p0 / p
        
        if self.getDebug():
            print("     ----> D:", D)
            print("     ----> E, p, Scl:", E, p, Scl)

        k = self.getkFQ() * Scl
        l = self.getLength()

        b = mth.sqrt(k/D)
        a = l * b
        b = b * D

        if self.getDebug():
            print("     ----> Length, Strength, kFQ:", \
                  self.getLength(), self.getStrength(), self.getkFQ())
            print("     ----> omegaPrime*L, omegaPrime*D:", a, b)

        TrnsMtrx = np.array([                                             \
            [   np.cos(a), np.sin(a)/b, 0., 0.,                   0., 0.],\
            [-b*np.sin(a),   np.cos(a), 0., 0.,                   0., 0.],\
            [          0.,          0., np.cosh(a), np.sinh(a)/b, 0., 0.],\
            [          0.,          0., b*np.sinh(a), np.cosh(a), 0., 0.],\
            [          0.,          0.,           0., 0.,  1., l/b02/g02],\
            [          0.,          0.,           0., 0.,  0.,        1.]\
                            ])

        if self.getDebug():
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print(TrnsMtrx)

        self._TrnsMtrx = TrnsMtrx

        
# -------- "Get methods"
# Methods believed to be self-documenting(!)
    @classmethod
    def getDebug(cls):
        return cls.__Debug

    def getFQmode(self):
        return self._FQmode
    
    def getLength(self):
        return self._Length

    def getStrength(self):
        return self._Strength

    def getkFQ(self):
        return self._kFQ

    
# -------- Utilities:
    def calckFQ(self):
        iRefPrtcl = Prtcl.ReferenceParticle.getinstance()
        if not isinstance(iRefPrtcl, Prtcl.ReferenceParticle):
            raise ReferenceParticleNotSpecified()

        iPrev = len(iRefPrtcl.getPrOut()) - 1

        p0        = mth.sqrt(np.dot(iRefPrtcl.getPrOut()[iPrev][:3], \
                                    iRefPrtcl.getPrOut()[iPrev][:3]))
        
        if self.getDebug():
            print(" FocusQuadrupole(BeamLineElement).calckFQ:")
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print("     ----> Reference particle 4-mmtm:", \
                      iRefPrtcl.getPrOut()[iPrev])
            print("         ----> p0:", p0)

        Brho = (1./(speed_of_light*1.E-9))*p0/1000.
        kFQ  = self.getStrength() / Brho

        if self.getDebug():
            print("     <---- kFQ:", kFQ)
            print(" <---- Done.")

        return kFQ

    def calcStrength(self):
        iRefPrtcl = Prtcl.ReferenceParticle.getinstance()
        if not isinstance(iRefPrtcl, Prtcl.ReferenceParticle):
            raise ReferenceParticleNotSpecified()

        iPrev = len(iRefPrtcl.getPrOut()) - 1

        p0        = mth.sqrt(np.dot(iRefPrtcl.getPrOut()[iPrev][:3], \
                                    iRefPrtcl.getPrOut()[iPrev][:3]))
        
        if self.getDebug():
            print(" FocusQuadrupole(BeamLineElement).calcStrength:")
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print("     ----> Reference particle 4-mmtm:", \
                      iRefPrtcl.getPrOut()[iPrev])
            print("         ----> p0:", p0)

        Brho = (1./(speed_of_light*1.E-9))*p0/1000.
        Strn = self.getkFQ() * Brho

        if self.getDebug():
            print("     <---- Strength:", Strn)
            print(" <---- Done.")

        return Strn
    
    
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
   _rStrt : numpy array; x, y, z position (in m) of start of element.
   _vStrt : numpy array; theta, phi of principal axis of element.
  _drStrt : "error", displacement of start from nominal position.
  _dvStrt : "error", deviation in theta and phy from nominal axis.

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
    __Debug   = False

    def __init__(self, _Name=None, \
                 _rStrt=None, _vStrt=None, _drStrt=None, _dvStrt=None, \
                 _Length=None, _Strength=None, _kDQ=None):

        if self.getDebug():
            print(' DefocusQuadrupole.__init__: ', \
                  'creating the DefocusQuadrupole object: Length=', \
                  _Length, ', Strength=', _Strength)

        DefocusQuadrupole.instances.append(self)

        self.setAll2None()

        #.. Hard wired:
        #   - FQmode = 0 ==> use particle momentum in calculation of k
        #            = 1 ==> use reference particle momentum and dispersion
        #                    calculation.
        self._DQmode = 0
        
        # BeamLineElement class initialization:
        BeamLineElement.__init__(self, _Name, _rStrt, _vStrt, _drStrt, _dvStrt)

        if not isinstance(_Length, float):
            raise badBeamLineElement("DefocusQuadrupole:",\
                                     " bad specification for length!")
        if not isinstance(_Strength, float) and \
           not isinstance(_kDQ, float):
            raise badBeamLineElement("FocusQuadrupole: bad specification", \
                                     " for quadrupole strength!")

        self.setLength(_Length)
        if isinstance(_Strength, float):
            self.setStrength(_Strength)
            self.setkDQ(self.calckDQ())
        if isinstance(_kDQ, float):
            self.setkDQ(_kDQ)
            self.setStrength(self.calcStrength())
                
        if self.getDebug():
            print("     ----> New DefocusQuadrupole instance: \n", self)
            print(" <---- Done.")

    def __repr__(self):
        return "DefocusQuadrupole()"

    def __str__(self):
        print(" DefocusQuadrupole:")
        print(" -------------------")
        print("     ---->     Debug flag:", DefocusQuadrupole.getDebug())
        print("     ---->     Length (m):", self.getLength())
        print("     ----> Strength (T/m):", self.getStrength())
        print("     ---->       kDQ (/m):", self.getkDQ())
        with np.printoptions(linewidth=500,precision=7,suppress=True):
            print("     ----> Transfer matrix: \n", self.getTransferMatrix())
        BeamLineElement.__str__(self)
        return " <---- DefocusQuadrupole parameter dump complete."

    def SummaryStr(self):
        Str  = "DefocusQuadrupole: " + BeamLineElement.SummaryStr(self) + \
            "; Length = " + str(self.getLength()) + \
            "; Strength = " + str(self.getStrength()) + \
            "; kDQ = " + str(self.getkDQ())
        return Str

    
# -------- "Set methods"
# Methods believed to be self-documenting(!)
    @classmethod
    def setDebug(cls, Debug):
        cls.__Debug = Debug
        
    def setAll2None(self):
        self._Length   = None
        self._Strength = None
        self._kDQ      = None
        self._TrnsMtrx = None
        self._DQmode   = None
        
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

    def setkDQ(self, _kDQ):
        if not isinstance(_kDQ, float):
            raise badParameter( \
                    "BeamLineElement.DefocusQuadrupole.setkDQ:", \
                                " bad quadrupole k constant:", _kDQ)
        self._kDQ = _kDQ

    def setTransferMatrix(self, _R):
        iRefPrtcl = Prtcl.ReferenceParticle.getinstance()
        if not isinstance(iRefPrtcl, Prtcl.ReferenceParticle):
            raise ReferenceParticleNotSpecified()

        iPrev = len(iRefPrtcl.getPrOut()) - 1

        p0        = mth.sqrt(np.dot(iRefPrtcl.getPrOut()[iPrev][:3], \
                                    iRefPrtcl.getPrOut()[iPrev][:3]))
        E0        = iRefPrtcl.getPrOut()[iPrev][3]
        b0        = p0/E0
        b02       = b0**2
        g02       = 1./(1.-b02)
        
        if self.getDebug():
            print(" DefocusQuadrupole(BeamLineElement).setTransferMatrix:")
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print("     ----> Reference particle 4-mmtm:", \
                      iRefPrtcl.getPrOut()[iPrev])
            print("         ----> p0, E0:", p0, E0)
            print("     <---- b0, b02, g02:", b0, b02, g02)

        if self.getDebug():
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print("     ----> Trace space:", _R)

        D   = 1.
        Scl = 1.
        if self.getDQmode() == 1:
            D = mth.sqrt(1. + 2.*_R[5]/b0 + _R[5]**2)
        else:
            E   = E0 + _R[5]*p0
            p   = mth.sqrt(E**2 - protonMASS**2)
            Scl = p0 / p
        
        if self.getDebug():
            print("     ----> D:", D)
            print("     ----> E, p, Scl:", E, p, Scl)

        k = self.getkDQ() * Scl
        l = self.getLength()

        b = mth.sqrt(k/D)
        a = l * b
        b = b * D

        if self.getDebug():
            print("     ----> Length, Strength, kDQ:", \
                  self.getLength(), self.getStrength(), self.getkDQ())
            print("     ----> omegaPrime*L, omegaPrime*D:", a, b)

        TrnsMtrx = np.array([                                               \
            [  np.cosh(a), np.sinh(a)/b,           0.,          0., 0., 0.],\
            [b*np.sinh(a),   np.cosh(a),           0.,          0., 0., 0.],\
            [          0.,           0.,    np.cos(a), np.sin(a)/b, 0., 0.],\
            [          0.,           0., -b*np.sin(a),   np.cos(a), 0., 0.],\
            [          0.,           0.,           0.,  0.,  1., l/b02/g02],\
            [          0.,           0.,           0.,  0.,  0.,        1.]\
        ])

        if self.getDebug():
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print(TrnsMtrx)

        self._TrnsMtrx = TrnsMtrx

        
# -------- "Get methods"
# Methods believed to be self-documenting(!)
    @classmethod
    def getDebug(cls):
        return cls.__Debug
    
    def getDQmode(self):
        return self._DQmode
    
    def getLength(self):
        return self._Length

    def getStrength(self):
        return self._Strength

    def getkDQ(self):
        return self._kDQ

    
# -------- Utilities:
    def calckDQ(self):
        iRefPrtcl = Prtcl.ReferenceParticle.getinstance()
        if not isinstance(iRefPrtcl, Prtcl.ReferenceParticle):
            raise ReferenceParticleNotSpecified()

        iPrev = len(iRefPrtcl.getPrOut()) - 1

        p0        = mth.sqrt(np.dot(iRefPrtcl.getPrOut()[iPrev][:3], \
                                    iRefPrtcl.getPrOut()[iPrev][:3]))
        
        if self.getDebug():
            print(" DefocusQuadrupole(BeamLineElement).calckDQ:")
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print("     ----> Reference particle 4-mmtm:", \
                      iRefPrtcl.getPrOut()[iPrev])
            print("         ----> p0:", p0)

        Brho = (1./(speed_of_light*1.E-9))*p0/1000.
        kDQ  = self.getStrength() / Brho

        if self.getDebug():
            print("     <---- kDQ:", kDQ)
            print(" <---- Done.")

        return kDQ

    def calcStrength(self):
        iRefPrtcl = Prtcl.ReferenceParticle.getinstance()
        if not isinstance(iRefPrtcl, Prtcl.ReferenceParticle):
            raise ReferenceParticleNotSpecified()

        iPrev = len(iRefPrtcl.getPrOut()) - 1

        p0        = mth.sqrt(np.dot(iRefPrtcl.getPrOut()[iPrev][:3], \
                                    iRefPrtcl.getPrOut()[iPrev][:3]))
        
        if self.getDebug():
            print(" DefocusQuadrupole(BeamLineElement).calcStrength:")
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print("     ----> Reference particle 4-mmtm:", \
                      iRefPrtcl.getPrOut()[iPrev])
            print("         ----> p0:", p0)

        Brho = (1./(speed_of_light*1.E-9))*p0/1000.
        Strn = self.getkDQ() * Brho

        if self.getDebug():
            print("     <---- Strength:", Strn)
            print(" <---- Done.")

        return Strn

    
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
   _rStrt : numpy array; x, y, z position (in m) of start of element.
   _vStrt : numpy array; theta, phi of principal axis of element.
  _drStrt : "error", displacement of start from nominal position.
  _dvStrt : "error", deviation in theta and phy from nominal axis.

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
                 _rStrt=None, _vStrt=None, _drStrt=None, _dvStrt=None, \
                 _Angle=None, _B=None):
        if self.getDebug():
            print(' SectorDipole(BeamLineElement).__init__: ')
            print('     ----> Angle=', _Angle)
            print('     ----> Angle=', _B)

        SectorDipole.instances.append(self)

        # BeamLineElement class initialization:
        BeamLineElement.__init__(self, _Name, _rStrt, _vStrt, _drStrt, _dvStrt)

        if not isinstance(_Angle, float):
            raise badBeamLineElement( \
                "SectorDipole: bad specification for bending angle (Angle)!")

        self.setAngle(_Angle)
        self.setB(_B)
        self.setLength()

        if self.getDebug():
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
        return " <---- SectorDipole parameter dump com/plete."

    def SummaryStr(self):
        Str  = "Sector dipole    : " + BeamLineElement.SummaryStr(self) + \
            "; Angle = " + str(self.getAngle()) + \
            "; B = " + str(self.getB())
        return Str


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

    def setLength(self):
        iRefPrtcl = Prtcl.ReferenceParticle.getinstance()
        if not isinstance(iRefPrtcl, Prtcl.ReferenceParticle):
            raise ReferenceParticleNotSpecified()

        iPrev = len(iRefPrtcl.getPrOut()) - 1

        p0   = mth.sqrt(np.dot(iRefPrtcl.getPrOut()[iPrev][:3], \
                                    iRefPrtcl.getPrOut()[iPrev][:3]))

        if self.getDebug():
            print(" Dipole(BeamLineElement).setLength:")
            print("     ----> Reference particle 4-mmtm:", \
                  iRefPrtcl.getPrIn()[0])
            print("         ----> p0:", p0)
        
        Brho = (1/(speed_of_light*1.E-9))*p0/1000.
        r    = Brho / self.getB()
        l    = r * self.getAngle()

        if self.getDebug():
            print("     ----> Brho, r, l:", Brho, r, l)

        self._Length = l

    def setTransferMatrix(self, _R):
        iRefPrtcl = Prtcl.ReferenceParticle.getinstance()
        if not isinstance(iRefPrtcl, Prtcl.ReferenceParticle):
            raise ReferenceParticleNotSpecified()

        iPrev = len(iRefPrtcl.getPrOut()) - 1

        p0        = mth.sqrt(np.dot(iRefPrtcl.getPrOut()[iPrev][:3], \
                                    iRefPrtcl.getPrOut()[iPrev][:3]))
        E0        = iRefPrtcl.getPrOut()[iPrev][3]
        b0        = p0/E0
        b02       = b0**2
        g02       = 1./(1.-b02)
        
        if self.getDebug():
            print(" Dipole(BeamLineElement).setTransferMatrix:")
            print("     ----> Reference particle 4-mmtm:", \
                  iRefPrtcl.getPrIn()[0])
            print("         ----> p0, E0:", p0, E0)
            print("     <---- b02, g02:", b02, g02)
        
        E    = E0 + p0*_R[5]
        p    = mth.sqrt(E**2 - protonMASS**2)
        
        if self.getDebug():
            print("     ----> Particle energy and mmtm:", E, p)

        Brho = (1/(speed_of_light*1.E-9))*p/1000.
        r    = Brho / self.getB()
        c    = np.cos(self.getAngle())
        s    = np.sin(self.getAngle())
        l    = self.getLength()

        if self.getDebug():
            print("     ----> Brho, r, c, s, l:", Brho, r, c, s, l)

        TrnsMtrx = np.array([
            [     c,            r*s, 0., 0., 0.,                r*(1-c)/b0],
            [  -s/r,              c, 0., 0., 0.,                      s/b0],
            [    0.,             0., 1.,  l, 0.,                        0.],
            [    0.,             0., 0., 1., 0.,                        0.],
            [ -s/b0, -(r/b0)*(1.-c), 0., 0., 1., l/b02/g02 - (l-r*s)/b0**2],
            [    0.,             0., 0., 0., 0.,                        1.]
        ])

        if self.getDebug():
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print(TrnsMtrx)

        self._TrnsMtrx = TrnsMtrx

    @classmethod
    def setDebug(cls, Debug):
        cls.__Debug = Debug

# -------- "Get methods"
#..  Methods believed to be self-documenting(!)
    @classmethod
    def getDebug(cls):
        return cls.__Debug

    def getAngle(self):
        return self._Angle

    def getB(self):
        return self._B

    def getLength(self):
        return self._Length


class Octupole(BeamLineElement):
    instances = []
    __Debug = False

    def __init__(self, _Name=None, \
                 _rStrt=None, _vStrt=None, _drStrt=None, _dvStrt=None, \
                 _Length=None):
        if self.__Debug:
            print(' Octupole.__init__: ', 'creating the Octupole object: Length=', _Length)

        Octupole.instances.append(self)

        # BeamLineElement class initialization:
        BeamLineElement.__init__(self, _Name, _rStrt, _vStrt, _drStrt, _dvStrt)

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
   _rStrt : numpy array; x, y, z position (in m) of start of element.
   _vStrt : numpy array; theta, phi of principal axis of element.
  _drStrt : "error", displacement of start from nominal position.
  _dvStrt : "error", deviation in theta and phy from nominal axis.


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
                 _rStrt=None, _vStrt=None, _drStrt=None, _dvStrt=None, \
                 _Length=None, _Strength=None, _ksol=None):

        if self.getDebug():
            print(" Solenoid.__init__:", \
                  " creating the Solenoid object: Length=", _Length, " m,"\
                  " strength=", _Strength, " T")

        Solenoid.instances.append(self)

        self.setAll2None()

        # BeamLineElement class initialization:
        BeamLineElement.__init__(self, _Name, _rStrt, _vStrt, _drStrt, _dvStrt)

        if not isinstance(_Length, float):
            raise badBeamLineElement( \
                            "Solenoid: bad specification for length!")
        if not isinstance(_Strength, float) and \
           not isinstance(_ksol, float):
            raise badBeamLineElement( \
                            "Solenoid: bad specification for strength!")

        self.setLength(_Length)
        if isinstance(_Strength, float):
            self.setStrength(_Strength)
            self.setksol(self.calcksol())
        if isinstance(_ksol, float):
            self.setksol(_ksol)
            self.setStrength(self.calcStrength())
                
        if self.getDebug():
            print("     ----> New Solenoid instance: \n", self)
            print(" <---- Done.")

    def __repr__(self):
        return "Solenoid()"

    def __str__(self):
        print(" Solenoid:")
        print(" ---------")
        print("     ----> Debug flag:", Solenoid.getDebug())
        print("     ----> Length (m):", self.getLength())
        print("     ----> Strength:", self.getStrength())
        print("     ---->ksol (/m):", self.getksol())
        with np.printoptions(linewidth=500,precision=7,suppress=True):
            print("     ----> Transfer matrix: \n", self.getTransferMatrix())
        BeamLineElement.__str__(self)
        return " <---- Solenoid parameter dump complete."

    def SummaryStr(self):
        Str  = "Solenoid         : " + BeamLineElement.SummaryStr(self) + \
            "; Length = " + str(self.getLength()) + \
            "; Strength = " + str(self.getStrength()) + \
            "; ksol = " + str(self.getksol())
        return Str

    
# -------- "Set methods"
# Methods believed to be self-documenting(!)
    @classmethod
    def setDebug(cls, Debug):
        cls.__Debug = Debug
        
    def setAll2None(self):
        self._Length   = None
        self._Strength = None
        self._ksol     = None
        self._TrnsMtrx = None
        
    def setLength(self, _Length):
        if not isinstance(_Length, float):
            raise badParameter( \
                "BeamLineElement.Solenoid.setLength: bad length:", \
                                _Length)
        self._Length = _Length

    def setStrength(self, _Strength):
        if not isinstance(_Strength, float):
            raise badParameter("BeamLineElement.Solenoid.setStrength:" \
                               " bad strength value:", \
                               _Strength)
        self._Strength = _Strength

    def setksol(self, _ksol):
        if not isinstance(_ksol, float):
            raise badParameter( \
                    "BeamLineElement.Solenloid.setcsol:", \
                                " bad quadrupole k constant:", _kDQ)
        self._ksol = _ksol

    def setTransferMatrix(self, _R):
        iRefPrtcl = Prtcl.ReferenceParticle.getinstance()
        if not isinstance(iRefPrtcl, Prtcl.ReferenceParticle):
            raise ReferenceParticleNotSpecified()

        iPrev = len(iRefPrtcl.getPrOut()) - 1

        p0        = mth.sqrt(np.dot(iRefPrtcl.getPrOut()[iPrev][:3], \
                                    iRefPrtcl.getPrOut()[iPrev][:3]))
        E0        = iRefPrtcl.getPrOut()[iPrev][3]
        b02       = (p0/E0)**2
        g02       = 1./(1.-b02)
        
        if self.getDebug():
            print(" Solenoid(BeamLineElement).setTransferMatrix:")
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print("     ----> Reference particle 4-mmtm:", \
                      iRefPrtcl.getPrIn()[0])
            print("         ----> p0, E0:", p0, E0)
            print("     <---- b02, g02:", b02, g02)

        if self.getDebug():
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print("     ----> Trace space:", _R)

        E    = E0 + p0*_R[5]
        p    = mth.sqrt(E**2 - protonMASS**2)
        
        if self.getDebug():
            print("     ----> Particle energy and mmtm:", E, p)

        Brho = (1./(speed_of_light*1.E-9))*p/1000.
        l  = self.getLength()
        k  = self.getStrength() / (2.*Brho)
        
        ckl  = mth.cos(k*l)
        skl  = mth.sin(k*l)
        sckl = ckl*skl

        if self.getDebug():
            print("     ----> Length, Strength:", \
                  self.getLength(), self.getStrength())
            print("     ----> Brho, k, l:", Brho, k, l)

        TrnsMtrx = np.array([                                      \
            [   ckl**2,    sckl/k,      sckl, (skl**2)/k, 0., 0.], \
            [  -k*sckl,    ckl**2, -k*skl**2,       sckl, 0., 0.], \
            [    -sckl, -skl**2/k,    ckl**2,     sckl/k, 0., 0.], \
            [ k*skl**2,     -sckl,   -k*sckl,     ckl**2, 0., 0.], \
            [       0.,        0.,        0.,  0.,  1., l/b02/g02],\
            [       0.,        0.,        0.,  0.,  0.,        1.] \
                             ])

        if self.getDebug():
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print(TrnsMtrx)

        self._TrnsMtrx = TrnsMtrx

        
# -------- Get methods:
#..   Methods believed to be self-documenting(!)
    @classmethod
    def getDebug(cls):
        return cls.__Debug
    
    def getLength(self):
        return self._Length

    def getStrength(self):
        return self._Strength
    
    def getksol(self):
        return self._ksol


# -------- Utilities:
    def calcksol(self):
        iRefPrtcl = Prtcl.ReferenceParticle.getinstance()
        if not isinstance(iRefPrtcl, Prtcl.ReferenceParticle):
            raise ReferenceParticleNotSpecified()

        iPrev = len(iRefPrtcl.getPrOut()) - 1

        p0        = mth.sqrt(np.dot(iRefPrtcl.getPrOut()[iPrev][:3], \
                                    iRefPrtcl.getPrOut()[iPrev][:3]))
        
        if self.getDebug():
            print(" Solenoid(BeamLineElement).calckDQ:")
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print("     ----> Reference particle 4-mmtm:", \
                      iRefPrtcl.getPrOut()[iPrev])
            print("         ----> p0:", p0)

        Brho = (1./(speed_of_light*1.E-9))*p0/1000.
        ksol  = self.getStrength() / Brho

        if self.getDebug():
            print("     <---- ksol:", ksol)
            print(" <---- Done.")

        return ksol

    def calcStrength(self):
        iRefPrtcl = Prtcl.ReferenceParticle.getinstance()
        if not isinstance(iRefPrtcl, Prtcl.ReferenceParticle):
            raise ReferenceParticleNotSpecified()

        iPrev = len(iRefPrtcl.getPrOut()) - 1

        p0        = mth.sqrt(np.dot(iRefPrtcl.getPrOut()[iPrev][:3], \
                                    iRefPrtcl.getPrOut()[iPrev][:3]))
        
        if self.getDebug():
            print(" Solenoid(BeamLineElement).calcStrength:")
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print("     ----> Reference particle 4-mmtm:", \
                      iRefPrtcl.getPrOut()[iPrev])
            print("         ----> p0:", p0)

        Brho = (1./(speed_of_light*1.E-9))*p0/1000.
        Strn = self.getksol() * Brho

        if self.getDebug():
            print("     <---- Strength:", Strn)
            print(" <---- Done.")

        return Strn

    
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
   _rStrt : numpy array; x, y, z position (in m) of start of element.
   _vStrt : numpy array; theta, phi of principal axis of element.
  _drStrt : "error", displacement of start from nominal position.
  _dvStrt : "error", deviation in theta and phy from nominal axis.


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
    __Debug = False

    def __init__(self, _Name=None, \
                 _rStrt=None, _vStrt=None, _drStrt=None, _dvStrt=None, \
                 _Bz=None, _VA=None, _RA=None, _Rp=None, _Length=None, \
                 _Strength=None):
        
        if self.getDebug():
            print(" GaborLens.__init__:", \
                  " creating the GaborLens object:")
            print("     ---->       Bz:",      _Bz, " T")
            print("     ---->       VA:",       _VA, " V")
            print("     ---->       RA:",       _RA, " m")
            print("     ---->       RP:",       _Rp, " m")
            print("     ---->   Length:",   _Length, " m")
            print("     ----> Strength:", _Strength, " m^{-2}")

        GaborLens.instances.append(self)

        OK = self.setAll2None()
        
        # BeamLineElement class initialization:
        BeamLineElement.__init__(self, \
                                 _Name, _rStrt, _vStrt, _drStrt, _dvStrt)

        if not isinstance(_Length, float):
            raise badBeamLineElement( \
                            "GaborLens: bad specification for length!")
        self.setLength(_Length)

        if _Strength == None:
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

            self.setBz(_Bz)
            self.setVA(_VA)
            self.setRA(_RA)
            self.setRp(_Rp)
            
        else:
            if not isinstance(_Strength, float):
                raise badBeamLineElement( \
                            "GaborLens: bad specification for Strength!")
            self.setStrength(_Strength)
            
        self.setElectronDensity()

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
        Str  = "GaborLens        : " + BeamLineElement.SummaryStr(self) + \
            "; Length = " + str(self.getLength()) + \
            "; Electron density = " + str(self.getElectronDensity())
        return Str

    
# -------- "Set methods"
# Methods believed to be self-documenting(!)
    def setAll2None(self):
        self._Bz       = None
        self._VA       = None
        self._RA       = None
        self._Rp       = None
        self._Length   = None
        self._Strength = None
        self._TrnsMtrx = None
        
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

    def setStrength(self, _Strength):
        if not isinstance(_Strength, float):
            raise badParameter( \
                "BeamLineElement.GaborLens.setLength: bad strength:", \
                                _Strength)
        self._Strength = _Strength

    def setElectronDensity(self):
        if isinstance(self.getStrength(), float):
            iRefPrtcl = Prtcl.ReferenceParticle.getinstance()
            if not isinstance(iRefPrtcl, Prtcl.ReferenceParticle):
                raise ReferenceParticleNotSpecified()

            iPrev = len(iRefPrtcl.getPrOut()) - 1
            p0    = mth.sqrt(np.dot(iRefPrtcl.getPrOut()[iPrev][:3], \
                                    iRefPrtcl.getPrOut()[iPrev][:3]))
            E0    = iRefPrtcl.getPrOut()[iPrev][3]
            b02   = (p0/E0)**2
            g02   = 1./(1.-b02)
            g0    = mth.sqrt(g02)
            
            Brho = (1./(speed_of_light*1.E-9))*p0/1000.
            B0 = self.getStrength() * 2.*Brho
            ne = epsilon0SI * B0**2 / (2.*protonMASSSI*g0)

            ne_trans = ne
            ne_longi = ne
        else:
            if self.getBz() == None or              \
               self.getVA() == None or              \
               self.getRA() == None or              \
               self.getRp() == None:
                raise badParameter( \
                        "BeamLineElement.GaborLens.setElectronDensity:" \
                        " no parameters!")
            
            ne_trans = (epsilon0SI * self.getBz()**2) / (2. * electronMASSSI)
            ne_longi = 4. * epsilon0SI * self.getVA() / \
                (electronCHARGESI * self.getRp()**2 * \
                 (1. + 2.*mth.log(self.getRA()/self.getRp())) \
                                                 )
        if self.getDebug():
            print(" GaborLens(BeamLineElement).setElectronDensity:")
            print("     ----> ne_trans:", ne_trans)
            print("     ----> ne_longi:", ne_longi)

        self._ElectronDensity = min(ne_trans, ne_longi)
        
        if self.getDebug():
            print(" <---- Electron density:", self.getElectronDensity())
            
    def setTransferMatrix(self, _R):
        iRefPrtcl = Prtcl.ReferenceParticle.getinstance()
        if not isinstance(iRefPrtcl, Prtcl.ReferenceParticle):
            raise ReferenceParticleNotSpecified()

        iPrev = len(iRefPrtcl.getPrOut()) - 1

        p0  = mth.sqrt(np.dot(iRefPrtcl.getPrOut()[iPrev][:3], \
                              iRefPrtcl.getPrOut()[iPrev][:3]))
        E0  = iRefPrtcl.getPrOut()[iPrev][3]
        b02 = (p0/E0)**2
        g02 = 1./(1.-b02)
        g0  = mth.sqrt(g02)
        
        if self.getDebug():
            print(" GaborLens(BeamLineElement).setTransferMatrix:")
            print("     ----> Reference particle 4-mmtm:", \
                  iRefPrtcl.getPrIn()[0])
            b0 = mth.sqrt(b02)
            print("         ----> p0, E0:", p0, E0)
            print("     <---- b0, g0:", b0, g0)
            
        if self.getDebug():
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print("     ----> Trace space:", _R)

        E = E0 + p0*_R[5]
        p = mth.sqrt(E**2 - protonMASS**2)
        g = E / protonMASS  
        
        if self.getDebug():
            print("     ----> Particle energy and mmtm:", E, p)

        l      = self.getLength()
        ne     = self.getElectronDensity()

        if self.getDebug():
            print("     ----> alpha, electricCHARGE, epsilon0:", \
                  alpha, electricCHARGE, epsilon0)
            print("     ----> Joule2MeV:", Joule2MeV)
            print("     ----> m2InvMeV:", m2InvMeV)

        k      = (electricCHARGE**2 * protonMASS * g) / \
                 (2.*epsilon0 * p**2) * \
                 ne /m2InvMeV
        w      = mth.sqrt(k)
        if self.getDebug():
            print("     ----> k, w:", k, w)
        
        cwl  = mth.cos(w*l)
        swl  = mth.sin(w*l)

        TrnsMtrx = np.array([                               \
            [    cwl, swl/w,     0.,    0.,        0., 0.], \
            [ -w*swl,   cwl,     0.,    0.,        0., 0.], \
            [     0.,    0.,    cwl, swl/w,        0., 0.], \
            [     0.,    0., -w*swl,   cwl,        0., 0.], \
            [     0.,    0.,     0.,    0.,  1., l/b02/g02],\
            [     0.,    0.,     0.,    0.,  0.,        1.] \
                             ])
        
        if self.getDebug():
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print(TrnsMtrx)

        self._TrnsMtrx = TrnsMtrx

        
# -------- Get methods:
#..   Methods believed to be self-documenting(!)
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

    def getStrength(self):
        return self._Strength

    def getElectronDensity(self):
        return self._ElectronDensity
    

"""
Derived class CylindricalRFCavity:
====================

  CylindricalRFCavity class derived from BeamLineElement to contain
  paramters for a cylindrical RF cavity operated in the TM(010) mode.


  Class attributes:
  -----------------
    instances : List of instances of CylindricalRFCavity(BeamLineElement) class
  __Debug     : Debug flag


  Parent class attributes:
  ------------------------
   _rStrt : numpy array; x, y, z position (in m) of start of element.
   _vStrt : numpy array; theta, phi of principal axis of element.
  _drStrt : "error", displacement of start from nominal position.
  _dvStrt : "error", deviation in theta and phy from nominal axis.
  _TrnsMtrx : Transfer matrix.


  Instance attributes to define drift:
  ------------------------------------
  _       : 
  
    
  Methods:
  --------
  Built-in methods __init__, __repr__ and __str__.
      __init__ : Creates instance of beam-line element class.
      __repr__: One liner with call.
      __str__ : Dump of constants

  Set methods:
 setTransferMatrix : "Calculate" and set transfer matrix.

  Get methods:


"""
class CylindricalRFCavity(BeamLineElement):
    instances = []
    __Debug = False

    def __init__(self, _Name=None, \
                 _rStrt=None, _vStrt=None, _drStrt=None, _dvStrt=None, \
                 _Gradient=None, _Frequency=None, _Phase=None):
        if self.__Debug:
            print(" CylindricalRFCavity.__init__: ", \
                  "creating the CylindricalRFCavity object:")
            print("     ----> Gradient (MV/m):", _Gradient)
            print("     ----> Frequency (MHz):", _Frequency)
            print("     ----> Phase     (rad):", _Phase)

        CylindricalRFCavity.instances.append(self)

        OK = self.setAll2None()

        # BeamLineElement class initialization:
        BeamLineElement.__init__(self, \
                                 _Name, _rStrt, _vStrt, _drStrt, _dvStrt)


        if not isinstance(_Gradient, float) or \
           not isinstance(_Frequency, float) or \
           not isinstance(_Phase, float):
            raise badBeamLineElement( \
                                      "CylindricalRFCavity:" + \
                                      " bad specification:"  + \
                                      " gradient, frequency, phase:" + \
                                      _Gradient, _Frequency, _Phase)


        self.setGradient(_Gradient)
        self.setFrequency(_Frequency)
        self.setPhase(_Phase)

        _AngularFrequency  = self.getFrequency()*2.*mth.pi * 10.**6
        self.setAngularFrequency(_AngularFrequency)
        _WaveNumber        = self.getAngularFrequency() / speed_of_light
        self.setWaveNumber(_WaveNumber)
        
        iRefPrtcl = Prtcl.ReferenceParticle.getinstance()
        if not isinstance(iRefPrtcl, Prtcl.ReferenceParticle):
            raise ReferenceParticleNotSpecified()
        iPrev = len(iRefPrtcl.getPrOut()) - 1
        b0        = iRefPrtcl.getb0(iPrev)
        g0b0      = iRefPrtcl.getg0b0(iPrev)
        
        _Length   = mth.pi*b0*speed_of_light / \
            self.getAngularFrequency()
        self.setLength(_Length)

        _Radius   = sp.special.jn_zeros(0, 1)[0]/self.getWaveNumber()
        self.setRadius(_Radius)

        """
          Eqn 3.141 in Wolsli seems to have an error, expression for
          transit time factor below rederived 16Feb24, need to check
          with Andy.
        """
        _TransitTimeFactor = (2.*b0)                                 / \
                             (self.getWaveNumber()*self.getLength()) * \
                  mth.sin(self.getWaveNumber()*self.getLength()/2./b0)
        self.setTransitTimeFactor(_TransitTimeFactor)
        _V0 = self.getLength()*self.getGradient()*self.getTransitTimeFactor()
        self.setV0(_V0)

        _alpha = self.getV0()/iRefPrtcl.getMomentumIn(iPrev)/1000.
        self.setalpha(_alpha)

        _wperp = self.getWaveNumber()*mth.sqrt( \
                        self.getalpha()*mth.cos(self.getPhase())/2./mth.pi)
        self.setwperp(_wperp)
        _cperp = mth.cos(self.getwperp()*self.getLength())
        self.setcperp(_cperp)
        _sperp = mth.sin(self.getwperp()*self.getLength()) / self.getwperp()
        self.setsperp(_sperp)
        
        _wprll = self.getWaveNumber()*mth.sqrt( \
                        self.getalpha()*mth.cos(self.getPhase())/mth.pi) / \
                        g0b0
        self.setwprll(_wprll)
        _cprll = mth.cos(self.getwprll()*self.getLength())
        self.setcprll(_cprll)
        _sprll = mth.sin(self.getwprll()*self.getLength()) / self.getwprll()
        self.setsprll(_sprll)
        
        self.setTransferMatrix()
        self.setmrf()

        if self.__Debug:
            print("     ----> New CylindricalRFCavity instance: \n", self)

    def __repr__(self):
        return "CylindricalRFCavity()"

    def __str__(self):
        print(" CylindricalRFCavity:")
        print(" --------------------")
        print("     ---->        Debug flag:", CylindricalRFCavity.getDebug())
        print("     ---->   Gradient (MV/m):", self.getGradient())
        print("     ---->   Frequency (MHz):", self.getFrequency())
        print("     ---->       Phase (rad):", self.getPhase())
        print("     ----> Derived quantities:")
        print("         ---->  Angular frequency (rad/s):", \
              self.getAngularFrequency())
        print("         ---->           Wave number (/m):", \
              self.getWaveNumber())
        print("         ---->                 Length (m):", \
              self.getLength())
        print("         ---->                 Radius (m):", \
              self.getRadius())
        print("         ---->          TransitTimeFactor:", \
              self.getTransitTimeFactor())
        print("         ---->                    V0 (MV):", \
              self.getV0())
        print("         ---->                      alpha:", \
              self.getalpha())
        print("         ---->                      wperp:", \
              self.getwperp())
        print("         ---->                      cperp:", \
              self.getcperp())
        print("         ---->                      sperp:", \
              self.getsperp())
        print("         ---->                      wprll:", \
              self.getwprll())
        print("         ---->                      cprll:", \
              self.getcprll())
        print("         ---->                      sprll:", \
              self.getsprll())
        print("     <---- End derived quantities:")
        with np.printoptions(linewidth=500,precision=7,suppress=True):
            print("     ----> Transfer matrix: \n", self.getTransferMatrix())
        with np.printoptions(linewidth=500,precision=7,suppress=True):
            print("     ----> m_rf: \n", self.getmrf())
        BeamLineElement.__str__(self)
        return " <---- CylindricalRFCavity parameter dump complete."

    def SummaryStr(self):
        Str  = "CylindricalCavity: " + BeamLineElement.SummaryStr(self) + \
            "; Gradient = " + str(self.getGradient())   + \
            "; Frequency = " + str(self.getFrequency()) + \
            "; Phase = " + str(self.getPhase())
        return Str


# -------- "Set methods"
# Methods believed to be self-documenting(!)
    @classmethod
    def setDebug(cls, _Debug):
        if not isinstance(_Debug, bool):
            raise badParameter( \
                    "BeamLineElement.CylindricalRFCavity.setDebug:" + \
                                " bad flag:", _Debug)
        cls.__Debug = _Debug
        
    def setAll2None(self):
        self._Gradient          = None
        self._Frequency         = None
        self._Phase             = None
        self._TransitTimeFactor = None
        self._V0                = None
        self._alpha             = None
        self._wperp             = None
        self._cperp             = None
        self._sperp             = None
        self._wprll             = None
        self._cprll             = None
        self._sprll             = None

        self._TrnsMtrx  = None

    def setGradient(self, _Gradient):
        if not isinstance(_Gradient, float):
            raise badParameter( \
                    "BeamLineElement.CylindricalRFCavity.setVoltage:" + \
                    " bad gradient:", _Gradient)
        self._Gradient = _Gradient

    def setFrequency(self, _Frequency):
        if not isinstance(_Frequency, float):
            raise badParameter( \
                    "BeamLineElement.CylindricalRFCavity.setFrequency:" + \
                                " bad frequency:", _Frequency)
        self._Frequency = _Frequency

    def setAngularFrequency(self, _AngularFrequency):
        if not isinstance(_AngularFrequency, float):
            raise badParameter( \
             "BeamLineElement.CylindricalRFCavity.setAngularFrequency:" + \
                      " bad angular frequency:", _AngularFrequency)
        self._AngularFrequency = _AngularFrequency

    def setPhase(self, _Phase):
        if not isinstance(_Phase, float):
            raise badParameter( \
                    "BeamLineElement.CylindricalRFCavity.setPhase:" + \
                                " bad phase:", _Phase)
        self._Phase = _Phase

    def setWaveNumber(self, _WaveNumber):
        if not isinstance(_WaveNumber, float):
            raise badParameter( \
                    "BeamLineElement.CylindricalRFCavity.setPhase:" + \
                                " bad phase:", _WaveNumber)
        self._WaveNumber = _WaveNumber

    def setLength(self, _Length):
        if not isinstance(_Length, float):
            raise badParameter( \
                    "BeamLineElement.CylindricalRFCavity.setPhase:" + \
                                " bad phase:", _Length)
        self._Length = _Length        

    def setRadius(self, _Radius):
        if not isinstance(_Radius, float):
            raise badParameter( \
                    "BeamLineElement.CylindricalRFCavity.setPhase:" + \
                                " bad phase:", _Radius)
        self._Radius = _Radius        

    def setTransitTimeFactor(self, _TransitTimeFactor):
        if not isinstance(_TransitTimeFactor, float):
            raise badParameter( \
                    "BeamLineElement.CylindricalRFCavity.setPhase:" + \
                                " bad phase:", _TransitTimeFactor)
        self._TransitTimeFactor = _TransitTimeFactor        
        
    def setV0(self, _V0):
        if not isinstance(_V0, float):
            raise badParameter( \
                    "BeamLineElement.CylindricalRFCavity.setPhase:" + \
                                " bad phase:", _V0)
        self._V0 = _V0        
        
    def setalpha(self, _alpha):
        if not isinstance(_alpha, float):
            raise badParameter( \
                    "BeamLineElement.CylindricalRFCavity.setPhase:" + \
                                " bad phase:", _alpha)
        self._alpha = _alpha        
        
    def setwperp(self, _wperp):
        if not isinstance(_wperp, float):
            raise badParameter( \
                    "BeamLineElement.CylindricalRFCavity.setPhase:" + \
                                " bad phase:", _wperp)
        self._wperp = _wperp        
        
    def setcperp(self, _cperp):
        if not isinstance(_cperp, float):
            raise badParameter( \
                    "BeamLineElement.CylindricalRFCavity.setPhase:" + \
                                " bad phase:", _cperp)
        self._cperp = _cperp        
        
    def setsperp(self, _sperp):
        if not isinstance(_sperp, float):
            raise badParameter( \
                    "BeamLineElement.CylindricalRFCavity.setPhase:" + \
                                " bad phase:", _sperp)
        self._sperp = _sperp        
        
    def setwprll(self, _wprll):
        if not isinstance(_wprll, float):
            raise badParameter( \
                    "BeamLineElement.CylindricalRFCavity.setPhase:" + \
                                " bad phase:", _wprll)
        self._wprll = _wprll        
        
    def setcprll(self, _cprll):
        if not isinstance(_cprll, float):
            raise badParameter( \
                    "BeamLineElement.CylindricalRFCavity.setPhase:" + \
                                " bad phase:", _cprll)
        self._cprll = _cprll        
        
    def setsprll(self, _sprll):
        if not isinstance(_sprll, float):
            raise badParameter( \
                    "BeamLineElement.CylindricalRFCavity.setPhase:" + \
                                " bad phase:", _sprll)
        self._sprll = _sprll        
        
        
    def setmrf(self):
        iRefPrtcl = Prtcl.ReferenceParticle.getinstance()
        if not isinstance(iRefPrtcl, Prtcl.ReferenceParticle):
            raise ReferenceParticleNotSpecified()
        iPrev  = len(iRefPrtcl.getPrOut()) - 1
        g02b02 = iRefPrtcl.getg0b0(iPrev)**2

        if self.getDebug():
            print(" CylindricalRFCavity(BeamLineElement).setmrf:")
            print("     ----> Reference particle g02b02:", g02b02)
        
        _mrf   = np.array([0., 0., 0., 0., \
        (1.-self.getcprll())*mth.tan(self.getPhase())/self.getWaveNumber(), \
        g02b02*self.getwprll()**2*self.getsprll()*                          \
                        mth.tan(self.getPhase())/self.getWaveNumber()])
            
        if self.getDebug():
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print("     ----> mrf:", _mrf)

        self._mrf = _mrf

    def setTransferMatrix(self):
        iRefPrtcl = Prtcl.ReferenceParticle.getinstance()
        if not isinstance(iRefPrtcl, Prtcl.ReferenceParticle):
            raise ReferenceParticleNotSpecified()
        iPrev  = len(iRefPrtcl.getPrOut()) - 1
        g02b02 = iRefPrtcl.getg0b0(iPrev)**2

        if self.getDebug():
            print(" CylindricalRFCavity(BeamLineElement).setTransferMatrix:")
            print("     ----> Reference particle g02b02:", g02b02)
        
        TrnsMtrx = np.array([
            [                    self.getcperp(), self.getsperp(), \
                                                         0., 0., 0., 0.], \
            [-self.getwperp()**2*self.getsperp(), self.getcperp(), \
                                                         0., 0., 0., 0.], \
            [0., 0.,                     self.getcperp(), self.getsperp(), \
                                                                 0., 0.], \
            [0., 0., -self.getwperp()**2*self.getsperp(), self.getcperp(), \
                                                                 0., 0.], \
            [0., 0., 0., 0., \
                 self.getcprll(),                 self.getsprll()/g02b02], \
            [0., 0., 0., 0., \
                 -g02b02*self.getwprll()**2*self.getsprll(), \
                                                         self.getcprll()] \
        ])

        if self.getDebug():
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print(TrnsMtrx)

        self._TrnsMtrx = TrnsMtrx

# -------- "Get methods"
# Methods believed to be self-documenting(!)
    @classmethod
    def getDebug(cls):
        return cls.__Debug
    
    def getGradient(self):
        return self._Gradient

    def getFrequency(self):
        return self._Frequency

    def getAngularFrequency(self):
        return self._AngularFrequency

    def getPhase(self):
        return self._Phase

    def getWaveNumber(self):
        return self._WaveNumber

    def getLength(self):
        return self._Length

    def getRadius(self):
        return self._Radius

    def getTransitTimeFactor(self):
        return self._TransitTimeFactor

    def getV0(self):
        return self._V0

    def getalpha(self):
        return self._alpha

    def getwperp(self):
        return self._wperp

    def getcperp(self):
        return self._cperp

    def getsperp(self):
        return self._sperp

    def getwprll(self):
        return self._wprll

    def getcprll(self):
        return self._cprll

    def getsprll(self):
        return self._sprll

    def getmrf(self):
        return self._mrf

    
#--------  Utilities:
    def Transport(self, _R=None):
        iRefPrtcl = Prtcl.ReferenceParticle.getinstance()
        if not isinstance(iRefPrtcl, Prtcl.ReferenceParticle):
            raise ReferenceParticleNotSpecified()
        iPrev  = len(iRefPrtcl.getPrOut()) - 1
        g02b02 = iRefPrtcl.getg0b0(iPrev)**2
        
        if not isinstance(_R, np.ndarray) or np.size(_R) != 6:
            raise badParameter( \
            " CylindricalRFCavity(BeamLineElement).Transport:" + \
                                "bad input vector:", \
                                _R)

        if self.getDebug():
            print(" BeamLineElement.Transport:", \
                  Facility.getInstance().getName(), \
                  Facility.getInstance().getVCMVr())
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print("     ----> _R:", _R)
            print("     ----> Outside:", self.OutsideBeamPipe(_R))
            
        if self.OutsideBeamPipe(_R):
            _Rprime = None
        else:
            _Rprime = self.getTransferMatrix().dot(_R) + self.getmrf()

        if self.getDebug():
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print(" <---- Rprime:", _Rprime)

        if not isinstance(_Rprime, np.ndarray):
            pass

        return _Rprime

    
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
   _rStrt : numpy array; x, y, z position (in m) of start of element.
   _vStrt : numpy array; theta, phi of principal axis of element.
  _drStrt : "error", displacement of start from nominal position.
  _dvStrt : "error", deviation in theta and phy from nominal axis.


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

    ModeList   = [0, 1, 2]
    ModeText   = ["Parameterised laser driven", "Gaussian", "Flat"]
    ParamList  = [ [float, float, float, float, float, int], \
                   [float, float, float, float, float],      \
                   [float, float, float, float, float] ]

    Lsrdrvng_E = None
    LsrDrvnIni = False
    
    def __init__(self, _Name=None, \
                 _rStrt=None, _vStrt=None, _drStrt=None, _dvStrt=None, \
                 _Mode=None, _Param=[]):
        if self.__Debug:
            print(' Source.__init__: ', \
                  'creating the Source object')
            print("     ----> Parameters:", _Param)

        Source.instances.append(self)

        self.setAll2None()
        
        #.. BeamLineElement class initialisation:
        BeamLineElement.__init__(self, _Name, _rStrt, _vStrt, _drStrt, _dvStrt)

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
                raise FailToCreateTraceSpaceAtSource()
                
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
        elif self._Mode == 2:
            X             = rnd.gauss(0., self.getParameters()[0])
            Y             = rnd.gauss(0., self.getParameters()[1])
            cosTheta, Phi = self.getFlatThetaPhi()
            KE            = rnd.uniform(self.getParameters()[3], \
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
        if self.getDebug():
            print(" Source(BeamLineElement).getTraceSpace: start.")
            print("     ----> x, y, K, cTheta, Phi:", \
                  x, y, K, cTheta, Phi)
            
        iRefPrtcl = Prtcl.ReferenceParticle.getinstance()
        p0        = iRefPrtcl.getMomentumIn(0)
        E0        = mth.sqrt( protonMASS**2 + p0**2)
        b0        = p0/E0
        if self.getDebug():
            print("     ----> p0, E0, b0, ( K0 ):", p0, E0, b0, \
                  "(", E0-protonMASS, ")")

        E = protonMASS+K
        p = mth.sqrt(E**2 - protonMASS**2)
        if self.getDebug():
            print("     ----> K, E, p:", K, E, p)
        
        sTheta = mth.sqrt(1.-cTheta**2)
        xPrime = sTheta * mth.cos(Phi) * p / p0
        yPrime = sTheta * mth.sin(Phi) * p / p0
        """
        xPrime = sTheta * mth.cos(Phi)
        yPrime = sTheta * mth.sin(Phi)
        """
        
        if self.getDebug():
            print("     ----> sTheta, xPrime, yPrime:", 
                  sTheta, xPrime, yPrime)

        delta     = (E - E0) / p0
        
        if self.getDebug():
            print("     ----> E, delta:", E, delta)

        TrcSpc = np.array([x, xPrime, y, yPrime, 0., delta])

        if self.getDebug():
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print("     ----> Trace space:", TrcSpc)

        return TrcSpc

    
"""
To do:
------
 - put z/s position of components of doublet
 - put length of the doublet

Derived class QuadDoublet:
==========================

  QuadDoublet class derived from BeamLineElement to contain paramters
  for an quad doublet.


  Class attributes:
  -----------------
    instances : List of instances of QuadDoublet class
  __Debug     : Debug flag


  Parent class instance attributes:
  ---------------------------------
  Calling arguments:
   _Name : Name
   _rStrt : numpy array; x, y, z position (in m) of start of element.
   _vStrt : numpy array; theta, phi of principal axis of element.
  _drStrt : "error", displacement of start from nominal position.
  _dvStrt : "error", deviation in theta and phy from nominal axis.

  _TrnsMtrx : Transfer matrix:


  Instance attributes to define quadrupole:
  -----------------------------------------
  _xxx  : 
  _yyy  : 

    
  Methods:
  --------
  Built-in methods __init__, __repr__ and __str__.
      __init__ : Creates instance of beam-line element class.
      __repr__: One liner with call.
      __str__ : Dump of constants

    SummaryStr: No arguments, returns one-line string summarising quad
                parameterrs.

  Set methods:
     setDebug: Set debug flag
          Input: Debug (bool) 

  Get methods:
      getDebug

  Utilities:

"""
class QuadDoublet(BeamLineElement):
    instances = []
    __Debug   = False

    def __init__(self, _Name=None, \
                 _rStrt=None, _vStrt=None, _drStrt=None, _dvStrt=None,
                 _FDorDF=None, _Q1par=None, _d=None, _Q2par=None):
        
        if self.getDebug():
            print(' QuadDoublet.__init__: ', \
                  'creating the QuadDoublet object: ')

        QuadDoublet.instances.append(self)

        self.setAll2None()

        # BeamLineElement class initialization:
        BeamLineElement.__init__(self, _Name, _rStrt, _vStrt, _drStrt, \
                                 _dvStrt)

        if _FDorDF != "FD" and _FDorDF != "DF":
            raise badBeamLineElement("QuadDoublet: bad specification", \
                                     " for FDorDF")

        if isinstance(_Q1par,list):
            if len(_Q1par) != 3:
                raise badBeamLineElement("QuadDoublet: bad specification", \
                                         " for Q1par")
        else:
            raise badBeamLineElement("QuadDoublet: bad specification", \
                                     " for Q1par")

        if not(isinstance(_d, float)):
            raise badBeamLineElement("QuadDoublet: bad specification", \
                                     " for Q1par")

        if isinstance(_Q2par,list):
            if len(_Q2par) != 3:
                raise badBeamLineElement("QuadDoublet: bad specification", \
                                         " for Q2par")
        else:
            raise badBeamLineElement("QuadDoublet: bad specification", \
                                     " for Q2par")
        
        self.setFDorDF(_FDorDF)
        self.setQ1par(_Q1par)
        self.setSeparation(_d)
        self.setQ2par(_Q2par)

        if self.getFDorDF() == "FD":
            iQ1 = FocusQuadrupole(_Name+":FQ1", \
                            _rStrt, _vStrt, _drStrt, _dvStrt, \
                self.getQ1par()[0], self.getQ1par()[1], self.getQ1par()[2])
        else:
            iQ1 = DefocusQuadrupole(_Name+":DQ1", \
                            _rStrt, _vStrt, _drStrt, _dvStrt, \
                self.getQ1par()[0], self.getQ1par()[1], self.getQ1par()[2])
        iD = Drift(_Name+":sep", \
                            _rStrt, _vStrt, _drStrt, _dvStrt, \
                            self.getSeparation())
        if self.getFDorDF() == "FD":
            iQ2 = DefocusQuadrupole(_Name+":DQ2", \
                            _rStrt, _vStrt, _drStrt, _dvStrt, \
                self.getQ2par()[0], self.getQ2par()[1], self.getQ2par()[2])
        else:
            iQ2 = FocusQuadrupole(_Name+":FQ2", \
                            _rStrt, _vStrt, _drStrt, _dvStrt, \
                self.getQ2par()[0], self.getQ2par()[1], self.getQ2par()[2])

        if self.getDebug():
            print("     ----> Dump componenets:")
            print(iQ1)
            print(iD)
            print(iQ2)

        BeamLineElement.removeInstance(iQ1)
        BeamLineElement.removeInstance(iD)
        BeamLineElement.removeInstance(iQ2)
        self.setQ1(iQ1)
        self.setD(iD)
        self.setQ2(iQ2)
                   
        if self.getDebug():
            print("     ----> New QuadDoublet instance: \n", self)
            print(" <---- Done.")

    def __repr__(self):
        return "QuadDoublet()"

    def __str__(self):
        print(" QuadDoublet:")
        print(" ------------")
        print("     ---->     Debug flag:", QuadDoublet.getDebug())
        print("     ---->         FDorDF:", self.getFDorDF())
        print("     ---->          Q1par:", self.getQ1par())
        print("     ---->     Separation:", self.getSeparation())
        print("     ---->          Q2par:", self.getQ2par())
        print("     ---->     Components:", self.getQ1().getName(), \
              self.getD().getName(), self.getQ2().getName())
        with np.printoptions(linewidth=500,precision=7,suppress=True):
            print("     ----> Transfer matrix: \n", self.getTransferMatrix())
        BeamLineElement.__str__(self)
        return " <---- QuadDoublet parameter dump complete."

    def SummaryStr(self):
        Str  = "QuadDoublet  : " + BeamLineElement.SummaryStr(self) + \
            "; FDorDF = ", self.getFDorDF() + \
            "; Q1par = ", str(self.getQ1par()) + \
            "; separation = ", str(self.getSeparation()) + \
            "; Q2par = ", str(self.getQ2par())
        return Str

    
# -------- "Set methods"
# Methods believed to be self-documenting(!)
    @classmethod
    def setDebug(cls, Debug):
        cls.__Debug = Debug
        
    def setAll2None(self):
        self._FDorDF     = None
        self._Q1par      = None
        self._Separation = None
        self._Q2par      = None
        self._TrnsMtrx   = None
        

    def setFDorDF(self, _FDorDF):
        if _FDorDF != "FD" and _FDorDF != "DF":
            raise badParameter( \
                    "BeamLineElement.QuadDoublet.setFDorDF:", \
                                " bad FDorDF:", _FDorDF)
        self._FDorDF = _FDorDF
        
    def setSeparation(self, _d):
        if not(isinstance(_d, float)):
            raise badParameter( \
                    "BeamLineElement.QuadDoublet.setSeparation:", \
                    " bad separation:", _d)
               
        self._Separation = _d
        
    def setQ1par(self, _Q1par):
        if isinstance(_Q1par,list):
            if len(_Q1par) != 3:
                raise badBeamLineElement(
                    "BeamLineElement.QuadDoublet.setQ1par:", \
                    " for Q1par")
        else:
            raise badBeamLineElement(
                "BeamLineElement.QuadDoublet.setQ1par:", \
                " for Q1par")
        
        self._Q1par = _Q1par
        
    def setQ2par(self, _Q2par):
        if isinstance(_Q2par,list):
            if len(_Q2par) != 3:
                raise badBeamLineElement(
                    "BeamLineElement.QuadDoublet.setQ2par:", \
                    " for Q2par")
        else:
            raise badBeamLineElement(
                "BeamLineElement.QuadDoublet.setQ2par:", \
                " for Q2par")
        
        self._Q2par = _Q2par

    def setQ1(self, iQ1):
        if not isinstance(iQ1, BeamLineElement):
            raise badBeamLineElement(
                "BeamLineElement.QuadDoublet.setQ1:", \
                " not a beamline element")
        self._iQ1 = iQ1
            
    def setD(self, iD):
        if not isinstance(iD, BeamLineElement):
            raise badBeamLineElement(
                "BeamLineElement.QuadDoublet.setD:", \
                " not a beamline element")
        self._iD = iD
            
    def setQ2(self, iQ2):
        if not isinstance(iQ2, BeamLineElement):
            raise badBeamLineElement(
                "BeamLineElement.QuadDoublet.setQ2:", \
                " not a beamline element")
        self._iQ2 = iQ2
            
    def setTransferMatrix(self, _R):
        
        if self.getDebug():
            print(" QuadDoublet(BeamLineElement).setTransferMatrix:")

        if self.getDebug():
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print("     ----> Trace space:", _R)

        self.getQ1().setTransferMatrix(_R)
        TrnsfrQ1 = self.getQ1().getTransferMatrix()

        self.getD().setTransferMatrix()
        TrnsfrD  = self.getD().getTransferMatrix()

        self.getQ2().setTransferMatrix(_R) 
        TrnsfrQ2 = self.getQ2().getTransferMatrix()

        if self.getDebug():
            print("     ----> Transfer matrix for Q1:")
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print(TrnsfrQ1)
            print("     ----> Transfer matrix for D:")
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print(TrnsfrD)
            print("     ----> Transfer matrix for Q2:")
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print(TrnsfrQ2)

        
        TrnsMtrx = TrnsfrD.dot(TrnsfrQ1)
        TrnsMtrx = TrnsfrQ2.dot(TrnsMtrx)

        if self.getDebug():
            print("     ----> Transfer matrix for QuadDoublet:")
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print(TrnsMtrx)

        self._TrnsMtrx = TrnsMtrx

        
# -------- "Get methods"
# Methods believed to be self-documenting(!)
    @classmethod
    def getDebug(cls):
        return cls.__Debug

    def getFDorDF(self):
        return self._FDorDF

    def getQ1par(self):
        return self._Q1par

    def getSeparation(self):
        return self._Separation

    def getQ2par(self):
        return self._Q2par

    def getQ1(self):
        return self._iQ1

    def getD(self):
        return self._iD

    def getQ2(self):
        return self._iQ2

    
# -------- Utilities:
    
    
"""
Derived class QuadTriplet:
==========================

  QuadTriplet class derived from BeamLineElement to contain paramters
  for an quad doublet.


  Class attributes:
  -----------------
    instances : List of instances of QuadTriplet class
  __Debug     : Debug flag


  Parent class instance attributes:
  ---------------------------------
  Calling arguments:
   _Name : Name
   _rStrt : numpy array; x, y, z position (in m) of start of element.
   _vStrt : numpy array; theta, phi of principal axis of element.
  _drStrt : "error", displacement of start from nominal position.
  _dvStrt : "error", deviation in theta and phy from nominal axis.

  _TrnsMtrx : Transfer matrix:


  Instance attributes to define quadrupole:
  -----------------------------------------
  _xxx  : 
  _yyy  : 

    
  Methods:
  --------
  Built-in methods __init__, __repr__ and __str__.
      __init__ : Creates instance of beam-line element class.
      __repr__: One liner with call.
      __str__ : Dump of constants

    SummaryStr: No arguments, returns one-line string summarising quad
                parameterrs.

  Set methods:
     setDebug: Set debug flag
          Input: Debug (bool) 

  Get methods:
      getDebug

  Utilities:

"""
class QuadTriplet(BeamLineElement):
    instances = []
    __Debug   = False

    def __init__(self, _Name=None, \
                 _rStrt=None, _vStrt=None, _drStrt=None, _dvStrt=None, \
                 _FDForDFD=None, _Q1par=None, _d1=None, _Q2par=None,     \
                                              _d2=None, _Q3par=None     ):
        
        if self.getDebug():
            print(' QuadTriplet.__init__: ', \
                  'creating the QuadTriplet object: ')

        QuadTriplet.instances.append(self)

        self.setAll2None()

        # BeamLineElement class initialization:
        BeamLineElement.__init__(self, _Name, _rStrt, _vStrt, _drStrt, \
                                 _dvStrt)

        if _FDForDFD != "FDF" and _FDForDFD != "DFD":
            raise badBeamLineElement("QuadTriplet: bad specification", \
                                     " for FDForDFD")

        if isinstance(_Q1par,list):
            if len(_Q1par) != 3:
                raise badBeamLineElement("QuadTriplet: bad specification", \
                                         " for Q1par")
        else:
            raise badBeamLineElement("QuadTriplet: bad specification", \
                                     " for Q1par")

        if not(isinstance(_d1, float)):
            raise badBeamLineElement("QuadTriplet: bad specification", \
                                     " for d1")

        if isinstance(_Q2par,list):
            if len(_Q2par) != 3:
                raise badBeamLineElement("QuadTriplet: bad specification", \
                                         " for Q2par")
        else:
            raise badBeamLineElement("QuadTriplet: bad specification", \
                                     " for Q2par")
        
        if not(isinstance(_d2, float)):
            raise badBeamLineElement("QuadTriplet: bad specification", \
                                     " for d2")

        if isinstance(_Q2par,list):
            if len(_Q3par) != 3:
                raise badBeamLineElement("QuadTriplet: bad specification", \
                                         " for Q3par")
        else:
            raise badBeamLineElement("QuadTriplet: bad specification", \
                                     " for Q3par")
        
        self.setFDForDFD(_FDForDFD)
        self.setQ1par(_Q1par)
        self.setSeparation1(_d1)
        self.setQ2par(_Q2par)
        self.setSeparation2(_d2)
        self.setQ3par(_Q3par)
        
        if self.getFDForDFD() == "FDF":
            iQ1 = FocusQuadrupole(_Name+":FQ1", \
                            _rStrt, _vStrt, _drStrt, _dvStrt, \
                self.getQ1par()[0], self.getQ1par()[1], self.getQ1par()[2])
        else:
            iQ1 = DefocusQuadrupole(_Name+":DQ1", \
                            _rStrt, _vStrt, _drStrt, _dvStrt, \
                self.getQ1par()[0], self.getQ1par()[1], self.getQ1par()[2])
        iD1 = Drift(_Name+":sep1", \
                            _rStrt, _vStrt, _drStrt, _dvStrt, \
                            self.getSeparation1())
        if self.getFDForDFD() == "FDF":
            iQ2 = DefocusQuadrupole(_Name+":DQ2", \
                            _rStrt, _vStrt, _drStrt, _dvStrt, \
                self.getQ2par()[0], self.getQ2par()[1], self.getQ2par()[2])
        else:
            iQ2 = FocusQuadrupole(_Name+":FQ2", \
                            _rStrt, _vStrt, _drStrt, _dvStrt, \
                self.getQ2par()[0], self.getQ2par()[1], self.getQ2par()[2])
        iD2 = Drift(_Name+":sep2", \
                            _rStrt, _vStrt, _drStrt, _dvStrt, \
                            self.getSeparation2())
        if self.getFDForDFD() == "FDF":
            iQ3 = FocusQuadrupole(_Name+":FQ3", \
                            _rStrt, _vStrt, _drStrt, _dvStrt, \
                self.getQ3par()[0], self.getQ3par()[1], self.getQ3par()[2])
        else:
            iQ3 = DefocusQuadrupole(_Name+":DQ3", \
                            _rStrt, _vStrt, _drStrt, _dvStrt, \
                self.getQ3par()[0], self.getQ3par()[1], self.getQ3par()[2])

        if self.getDebug():
            print("     ----> Dump componenets:")
            print(iQ1)
            print(iD1)
            print(iQ2)
            print(iD2)
            print(iQ3)

        BeamLineElement.removeInstance(iQ1)
        BeamLineElement.removeInstance(iD1)
        BeamLineElement.removeInstance(iQ2)
        BeamLineElement.removeInstance(iD2)
        BeamLineElement.removeInstance(iQ3)
        self.setQ1(iQ1)
        self.setD1(iD1)
        self.setQ2(iQ2)
        self.setD2(iD2)
        self.setQ3(iQ3)
                   
        if self.getDebug():
            print("     ----> New QuadTriplet instance: \n", self)
            print(" <---- Done.")

    def __repr__(self):
        return "QuadTriplet()"

    def __str__(self):
        print(" QuadTriplet:")
        print(" ----------------")
        print("     ---->     Debug flag:", QuadTriplet.getDebug())
        print("     ---->         FDorDF:", self.getFDForDFD())
        print("     ---->          Q1par:", self.getQ1par())
        print("     ---->    Separation1:", self.getSeparation1())
        print("     ---->          Q2par:", self.getQ2par())
        print("     ---->    Separation2:", self.getSeparation2())
        print("     ---->          Q3par:", self.getQ3par())
        print("     ---->     Components:", self.getQ1().getName(), \
              self.getD1().getName(), self.getQ2().getName(), \
              self.getD2().getName(), self.getQ3().getName(), \
              )
        with np.printoptions(linewidth=500,precision=7,suppress=True):
            print("     ----> Transfer matrix: \n", self.getTransferMatrix())
        BeamLineElement.__str__(self)
        return " <---- QuadTriplet parameter dump complete."

    def SummaryStr(self):
        Str  = "QuadTriplet  : " + BeamLineElement.SummaryStr(self) + \
            "; FDForDFD = ", self.getFDForDFD() + \
            "; Q1par = ", str(self.getQ1par()) + \
            "; separation1 = ", str(self.getSeparation1()) + \
            "; Q2par = ", str(self.getQ2par()) + \
            "; separation2 = ", str(self.getSeparation2()) + \
            "; Q3par = ", str(self.getQ3par())
        return Str

    
# -------- "Set methods"
# Methods believed to be self-documenting(!)
    @classmethod
    def setDebug(cls, Debug):
        cls.__Debug = Debug
        
    def setAll2None(self):
        self._FDForDFF    = None
        self._Q1par       = None
        self._Separation1 = None
        self._Q2par       = None
        self._Separation2 = None
        self._Q3par       = None
        self._TrnsMtrx    = None

    def setFDForDFD(self, _FDForDFD):
        if _FDForDFD != "FDF" and _FDForDFD != "DFD":
            raise badParameter( \
                    "BeamLineElement.QuadDoublet.setFDForDFD:", \
                                " bad FDForDFD:", _FDForDFD)
        self._FDForDFD = _FDForDFD
        
    def setQ1par(self, _Q1par):
        if isinstance(_Q1par,list):
            if len(_Q1par) != 3:
                raise badBeamLineElement(
                    "BeamLineElement.QuadTriplet.setQ1par:", \
                    " for Q1par")
        else:
            raise badBeamLineElement(
                "BeamLineElement.QuadTriplet.setQ1par:", \
                " for Q1par")
        
        self._Q1par = _Q1par
        
    def setSeparation1(self, _d1):
        if not(isinstance(_d1, float)):
            raise badParameter( \
                    "BeamLineElement.QuadDoublet.setSeparation:", \
                    " bad separation 1:", _d1)
               
        self._Separation1 = _d1
        
    def setQ2par(self, _Q2par):
        if isinstance(_Q2par,list):
            if len(_Q2par) != 3:
                raise badBeamLineElement(
                    "BeamLineElement.QuadTriplet.setQ2par:", \
                    " for Q2par")
        else:
            raise badBeamLineElement(
                "BeamLineElement.QuadTriplet.setQ2par:", \
                " for Q2par")
        
        self._Q2par = _Q2par

    def setSeparation2(self, _d2):
        if not(isinstance(_d2, float)):
            raise badParameter( \
                    "BeamLineElement.QuadDoublet.setSeparation:", \
                    " bad separation 2:", _d2)
               
        self._Separation2 = _d2
        
    def setQ3par(self, _Q3par):
        if isinstance(_Q3par,list):
            if len(_Q3par) != 3:
                raise badBeamLineElement(
                    "BeamLineElement.QuadTriplet.setQ3par:", \
                    " for Q3par")
        else:
            raise badBeamLineElement(
                "BeamLineElement.QuadTriplet.setQ3par:", \
                " for Q3par")
        
        self._Q3par = _Q3par

    def setQ1(self, iQ1):
        if not isinstance(iQ1, BeamLineElement):
            raise badBeamLineElement(
                "BeamLineElement.QuadTriplet.setQ1:", \
                " not a beamline element")
        self._iQ1 = iQ1
            
    def setD1(self, iD1):
        if not isinstance(iD1, BeamLineElement):
            raise badBeamLineElement(
                "BeamLineElement.QuadTriplet.setD1:", \
                " not a beamline element")
        self._iD1 = iD1
            
    def setQ2(self, iQ2):
        if not isinstance(iQ2, BeamLineElement):
            raise badBeamLineElement(
                "BeamLineElement.QuadTriplet.setQ2:", \
                " not a beamline element")
        self._iQ2 = iQ2
            
    def setD2(self, iD2):
        if not isinstance(iD2, BeamLineElement):
            raise badBeamLineElement(
                "BeamLineElement.QuadTriplet.setD2:", \
                " not a beamline element")
        self._iD2 = iD2
            
    def setQ3(self, iQ3):
        if not isinstance(iQ3, BeamLineElement):
            raise badBeamLineElement(
                "BeamLineElement.QuadTriplet.setQ3:", \
                " not a beamline element")
        self._iQ3 = iQ3
            
    def setTransferMatrix(self, _R):
        
        if self.getDebug():
            print(" QuadTriplet(BeamLineElement).setTransferMatrix:")

        if self.getDebug():
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print("     ----> Trace space:", _R)

        self.getQ1().setTransferMatrix(_R)
        TrnsfrQ1 = self.getQ1().getTransferMatrix()

        self.getD1().setTransferMatrix()
        TrnsfrD1 = self.getD1().getTransferMatrix()

        self.getQ2().setTransferMatrix(_R) 
        TrnsfrQ2 = self.getQ2().getTransferMatrix()

        self.getD2().setTransferMatrix()
        TrnsfrD2 = self.getD2().getTransferMatrix()

        self.getQ3().setTransferMatrix(_R) 
        TrnsfrQ3 = self.getQ3().getTransferMatrix()

        if self.getDebug():
            print("     ----> Transfer matrix for Q1:")
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print(TrnsfrQ1)
            print("     ----> Transfer matrix for D1:")
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print(TrnsfrD1)
            print("     ----> Transfer matrix for Q2:")
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print(TrnsfrQ2)
            print("     ----> Transfer matrix for D2:")
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print(TrnsfrD2)
            print("     ----> Transfer matrix for Q3:")
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print(TrnsfrQ3)

        TrnsMtrx = TrnsfrD1.dot(TrnsfrQ1)
        TrnsMtrx = TrnsfrQ2.dot(TrnsMtrx)
        TrnsMtrx = TrnsfrD2.dot(TrnsMtrx)
        TrnsMtrx = TrnsfrQ3.dot(TrnsMtrx)
                
        if self.getDebug():
            print("     ----> Transfer matrix for QuadTriplet:")
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print(TrnsMtrx)

        if self.getDebug():
            with np.printoptions(linewidth=500,precision=7,suppress=True):
                print(TrnsMtrx)

        self._TrnsMtrx = TrnsMtrx

        
# -------- "Get methods"
# Methods believed to be self-documenting(!)
    @classmethod
    def getDebug(cls):
        return cls.__Debug

    def getFDForDFD(self):
        return self._FDForDFD
        
    def getQ1par(self):
        return self._Q1par
        
    def getSeparation1(self):
        return self._Separation1
        
    def getQ2par(self):
        return self._Q2par

    def getSeparation2(self):
        return self._Separation2
        
    def getQ3par(self):
        return self._Q3par

    def getQ1(self):
        return self._iQ1
            
    def getD1(self):
        return self._iD1
            
    def getQ2(self):
        return self._iQ2
            
    def getD2(self):
        return self._iD2
            
    def getQ3(self):
        return self._iQ3
                
    
# -------- Utilities:
    
    
#--------  Exceptions:
class badBeamLineElement(Exception):
    pass

class badParameter(Exception):
    pass

class badSourceSpecification(Exception):
    pass

class secondFacility(Exception):
    pass

class badParameters(Exception):
    pass

class ReferenceParticleNotSpecified(Exception):
    pass

class FailToCreateTraceSpaceAtSource(Exception):
    pass

