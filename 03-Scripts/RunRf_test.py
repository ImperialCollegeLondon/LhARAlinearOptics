#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import Simulation as Simu
import BeamLine as BL
import Particle as Prtcl
import csv
import numpy as np

def time_spread_voltage(voltage, num_of_events):
    
    print("========  Simulation: start  ========")
    print()
    HOMEPATH = os.getenv('HOMEPATH')
    print("HOMEPATH:", HOMEPATH)

    # Original filename
    filename = os.path.join(HOMEPATH, '11-Parameters/RFtest.csv')
    # Open the original CSV file and read its contents
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)    
        rows = list(reader)
    # Modify the "Value" of "Gradient" only in rows where "Element" is "Cavity"
    for row in rows:
        if row['Element'] == "Cavity" and row['Parameter'] == "Gradient":
            print(voltage)
            row["Value"] = voltage  # Modify the value to 5

    # Write the modified data back to the original CSV file
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    datafiledir = os.path.join(HOMEPATH, '99-Scratch')

    Smltn = Simu.Simulation(num_of_events, filename, datafiledir, 'LhARAsimu.dat') 

    print(" <---- Simulation initialised.")
    ##! Start:
    print(" ----> Run simulation test:")
    print()
    Smltn.RunSim()
    print()
    print(" <---- Simulation test done.")
    ##! Complete:
    print()
    print("========  Simulation: complete  ========")

    LhARAbI  = BL.BeamLine(filename)
    
    print("     <---- LhARA instance created.")
    ParticleFILE = Prtcl.Particle.openParticleFile("99-Scratch", "LhARAsimu.dat")

    print("     ----> Read events from:", ParticleFILE)

    print()
    print(" <---- Initialisation done.")

    ##! Create LhARA instance:
    print(" ----> Read event file:")
    print()

    print("========  Read and plot: start  ========")
    EndOfFile = False
    iEvt = 0
    iCnt = 0
    Scl  = 10
    while not EndOfFile:
        EndOfFile = Prtcl.Particle.readParticle(ParticleFILE)
        if not EndOfFile:
            iEvt += 1
            if (iEvt % Scl) == 0:
                print("     ----> Read event ", iEvt)
                iCnt += 1
                if iCnt == 10:
                    iCnt = 1
                    Scl  = Scl * 10

    print(" <----", iEvt, "events read")
    
    print("========  Read: complete  ========")  



voltage_list = [5]

for voltage in voltage_list:
    time_spread_voltage(voltage,2000)

