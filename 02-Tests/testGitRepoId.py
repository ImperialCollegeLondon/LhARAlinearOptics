#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import git
import os
import datetime as dt

print(" Load git repo")
LhARAOpticsPATH = os.getenv('LhARAOpticsPATH')
repo = git.Repo(LhARAOpticsPATH)

print(" Get tags, order by time")
tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)

print(" Most recent tag:", tags[-1])

tagDT = tags[-1].commit.committed_datetime
print(" Date time of most recent tag:", tagDT)
print('     ----> tagDT.strftime("%Y-%m-%d %H:%M:%S")', \
      tagDT.strftime("%Y-%m-%d %H:%M:%S"))

log = repo.head.reference.log()
"""
print(" Last entry in log:", log[-1])
"""
entryDT = dt.datetime.fromtimestamp(log[-1][3][0])
print(entryDT, type(entryDT), entryDT.strftime("%Y-%m-%d %H:%M:%S"))


exit()
print(log)


Commit = False
print("    Length:", len(log))
"""
for iEnt in range(len(log)):
    print(iEnt, log[iEnt])
"""
