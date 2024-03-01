#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import Simulation as Simu
import ReadRF_test
import csv

voltage_list = [1,10,20,50]


for voltage in voltage_list:
    ##! Start:
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
    Smltn = Simu.Simulation(1000, filename, datafiledir, 'LhARAsimu.dat')
    

    print()
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