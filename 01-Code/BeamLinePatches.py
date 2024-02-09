# -*- coding: utf-8 -*-

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import matplotlib as mpl

import numpy as np


def rad2deg(rad):
    return rad / np.pi * 180


def dipolePatch(ax, angle, R, w):

    patchBLE = patches.Wedge(
        center=[0, 0],
        r=R - w,
        theta1=0,
        theta2=rad2deg(np.abs(angle)),
        width=2 * w,
        facecolor="lightblue",
        label="Dipole",
        alpha=1.0,
    )

    r = mpl.transforms.Affine2D().rotate_deg(-90)
    t = mpl.transforms.Affine2D().translate(0, R - 0.2)
    refx = mpl.transforms.Affine2D(np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]]))

    if angle >= 0:
        trans = r + t + ax.transData
    elif angle < 0:
        trans = refx + r + t + ax.transData

    patchBLE.set_transform(trans)

    return patchBLE


def sourcePatch(L):

    patchBLE = patches.Arrow(
        x=0,
        y=0,
        dx=L,
        dy=0,
        label="Source",
        facecolor="green",
    )

    return patchBLE


def aperturePatch(D, L, h):

    patchBLEi = patches.Rectangle(
        xy=(-L / 2, D / 2),
        width=L,
        height=h,
        edgecolor="black",
        hatch="//",
    )

    patchBLEii = patches.Rectangle(
        xy=(-L / 2, -D / 2),
        width=L,
        height=h,
        label="Aperture",
        edgecolor="black",
        hatch="//",
    )

    return patchBLEi + patchBLEii
