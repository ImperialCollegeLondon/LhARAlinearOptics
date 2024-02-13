# -*- coding: utf-8 -*-

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import matplotlib as mpl

import numpy as np


def rad2deg(rad):
    return (rad / np.pi) * 180


class patchBLE:

    def __init__(self, ax):
        self.set_Patch(None)
        self.set_ax(ax)
        self.reset_Trans()

    def set_ax(self, ax):
        self._ax = ax
        return self

    def set_Patch(self, Patch):
        self._Patch = Patch
        return self

    def get_ax(self):
        return self._ax

    def get_Patch(self):
        return self._Patch

    def get_Trans(self):
        return self._Trans

    def append_Trans(self, trans):
        if isinstance(trans, mpl.transforms.Transform):
            self._Trans += trans
            return self
        else:
            raise Exception("Needs to be a matplotlib transform.")

    def reset_Trans(self):
        self._Trans = mpl.transforms.Affine2D(np.eye(3))
        return self

    def transformPatchYZ(self, Rot2Lab, R2Lab):
        Mat = Rot2Lab[1:, 1:]
        dR = R2Lab[1:3]

        A2D = np.eye(3)
        A2D[0:2, 0:2] = Mat
        A2D[0:2, 2] = dR

        print(A2D)

        trans = mpl.transforms.Affine2D(A2D)

        self.append_Trans(trans)

        return self

    def render_Patch(self):
        ax = self.get_ax()
        Patch = self.get_Patch()
        Trans = self.get_Trans()

        Patch.set_transform(Trans + ax.transData)

        ax.add_patch(Patch)


class dipolePatch(patchBLE):

    def __init__(self, ax, angle, R, w):

        print("patch3:", R)

        Patch = patches.Wedge(
            center=[0, 0],
            r=R + w,
            theta1=0,
            theta2=rad2deg(np.abs(angle)),
            width=2 * w,
            facecolor="lightblue",
            label="Dipole",
            alpha=1,
            zorder=999,
        )

        r = mpl.transforms.Affine2D().rotate_deg(-90)
        t = mpl.transforms.Affine2D().translate(0, R)
        refx = mpl.transforms.Affine2D(np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]]))

        if angle >= 0:
            trans = r + t
        elif angle < 0:
            trans = r + t + refx

        self.set_Patch(Patch)
        self.set_ax(ax)
        self.reset_Trans()
        self.append_Trans(trans)


class sourcePatch(patchBLE):

    def __init__(self, ax, w):

        Patch = patches.Polygon(
            ((-w / 2, -np.sqrt(3) / 2 * w), (w, 0), (-w / 2, np.sqrt(3) / 2 * w)),
            facecolor="green",
            zorder=999,
        )

        trans = mpl.transforms.Affine2D().rotate_deg(-30)

        self.set_Patch(Patch)
        self.set_ax(ax)
        self.reset_Trans()
        self.append_Trans(trans)


class aperturePatch(patchBLE):

    def __init__(self, ax, D, L, h):

        Patchi = patches.Rectangle(
            xy=(-L / 2, D / 2),
            width=L,
            height=h,
            edgecolor="black",
            hatch="////",
            zorder=999,
            facecolor="none",
            linewidth=0.5,
        )

        Patchii = patches.Rectangle(
            xy=(-L / 2, -D / 2 - h),
            width=L,
            height=h,
            label="Aperture",
            edgecolor="black",
            hatch="////",
            zorder=999,
            facecolor="none",
            linewidth=0.5,
        )

        self.set_Patch((Patchi, Patchii))
        self.set_ax(ax)
        self.reset_Trans()

    def render_Patch(self):
        ax = self.get_ax()
        Patch = self.get_Patch()
        Trans = self.get_Trans()

        for iPatch in Patch:
            iPatch.set_transform(Trans + ax.transData)
            ax.add_patch(iPatch)


class fquadPatch(patchBLE):

    def __init__(self, ax, w, h):

        Patch = patches.Rectangle(
            xy=[0, 0],
            width=w,
            height=h,
            zorder=999,
            label="FQuad",
            facecolor="purple",
        )

        self.set_Patch(Patch)
        self.set_ax(ax)
        self.reset_Trans()


class dquadPatch(patchBLE):

    def __init__(self, ax, w, h):

        Patch = patches.Rectangle(
            xy=[0, -h],
            width=w,
            height=h,
            zorder=999,
            label="DQuad",
            facecolor="silver",
        )

        self.set_Patch(Patch)
        self.set_ax(ax)
        self.reset_Trans()


class solenoidPatch(patchBLE):

    def __init__(self, ax, w, h):

        Patch = patches.Rectangle(
            xy=[0, -h / 2],
            width=w,
            height=h,
            zorder=999,
            label="DQuad",
            facecolor="gold",
        )

        self.set_Patch(Patch)
        self.set_ax(ax)
        self.reset_Trans()
