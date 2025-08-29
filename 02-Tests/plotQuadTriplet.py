#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plot script for "QuadTriplet" class
===================================

QuadTriplet.py -- set "relative" path to code

"""

import numpy as np
import scipy as sp
import math  as mth
import os

import PhysicalConstants as PhysCnst
import BeamLineElement   as BLE
import BeamLine          as BL
import Particle          as Prtcl

constants_instance = PhysCnst.PhysicalConstants()
protonMASS         = constants_instance.mp()

HOMEPATH = os.getenv('HOMEPATH')
filename = os.path.join(HOMEPATH, \
                        '11-Parameters/Dummy4Tests.csv')

##! Start:
print("========  QuadTriplet: start  ========")

##! Plot built-in methods:
QuadTripletPlot = 1
print()
print("QuadTripletPlot:", QuadTripletPlot, \
      " initialise")

print(filename)
BLI  = BL.BeamLine(filename)
iRefPrtcl = Prtcl.ReferenceParticle.getinstances()

##! Reference particle
QuadTripletPlot += 1
print()
print("QuadTripletPlot:", QuadTripletPlot, \
      " create reference particle")

print("     ----> Reference particle:")
K0  = 0.1
E0  = protonMASS + K0
p0  = mth.sqrt(E0**2 - protonMASS**2)
p04 = np.array([0., 0., p0, E0])

iRefPrtcl.setPrIn(p04)
iRefPrtcl.setPrOut(p04)

with np.printoptions(linewidth=500,precision=7,suppress=True):
    print("         <---- In:", iRefPrtcl.getPrIn())
with np.printoptions(linewidth=500,precision=7,suppress=True):
    print("              Out:", iRefPrtcl.getPrOut())
print("     <---- Reference particle set:")

##! Create quad triplet
QuadTripletPlot += 1
print()
print("QuadTripletPlot:", QuadTripletPlot, \
      " create reference particle")

rStrt = np.array([0., 0., 0.])
vStrt = np.array([[np.pi/2.,np.pi/2.],[0.,0.]])
drStrt = np.array([0., 0., 0.])
dvStrt = np.array([0., 0., 0.])

QT1 = BLE.QuadTriplet("QuadTriplet1", rStrt, vStrt, drStrt, dvStrt, \
                     "FDF",                      \
                     [0.1, None, 30.256], 0.1, \
                     [0.1, None, 53.393], 0.1, \
                     [0.1, None, 30.256])
BL.BeamLine.addBeamLineElement(QT1)
refPrtclSet = iRefPrtcl.setReferenceParticle(QT1)
QT2 = BLE.QuadTriplet("QuadTriplet2", rStrt, vStrt, drStrt, dvStrt, \
                     "DFD",                      \
                     [0.04, None, 302.563], 0.02, \
                     [0.04, None, 549.933], 0.02, \
                     [0.04, None, 302.563])
BL.BeamLine.addBeamLineElement(QT2)
refPrtclSet = iRefPrtcl.setReferenceParticle(QT2)

            
##! Check transport and inverse:
QuadTripletPlot += 1
print()
print("QuadTripletPlot:", QuadTripletPlot, \
      " check transport and inverse transport")

R      = np.array([0.005/mth.sqrt(2.), 0., 0.005/mth.sqrt(2.), 0., 0., 0.])
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Input trace-space vector:", R)

Rprime = QT1.Transport(R)
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Transported trace-space vector:", Rprime)

TrnsfMtrx = QT1.getTransferMatrix()
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> QT1 transfer matrix: \n", TrnsfMtrx)

invTrnsfMtrx = np.linalg.inv(TrnsfMtrx)
TrnsfMtrx = QT1.getTransferMatrix()
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Inverse transfer matrix: \n", invTrnsfMtrx)

chkMtrx = np.dot(invTrnsfMtrx, TrnsfMtrx)
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Check, invTrnsfMtrx . TrnsfMtrx: \n", chkMtrx)

Rcheck = np.dot(invTrnsfMtrx, Rprime)
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Transported trace-space vector:", Rcheck)

##! Try one particle estimate of focal length:
QuadTripletPlot += 1
print()
print("QuadTripletPlot:", QuadTripletPlot, \
      "Try one particle estimate of focal length: QT1")

R      = np.array([0.001, 0., 0.001, 0., 0., 0.])
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Input trace-space vector:", R)

Rprime = np.dot(invTrnsfMtrx, R)
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Transported trace-space vector:", Rprime)

zx = -Rprime[0] / Rprime[1]
zy = -Rprime[2] / Rprime[3]
print("     <---- zx, zy:", zx, zy)

##! Try one particle estimate of focal length:
QuadTripletPlot += 1
print()
print("QuadTripletPlot:", QuadTripletPlot, \
      "Try one particle estimate of focal length: QT2")

R      = np.array([0.001, 0., 0.001, 0., 0., 0.])
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Input trace-space vector:", R)

Rprime = QT2.Transport(R)
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Transported trace-space vector:", Rprime)

TrnsfMtrx = QT2.getTransferMatrix()
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> QT2 transfer matrix: \n", TrnsfMtrx)

invTrnsfMtrx = np.linalg.inv(TrnsfMtrx)
TrnsfMtrx = QT2.getTransferMatrix()
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Inverse transfer matrix: \n", invTrnsfMtrx)

chkMtrx = np.dot(invTrnsfMtrx, TrnsfMtrx)
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Check, invTrnsfMtrx . TrnsfMtrx: \n", chkMtrx)

Rprime = np.dot(invTrnsfMtrx, R)
with np.printoptions(linewidth=500,precision=5,suppress=True): \
     print("     ----> Transported trace-space vector:", Rprime)

zx = -Rprime[0] / Rprime[1]
zy = -Rprime[2] / Rprime[3]
print("     <---- zx, zy:", zx, zy)


##! Complete:
print()
print("========  QuadTriplet: complete  ========")
