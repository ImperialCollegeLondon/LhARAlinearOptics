#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
   Methods:
    calcX2: calculates x coordinate at end of LION beam line.
       Input: Brho, x1prime
      Return: x2

    calcy2: calculates x coordinate at end of LION beam line.
       Input: Brho, x1prime
      Return: x2
"""
def calcX2(Brho, x16D):

    Debug = False
    iBLE = 0
        
    T    = np.array( \
                     [ \
                       [1., 0.], \
                       [0., 1.]  \
                      ])
    Ti   = np.array( \
                     [ \
                       [1., 0.], \
                       [0., 1.]  \
                      ])
        
    if Debug:
        print(" Beam line:")
        print("     ----> T: \n", T)
    for BLEinst in BLE.BeamLineElement.getinstances():
        if isinstance(BLEinst, BLE.Source):
            continue

        iBLE +=1
        if Debug:
            print("             ----> i, type", iBLE, type(BLEinst))
        if isinstance(BLEinst, BLE.FocusQuadrupole) or \
           isinstance(BLEinst, BLE.DefocusQuadrupole):
            BLEinst.setTransferMatrix(Brho)
        Ti = np.array([ \
      [BLEinst.getTransferMatrix()[0][0], BLEinst.getTransferMatrix()[0][1]], \
      [BLEinst.getTransferMatrix()[1][0], BLEinst.getTransferMatrix()[1][1]]  \
                       ])
        if Debug:
            print("                 ----> Ti: \n", Ti)
        T  = np.matmul(Ti, T)
        if Debug:
            print("                 ----> Ti*T: \n", T)
        
    x1      = np.array([x16D[0], x16D[1]])
    x2      = np.matmul(T, x1)
    if Debug:
        print("         ----> T[1,2], x1prime, x2:", T12, x1prime, x2)

    return x2
def calcY2(Brho, y16D):
    Debug = False
    iBLE = 0
        
    T    = np.array( \
                     [ \
                       [1., 0.], \
                       [0., 1.]  \
                      ])
    Ti   = np.array( \
                     [ \
                       [1., 0.], \
                       [0., 1.]  \
                      ])
        
    if Debug:
        print(" Beam line:")
        print("     ----> T: \n", T)
    for BLEinst in BLE.BeamLineElement.getinstances():
        if isinstance(BLEinst, BLE.Source):
            continue
        
        iBLE +=1
        if Debug:
            print("             ----> i, type", iBLE, type(BLEinst))
        if isinstance(BLEinst, BLE.FocusQuadrupole) or \
           isinstance(BLEinst, BLE.DefocusQuadrupole):
            BLEinst.setTransferMatrix(Brho)
        Ti = np.array([ \
      [BLEinst.getTransferMatrix()[2][2], BLEinst.getTransferMatrix()[2][3]], \
      [BLEinst.getTransferMatrix()[3][2], BLEinst.getTransferMatrix()[3][3]]  \
                       ])
        if Debug:
            print("                 ----> Ti: \n", Ti)
        T  = np.matmul(Ti, T)
        if Debug:
            print("                 ----> Ti*T: \n", T)
        
    y1     = np.array([y16D[2], y16D[3]])
    y2     = np.matmul(T, y1)
    if Debug:
        print("         ----> T[1,2], y1prime, y2:", T12, y1prime, y2)

    return y2
"""
Test script for setting up the "LIONFacility"
=============================================

  LIONFacility.py -- set "relative" path to code

