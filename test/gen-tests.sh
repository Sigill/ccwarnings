#!/bin/bash

cppcheck --enable=warning,style,performance,portability --language=c++ main.cpp 2>&1 >/dev/null | tee cppcheck.txt
g++ -W -Wall -Wextra -Wconversion -O2 -c main.cpp 2>&1 >/dev/null | tee gcc-warnings.txt
clang++ -W -Wall -Wextra -Wconversion -O2 -c main.cpp 2>&1 >/dev/null | tee clang-warnings.txt
