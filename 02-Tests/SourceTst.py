#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "Source" class
=============================

  Source.py -- set "relative" path to code

"""

import os
import math  as mth
import numpy as np
import matplotlib.pyplot as plt

import BeamLineElement as BLE
import BeamLine        as BL
import Particle        as Prtcl

HOMEPATH = os.getenv('HOMEPATH')
filename = os.path.join(HOMEPATH, \
                        '11-Parameters/LIONBeamLine-Params-LsrDrvn.csv')
BLI  = BL.BeamLine(filename)

iRefPrtcl = Prtcl.ReferenceParticle.getinstance()


##! Start:
print("========  Source: tests start  ========")

##! Test creation and built-in methods:
SourceTest = 1
print()
print("SourceTest:", SourceTest, \
      " check creation and built-in methods.")

#.. __init__
print("    __init__:")
try:
    Src = BLE.Source()
except:
    print('      ----> Correctly trapped no argument exception.')
rStrt = np.array([0.,0.,0.])
vStrt = np.array([[np.pi/2.,np.pi/2.],[0.,0.]])
drStrt = np.array([0.,0.,0.])
dvStrt = np.array([[0.,0.],[0.,0.]])
try:
    Src = BLE.Source(rStrt, vStrt, drStrt, dvStrt)
except:
    print('      ----> Correctly trapped no Source paramters exception.')

#.. Create valid instance:
Mode  = 0
Param = [0.000004, 0.000004, 0.999691155, 1., 25., 1000, 2.5E+15, 70., \
         0.8, 2.80E-14, 0.0000004, 4.00E+20, 25.]
Src = BLE.Source("Source0", rStrt, vStrt, drStrt, dvStrt, Mode, Param)
    
#.. __repr__
print("    __repr__:")
print("      ---->", repr(Src))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(str(Src))
print("    <---- __str__ done.")

print(" <---- Creation and built in method tests done!  --------  --------")


##! Ca commence: check gaussian source distribution:
SourceTest += 1
print()
print("BeamLineElement(Source)Test:", SourceTest, \
      " test gaussian source distribution.")
BLE.Source.setDebug(False)
BLE.Source.cleaninstances()
Src = BLE.Source("Source1", rStrt, vStrt, drStrt, dvStrt, \
                 1, [0.000004, 0.000004, 0.998, 20., 0.3])
x, y, K, cTheta, Phi = Src.getParticle()
print("     ----> First particle: x, y, KE, cosTheta, Phi:", \
      x, y, K, cTheta, Phi)
print("         ----> And now in trace space:", \
      Src.getTraceSpace(x, y, K, cTheta, Phi))

PrtclX   = np.array([])
PrtclY   = np.array([])
PrtclKE  = np.array([])
PrtclcT  = np.array([])
PrtclPhi = np.array([])

SrcX     = np.array([])
SrcY     = np.array([])
SrcXp    = np.array([])
SrcYp    = np.array([])
SrcE     = np.array([])

print("     ----> Generate many particles:")
for i in range(10000):
    X, Y, KE, cTheta, Phi = Src.getParticle()
    PrtclX   = np.append(PrtclX , X)
    PrtclY   = np.append(PrtclY , Y)
    PrtclKE  = np.append(PrtclKE , KE)
    PrtclcT  = np.append(PrtclcT , cTheta)
    PrtclPhi = np.append(PrtclPhi, Phi)

    TrcSpcFrmSrc = Src.getParticleFromSource()
    SrcX         = np.append(SrcX,  TrcSpcFrmSrc[0])
    SrcY         = np.append(SrcY,  TrcSpcFrmSrc[2])
    SrcXp        = np.append(SrcXp, TrcSpcFrmSrc[1])
    SrcYp        = np.append(SrcYp, TrcSpcFrmSrc[3])
    SrcE         = np.append(SrcE,  TrcSpcFrmSrc[5])
    
n, bins, patches = plt.hist(PrtclX, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('X (m)')
plt.ylabel('Entries')
plt.title('Guassian X position distribution')
plt.savefig('99-Scratch/SourceTst_plot1.pdf')
plt.close()

n, bins, patches = plt.hist(PrtclY, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('Y (m)')
plt.ylabel('Entries')
plt.title('Guassian Y position distribution')
plt.savefig('99-Scratch/SourceTst_plot2.pdf')
plt.close()

n, bins, patches = plt.hist(PrtclKE, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('Energy (MeV)')
plt.ylabel('Entries')
plt.title('Gaussian source: energy distribution')
plt.savefig('99-Scratch/SourceTst_plot3.pdf')
plt.close()

n, bins, patches = plt.hist(PrtclcT, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('cos(theta)')
plt.ylabel('Entries')
plt.title('Gaussian source: (cos) polar angle distribution')
plt.savefig('99-Scratch/SourceTst_plot4.pdf')
plt.close()

n, bins, patches = plt.hist(PrtclPhi, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('Phi')
plt.ylabel('Entries')
plt.title('Gaussian source: azimuthal; angle distribution')
plt.savefig('99-Scratch/SourceTst_plot5.pdf')
plt.close()

n, bins, patches = plt.hist(SrcX, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('X')
plt.ylabel('Entries')
plt.title('Gaussian source: X position at exit from source')
plt.savefig('99-Scratch/SourceTst_plot6.pdf')
plt.close()

n, bins, patches = plt.hist(SrcY, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('Y')
plt.ylabel('Entries')
plt.title('Gaussian source: Y position at exit from source')
plt.savefig('99-Scratch/SourceTst_plot7.pdf')
plt.close()

n, bins, patches = plt.hist(SrcXp, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('X-prime')
plt.ylabel('Entries')
plt.title('Gaussian source: X-prime position at exit from source')
plt.savefig('99-Scratch/SourceTst_plot8.pdf')
plt.close()

n, bins, patches = plt.hist(SrcYp, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('Y-prime')
plt.ylabel('Entries')
plt.title('Gaussian source: Y-prime position at exit from source')
plt.savefig('99-Scratch/SourceTst_plot9.pdf')
plt.close()

n, bins, patches = plt.hist(SrcE, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('delta')
plt.ylabel('Entries')
plt.title('Gaussian source: delta at exit from source')
plt.savefig('99-Scratch/SourceTst_plot10.pdf')
plt.close()


##! Next: check paramterised laser-driven source distribution:
SourceTest += 1
print()
print("SourceTest:", SourceTest, \
      " test parameterised laser-driven source distribution ", \
      "check.")
Src1 = BLE.Source("Source2", rStrt, vStrt, drStrt, dvStrt, \
                  0, [0.000004, 0.000004, 0.999691155, 1., 25., 1000, \
                      2.5E+15, 70., 0.8, 2.80E-14, 0.0000004, 4.00E+20, 25.])
print(Src1)
print(" Test generation:")
print("     ----> First particle: KE, cosThetaPhi:", \
      Src1.getParticle())

PrtclX   = np.array([])
PrtclY   = np.array([])
PrtclKE  = np.array([])
PrtclcT  = np.array([])
PrtclPhi = np.array([])

SrcX     = np.array([])
SrcY     = np.array([])
SrcXp    = np.array([])
SrcYp    = np.array([])
SrcE     = np.array([])

print("     ----> Generate many particles:")
for i in range(100000):
    X, Y, KE, cTheta, Phi = Src1.getParticle()
    PrtclX   = np.append(PrtclX , X)
    PrtclY   = np.append(PrtclY , Y)
    PrtclKE  = np.append(PrtclKE , KE)
    PrtclcT  = np.append(PrtclcT , cTheta)
    PrtclPhi = np.append(PrtclPhi, Phi)

    TrcSpcFrmSrc = Src1.getParticleFromSource()
    SrcX         = np.append(SrcX,  TrcSpcFrmSrc[0])
    SrcY         = np.append(SrcY,  TrcSpcFrmSrc[2])
    SrcXp        = np.append(SrcXp, TrcSpcFrmSrc[1])
    SrcYp        = np.append(SrcYp, TrcSpcFrmSrc[3])
    SrcE         = np.append(SrcE,  TrcSpcFrmSrc[5])
    
n, bins, patches = plt.hist(PrtclX, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('X (m)')
plt.ylabel('Entries')
plt.title('LsrDrvnSrc: X position distribution')
plt.savefig('99-Scratch/SourceTst_plot11.pdf')
plt.close()

n, bins, patches = plt.hist(PrtclY, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('Y (m)')
plt.ylabel('Entries')
plt.title('LsrDrvnSrc: Y position distribution')
plt.savefig('99-Scratch/SourceTst_plot12.pdf')
plt.close()

n, bins, patches = plt.hist(PrtclKE, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('Energy (MeV)')
plt.ylabel('Entries')
plt.title('LsrDrvnSrc: Energy distribution')
plt.savefig('99-Scratch/SourceTst_plot13.pdf')
plt.close()

n, bins, patches = plt.hist(PrtclcT, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('cos(theta)')
plt.ylabel('Entries')
plt.title('LsrDrvnSrc: (cos) polar angle distribution')
plt.savefig('99-Scratch/SourceTst_plot14.pdf')
plt.close()

n, bins, patches = plt.hist(PrtclPhi, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('Phi')
plt.ylabel('Entries')
plt.title('LsrDrvnSrc: Azimuthal; angle distribution')
plt.savefig('99-Scratch/SourceTst_plot15.pdf')
plt.close()

n, bins, patches = plt.hist(SrcX, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('X')
plt.ylabel('Entries')
plt.title('LsrDrvnSrc: X position at exit from source')
plt.savefig('99-Scratch/SourceTst_plot16.pdf')
plt.close()

n, bins, patches = plt.hist(SrcY, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('Y')
plt.ylabel('Entries')
plt.title('LsrDrvnSrc: Y position at exit from source')
plt.savefig('99-Scratch/SourceTst_plot17.pdf')
plt.close()

n, bins, patches = plt.hist(SrcXp, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('X-prime')
plt.ylabel('Entries')
plt.title('LsrDrvnSrc: X-prime position at exit from source')
plt.savefig('99-Scratch/SourceTst_plot18.pdf')
plt.close()

n, bins, patches = plt.hist(SrcYp, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('Y-prime')
plt.ylabel('Entries')
plt.title('LsrDrvnSrc: Y-prime position at exit from source')
plt.savefig('99-Scratch/SourceTst_plot19.pdf')
plt.close()

n, bins, patches = plt.hist(SrcE, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('delta')
plt.ylabel('Entries')
plt.title('LsrDrvnSrc: delta at exit from source')
plt.savefig('99-Scratch/SourceTst_plot20.pdf')
plt.close()


##! Next: check flat energy distribution:
SourceTest += 1
print()
print("SourceTest:", SourceTest, \
      " test flat source distribution ", \
      "check.")
Src2 = BLE.Source("Source2", rStrt, vStrt, drStrt, dvStrt, \
                  2, [0.000004, 0.000004, 0.998, 1., 25.])

print(Src2)
print(" Test generation:")
print("     ----> First particle: KE, cosThetaPhi:", \
      Src2.getParticle())

PrtclX   = np.array([])
PrtclY   = np.array([])
PrtclKE  = np.array([])
PrtclcT  = np.array([])
PrtclPhi = np.array([])

SrcX     = np.array([])
SrcY     = np.array([])
SrcXp    = np.array([])
SrcYp    = np.array([])
SrcE     = np.array([])

print("     ----> Generate many particles:")
for i in range(100000):
    X, Y, KE, cTheta, Phi = Src2.getParticle()
    PrtclX   = np.append(PrtclX , X)
    PrtclY   = np.append(PrtclY , Y)
    PrtclKE  = np.append(PrtclKE , KE)
    PrtclcT  = np.append(PrtclcT , cTheta)
    PrtclPhi = np.append(PrtclPhi, Phi)

    TrcSpcFrmSrc = Src2.getParticleFromSource()
    SrcX         = np.append(SrcX,  TrcSpcFrmSrc[0])
    SrcY         = np.append(SrcY,  TrcSpcFrmSrc[2])
    SrcXp        = np.append(SrcXp, TrcSpcFrmSrc[1])
    SrcYp        = np.append(SrcYp, TrcSpcFrmSrc[3])
    SrcE         = np.append(SrcE,  TrcSpcFrmSrc[5])
    
n, bins, patches = plt.hist(PrtclX, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('X (m)')
plt.ylabel('Entries')
plt.title('FlatSrc: X position distribution')
plt.savefig('99-Scratch/SourceTst_plot21.pdf')
plt.close()

n, bins, patches = plt.hist(PrtclY, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('Y (m)')
plt.ylabel('Entries')
plt.title('FlatSrc: Y position distribution')
plt.savefig('99-Scratch/SourceTst_plot22.pdf')
plt.close()

n, bins, patches = plt.hist(PrtclKE, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('Energy (MeV)')
plt.ylabel('Entries')
plt.title('FlatSrc: Energy distribution')
plt.savefig('99-Scratch/SourceTst_plot23.pdf')
plt.close()

n, bins, patches = plt.hist(PrtclcT, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('cos(theta)')
plt.ylabel('Entries')
plt.title('FlatSrc: (cos) polar angle distribution')
plt.savefig('99-Scratch/SourceTst_plot24.pdf')
plt.close()

n, bins, patches = plt.hist(PrtclPhi, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('Phi')
plt.ylabel('Entries')
plt.title('FlatSrc: Azimuthal; angle distribution')
plt.savefig('99-Scratch/SourceTst_plot25.pdf')
plt.close()

n, bins, patches = plt.hist(SrcX, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('X')
plt.ylabel('Entries')
plt.title('FlatSrc: X position at exit from source')
plt.savefig('99-Scratch/SourceTst_plot26.pdf')
plt.close()

n, bins, patches = plt.hist(SrcY, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('Y')
plt.ylabel('Entries')
plt.title('FlatSrc: Y position at exit from source')
plt.savefig('99-Scratch/SourceTst_plot27.pdf')
plt.close()

n, bins, patches = plt.hist(SrcXp, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('X-prime')
plt.ylabel('Entries')
plt.title('FlatSrc: X-prime position at exit from source')
plt.savefig('99-Scratch/SourceTst_plot28.pdf')
plt.close()

n, bins, patches = plt.hist(SrcYp, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('Y-prime')
plt.ylabel('Entries')
plt.title('FlatSrc: Y-prime position at exit from source')
plt.savefig('99-Scratch/SourceTst_plot29.pdf')
plt.close()

n, bins, patches = plt.hist(SrcE, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('delta')
plt.ylabel('Entries')
plt.title('FlatSrc: delta at exit from source')
plt.savefig('99-Scratch/SourceTst_plot30.pdf')
plt.close()


##! Complete:
print()
print("========  Source: tests complete  ========")