"""

import os
import sys
import math  as mth
import scipy as sp
import numpy as np
import matplotlib.pyplot as plt


import Simulation      as Sml
import LIONbeam        as LNb
import BeamLineElement as BLE
import Particle        as Prtcl

##! Start:
print("========  LIONFacility tests  ========")
HOMEPATH    = os.getenv('HOMEPATH')
print("Initialising with HOMEPATH:", HOMEPATH)
filename     = os.path.join(HOMEPATH, \
                        '11-Parameters/LIONBeamLine-Params-LsrDrvn.csv')
print(" <---- Parameters will be read from:", filename)

##! Start:
print()
print(" ----> Tests start:")

##! Create facility instance:
LIONFacilityTest = 1
print()
print("     ----> LIONFacilityTest:", LIONFacilityTest, \
      " create facility instance.")

LNbI  = LNb.LIONbeam(filename)
print(LNbI)

print()
print("     <---- LIONFacilityTest:", LIONFacilityTest, \
      " facility instance created.")

##! Check generation
LIONFacilityTest += 1
print()
print("     ----> LIONFacilityTest:", LIONFacilityTest, \
      " check generation/tracking.")

print("         ----> First using hard-coded trace space at source.")
LNbI.setDebug(True)
LNbI.setSrcTrcSpc(np.array([0.0001, -0.0001, 0.0002, 0.0001, 0., 20.]))
OK = LNbI.trackLION(1)
LNbI.setDebug(False)

print("         ----> Second using generated beam:")
LNbI.setSrcTrcSpc()
print(LNbI)

NEvt = 10
OK = LNbI.trackLION(NEvt)


""" Legacy; need to recheck tests from here:
print("     ----> Print one event that made it to end of delivery:", \
      LNbI.getSrcTrcSpc())

Prt    = False
iPrtcl = 0

while not Prt:
    OK = LNbI.trackLION(1)
    print(" HereHere:", len(Prtcl.Particle.instances))
    iPrtclInst = Prtcl.Particle.instances[len(Prtcl.Particle.instances)-1]
    if iPrtcl >= NEvt:
        print("         ----> No events made it to end of delivery section.")
        Prt = True
    if iPrtclInst.getz()[len(iPrtclInst.getLocation())-1] > 1.88:
        OK     = iPrtclInst.printProgression()
        TrcSpc = iPrtclInst.getTraceSpace()[0]
        Prt    = True
print("     <---- Done printing one event that made it to end of delivery:")


##! Investigate focussing
LIONFacilityTest += 1
print()
print("     ----> LIONFacilityTest:", LIONFacilityTest, \
      " investigate focusing.")

print("         ----> Speed of light:", BLE.speed_of_light, " m/s")
print()
print("         ----> Test with particle that made it all the way through:")
cprime = BLE.speed_of_light * 1.E-6
Enrgy = TrcSpc[5]
print("             ----> Energy:", Enrgy, " MeV")
Mmtm  = mth.sqrt(2.*938.27208816*Enrgy)
Brho = Mmtm / (BLE.speed_of_light * 1.E-9) / 1000.
print("             ----> Mmtm:", Mmtm, " MeV")
print("                   Brho:", Brho, " T m")
Brho = Mmtm / cprime
print("                   Brho:", Brho, " T m")
print()
x2 = calcX2(Brho, TrcSpc)
print("             ----> x2:", x2)
y2 = TrcSpc[2] + calcY2(Brho, TrcSpc)
print("             ----> y2:", y2)
print()

print("         ----> Test at p=[1, ..., 20] MeV:")
EnergyRange = np.arange(1., 20., 0.01)
Energy  = []
x2      = []
x1prime = 1./60.
TrcSpc  = np.array([0., x1prime, 0., x1prime, 0., 0.])
for Enrgy in EnergyRange:
    Mmtm      = mth.sqrt(2.*938.27208816*Enrgy)
    TrcSpc[5] = Enrgy
    Brho      = Mmtm / cprime
    xx2       = calcX2(Brho, TrcSpc)
    Energy.append(Enrgy)
    x2.append(xx2[0])
plt.plot(Energy, x2, 'r')
Energy  = []
x2      = []
x1prime = 0.01/60.
TrcSpc  = np.array([0., x1prime, 0., x1prime, 0., 0.])
for Enrgy in EnergyRange:
    Mmtm      = mth.sqrt(2.*938.27208816*Enrgy)
    Brho      = Mmtm / cprime
    TrcSpc[5] = Enrgy
    xx2       = calcX2(Brho, TrcSpc)
    Energy.append(Enrgy)
    x2.append(xx2[0])
