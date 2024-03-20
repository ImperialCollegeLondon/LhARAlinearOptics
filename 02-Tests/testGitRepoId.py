#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import git
import os

LhARAOpticsPATH = os.getenv('LhARAOpticsPATH')
repo = git.Repo(LhARAOpticsPATH)
tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
print(tags)

head   = repo.head
master = head.reference
log    = master.log()
Commit = False
print("Last entry:", log[-1])
print("    Length:", len(log))
for iEnt in range(len(log)):
    print(iEnt, log[iEnt])
