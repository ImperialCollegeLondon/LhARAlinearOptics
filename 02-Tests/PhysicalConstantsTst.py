#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "PhysicalConstants" class ... initialisation and get methods
=========================================

  PhysicalConstants.py -- set "relative" path to code

"""

import PhysicalConstants as PC
import sys

##! Start:
print("========  PhysicalConstants: tests start  ========")

##! Test singleton class feature:
PhysicalConstantsTest = 1
print()
print("PhysicalConstantsTest:", PhysicalConstantsTest, \
      " check if class is a singleton.")
physCnst  = PC.PhysicalConstants()
physCnst1 = PC.PhysicalConstants()
print("    physCnst singleton test:", id(physCnst), id(physCnst1), \
      id(physCnst)-id(physCnst1))
if physCnst != physCnst1:
    raise Exception("PhysicalConstants is not a singleton class!")

##! Check built-in methods:
PhysicalConstantsTest = 2
print()
print("PhysicalConstantsTest:", PhysicalConstantsTest, \
      " check built-in methods.")
print("    __repr__:")
print(physCnst)

##! Check get methods:
PhysicalConstantsTest = 3
print()
print("PhysicalConstantsTest:", PhysicalConstantsTest, " check get methods.")
print("    ----> Tests all get methods")
print(physCnst)

##! Check set method:
PhysicalConstantsTest = 4
print()
print("PhysicalConstantsTest:", PhysicalConstantsTest, " check set method.")
PC.PhysicalConstants.setDebug(True)
print(physCnst)
PC.PhysicalConstants.setDebug(False)

##! Complete:
print()
print("========  PhysicalConstants: tests complete  ========")
