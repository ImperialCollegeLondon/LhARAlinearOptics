#!/usr/bin/env python

import numpy as np

def RotMat_x(theta):

    '''
    Creating a General Matrix method for ease as need to perform several rotations

    Use "@" for matrix multiplication
    '''

    Mx=np.array(
            [
                [1.0, 0.0, 0.0],
                [0.0, np.cos(theta), -np.sin(theta)],
                [0.0, np.sin(theta), np.cos(theta)],
            ])

    return Mx

def RotMat_y(theta):

    My=np.array(
            [
                [np.cos(theta), 0.0, np.sin(theta)],
                [0.0, 1.0, 0.0],
                [-np.sin(theta), 0.0, np.cos(theta)],
            ])

    return My

def RotMat_z(theta):

    Mz=np.array(
            [
                [np.cos(theta), -np.sin(theta), 0.0],
                [np.sin(theta), np.cos(theta), 0.0],
                [0.0, 0.0, 1.0],
            ])

    return Mz

