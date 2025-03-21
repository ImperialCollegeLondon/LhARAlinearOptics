#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Profile statistics formatter
============================


"""
import pstats
from pstats import SortKey

p = pstats.Stats('99-Scratch/restats')

"""
p.strip_dirs().sort_stats(-1).print_stats()
p.sort_stats(SortKey.TIME, SortKey.CUMULATIVE).print_stats(.5, 'init')

"""

p.sort_stats(SortKey.TIME).print_stats(20)
