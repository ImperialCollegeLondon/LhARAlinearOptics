#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import Simulation            as Simu
import Particle              as Prtcl
import csv
import numpy                 as np
import random                as __Rnd
import scipy                 as sp
import scipy.constants
import matplotlib.pyplot     as plt


def quad_strength_rate_end(element, parameter,values, elements_to_change, num_of_events, iLoc=-1):
    """_summary_

    Args:
        element (string): Element to be modified in parameter file
        parameter (string): Parameter corresponding to element to be changed 
        values (list): List of values to be changed corresponding to parameter
        elements_to_change(list): list of which index of type element to modify
        num_of_events(int): number of events to simulate
        iLoc (int, optional): _description_. Defaults to -1.

    Returns:
        _type_: _description_
    """

    HOMEPATH = os.getenv("HOMEPATH")
    # Original filename
    filename = os.path.join(HOMEPATH, "11-Parameters/LhARABeamLine-Params-Gauss-Gabor.csv")
    # Open the original CSV file and read its contents
    
    with open(filename, "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
    
    #Modify parameters
    for i, row in enumerate(rows):
        if row["Element"] == element and row["Parameter"] == parameter:
        
            if i in elements_to_change:
                row["Value"] = values[i]  
            else:            
                print("Parameter for", element, i, "is unchanged")

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

    end_station_rate = Prtcl.Particle.end_station_rate()

    Prtcl.Particle.cleanParticles()

    return end_station_rate


d_quad_kq = np.linspace(10,40, 150)
index_to_change = [0]
rate = []

for kq in d_quad_kq:
    rate.append(quad_strength_rate_end("Dquad","kq", [kq], index_to_change, 10000))

plt.plot(d_quad_kq, rate)
plt.savefig("99-Scratch/Quad_optimisation.png")


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





