#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import Particle as Prtcl

import BeamLine as BL

"""
Things to revise:
    
    Arbitrary parameters for centering structures in plt_apt (5E-3, 6E-3)
    Automatize elliptical aperture

Methods to do list:
    Particle number along beamline
    Phase space evolution along beamline
    Twiss parameters along beamline and brightness (in development as sequential code)
    
"""


# ------------Module methods:---------------------------------


def find_rows(dataframe, target_name, avoid=None, use_include=False, include=None):
    if "Element" in dataframe.columns:
        if use_include == True:
            matching_rows = dataframe.index[
                dataframe["Element"].str.contains(target_name, case=False)
                & (dataframe["Comment"].astype(str).str.strip() != avoid)
                & (dataframe["Parameter"].astype(str).str.strip() == include)
            ].tolist()
        else:
            matching_rows = dataframe.index[
                dataframe["Element"].str.contains(target_name, case=False)
                & (dataframe["Comment"].astype(str).str.strip() != avoid)
            ].tolist()

        if len(matching_rows) != 0:
            return matching_rows

        else:
            print(
                f"No matching rows for '{target_name}' found in the 'Element' column."
            )
            return pd.DataFrame()

    else:
        print("DataFrame does not have an 'Element' column.")
        return pd.DataFrame()


fig, axs = plt.subplots(3, 1, figsize=(11, 11))

# -------------------Class definition----------------------------


