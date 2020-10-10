import re
import editdistance


def parse_warnings(iterable):
    ctx_re = re.compile("^[^:\n]+: .*")
    # Exclude notes as they are used to provide additional information to the enclosing warning
    start_re = re.compile('^[^:]*:[0-9]+:[0-9]+: (?!note)\\w+')
    warning = None

    for line in iterable:
        if ctx_re.match(line):
            continue
        if start_re.match(line):
            if warning is not None:
                while len(warning[-1].rstrip()) == 0:
                    del warning[-1]
                yield warning

            warning = [line.rstrip()]
        elif warning is not None:
            warning.append(line.rstrip())

    if warning is not None:
        while len(warning[-1].rstrip()) == 0:
            del warning[-1]
        yield warning


class FirstLineMatcher(object):
    def __init__(self, pattern):
        self.pattern = re.compile(pattern)

    def __call__(self, lines):
        return self.pattern.search(lines[0])


class AnyLineMatcher(object):
    def __init__(self, pattern):
        self.pattern = re.compile(pattern)

    def __call__(self, lines):
        return any(self.pattern.search(line) for line in lines)


def filter_warnings(warnings, include=[], exclude=[]):
    if len(include) > 0:
        warnings = filter(lambda lines: any(matcher(lines) for matcher in include), warnings)

    if len(exclude) > 0:
        warnings = filter(lambda lines: not any(matcher(lines) for matcher in exclude), warnings)

    return warnings


def fuzzy_find(needle, haystack, dst_threshold=0):
    return any(editdistance.distance(needle, other) < dst_threshold for other in haystack)
