#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class muonDECAY:
================

  Generates decay distributions for muon decay at rest.  Kinematic 
  distributions are for muon decay at rest.

  Citations: 
   - G4 manual

  Dependencies:
   - numpy, Simulation, math, MuonConst

  Class attributes:
  -----------------
  __muCnst: Instance of MuonConst class.
      
  Instance attributes:
  --------------------
  _Lifetimre: Time to decay (s) multiplied by the speed of light.  This is
              is for "this particular muon"
  _v_e      : Electron 4-vector (E, array(px, py, pz)); MeV
  _v_nue    : Electron-neutrino 4-vector (E, array(px, py, pz)); MeV
  _v_numu   : Muon-neutrino 4-vector (E, array(px, py, pz)); MeV
  _costheta : Cosine of angle between electron and nue in muon rest frame
  _cosphi   : Cosine of angle between electron and numu in muon rest frame

  Methods:
  --------
  Built-in methods __new__, __repr__ and __str__.
      __init__ : Creates decay instance:
                 Optional keyword argument Tmax -- cut off lifetime at Tmax
      __repr__ : One liner with call.
      __str__  : Dump of values of decay

  Get/set methods:
    getLifetime: Returns lifetime (s) of this decay instance
                 Optional keyword argument Tmax -- cut off lifetime at Tmax
    getve      : Returns 4-vector of electron (MeV)
    getvnue    : Returns 4-vector of electron neutrino (MeV)
    getvnumu   : Returns 4-vector of muon neutrino (MeV)
    getcostheta: Returns cosine of angle between electron and 
                 electron-neutrino in muon rest frame
    getcosphi  : Returns cosine of angle between electron and 
                 muon-neutrino in muon rest frame
  
  Muon-decay methods:
    GenerateLifetime: Generates lifetime of this instance.  Returns
                      lifetime (float). Units s
    decaymuon       : Generates a particular muon decay; calls each of 
                      following methods in turn.  Returns 3 4-vectors,
                      v_e, v_nue, v_numu.  v_i = [Energy, array(px, py, px)] 
                      (units MeV), and two floats, costheta, cosphi
    GenerateScldE   : Generates scaled energies of electron, nu_e, and nu_mu. 
                      Returns three floats, (f_e, f_nue, f_numu).  Units
                      m_mu/2.
    get3vectors     : Generates 3-vector momenta (MeV).  Electron direction
                      taken as positive z direction.  Returns three floar
                      array objects, p_e, p_mue, p_numu; p_i = array(px, py,
                      pz), and two floats costheta and cosphi
    ranCoor         : Applies random 3D rotation and returns 4-vectors:
                      v_e, v_nue, v_numu.  v_i = [Energy, array(px, py, px)]
                      Units MeV.

Created on Sat 09Jan21;17:18: Version history:
----------------------------------------------
 2.0: 15Jan26; Begin to port to LhARAlinearOptics framework.
 1.2: 07Apr21: Update GenerateScldE to minimise calls to random-number
               generatory.  Hope is that this version runs a little more
               quickly.
 1.1: 03Apr21: Optional (keyword) argument to limit generation to Tmax
 1.0: 09Jan21: First implementation

