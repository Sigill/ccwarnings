#!/usr/bin/env python

import re
import argparse
from argparse import RawTextHelpFormatter
from gccwarnings import VERSION, parse_warnings, filter_warnings, fuzzy_find


def regex_arg(string):
    try:
        return re.compile(string)
    except re.error:
        msg = "%s is not a regex" % string
        raise argparse.ArgumentTypeError(msg)


def positive_int(string):
    i = int(string)
    if i < 0:
        raise argparse.ArgumentTypeError("%s is a negative value" % string)
    return i


def main():
    parser = argparse.ArgumentParser(description='Utility to process warnings produced by GCC (and other tools producing GCC-like output).',
                                     formatter_class=RawTextHelpFormatter)
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

    parser.add_argument('--version', '-v', action='version', version='.'.join([str(v) for v in VERSION]))

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
