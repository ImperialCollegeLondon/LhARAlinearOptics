#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class pionDECAY:
================

  Generates decay distributions for pion decay at rest.  Kinematic 
  distributions are for pion decay at rest.

  Dependencies:
   - numpy, math, Simulation

  Class attributes:
  -----------------
  __xxx
      
  Instance attributes:
  --------------------
  _v_numu   : Muon-neutrino 4-vector (E, array(px, py, pz)); MeV
  _v_mu     : Muon 4-vector (E, array(px, py, pz)); MeV
  _costheta : Cosine of angle between the pion and the decay muon in the
              pion rest frame
  _phi      : Polar angle of the decay between the pion and the decay
              muon in the pion rest frame - measured with respect to
              the x axis of the nuStorm co-ordinate system
 

  Methods:
  --------
  Built-in methods __new__, __repr__ and __str__.
      __init__ : Creates decay instance
      __repr__ : One liner with call.
      __str__  : Dump of values of decay

  Get/set methods:
    getLifetime: Returns lifetime (s) of this decay instance
    get4vnumu  : Returns 4-vector of muon neutrino (MeV)
    get4mu     : Returns 4-vector of muon (MeV)
    getcostheta: Returns cosine of angle between muon and the parent
                 pion in the pion rest frame
    getphi     : The polar  angle of the muon in the pion rest frame,
                 wrt the x axis of nuStorm

  
  Pion-decay methods:
    GenerateLifetime: Generates lifetime of this instance.  Returns
                      lifetime (float). Units s
    decaypion       : Generates a particular muon decay; calls each of 
                      following methods in turn.  Returns 32 4-vectors,
                      v_mu, v_numu.  v_i = [Energy, array(px, py, px)] 
                      (units MeV), and two floats, costheta, phi
    get3vectors     : Generates 3-vector momenta (MeV).  muon direction
                      taken as positive z direction.  Returns two float
                      array objects, p_mu, p_numu;
                      p_i = array(px, py, pz),
                      and two floats costheta and phi
    ranCoor         : Applies random 3D rotation and returns 4-vectors:
                      v_mu, v_numu.  v_i = [Energy, array(px, py, px)]
                      Units MeV.

Created on 26March21; Version history:
----------------------------------------------
 2.0: 18Dec25: Begin to port to LhARAlinearOptics framework.
 1.0: 26Mar21: First implementation - based on MuonDecay

