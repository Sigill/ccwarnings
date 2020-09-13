# gcc-warnings

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
$ gcc-warnings -h
usage: gcc-warnings [-h] [--diff file] [--dst N] [--grep regex [regex ...]]
                    [--grep1 regex [regex ...]] [--grepv regex [regex ...]]
                    [--grepv1 regex [regex ...]] [--sep string] [--version]
                    file

Utility to process warnings produced by GCC (and other tools producing GCC-like output).

positional arguments:
  file                  Input set of warnings.

optional arguments:
  -h, --help            show this help message and exit
  --diff file           Previous set of warnings to diff from.
  --dst N               Edition distance threshold used to identify new warnings (wrt the previous set of warnings).
                        Warnings with an edition distance < to this value will be considered as already known and will be dropped.
  --grep regex [regex ...]
                        Will only print warnings matching this expression.
  --grep1 regex [regex ...]
                        Will only print warnings whose first line matches this expression.
  --grepv regex [regex ...]
                        Will not print warnings matching this expression.
  --grepv1 regex [regex ...]
                        Will not print warnings whose first line matches this expression.
  --sep string          Optional separator to print between entries.
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
pip install dist/gcc-warnings*.whl
```

## Test

```
./test/test.py
```

## License

This tool is released under the terms of the MIT License. See the LICENSE.txt file for more details.
