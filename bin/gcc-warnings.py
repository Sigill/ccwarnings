#!/usr/bin/env python

import sys
import re
import argparse
from argparse import RawTextHelpFormatter
import editdistance as editdist

def regex_arg(string):
  try:
    return re.compile(string)
  except re.error, ex:
    msg = "%s is not a regex" % string
    raise argparse.ArgumentTypeError(msg)
  except:
    msg = "Unsupported value: %s" % string
    raise argparse.ArgumentTypeError(msg)

def positive_int(string):
  i = int(string)
  if i < 0:
    raise argparse.ArgumentTypeError("%s is a negative value" % string)
  return i

def parse_warnings(iterable, callback):
  ctx_re = re.compile("^[^:\n]+: .*")
  start_re = re.compile('^[^:]*:[0-9]+:[0-9]+: (?!note)\\w+') # Exclude notes as they are used to provide additional informations to the enclosing warning
  warning = None

  for line in iterable:
    if ctx_re.match(line):
      continue
    if start_re.match(line):
      if warning is not None:
        while len(warning[-1].rstrip()) == 0:
          del warning[-1]
        callback(warning)

      warning = [line.rstrip()]
    elif warning is not None:
      warning.append(line.rstrip())

  if warning is not None:
    while len(warning[-1].rstrip()) == 0:
      del warning[-1]
    callback(warning)

class GCCWarningsFilter(object):
  def __init__(self, grep1=[], grep=[], grepv1=[], grepv=[]):
    self.grep1  = grep1
    self.grep   = grep
    self.grepv1 = grepv1
    self.grepv  = grepv

  def __call__(self, lines):
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

def first_line_match(lines, regexes):
  return any(p.search(lines[0]) for p in regexes)

def any_line_match(lines, regex):
  return any(any(p.search(l) for l in lines) for p in regex)

def filter_warnings(warnings, grep1=[], grep=[], grepv1=[], grepv=[]):
  if len(grep1) > 0:
    warnings = filter(lambda lines: first_line_match(lines, grep1), warnings)
  if len(grep) > 0:
    warnings = filter(lambda lines: any_line_match(lines, grep), warnings)

  if len(grepv1) > 0:
    warnings = filter(lambda lines: not first_line_match(lines, grepv1), warnings)
  if len(grepv) > 0:
    warnings = filter(lambda lines: not any_line_match(lines, grepv), warnings)

  return warnings

def fuzzy_find(needle, haystack, max_dst=0): # Do not authorize more than 8 editions.
  for other in haystack:
    dst = editdist.distance(needle, other)
    if dst < max_dst:
      return True

  return False

def main():
  parser = argparse.ArgumentParser(description='Utility to process warnings produced by GCC (and other tools producing GCC-like output).', formatter_class=RawTextHelpFormatter)
  parser.add_argument('input', metavar='file', action='store', type=argparse.FileType('r'),
                      help='Input set of warnings.')
  parser.add_argument('--diff', dest='diff', metavar='file', action='store', type=argparse.FileType('r'),
                      help='Previous set of warnings to diff from.')
  parser.add_argument('--dst', dest='dst', metavar='N', action='store', type=positive_int, default=8,
                      help='Edition distance threshold used to identify new warnings (wrt the previous set of warnings).\n'
                      'Warnings with an edition distance < to this value will be considered as already known and will be dropped.')
  parser.add_argument('--grep', dest='grep', metavar='regex', action='append', type=regex_arg, default=list(),
                      help='Will only print warnings matching this expression.')
  parser.add_argument('--grep1', dest='grep1', metavar='regex', action='append', type=regex_arg, default=list(),
                      help='Will only print warnings whose first line matches this expression.')
  parser.add_argument('--grepv', dest='grepv', metavar='regex', action='append', type=regex_arg, default=list(),
                      help='Will not print warnings matching this expression.')
  parser.add_argument('--grepv1', dest='grepv1', metavar='regex', action='append', type=regex_arg, default=list(),
                      help='Will not print warnings whose first line matches this expression.')
  parser.add_argument('--sep', dest='sep', metavar='string', default='',
                      help='Optional separator to print between entries.')

  args = parser.parse_args()

  warnings = list()
  parse_warnings(args.input.readlines(), lambda w: warnings.append(w))
  warnings = filter_warnings(warnings, grep1=args.grep1, grep=args.grep, grepv1=args.grepv1, grepv=args.grepv)
  warnings = list(["\n".join(lines) for lines in warnings])

  if args.diff is not None:
    prev = list()
    parse_warnings(args.diff.readlines(), lambda w: prev.append(w))
    prev = filter_warnings(prev, grep1=args.grep1, grep=args.grep, grepv1=args.grepv1, grepv=args.grepv)
    prev = list(["\n".join(lines) for lines in prev])

    warnings = [warning for warning in warnings if not fuzzy_find(warning, prev, args.dst)]

  for i, warning in enumerate(warnings):
    if i > 0 and len(args.sep) > 0:
      print(args.sep)

    print(warning)

if __name__ == '__main__':
    main()
