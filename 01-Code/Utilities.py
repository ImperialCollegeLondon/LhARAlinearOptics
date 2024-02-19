#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------------------------------------------
# Rotations
# --------------------------------------------------------------------------------------


def RotMat_x(theta):
    """
    Creating a General Matrix method for ease as need to perform several rotations

    Use "@" for matrix multiplication
    """

    Mx = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, np.cos(theta), -np.sin(theta)],
            [0.0, np.sin(theta), np.cos(theta)],
        ]
    )

    return Mx


def RotMat_y(theta):

    My = np.array(
        [
            [np.cos(theta), 0.0, np.sin(theta)],
            [0.0, 1.0, 0.0],
            [-np.sin(theta), 0.0, np.cos(theta)],
        ]
    )

    return My


def RotMat_z(theta):

    Mz = np.array(
        [
            [np.cos(theta), -np.sin(theta), 0.0],
            [np.sin(theta), np.cos(theta), 0.0],
            [0.0, 0.0, 1.0],
        ]
    )

    return Mz

def TrRotMat_z(theta):
    MTr=np.array(
        [
            [np.cos(theta), 0.0, -np.sin(theta),0.0,0.0,0.0],
            [0.0, np.cos(theta), 0.0,-np.sin(theta),0.0,0.0],
            [np.sin(theta), 0.0, np.cos(theta) ,0.0,0.0,0.0],
            [0.0, np.sin(theta), 0.0,np.cos(theta),0.0,0.0],
            [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0,0.0,0.0,1.0],


        ]
    )
   
    return MTr


    




# --------------------------------------------------------------------------------------
# Plotting
# --------------------------------------------------------------------------------------


def save_all_figs(prefix, loc, figs=None, dpi=170):
    if figs is None:
        figs = [plt.figure(k) for k in plt.get_fignums()]
    for i, fig in enumerate(figs):
        path = loc + prefix + f"_{i}" + ".pdf"
        fig.tight_layout()
        fig.savefig(path, dpi=dpi, format="pdf", bbox_inches="tight", pad_inches=0)