plt.plot(Energy, x2, 'g')
Energy  = []
x2      = []
x1prime = 10.0/60.
TrcSpc  = np.array([0., x1prime, 0., x1prime, 0., 0.])
for Enrgy in EnergyRange:
    Mmtm      = mth.sqrt(2.*938.27208816*Enrgy)
    Brho      = Mmtm / cprime
    TrcSpc[5] = Enrgy
    xx2       = calcX2(Brho, TrcSpc)
    Energy.append(Enrgy)
    x2.append(xx2[0])
plt.plot(Energy, x2, 'b')
plt.title('x2 vs energy')
plt.xlabel('E (MeV)')
plt.ylabel('x2 (m)')
plt.savefig('99-Scratch/Tst_plot11x.pdf')
plt.close()

Energy  = []
y2      = []
y1prime = 1./60.
TrcSpc  = np.array([0., y1prime, 0., y1prime, 0., 0.])
for Enrgy in EnergyRange:
    Mmtm      = mth.sqrt(2.*938.27208816*Enrgy)
    Brho      = Mmtm / cprime
    TrcSpc[5] = Enrgy
    yy2       = calcY2(Brho, TrcSpc)
    Energy.append(Enrgy)
    y2.append(yy2[0])
plt.plot(Energy, y2, 'r')
Energy  = []
y2      = []
y1prime = 0.01/60.
TrcSpc  = np.array([0., y1prime, 0., y1prime, 0., 0.])
for Enrgy in EnergyRange:
    Mmtm      = mth.sqrt(2.*938.27208816*Enrgy)
    Brho      = Mmtm / cprime
    TrcSpc[5] = Enrgy
    yy2       = calcY2(Brho, TrcSpc)
    Energy.append(Enrgy)
    y2.append(yy2[0])
plt.plot(Energy, y2, 'g')
Energy  = []
y2      = []
y1prime = 10.0/60.
TrcSpc  = np.array([0., y1prime, 0., y1prime, 0., 0.])
for Enrgy in EnergyRange:
    Mmtm      = mth.sqrt(2.*938.27208816*Enrgy)
    Brho      = Mmtm / cprime
    TrcSpc[5] = Enrgy
    yy2       = calcY2(Brho, TrcSpc)
    Energy.append(Enrgy)
    y2.append(yy2[0])
plt.plot(Energy, y2, 'b')
plt.title('y2 vs energy')
plt.ylabel('E (MeV)')
plt.ylabel('y2 (m)')
plt.savefig('99-Scratch/Tst_plot11y.pdf')
plt.close()

x1primeRange = np.arange(0.001, 0.020, 0.015)
y1primeRange = np.arange(0.001, 0.020, 0.003)
col          = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
icol         = -1
for x1prime in x1primeRange:
    icol += 1
    for y1prime in y1primeRange:
        Energy  = []
        r       = []
        for Enrgy in EnergyRange:
            Mmtm   = mth.sqrt(2.*938.27208816*Enrgy)
            Brho   = Mmtm / cprime
            TrcSpc = np.array([0., x1prime, 0., y1prime, 0., Enrgy])
            xx2    = calcX2(Brho, TrcSpc)
            yy2    = calcY2(Brho, TrcSpc)
            rr     = mth.sqrt(xx2[0]**2 + yy2[0]**2)
            Energy.append(Enrgy)
            r.append(rr)
        Str = "[" + str(round(x1prime,3)) + ", " \
                  + str(round(y1prime,3)) + ")"
        plt.plot(Energy, r, c=col[icol], label=Str)
        Str = "[" + str(round(x1prime,3)) + ", " \
                  + str(round(y1prime,3)) + ")"
