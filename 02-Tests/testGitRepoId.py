#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import git


repo = git.Repo(search_parent_directories=True)
tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)

print(tags)
