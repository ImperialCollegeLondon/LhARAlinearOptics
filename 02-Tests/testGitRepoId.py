#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import git
import os
import datetime as dt

LhARAOpticsPATH = os.getenv('LhARAOpticsPATH')
repo = git.Repo(LhARAOpticsPATH)
tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
print(tags)

tagDT = tags[-1].commit.committed_datetime
print(tagDT, type(tagDT), tagDT.strftime("%Y-%m-%d %H:%M:%S"))

master = repo.head.reference
print(master)
log    = master.log()
print("Last entry:", log[-1])

entry = log[-1]
print(entry, type(entry))

entryDT = dt.datetime.fromtimestamp(entry[3][0])
print(entryDT, type(entryDT), entryDT.strftime("%Y-%m-%d %H:%M:%S"))


exit()
print(log)


Commit = False
print("    Length:", len(log))
"""
for iEnt in range(len(log)):
    print(iEnt, log[iEnt])
"""
