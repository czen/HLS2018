#!/bin/bash

wget http://releases.llvm.org/7.0.0/clang+llvm-7.0.0-x86_64-linux-gnu-ubuntu-16.04.tar.xz #  or `curl -O <url>`
tar xf clang*

git clone https://gitlab.com/cfreksen/llvm--emulator llvm--emulator
cd llvm--emulator

# using pip3 here
pip install .
# now we can just run llvm--emulator

apt-get install graphviz
