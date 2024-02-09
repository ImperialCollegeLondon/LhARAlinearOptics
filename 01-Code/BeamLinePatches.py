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
        trans = r + t + refx + ax.transData

    patchBLE.set_transform(trans)

    return patchBLE


def sourcePatch(w, L):

    patchBLE = patches.Arrow(
        x=0,
        y=0,
        dx=L,
        dy=0,
        width=w,
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
        xy=(-L / 2, -D / 2 - h),
        width=L,
        height=h,
        label="Aperture",
        edgecolor="black",
        hatch="//",
    )

    return patchBLEi, patchBLEii


def transformPatchYZ(ax, patch, Rot2Lab, R2Lab):

    Mat = Rot2Lab[1:, 1:]
    dR = R2Lab[1:3]
    A2D = np.eye(3)

    A2D[0:2, 0:2] = Mat
    A2D[0:2, 2] = dR[::-1]

    print(A2D)

    transA2D = mpl.transforms.Affine2D(A2D)

    trans = transA2D + patch.get_transform()

    patch.set_transform(trans)

    return patch
