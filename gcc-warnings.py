#!/usr/bin/env python

import sys
import re
import argparse
from argparse import RawTextHelpFormatter

class GCCWarningsProcessor(object):
  def __init__(self, grep1=[], grep=[], grepv1=[], grepv=[], sep=None):
    self.start_re = re.compile('^[^:]*:[0-9]+:[0-9]+: (warning|error)')
    self.grep1  = grep1
    self.grep   = grep
    self.grepv1 = grepv1
    self.grepv  = grepv
    self.sep    = sep

  @staticmethod
  def __print_warning(lines):
    for l in lines:
      sys.stdout.write(l)

  def keep_warning(self, lines):
    if len(self.grepv1) > 0 and any(p.search(lines[0]) for p in self.grepv1):
      return False
    if len(self.grepv) > 0 and any(any(p.search(l) for l in lines) for p in self.grepv):
      return False

    if len(self.grep1) > 0 or len(self.grep) > 0:
      match = False
      if len(self.grep1) > 0:
        match = any(p.search(lines[0]) for p in self.grep1)
      if not match and len(self.grep) > 0:
        match = any(any(p.search(l) for l in lines) for p in self.grep)
      if not match:
        return False

    return True

  def __process_warning(self, lines):
    while len(lines[-1].rstrip()) == 0:
      del lines[-1]

    if self.keep_warning(lines):
      if self.sep is not None:
        print(self.sep)
      GCCWarningsProcessor.__print_warning(lines)

  def process_warnings(self, iterable):
    warning = None
    for line in iterable:
      if self.start_re.match(line):
        if warning is not None:
          self.__process_warning(warning)

        warning = [line]
      elif warning is not None:
        warning.append(line)

    if warning is not None:
      self.__process_warning(warning)

def compile_patterns(patterns):
  if patterns is None or len(patterns) == 0:
    return []
  return [re.compile(r) for r in patterns]

def main():
  parser = argparse.ArgumentParser(description='.', formatter_class=RawTextHelpFormatter)
  parser.add_argument('--sep', dest='sep', metavar='separator', default=None,
                      help='Add separator between entries.')
  parser.add_argument('--grep', dest='grep', metavar='regex', action='append',
                      help='Will only print warnings matching this expression.')
  parser.add_argument('--grep1', dest='grep1', metavar='regex', action='append',
                      help='Will only print warnings whose first line matches this expression.')
  parser.add_argument('--grepv', dest='grepv', metavar='regex', action='append',
                      help='Will not print warnings matching this expression.')
  parser.add_argument('--grepv1', dest='grepv1', metavar='regex', action='append',
                      help='Will not print warnings whose first line matches this expression.')

  args = parser.parse_args()

  processor = GCCWarningsProcessor(grep1=compile_patterns(args.grep1), grep=compile_patterns(args.grep), grepv1=compile_patterns(args.grepv1), grepv=compile_patterns(args.grepv), sep=args.sep)

  processor.process_warnings(sys.stdin)

if __name__ == '__main__':
    main()
