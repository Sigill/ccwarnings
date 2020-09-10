#!/bin/bash -x

cppcheck --enable=warning,style,performance,portability --language=c++ main-1.cpp 2>&1 >/dev/null | sed 's/main-1.cpp/main.cpp/g' | tee cppcheck-1.log
cppcheck --enable=warning,style,performance,portability --language=c++ main-2.cpp 2>&1 >/dev/null | sed 's/main-2.cpp/main.cpp/g' | tee cppcheck-2.log

g++ -W -Wall -Wextra main-1.cpp 2>&1 >/dev/null | sed 's/main-1.cpp/main.cpp/g' | tee warnings-1.log
g++ -W -Wall -Wextra main-2.cpp 2>&1 >/dev/null | sed 's/main-2.cpp/main.cpp/g' | tee warnings-2.log
