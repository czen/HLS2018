# -*- coding: utf-8 -*-
"""
Read similarity_tester output and count 
number of duplicates, number of duplicated lines,
percentages, etc.
"""
#%%
import os
from pathlib import Path

os.chdir(Path("E:/work/HLS2018/repo/Duplicates/"))

#%%

# how to use pathlib: https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f

print('current working directory: ' + os.getcwd())

CHStonePath = Path("data/CHStone_similarity_tester")
input_file = CHStonePath / "aes.txt"
file_in = open(input_file)
#print(input_file.read_text())
#print(file_in.readlines())
#%%
# regular expression examples
import re
m = re.search('abc','abcdefg abc ')
print(m.group(0))
m = re.search('(?P<path1>.:(/[^:]*)*)', 'E:/path/to/smth/asf: assfasf ');
print(m.group("path1"))


#E:\work\CHStone\CHStone_v1.11_150204\aes\aes_func.c: line 384-396
# |E:\work\CHStone\CHStone_v1.11_150204\aes\aes_func.c: line 396-408[122]
#%%
m = re.search('(?P<path1>.:(\\\\[^:]*)*)', 'E:\\path\\to\\smth\\asf.c: line 333-222 ');
print(m.group("path1"))
#%%

m = re.search('(?P<path1>.:(/[^:]*)*)', 'E:/path/to/smth/asf.c: line 333-222 ');
print(m.group("path1"))
path1 = '(?P<path1>.:(/[^:]*)*'
path2 = '(?P<path2>.:(/[^:]*)*'
lines1 = '(?P<lines1>line (?P<number1>[0-9]*)-(?P<number2>[0-9]*))'
print(re.search(lines1,'line 333-222').groups())

#%%
test_line = "E:\\work\\CHStone\\CHStone_v1.11_150204\\aes\\aes_func.c: line 384-396|E:\\work\\CHStone\\CHStone_v1.11_150204\\aes\\aes_func.c: line 396-408[122]"
report_match = '(?P<path1>.:([\\\\][^:]*)*): line (?P<number1>[0-9]*)-(?P<number2>[0-9]*)\|(?P<path2>.:([\\\\][^:]*)*): line (?P<number3>[0-9]*)-(?P<number4>[0-9]*)\[(?P<chcount>[0-9]*)\]'
m = re.search(report_match, test_line)
print(m.group('path1'))
print(m.group('path2'))
print(m.group('number1'))
print(m.group('number2'))
print(m.group('number3'))
print(m.group('number4'))
print(m.group('chcount'))
#%%

import ntpath
class MatchingBlock:

    def __init__(self, dict):
        self.file1 = ntpath.basename(dict['path1'])
        self.file2 = ntpath.basename(dict['path1'])
        self.file1_start_line = int(dict['number1'])
        self.file1_end_line = int(dict['number2'])
        self.file2_start_line = int(dict['number3'])
        self.file2_end_line = int(dict['number4'])
        self.char_count = dict['chcount']
        self.commented = dict['stop'] == '#'
#%%

def gather_stats(report_path):
    stats = []
    blocks = []
    report_match = '(?P<stop>#?)(?P<path1>.:([\\\\][^:]*)*): line (?P<number1>[0-9]*)-(?P<number2>[0-9]*)\|(?P<path2>.:([\\\\][^:]*)*): line (?P<number3>[0-9]*)-(?P<number4>[0-9]*)\[(?P<chcount>[0-9]*)\]'
    with open(report_path) as report:
        next_line = report.readline()
        while next_line != '':
            match = re.match(report_match, next_line)
            if match is not None:
                stats.append(match.groupdict())
                blocks.append(MatchingBlock(match.groupdict()))
            next_line = report.readline()
    return stats,blocks

test_path = Path('data/CHStone_similarity_tester/aes.txt')
stats, blocks = gather_stats(test_path)
#print(stats)

def print_stats(stats):
    print('Number of blocks: ', len(stats))
    commented_count = 0
    for block in stats:
        if block.commented:
            commented_count+=1
    print('Number of commented out blocks: ', commented_count)

print_stats(blocks)