@author: kennethlong and PaulKyberd
"""

from copy import deepcopy 
import Simulation as Simu
import numpy as np
import math as mth
import PhysicalConstants as PC

iPC = PC.PhysicalConstants()

class pionDECAY:

    __Debug = False
    
#--------  "Built-in methods":
    def __init__(self):

        if self.getDebug():
            print(" pionDecay.__init__ starts:")
        
        v_mu, v_numu, costheta, phi = self.decaypion()

        if self.getDebug():
            print("     ---->     v_mu:", v_mu, "\n", \
                  "             v_numu:", v_numu, "\n", \
                  "           costheta:", costheta, "\n", \
                  "                phi:", phi)

        self.setvmu(v_mu)
        self.setvnumu(v_numu)
        
        self.setcostheta(costheta)
        self.setphi(phi)

        if self.getDebug():
            print(self)
        
    def __repr__(self):
        return "pionDECAY()"

    def __str__(self):
        return " pionDECAY: v_mu=(%g, [%g, %g, %g]), \r\n \
         v_numu=(%g, [%g, %g, %g])" %                       \
                   (self.getvmu()[0], self.getvmu()[1],     \
                    self.getvmu()[2], self.getvmu()[3],     \
                    self.getvnumu()[0], self.getvnumu()[1], \
                    self.getvnumu()[2], self.getvnumu()[3])

    
#--------  "Dynamic methods"; individual lifetime, energies, and angles

    #..  Lifetime
    @staticmethod
    def GenerateLifetime(**kwargs):
        Tmax = kwargs.get('Tmax', float('inf'))
        Gmx = 1. - mth.exp( -Tmax / iPC.tauPion() )
        ran = Simu.getRandom() * Gmx
        lt  = -mth.log(1.-ran) * iPC.tauPion()
        return lt


    #..  Random rotation flat in phi and cos Theta
    def ranCoor(self, p_mu, p_numu):
        #.. Rotation angles
        phi = Simu.getRandom() * 2.*mth.pi
        cPhi = mth.cos(phi)
        sPhi = mth.sin(phi)

        cTheta = -1. + 2.*Simu.getRandom()
        sTheta = mth.sqrt(1. - cTheta**2)
        theta = mth.acos(cTheta)

        #.. Rotation matrices:
        Ra = np.array([          \
             [cPhi   , -sPhi,    0.      ], \
             [sPhi   ,  cPhi,    0.      ], \
             [0.     , 0.,       1.      ] \
                                ])
        Rb = np.array([          \
             [cTheta    , 0.,    -sTheta     ], \
             [0.        , 1.,    0.          ], \
             [sTheta    , 0.,    cTheta      ] \
                                   ])

        Rr = np.dot(Ra, Rb)
        
        #.. Do rotation:
        p_mu1  = np.dot(Rr, p_mu)
        p_numu1 = np.dot(Rr, p_numu)

        return  p_mu1, p_numu1, cTheta, phi

    def decaypion(self):
        #.. Calculate 3-vectors - muon is going forward:
        pmu = (iPC.mPion()+iPC.mMuon())*(iPC.mPion()-iPC.mMuon()) / \
              (2.*iPC.mPion())
        f_mu = np.array([0.0, 0.0, pmu])
        f_numu = np.array([0.0, 0.0, -pmu])
        if self.getDebug():
            print ("     ----> muon 3 vector:", f_mu, "\n", \
                   "           numu 3 vector:", f_numu)

        #.. Rotate to arbitrary axis orientation:
        p_mu, p_numu, cosTheta, phi = self.ranCoor(f_mu, f_numu)

        if self.getDebug():
            print ("     ----> Back from rotation: p_mu:", p_mu, "\n", \
                   "                            p_numu:", p_numu)

        E_mu = mth.sqrt( iPC.mMuon()*iPC.mMuon() + \
                         p_mu[0]*p_mu[0] + p_mu[1]*p_mu[1] + \
                         p_mu[2]*p_mu[2])
        
        E_numu = 29.7923147
        
        #  Energy conservation check:
        ETot = E_mu + E_numu
        if self.__Debug == True:
            print("     ----> Check energy conservation Emu =", E_mu, \
                   "Enumu =", E_numu, "ETotal =", ETot)
            
        if abs(ETot-iPC.mPion()) > 1.E-6:
            raise EnergyNonConservation("Energy not conserved " + \
                                        "delta E is " + \
                                        str(ETot-iPC.mPion()))
        
        v_mu   = np.array([E_mu,  p_mu[0], p_mu[1], p_mu[2]])
        v_numu = np.array([E_numu, p_numu[0], p_numu[1], p_numu[2]])

        return v_mu, v_numu, cosTheta, phi

#--------  Set methods:
    @classmethod
    def setDebug(cls, _Debug):
        if not isinstance(_Debug, bool):
            raise badPARAMETER(" pionDECAY.setDebug:" + str(_Debug) + \
                               " not boolean, exit.")
        cls.__Debug = _Debug

        if cls.getDebug():
            print(" pionDECAY.setDebug:", cls.getDebug())

    def setvmu(self, _vmu):
        if not isinstance(_vmu, np.ndarray):
            raise badPARAMETER(" pionDECAY.setvmu:" + \
                               str(_vmu) + \
                               " not np.ndarray, exit.")
        self._vmu = _vmu

        if self.getDebug():
            print(" pionDECAY.setvmu:", self.getvmu())

    def setvnumu(self, _vnumu):
        if not isinstance(_vnumu, np.ndarray):
            raise badPARAMETER(" pionDECAY.setvnumu:" + \
                               str(_vnumu) + \
                               " not np.ndarray, exit.")
        self._vnumu = _vnumu

        if self.getDebug():
            print(" pionDECAY.setvnumu:", self.getvnumu())

    def setcostheta(self, _costheta):
        if not isinstance(_costheta, float):
            raise badPARAMETER(" pionDECAY.setcostheta:" + \
                               str(_costheta) + \
                               " not float, exit.")
        self._costheta = _costheta

        if self.getDebug():
            print(" pionDECAY.setcostheta:", self.getcostheta())

    def setphi(self, _phi):
        if not isinstance(_phi, float):
            raise badPARAMETER(" pionDECAY.setphi:" + \
                               str(_phi) + \
                               " not float, exit.")
        self._phi = _phi

        if self.getDebug():
            print(" pionDECAY.setphi:", self.getphi())


#--------  "Get methods" only; version, reference, and constants
#.. Methods believed to be self documenting(!)
    @classmethod
    def getDebug(cls):
        return cls.__Debug

    def getvmu(self):
        return deepcopy(self._vmu)

    def getvnumu(self):
        return deepcopy(self._vnumu)

    def getcostheta(self):
        return deepcopy(self._costheta)

    def getphi(self):
        return deepcopy(self._phi)

    
#--------  Exceptions:
class badPARAMETER(Exception):
    pass
