# -*- coding: utf-8 -*-
"""
Read similarity_tester output and count 
number of duplicates, number of duplicated lines,
percentages, etc.
"""

#%%
import os
# how to use pathlib: https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f
from pathlib import Path
print('current working directory: ' + os.getcwd())

CHStonePath = Path("data/CHStone_similarity_tester")
input_file = CHStonePath / "aes.txt"
#file_in = open(input_file)
print(input_file.read_text())
#%%

#%%

