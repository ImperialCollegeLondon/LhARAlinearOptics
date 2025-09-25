#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LhARALinearOptics utilities:
============================

Methods:
 Version(): Returns most recent tag and most recent commit to git repository.
      Return: List: [ [tagNAME, tagDATETIME], [commitSTRING, commitDATETIME] ]

"""

import git
import os
import datetime as dt

def version():
    Debug = True
    
    LLOversion = []

    if Debug:
        print(" LhARALinearOptics.version start")

    LhARAOpticsPATH = os.getenv('LhARAOpticsPATH')
    if not os.path.isdir(LhARAOpticsPATH):
        raise versionException("LhARAOpticsPATH not set")

    try:
        repo = git.Repo(LhARAOpticsPATH)
    except:
        return ["LhARALinearOptics.version: git repo not found"]
    
    if Debug:
        print("     ----> git repo:", repo)

    tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
    if Debug:
        print("     ----> Most recent tag:", tags[-1])

    tagDT = tags[-1].commit.committed_datetime.strftime("%Y-%m-%d %H:%M:%S")
    if Debug:
        print("         ----> Date time:", tagDT)

    log     = repo.head.reference.log()
    entryDT = dt.datetime.fromtimestamp(log[-1][3][0]).strftime("%Y-%m-%d %H:%M:%S")
    if Debug:
        print("     ----> Most recent commit:", log[-1][4])
        print("         ----> Date time:", entryDT)

    LLOversion = [ \
                   [tags[-1].__str__(),     tagDT], \
                   [log[-1][4].__str__(), entryDT]  \
                  ]

    if Debug:
        print(" <---- LLOversion:", LLOversion)
    
    return LLOversion

class versionException(Exception):
    pass
