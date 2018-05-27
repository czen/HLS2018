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
test_line = 'File E:\\work\\CHStone\\CHStone_v1.11_150204\\aes\\aes_enc.c: 267 tokens, 130 lines'
file_match = 'File (?P<path>.:([\\\\][^:]*)*): (?P<number1>[0-9]*) tokens, (?P<number2>[0-9]*) lines'
m = re.search(file_match, test_line)
print(m.groups())
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

    def get_total_lines(self):
        return self.file1_end_line - self.file1_start_line_line + self.file2_end_line - self.file2_start_line
#%%
# parse similarity_tester logs from file

import ntpath

def gather_stats(report_path):
    stats = []
    blocks = []
    files = {}
    file_match = 'File (?P<path>.:([\\\\][^:]*)*): (?P<number1>[0-9]*) tokens, (?P<number2>[0-9]*) lines'
    report_match = '(?P<stop>#?)(?P<path1>.:([\\\\][^:]*)*): line (?P<number1>[0-9]*)-(?P<number2>[0-9]*)\|(?P<path2>.:([\\\\][^:]*)*): line (?P<number3>[0-9]*)-(?P<number4>[0-9]*)\[(?P<chcount>[0-9]*)\]'
    with open(report_path) as report:
        next_line = report.readline()
        while next_line != '':
            match = re.match(report_match, next_line)
            if match is not None:
                stats.append(match.groupdict())
                blocks.append(MatchingBlock(match.groupdict()))
            else:
                match = re.match(file_match, next_line)
                if match is not None:
                    files[ntpath.basename(match.group('path'))] = int(match.group('number2'))
            next_line = report.readline()
    return stats, files, blocks

test_path = Path('data/CHStone_similarity_tester/aes.txt')
stats, files, blocks = gather_stats(test_path)
#print(stats)

def print_stats(stats):
    print('Number of blocks: ', len(stats))
    commented_count = 0
    for block in stats:
        if block.commented:
            commented_count+=1
    print('Number of commented out blocks: ', commented_count)

print_stats(blocks)
print(files)
#import json
#print(json.dumps(stats))

#%%
# parse similarity_tester reports from folder

def collect_folder_stats(path, ext):
    programs = []
    for file in os.listdir(path):
        if file.endswith(ext):
            stats, files, blocks = gather_stats(Path(path, file));
            programs.append({'name': file, 'blocks': blocks, 'files': files})
    return programs

#report_folder = 'E:/work/HLS2018/CHStone/CHStone_similarity_tester'
report_folder = 'E:/work/HLS2018/RosettaBench/rosetta_similarity_tester'
programs = collect_folder_stats(report_folder, '.txt')
print(programs)


#%%

def print_stats_table(stats):
    table = ''
    for program in stats:
        name = program["name"]
        blocks = program["blocks"]
        files = program["files"]
        num_blocks = 0
        percent_lines = 0
        for block in blocks:
            if not block.commented:
                num_blocks += 1
        lines = []
        files_start = {}
        current_length = 0
        for file in files:
            files_start[file] = current_length
            for i in range(0, files[file]):
                lines.append(1)
                current_length += 1
        for block in blocks:
            if block.commented:
                continue
            fname = block.file1
            if (not fname in files_start):
                continue
            for i in range(files_start[fname] + block.file1_start_line-1, files_start[fname] + block.file1_end_line):
                lines[i] = 0
            fname = block.file2
            for i in range(files_start[fname] + block.file2_start_line-1, files_start[fname] + block.file2_end_line):
                lines[i] = 0

        total_lines = 0
        dup_lines = 0
        for i in range(0,len(lines)):
            total_lines += 1
            if (lines[i] == 0):
                dup_lines += 1

        table_row =  '| ' + name + ' | ' + str(total_lines) + ' | ' + str(num_blocks) + ' | ' + "{0:.2f}".format(100*dup_lines/total_lines) + '% | ' + str(dup_lines) + '| \n'
        table += table_row
    return table


t = print_stats_table(programs)
print(t)
#%%