@author: kennethlong
"""

from copy import deepcopy 
import Simulation as Simu
import numpy as np
import math as mth

import PhysicalConstants as PC

iPC = PC.PhysicalConstants()

class muonDECAY:
    
    __Debug = False
    
#--------  "Built-in methods":
    def __init__(self, **kwargs):

        Tmax = kwargs.get('Tmax', float('inf'))

        self._Lifetime = self.GenerateLifetime(Tmax=Tmax)

        v_e, v_nue, v_numu, costheta, cosphi = self.decaymuon()

        self._v_e = v_e
        self._v_nue = v_nue
        self._v_numu = v_numu
        
        self._costheta = costheta
        self._cosphi   = cosphi

        return

    def __repr__(self):
        return "muonDECAY()"

    def __str__(self):
        return "muonDECAY: Lifetime=%g, \r\n \
                           v_e=(%g, [%g, %g, %g]), \r\n \
                         v_nue=(%g, [%g, %g, %g]), \r\n \
                        v_numu=(%g, [%g, %g, %g]),      \
               " % (self._Lifetime,                                  \
                     self._v_e[0], self._v_e[1], self._v_e[2], \
                                                    self._v_e[3], \
                     self._v_nue[0], self._v_nue[1], self._v_nue[2], \
                                                   self._v_nue[3],      \
                     self._v_numu[0], self._v_numu[1], \
                                     self._v_numu[2], self._v_numu[3])

    
#--------  "Dynamic methods"; individual lifetime, energies, and angles
    def GenerateLifetime(self, **kwargs):
        Tmax = kwargs.get('Tmax', float('inf'))
        Gmx = 1. - mth.exp( -Tmax / iPC.tauMuon() )
        ran = Simu.getRandom() * Gmx
        lt = -mth.log(1.-ran) * iPC.tauMuon()
        return lt

    def GenerateScldE(self):
#----  See P. 3, my "Notes and calcs"
        f_nue = 0.5
        f_e   = 0.
        while f_nue < (1. - f_e):
#.. fractional electron energy:
            Ge    = Simu.getRandom()
            Coefe = [0., 0., 0., 0., 0.]
            Coefe[0] =  1.
            Coefe[1] = -2.
            Coefe[2] =  0.
            Coefe[3] =  0.
            Coefe[4] =  Ge
            Rootse   = np.roots(Coefe)

            Sln = 0
            Rt  = -99
            for r in Rootse:
                if r.imag == 0.:
                    if r >= 0. and r <= 1.:
                        Sln += 1
                        Rt   = r.real

            if Sln !=1:
                Err = ' Number of solutions for f_e = ' + str(Sln)
                raise Exception(Err)
            elif Rt == -99.:
                Err = ' Number of solutions for f_e = ' + str(Sln) + \
                    " but Rt = " + str(Rt)
                raise Exception(Err)
            else:
                f_e = Rt

#.. fractional electron-neutrino energy:
            Alpha   = (1. - f_e)**2 * (1. + 2.*f_e)
            Gnue    = Simu.getRandom()
            Coefnue    = [0., 0., 0., 0.]
            Coefnue[0] =  2.
            Coefnue[1] = -3.
            Coefnue[2] =  0.
            Coefnue[3] = Gnue * (1. - Alpha) + Alpha
            Roots   = np.roots(Coefnue)

            Sln = 0
            Rt  = -99
            for r in Roots:
                if not isinstance(r, complex):
                    if r >= 0. and r <= 1.:
                        Sln += 1
                        Rt   = r

            if Sln !=1:
                Err = ' Number of solutions for f_nue = ' + str(Sln)
                raise Exception(Err)
            elif Rt == -99.:
                Err = ' Number of solutions for f_nue = ' + str(Sln) + \
                    " but Rt = " + str(Rt)
                raise Exception(Err)
            else:
                f_nue = Rt
            if (1.-f_e) > f_nue:
                print(" (1.-f_e) > f_nue:", \
                      f_e, (1.-f_e), f_nue, (f_e + f_nue))
            elif (f_e+f_nue) < 1.:
                print(" (f_e+f_nue) < 1.:", \
                      f_e, (1.-f_e), f_nue, (f_e + f_nue))
                        
            """ Start old code
            gam = 1.
            x   = 1.
            while gam > x*(1.-x):
                x   = Simu.getRandom()
                gam = Simu.getRandom()
            f_nue = x
            End old code """

        f_numu = 2. - f_e - f_nue
        
        return f_e, f_nue, f_numu
    
    def get3vectors(self, f_e, f_nue, f_numu):
#----  See P. 3, my "Notes and calcs"
#.. electron neutrino
        costheta = 1. - 2.*( 1./f_e + 1/f_nue - 1/(f_e*f_nue) )
        sintheta = mth.sqrt(1. - costheta**2)
        
#.. muon neutrino
        cosphi = -(f_e + f_nue*costheta) / f_numu
        sinphi = -f_nue*sintheta / f_numu
        diff = abs(1. - (cosphi**2 + sinphi**2))

        theta = mth.acos(costheta) * 180./mth.pi
        phi   = mth.acos(cosphi)   * 180./mth.pi

#.. Three vectors:
        p_e    = np.array([             0., 0., f_e            ])
        p_nue  = np.array([ f_nue*sintheta, 0., f_nue*costheta ])
        p_numu = np.array([  f_numu*sinphi, 0., f_numu*cosphi  ])
        
        return p_e, p_nue, p_numu, costheta, cosphi

    def ranCoor(self, p_e, p_nue, p_numu):
#.. Rotation angles
        alpha  = Simu.getRandom() * 2.*mth.pi
        calpha = mth.cos(alpha)
        salpha = mth.sin(alpha)

        cbeta = -1. + 2.*Simu.getRandom()
        sbeta = mth.sqrt(1. - cbeta**2)

        gamma = Simu.getRandom() * 2.*mth.pi
        cgamma = mth.cos(gamma)
        sgamma = mth.sin(gamma)


#.. Rotation angles
        Ra = np.array([          \
             [calpha   , -salpha,      0.      ], \
             [salpha   ,  calpha,      0.      ], \
             [0.       , 0.,      1.      ] \
                                   ])
        Rb = np.array([          \
             [cbeta    , 0.,      -sbeta     ], \
             [0.       , 1.,      0.      ], \
             [sbeta    , 0.,      cbeta      ] \
                                   ])
        Rc = np.array([          \
             [cgamma   , -sgamma,      0.      ], \
             [sgamma   ,  cgamma,      0.      ], \
             [0.       , 0.,      1.      ] \
                                   ])

        Rr = np.dot(Ra, Rb)
        Rr = np.dot(Rr, Rc)
        
#.. Do rotation:
        p_e1    = np.dot(Rr, p_e)
        p_nue1  = np.dot(Rr, p_nue)
        p_numu1 = np.dot(Rr, p_numu)

        return p_e1, p_nue1, p_numu1

    def decaymuon(self):
#.. Get scaled muon eneries:        
        f_e, f_nue, f_numu = self.GenerateScldE()
        
#.. Get scaled 3-vectors:
        s_e, s_nue, s_numu, costheta, cosphi = \
                        self.get3vectors(f_e, f_nue, f_numu)

#.. Rotate to arbitrary axis orientation:
        p_e, p_nue, p_numu = self.ranCoor(s_e, s_nue, s_numu)

#.. Scale to MeV and make 4-vectors:
        mo2    = iPC.mMuon() / 2.

        f_e    = f_e    * mo2
        p_e    = p_e    * mo2
        
        f_nue  = f_nue  * mo2
        p_nue  = p_nue  * mo2
        
        f_numu = f_numu * mo2
        p_numu = p_numu * mo2

        v_e    = np.array([f_e, p_e[0], p_e[1], p_e[2]])
        v_nue  = np.array([f_nue,  p_nue[0], p_nue[1], p_nue[2]])
        v_numu = np.array([f_numu, p_numu[0], p_numu[1], p_numu[2]])

        return v_e, v_nue, v_numu, costheta, cosphi

#--------  "Get methods" only; version, reference, and constants
#.. Methods believed to be self documenting(!)
    def getLifetime(self):
        return self._Lifetime

    def getve(self):
        return deepcopy(self._v_e)

    def getvnue(self):
        return deepcopy(self._v_nue)

    def getvnumu(self):
        return deepcopy(self._v_numu)

    def getcostheta(self):
        return deepcopy(self._costheta)

    def getcosphi(self):
        return deepcopy(self._cosphi)
    