class BeamlinePlotter(object):
    import numpy as np
    import os
    import pandas as pd
    import matplotlib.pyplot as plt
    import Particle as Prtcl

    __Debug = False
    __instance = None
    __Facility = None

    # -------"Get" Methods--------------------

    def get_zlist(HOMEPATH=os.getenv("HOMEPATH"), filename=None):
        aux = 0
        z = []
        params = pd.read_csv(HOMEPATH + "/11-Parameters/" + filename)
        indexes = params[params["Parameter"] == "Length"].index.tolist()
        for i in indexes:
            aux += float(params["Value"][i])
            z.append(aux)

        z.insert(0, 0.0)  # insert source position

        return z

    def get_elementlist(HOMEPATH=os.getenv("HOMEPATH"), filename=None):
        params = pd.read_csv(HOMEPATH + "/11-Parameters/" + filename)
        my_list = []
        prev_element = None

        for element in params["Element"]:
            if element != prev_element:
                my_list.append(element)
            prev_element = element

        # Eliminate the Aperture occurences before and after every solenoid
        new_list = []
        i = 0
        while i < len(my_list):
            if (
                my_list[i] == "Solenoid"
                and i > 0
                and i < len(my_list) - 1
                and my_list[i - 1] == "Aperture"
                and my_list[i + 1] == "Aperture"
            ):
                new_list.append(my_list[i])
                new_list.append("Solenoid_end")
                i += 2  # Skip the 'Apt' elements
            elif (
                my_list[i] == "Aperture"
                and i > 0
                and i < len(my_list) - 1
                and my_list[i + 1] == "Solenoid"
            ):
                i += 1  # Skip the 'Apt' elements
            else:
                new_list.append(my_list[i])
                i += 1
        my_list = new_list

        # Eliminate one of the apertures for every Fquad and Dquad

        lst = my_list
        result = []
        skip_next = False

        for i in range(len(lst)):
            if skip_next:
                skip_next = False
                # continue

            if (
                lst[i] == "Aperture"
                and i + 1 < len(lst)
                and (lst[i + 1] == "Fquad" or lst[i + 1] == "Dquad")
            ):
                skip_next = True
            else:
                result.append(lst[i])
        my_list = result

        # Eliminate the Drifts
        new_list = []
        for i in my_list:
            if i != "Drift" and i != "Global":
                new_list.append(i)

        return new_list

    def get_ReferenceEnergy(HOMEPATH=os.getenv("HOMEPATH"), filename=None):
        params = pd.read_csv(HOMEPATH + "/11-Parameters/" + filename)
        index = params[params["Parameter"] == "Kinetic energy"].index
        E = float(params["Value"][index])
        return E

    # --------Beamline plotting Methods---------------

    def Tracer(
        mini,
        maxi,
        filename,
        maxz=0.0,
        facility=None,
        HOMEPATH=os.getenv("HOMEPATH"),
        label=None,
        NEvts=False,
        alpha=0.5,
        colour="r",
    ):
        ParticleFILE = Prtcl.Particle.openParticleFile(
            HOMEPATH + "/99-Scratch", filename
        )

        EndOfFile = False
        iEvt = 0
        iPrtcl = None

        DRACObI = BL.BeamLine(HOMEPATH + "/11-Parameters/" + facility)

        RefE = BeamlinePlotter.get_ReferenceEnergy(HOMEPATH=HOMEPATH, filename=facility)

        try:
            while not EndOfFile:
                EndOfFile = Prtcl.Particle.readParticle(ParticleFILE)

                iPrtcl = Prtcl.Particle.getParticleInstances()[
                    1
                ]  # used to be 0 in the previous PhaseSpace implementation

                if iPrtcl.getz()[-1] > maxz:  # the ones that get to the end of beamline
                    if mini < iPrtcl.getTraceSpace()[0][5] + RefE < maxi:
                        iEvt += 1
                        particle = iPrtcl
                        print(iEvt)
                        x = []
                        y = []
                        z = particle.getz()
                        x_lab = []
                        y_lab = []
                        z_lab = []
                        particle.fillPhaseSpace()

                        for i in range(len(particle.getTraceSpace())):
                            x.append(particle.getTraceSpace()[i][0])
                            y.append(particle.getTraceSpace()[i][2])

                        for i in range(len(particle.getTraceSpace())):
                            x_lab.append(particle.getLabPhaseSpace()[i][0][0])
                            y_lab.append(particle.getLabPhaseSpace()[i][0][1])
                            z_lab.append(particle.getLabPhaseSpace()[i][0][2])

                        xd = x[-1]
                        yd = y[-1]
                        x_lab_d = x_lab[-1]
                        y_lab_d = y_lab[-1]

                        if iEvt == 1:
                            axs[0].plot(
                                x_lab_d,
                                y_lab_d,
                                "o",
                                color=colour,
                                alpha=alpha,
                                label=label,
                            )

                        else:
                            axs[0].plot(
                                x_lab_d, y_lab_d, "o", color=colour, alpha=alpha
                            )
                        axs[1].plot(z_lab, x_lab, color=colour, alpha=alpha)
                        axs[2].plot(z_lab, y_lab, color=colour, alpha=alpha)

                        cleaned = Prtcl.Particle.cleanParticles()

                        if iEvt == NEvts:  # Ends the loop if everything is plotted
                            EndOfFile = True
                    else:
                        cleaned = Prtcl.Particle.cleanParticles()
                else:
                    cleaned = Prtcl.Particle.cleanParticles()

        except:  # Handles the exception if you already plotted all the particles within energy range
            IndexError
            print(
                "All particles within energy range E =", str(label), "have been plotted"
            )
            pass

        return fig, axs

    def plt_save(path="99-Scratch/ParticleTrajectory.pdf"):
        axs[0].grid(True)
        axs[0].legend(loc="upper left", fontsize="small")
        axs[0].set_xlabel("x-axis")
        axs[0].set_ylabel("y-axis")
        axs[0].set_title("Particle Beam after Final Collimator x-y plane")

        axs[1].grid(True)
        """
        axs[1].legend(
            loc="upper left", bbox_to_anchor=(-0.2, 0.5, 0.5, 0.5), fontsize="small"
        )
        """
        axs[1].set_xlabel("z-axis")
        axs[1].set_ylabel("x-axis")
        axs[1].set_title("Particle Trajectory x-z plane")

        axs[2].grid(True)
        """
        axs[2].legend(
            loc="upper left", bbox_to_anchor=(-0.2, 0.5, 0.5, 0.5), fontsize="small"
        )
        """
        axs[2].set_xlabel("z-axis")
        axs[2].set_ylabel("y-axis")
        axs[2].set_title("Particle Trajectory y-z plane")

        fig.tight_layout()
        fig.legend()
        plt.savefig(path)
        plt.close()
