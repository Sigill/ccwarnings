#!/bin/bash -x

cppcheck --enable=warning,style,performance,portability --language=c++ main.cpp 2>&1 >/dev/null | tee cppcheck.txt

g++ -W -Wall -Wextra -Wconversion main.cpp 2>&1 >/dev/null | tee gcc-warnings.txt
