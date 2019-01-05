# tox-asdf

[![Build Status](https://travis-ci.com/apihackers/tox-asdf.svg?tag=0.1.0)](https://travis-ci.com/apihackers/tox-asdf)
[![codecov](https://codecov.io/gh/apihackers/tox-asdf/branch/master/graph/badge.svg)](https://codecov.io/gh/apihackers/tox-asdf)
[![Last version](https://img.shields.io/pypi/v/tox-asdf.svg)](https://pypi.python.org/pypi/tox-asdf)
[![License](https://img.shields.io/pypi/l/tox-asdf.svg)](https://pypi.python.org/pypi/tox-asdf)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/tox-asdf.svg)](https://pypi.python.org/pypi/tox-asdf)

A Tox plugin using [asdf] to find python executables.


## Prerequisites

This plugin is made exclusevly to support [asdf] so obviously you will need a functionnal [asdf] installation as well as the [`asdf-python`][asdf-python] plugin.


## Installation

Simply install `tox-asdf` in addition to `tox` to get ready:

```shell
pip install tox tox-asdf
```

That's it, you can now run `tox` as usual but using [asdf] Python installations.

## Options

### No fallback on system pythons

By default this plugin won't fail if a required Python version is missing from `æsdf`, tox will fallback on its classic way of finding Python binaries from `$PATH`.
You can override this behavior and force `tox` to only use `asdf` by using the `--asdf-no-fallback` option:

```shell
tox --asdf-no-fallback
```

### Automatically install pythons

By default, `tox-asdf` won't try to install missing Python version, but you can force this by using the `--asdf-install` option.

```shell
tox --asdf-install
```

Obviously this will only useful on the first run.


[asdf]: https://github.com/asdf-vm/asdf
[asdf-python]: https://github.com/asdf-vm/asdf-python
