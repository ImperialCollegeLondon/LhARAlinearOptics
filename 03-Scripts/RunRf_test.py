#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import Simulation   as Simu
import Particle     as Prtcl
import csv
import numpy        as np
import random       as __Rnd
import scipy        as sp
import scipy.constants


def time_spread(voltage, num_of_events, iLoc=-1):

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
    print(time_spread(voltage, 2000))


def proposal_distribution(voltage, sigma):
    return voltage + random.gaus(0, sigma)

#Implementing the simulated annealing
    
def simulated_annealing(inititial_voltage, final_tempertaure, sigma,  num_of_iterations = 1e4):
    it_counter = 0 

    #For testing store accepted voltages and time spreads in lists
    current_voltage = inititial_voltage #Temperature
    current_timespread = time_spread(current_voltage) #Energy

    voltage_list = [current_voltage]
    time_spread_list = [current_timespread]
    
    while True:    
        temperature = 1.0  # Initial temperature
        cooling_rate = 0.99 

        while temperature > final_tempertaure:
            if it_counter > num_of_iterations:
                RuntimeError("The annealing has exceeded the maximum number of iterations")
            it_counter += 1    
            #Propose voltage using proposal distribution
            proposed_voltage = proposal_distribution(current_voltage, sigma)
            proposed_timespread = time_spread(proposed_voltage)

            #Accept reject:
            delta = proposed_timespread-current_timespread

            if delta <= 0:
                current_voltage = proposed_voltage
                current_timespread = proposed_timespread
                voltage_list.append(current_voltage)
                time_spread_list.append(current_timespread)
            else:
                p_acc = np.exp(delta/(sp.constants.k*temperature))
                if __Rnd.random < p_acc:
                    current_voltage = proposed_voltage
                    current_timespread = proposed_timespread
                    voltage_list.append(current_voltage)
                    time_spread_list.append(current_timespread)
            
            temperature *= cooling_rate

        return current_voltage





