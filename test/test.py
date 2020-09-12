#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
pkgroot = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, pkgroot)

import re
import unittest

import gccwarnings

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
    warnings = list()
    gccwarnings.parse_warnings(txt, lambda w: warnings.append(w))
    return warnings

  def assert_parsed_warnings(self, filename, expected):
    warnings = TestGCCWarnings.parse_warnings(filename)
    self.assertEqual(warnings, expected)

  def test_parse_warnings_gcc(self):
    self.assert_parsed_warnings('test/warnings-1.log', [self.w1, self.w2, self.w3])

  def test_parse_warnings_cppcheck(self):
    self.assert_parsed_warnings('test/cppcheck-1.log', [self.p1])

  def test_filter(self):
    warnings = TestGCCWarnings.parse_warnings('test/warnings-1.log')
    self.assertEqual(gccwarnings.filter_warnings(warnings, grep1=[re.compile('std')]), [self.w1])
    self.assertEqual(gccwarnings.filter_warnings(warnings, grep=[re.compile('unused')]), [self.w2, self.w3])
    self.assertEqual(gccwarnings.filter_warnings(warnings, grepv=[re.compile('int main')]), [self.w1, self.w3])
    self.assertEqual(gccwarnings.filter_warnings(warnings, grep=[re.compile('{')], grepv1=[re.compile('{')]), [self.w1])

  def test_fuzzy(self):
    warnings = TestGCCWarnings.parse_warnings('test/warnings-1.log')
    warnings = list(["\n".join(lines) for lines in warnings])
    w = """main.cpp:8:14: warning: unused parameter ‘argc’ [-Wunused-parameter]
 int main(int argc,
          ~~~~^~~~"""
    self.assertTrue(gccwarnings.fuzzy_find(w, warnings, 3))
    self.assertFalse(gccwarnings.fuzzy_find(w, warnings, 2))


if __name__ == '__main__':
  unittest.main()
