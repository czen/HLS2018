#!/bin/bash

# wget <clang-binaries-tarball-url> #  or `curl -O <url>`
# tar xf clang*

../../../clang/bin/clang++ -S -emit-llvm $1