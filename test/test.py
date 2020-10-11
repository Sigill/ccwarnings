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
    w1 = ["main.cpp:12:33: warning: catching polymorphic type ‘const class std::exception’ by value [-Wcatch-value=]",
          "   } catch (const std::exception ex) {",
          "                                 ^~"]
    w2 = ["main.cpp:17:14: warning: unused parameter ‘argc’ [-Wunused-parameter]",
          " int main(int argc,",
          "          ~~~~^~~~"]
    w3 = ["main.cpp:5:6: warning: ‘void {anonymous}::g()’ defined but not used [-Wunused-function]",
          " void g() {",
          "      ^"]

    p1 = ["main.cpp:12:5: style: Exception should be caught by reference. [catchExceptionByValue]",
          "  } catch (const std::exception ex) {",
          "    ^"]

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
        self.assert_parsed_warnings('test/gcc-warnings-1.txt', [self.w1, self.w2, self.w3])

    def test_parse_warnings_cppcheck(self):
        self.assert_parsed_warnings('test/cppcheck-1.txt', [self.p1])

    def test_filter(self):
        warnings = TestGCCWarnings.parse_warnings('test/gcc-warnings-1.txt')
        self.assertListEqual(list(filter_warnings(warnings,
                                                  include=[FirstLineMatcher('std')])),
                             [self.w1])
        self.assertListEqual(list(filter_warnings(warnings,
                                                  include=[AnyLineMatcher('unused')])),
                             [self.w2, self.w3])
        self.assertListEqual(list(filter_warnings(warnings,
                                                  exclude=[AnyLineMatcher('int main')])),
                             [self.w1, self.w3])
        self.assertListEqual(list(filter_warnings(warnings,
                                                  include=[AnyLineMatcher('{')],
                                                  exclude=[FirstLineMatcher('{')])),
                             [self.w1])

    def test_fuzzy(self):
        warnings = TestGCCWarnings.parse_warnings('test/gcc-warnings-1.txt')
        warnings = ["\n".join(lines) for lines in warnings]
        w = """main.cpp:8:14: warning: unused parameter ‘argc’ [-Wunused-parameter]
 int main(int argc,
          ~~~~^~~~"""
        self.assertTrue(ccwarnings.utils.fuzzy_find(w, warnings, 3))
        self.assertFalse(ccwarnings.utils.fuzzy_find(w, warnings, 2))


if __name__ == '__main__':
    unittest.main()
