#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
  --------  ----------  --------  ----------  --------  ----------  
   LaTeX module tests
  --------  ----------  --------  ----------  --------  ----------  
'''

#.. Import necessary modules:
import LaTeX as Tx

#%%
#.. Test table-header method:
i = 1
Tx.TableHeader()
Tx.TableHeader('99-Scratch/MyLaTeX.tex', '|l|c|r|')

#%%
#.. Test table-line method:
i += 1
Tx.TableLine()
Tx.TableLine('99-Scratch/MyLaTeX.tex', '|3|4|5|')

#%%
#.. Test table-trailer method:
i += 1
Tx.TableTrailer()
Tx.TableTrailer('99-Scratch/MyLaTeX.tex')
