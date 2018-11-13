#!/bin/bash
git clone git://github.com/libffi/libffi.git

sudo apt-get install autoconf automake libtool
sudo apt-get install texinfo

cd libffi
./autogen.sh
./configure
make
sudo make install     

# http://lists.llvm.org/pipermail/llvm-bugs/2013-July/029324.html
 cmake