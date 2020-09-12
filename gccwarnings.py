import re
import editdistance

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

def fuzzy_find(needle, haystack, max_dst=0): # Do not authorize more than max_dst editions.
  for other in haystack:
    dst = editdistance.distance(needle, other)
    if dst < max_dst:
      return True

  return False

