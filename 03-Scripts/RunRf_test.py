#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import Simulation as Simu
import BeamLine as BL
import Particle as Prtcl
import csv
import numpy as np


def time_spread_voltage(voltage, num_of_events, iLoc=-1):

    HOMEPATH = os.getenv("HOMEPATH")
    # Original filename
    filename = os.path.join(HOMEPATH, "11-Parameters/RFtest.csv")
    # Open the original CSV file and read its contents
    with open(filename, "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
    # Modify the "Value" of "Gradient" only in rows where "Element" is "Cavity"
    for row in rows:
        if row["Element"] == "Cavity" and row["Parameter"] == "Gradient":
            row["Value"] = voltage  # Modify the value to 5

    # Write the modified data back to the original CSV file
    with open(filename, "w", newline="") as csvfile:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    datafiledir = os.path.join(HOMEPATH, "99-Scratch")

    # if PARTICLEPATH = None does not delete Particles!

    Smltn = Simu.Simulation(num_of_events, filename, datafiledir, None)

    Smltn.RunSim()

    return Prtcl.Particle.calcLongitudinalSpread(iLoc)


voltage_list = [5, 6, 100]

for voltage in voltage_list:
    print(time_spread_voltage(voltage, 2000))
