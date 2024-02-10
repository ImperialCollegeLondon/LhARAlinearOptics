# -*- coding: utf-8 -*-

from BeamLinePatches import dipolePatch, sourcePatch, aperturePatch
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()

ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)

dipolePatch(ax, 45, 1, 0.1).render_Patch()
dipolePatch(ax, -45, 1, 0.1).render_Patch()
aperturePatch(ax, 1, 0.1, 0.2).render_Patch()
sourcePatch(ax, 0.2, 0.5).render_Patch()

testRot = np.array(
    [
        [0.1, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
    ]
)
testdR = np.array([0.0, 1, 0.1, 0.0])

dipolePatch(ax, 45, 1, 0.1).transformPatchYZ(testRot, testdR).render_Patch()

ax.legend()


plt.savefig("99-Scratch/BeamLinePatches.pdf")

fig2, ax2 = plt.subplots()

ax2.set_xlim(-2, 2)
ax2.set_ylim(-2, 2)

for i in range(10):

    patchBLE = sourcePatch(ax2, 0.5, 0.5)

    Rot2Lab = np.eye(3)

    R2Lab = np.array([0.1, 0.2, 0.3 - 0.1 * i, 0.4])

    patchBLE.transformPatchYZ(Rot2Lab, R2Lab)
    patchBLE.render_Patch()

for i in range(10):

    patchBLE = dipolePatch(ax2, 45, 1, 0.1)

    Rot2Lab = np.eye(3)

    R2Lab = np.array([0.1, 0.2, 0.3 + 0.1 * i, 0.4])

    patchBLE.transformPatchYZ(Rot2Lab, R2Lab)
    patchBLE.render_Patch()

ax2.legend()
plt.savefig("99-Scratch/BeamLinePatches2.pdf")