plt.legend(loc="upper right")
plt.xlabel('E (MeV)')
plt.ylabel('r (m)')
plt.savefig('99-Scratch/Tst_plot11ra.pdf')
plt.close()

x1primeRange = np.arange(0.001, 0.020, 0.015)
y1primeRange = np.arange(-0.001, -0.020, -0.003)
col          = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
icol         = -1
for x1prime in x1primeRange:
    icol += 1
    for y1prime in y1primeRange:
        Energy  = []
        r       = []
        for Enrgy in EnergyRange:
            Mmtm   = mth.sqrt(2.*938.27208816*Enrgy)
            Brho   = Mmtm / cprime
            TrcSpc = np.array([0., x1prime, 0., y1prime, 0., Enrgy])
            xx2    = calcX2(Brho, TrcSpc)
            yy2    = calcY2(Brho, TrcSpc)
            rr     = mth.sqrt(xx2[0]**2 + yy2[0]**2)
            Energy.append(Enrgy)
            r.append(rr)
        Str = "[" + str(round(x1prime,3)) + ", " \
                  + str(round(y1prime,3)) + ")"
        plt.plot(Energy, r, c=col[icol], label=Str)
plt.legend(loc="upper right")
plt.xlabel('E (MeV)')
plt.ylabel('r (m)')
plt.savefig('99-Scratch/Tst_plot11rb.pdf')
plt.close()

x1primeRange = np.arange(-0.001, -0.020, -0.015)
y1primeRange = np.arange(-0.001, -0.020, -0.003)
col          = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
icol         = -1
for x1prime in x1primeRange:
    icol += 1
    for y1prime in y1primeRange:
        Energy  = []
        r       = []
        for Enrgy in EnergyRange:
            Mmtm   = mth.sqrt(2.*938.27208816*Enrgy)
            Brho   = Mmtm / cprime
            TrcSpc = np.array([0., x1prime, 0., y1prime, 0., Enrgy])
            xx2    = calcX2(Brho, TrcSpc)
            yy2    = calcY2(Brho, TrcSpc)
            rr     = mth.sqrt(xx2[0]**2 + yy2[0]**2)
            Energy.append(Enrgy)
            r.append(rr)
        Str = "[" + str(round(x1prime,3)) + ", " \
                  + str(round(y1prime,3)) + ")"
        plt.plot(Energy, r, c=col[icol], label=Str)
plt.legend(loc="upper right")
plt.xlabel('E (MeV)')
plt.ylabel('r (m)')
plt.savefig('99-Scratch/Tst_plot11rc.pdf')
plt.close()

x1primeRange = np.arange(-0.001, -0.020, -0.015)
y1primeRange = np.arange(0.001, 0.020, 0.003)
col          = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
icol         = -1
for x1prime in x1primeRange:
    icol += 1
    for y1prime in y1primeRange:
        Energy  = []
        r       = []
        for Enrgy in EnergyRange:
            Mmtm   = mth.sqrt(2.*938.27208816*Enrgy)
            Brho   = Mmtm / cprime
            TrcSpc = np.array([0., x1prime, 0., y1prime, 0., Enrgy])
            xx2    = calcX2(Brho, TrcSpc)
            yy2    = calcY2(Brho, TrcSpc)
            rr     = mth.sqrt(xx2[0]**2 + yy2[0]**2)
            Energy.append(Enrgy)
            r.append(rr)
        Str = "[" + str(round(x1prime,3)) + ", " \
                  + str(round(y1prime,3)) + ")"
        plt.plot(Energy, r, c=col[icol], label=Str)
plt.legend(loc="upper right")
plt.xlabel('E (MeV)')
plt.ylabel('r (m)')
plt.savefig('99-Scratch/Tst_plot11rd.pdf')
plt.close()
"""

##! End:
print()
print(" <---- Tests finished.")


##! Complete:
print()
print("========  LIONFacility tests complete  ========")
