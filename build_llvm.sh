#!/bin/bash

cd ..
wget http://releases.llvm.org/3.8.1/llvm-3.8.1.src.tar.xz
tar xf llvm-3.8.1.src.tar.xz
rm llvm-3.8.1.src.tar.xz
cd llvm-3.8.1.src
cd tools
wget http://releases.llvm.org/3.8.1/cfe-3.8.1.src.tar.xz
tar xf cfe-3.8.1.src.tar.xz
rm cfe-3.8.1.src.tar.xz
mv cfe-3.8.1.src clang
cd ../..
mkdir llvm-build  
cd llvm-build  

