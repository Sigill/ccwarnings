# ccwarnings

Utility to process issues (warnings, errors) emmited by [GCC](https://gcc.gnu.org/) (and others tools like [clang](https://clang.llvm.org/), [clang-tidy](https://clang.llvm.org/extra/clang-tidy/), [cppcheck](http://cppcheck.sourceforge.net/)...).

Required python packages (`pip install -r requirements.txt`):
- argparse
- editdistance

## Details

When producing warnings, GCC will print them continuously on the standard output.

Each entry can span multiple lines, eventually containing additional notes describing more details of the issue.

This tool allows to group related lines into a single entity and apply grep-filters on them, identify new warnings using fuzzy analysis.

## Usage

```
$ ccwarnings -h
usage: ccwarnings [-h] [--diff FILE] [--dst N]
                  [--include PATTERN [PATTERN ...]]
                  [--include1 PATTERN [PATTERN ...]]
                  [--exclude PATTERN [PATTERN ...]]
                  [--exclude1 PATTERN [PATTERN ...]] [--sep STRING] [-c] [-s]
                  [--version]
                  [FILE]

Utility to process warnings produced by GCC (and other tools producing GCC-like output).

positional arguments:
  FILE                  Input warnings (defaults: stdin).

optional arguments:
  -h, --help            show this help message and exit
  --diff FILE           Previous set of warnings to diff from.
  --dst N               To use with --diff to specify the edition distance threshold.
                        Warnings with an edition distance < to this value will be considered as already known
                        and will therefore be ignored (default: 8)
  --include PATTERN [PATTERN ...]
                        Will only keep warnings matching one of the patterns.
  --include1 PATTERN [PATTERN ...]
                        Will only keep warnings whose first line is matching  one of the patterns.
  --exclude PATTERN [PATTERN ...]
                        Will discard warnings matching any of the patterns.
  --exclude1 PATTERN [PATTERN ...]
                        Will discard warnings whose first line is matching any of the patterns.
  --sep STRING          Optional separator to print between entries.
  -c, --count           Only print the number of warnings.
  -s, --short           Only print the first line of the warning.
  --version, -v         show program's version number and exit
```

## Building & packaging

```
virtualenv .venv
source .venv/bin/activate

# Editable install, for development purpose
pip install -e .

# Standard install
python setup.py bdist_wheel --universal # might require pip install wheel
pip install dist/ccwarnings*.whl
```

## Test

```
./test/test.py
```

## License

This tool is released under the terms of the MIT License. See the LICENSE.txt file for more details.
