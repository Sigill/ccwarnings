# gcc-warnings

Utility to process issues (warnings, errors) emmited by [GCC](https://gcc.gnu.org/) (and others tools like [clang](https://clang.llvm.org/), [clang-tidy](https://clang.llvm.org/extra/clang-tidy/), [cppcheck](http://cppcheck.sourceforge.net/)...).

## Details

When emmiting warnings, GCC will print them continuously on the standard output.

Each entry can span multiple lines, eventually containing additional notes describing more details of the issue.

This tool allows to group related lines into a single entity and apply grep-filters on them.


## License

This tool is released under the terms of the MIT License. See the LICENSE.txt file for more details.
