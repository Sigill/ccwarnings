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
    maxDiff = None

    gcc1 = [u"main.cpp:26:27: warning: conversion from ‘double’ to ‘int’ changes value from ‘1.23456e+2’ to ‘123’ [-Wfloat-conversion]",
            u"     return bad_conversion(123.456);",
            u"                           ^~~~~~~"]
    gcc2 = [u"main.cpp:27:33: warning: catching polymorphic type ‘const class std::exception’ by value [-Wcatch-value=]",
            u"   } catch (const std::exception ex) {",
            u"                                 ^~"]
    gcc3 = [u"main.cpp:6:6: warning: ‘void {anonymous}::useless_function()’ defined but not used [-Wunused-function]",
            u" void useless_function() {}",
            u"      ^~~~~~~~~~~~~~~~"]
    gcc4 = [u"main.cpp:15:30: warning: ‘%d’ directive output truncated writing 9 bytes into a region of size 7 [-Wformat-truncation=]",
            u"   snprintf(buf, sizeof(buf), \"#%d\", i);",
            u"                              ^~~~~",
            u"main.cpp:15:11: note: ‘snprintf’ output 11 bytes into a destination of size 8",
            u"   snprintf(buf, sizeof(buf), \"#%d\", i);",
            u"   ~~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~"]

    clang1 = [u"main.cpp:26:27: warning: implicit conversion from 'double' to 'int' changes value from 123.456 to 123 [-Wliteral-conversion]",
              u"    return bad_conversion(123.456);",
              u"           ~~~~~~~~~~~~~~ ^~~~~~~"]
    clang2 = [u"main.cpp:6:6: warning: unused function 'useless_function' [-Wunused-function]",
              u"void useless_function() {}",
              u"     ^"]

    cppcheck1 = [u"main.cpp:27:5: style: Exception should be caught by reference. [catchExceptionByValue]",
                 u"  } catch (const std::exception ex) {",
                 u"    ^"]

    cppcheck2 = [u"main.cpp:9:51: performance: Function parameter 's' should be passed by const reference. [passedByValue]",
                 u"std::string should_pass_by_cref(const std::string s, int i) {",
                 u"                                                  ^"]

    @staticmethod
    def parse_warnings(filename, fmt):
        with open(os.path.join(pkgroot, filename), 'rb') as f:
            txt = f.read().decode("UTF-8").splitlines()
            return [warning for warning in ccwarnings.utils.parse_warnings(txt, fmt)]

    def assert_parsed_warnings(self, fmt, filename, expected):
        warnings = TestGCCWarnings.parse_warnings(filename, fmt)
        self.assertListEqual(warnings, expected)

    def test_parse_warnings_gcc(self):
        self.assert_parsed_warnings('gcc', 'test/gcc-warnings.txt', [self.gcc1, self.gcc2, self.gcc3, self.gcc4])

    def test_parse_warnings_clang(self):
        self.assert_parsed_warnings('clang', 'test/clang-warnings.txt', [self.clang1, self.clang2])

    def test_parse_warnings_cppcheck(self):
        self.assert_parsed_warnings('cppcheck', 'test/cppcheck.txt', [self.cppcheck1, self.cppcheck2])

    def test_filter(self):
        warnings = TestGCCWarnings.parse_warnings('test/gcc-warnings.txt', 'gcc')
        self.assertListEqual(list(filter_warnings(warnings,
                                                  include=[FirstLineMatcher('-Wfloat-conversion')])),
                             [self.gcc1])
        self.assertListEqual(list(filter_warnings(warnings,
                                                  include=[AnyLineMatcher('bad_conversion')])),
                             [self.gcc1])
        self.assertListEqual(list(filter_warnings(warnings,
                                                  exclude=[AnyLineMatcher('anonymous')])),
                             [self.gcc1, self.gcc2, self.gcc4])
        self.assertListEqual(list(filter_warnings(warnings,
                                                  include=[AnyLineMatcher('value')],
                                                  exclude=[AnyLineMatcher('catch-value')])),
                             [self.gcc1])

    def test_fuzzy(self):
        warnings = TestGCCWarnings.parse_warnings('test/gcc-warnings.txt', 'gcc')
        warnings = ["\n".join(lines) for lines in warnings]
        w = u"""main.cpp:32:33: warning: catching polymorphic type ‘const class std::exception’ by value [-Wcatch-value=]
   } catch (const std::exception ex) {
                                 ^~"""
        self.assertTrue(ccwarnings.utils.fuzzy_find(w, warnings, 3))
        self.assertFalse(ccwarnings.utils.fuzzy_find(w, warnings, 2))


if __name__ == '__main__':
    unittest.main()
