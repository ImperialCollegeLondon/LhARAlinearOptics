# -*- coding: utf-8 -*-

from BeamLinePatches import dipolePatch, sourcePatch, aperturePatch
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)

ax.add_patch(dipolePatch(ax, 45, 1, 0.1))
ax.legend()

plt.savefig("99-Scratch/BeamLinePatches.pdf")
