# -*- coding: utf-8 -*-

from BeamLinePatches import dipolePatch, sourcePatch, aperturePatch
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()

ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)

ax.add_patch(dipolePatch(ax, 45, 1, 0.1))
ax.add_patch(dipolePatch(ax, -45, 1, 0.1))
ax.add_patch(aperturePatch(1, 0.1, 0.2)[1])
ax.add_patch(aperturePatch(1, 0.1, 0.2)[0])
ax.add_patch(sourcePatch(0.2, 0.5))
ax.legend()


from BeamLinePatches import transformPatchYZ

testRot = np.array(
    [
        [0.1, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
    ]
)
testdR = np.array([0.0, 0.5, -0.5, 0.0])

transPatch = dipolePatch(ax, 45, 1, 0.1)

transPatch = transformPatchYZ(ax, transPatch, testRot, testdR)

ax.add_patch(transPatch)

plt.savefig("99-Scratch/BeamLinePatches.pdf")
