#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "Facility" derived class
========================================

"""
import numpy           as np

import BeamLineElement as BLE


##! Start:
print("========  Facility: tests start  ========")

##! Test creation and built-in methods:
FacilityTest = 1
print()
print("BeamLineElement(Facility) test:", FacilityTest, \
      " check creation and built-in methods.")

#.. __init__
print("    __init__:")
try:
    Fclty = BLE.Facility()
except:
    print('      ----> Correctly trapped no argument exception.')
BLE.BeamLineElement.cleaninstances()
    
#.. Create valid instance:
rStrt = np.array([0.,0.,0.])
vStrt = np.array([[np.pi/2.,np.pi/2.],[0.,0.]])
drStrt = np.array([0.,0.,0.])
dvStrt = np.array([[0.,0.],[0.,0.]])
p0     = 15.
VCMV   = 0.5
Fclty = BLE.Facility("Facility0", rStrt, vStrt, drStrt, dvStrt, \
                     p0, VCMV)
    
#.. __repr__
print("    __repr__:")
print("      ---->", repr(Fclty))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(str(Fclty))
print("    <---- __str__ done.")

print(" <---- Creation and built in method tests done!  --------  --------")


##! Ca commence: check singleton nature of Facility instanciation:
FacilityTest += 1
print()
print("BeamLineElement(Facility) test:", FacilityTest, \
      " check singleton nature of Facility instanciation:")
try:
    Fclty = BLE.Facility("Facility1", rStrt, vStrt, drStrt, dvStrt, \
                         p0, VCMV)
except:
    print(' <---- Correctly trapped attempt to create second instance.')


##! Complete:
print()
print("========  Facility: tests complete  ========")
