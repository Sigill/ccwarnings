#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest
from ccwarnings.utils import filter_warnings, FirstLineMatcher, AnyLineMatcher
import ccwarnings


pkgroot = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


class TestGCCWarnings(unittest.TestCase):
    gcc1 = ["main.cpp:12:33: warning: catching polymorphic type ‘const class std::exception’ by value [-Wcatch-value=]",
            "   } catch (const std::exception ex) {",
            "                                 ^~"]
    gcc2 = ["main.cpp:20:27: warning: conversion from ‘double’ to ‘int’ changes value from ‘3.1400000000000001e+0’ to ‘3’ [-Wfloat-conversion]",
            "   std::cout << f(argv[0], 3.14) << std::endl;",
            "                           ^~~~"]
    gcc3 = ["main.cpp:17:14: warning: unused parameter ‘argc’ [-Wunused-parameter]",
            " int main(int argc,",
            "          ~~~~^~~~"]
    gcc4 = ["main.cpp:5:6: warning: ‘void {anonymous}::g()’ defined but not used [-Wunused-function]",
            " void g() {",
            "      ^"]

    cppcheck1 = ["main.cpp:12:5: style: Exception should be caught by reference. [catchExceptionByValue]",
                 "  } catch (const std::exception ex) {",
                 "    ^"]

    cppcheck2 = ["main.cpp:9:33: performance: Function parameter 's' should be passed by const reference. [passedByValue]",
                 "std::string f(const std::string s, int i) {",
                 "                                ^"]

    @staticmethod
    def parse_warnings(filename):
        with open(os.path.join(pkgroot, filename)) as f:
            txt = f.read().splitlines()
        warnings = [warning for warning in ccwarnings.utils.parse_warnings(txt)]
        return warnings

    def assert_parsed_warnings(self, filename, expected):
        warnings = TestGCCWarnings.parse_warnings(filename)
        self.assertListEqual(warnings, expected)

    def test_parse_warnings_gcc(self):
        self.assert_parsed_warnings('test/gcc-warnings.txt', [self.gcc1, self.gcc2, self.gcc3, self.gcc4])

    def test_parse_warnings_cppcheck(self):
        self.assert_parsed_warnings('test/cppcheck.txt', [self.cppcheck1, self.cppcheck2])

    def test_filter(self):
        warnings = TestGCCWarnings.parse_warnings('test/gcc-warnings.txt')
        self.assertListEqual(list(filter_warnings(warnings,
                                                  include=[FirstLineMatcher('std')])),
                             [self.gcc1])
        self.assertListEqual(list(filter_warnings(warnings,
                                                  include=[AnyLineMatcher('unused')])),
                             [self.gcc3, self.gcc4])
        self.assertListEqual(list(filter_warnings(warnings,
                                                  exclude=[AnyLineMatcher('int main')])),
                             [self.gcc1, self.gcc2, self.gcc4])
        self.assertListEqual(list(filter_warnings(warnings,
                                                  include=[AnyLineMatcher('{')],
                                                  exclude=[FirstLineMatcher('{')])),
                             [self.gcc1])

    def test_fuzzy(self):
        warnings = TestGCCWarnings.parse_warnings('test/gcc-warnings.txt')
        warnings = ["\n".join(lines) for lines in warnings]
        w = """main.cpp:8:14: warning: unused parameter ‘argc’ [-Wunused-parameter]
 int main(int argc,
          ~~~~^~~~"""
        self.assertTrue(ccwarnings.utils.fuzzy_find(w, warnings, 3))
        self.assertFalse(ccwarnings.utils.fuzzy_find(w, warnings, 2))


if __name__ == '__main__':
    unittest.main()
