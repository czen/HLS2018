#!/bin/bash
# use https://github.com/mchalupa/dg

tools/llvm-dg-dump $1 > "$1_dg.dot"