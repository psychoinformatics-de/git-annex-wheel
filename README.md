# Python wheel package for git-annex

[![Test git-annex wheel from PyPi](https://github.com/psychoinformatics-de/git-annex-wheel/actions/workflows/test-pypi-wheel.yaml/badge.svg)](https://github.com/psychoinformatics-de/git-annex-wheel/actions/workflows/test-pypi-wheel.yaml)

## Why?

[Git-annex](https://git-annex.branchable.com/) is written in Haskell and plenty
of [installation methods](https://git-annex.branchable.com/install/) are
available. However, for deploying git-annex as a dependency of a Python
library/application, like [DataLad](https://datalad.org) or
[AnnexRemote](https://github.com/Lykos153/AnnexRemote), system packages
are a lot less flexible than Python's virtual environments, and other methods
are more complex and fragile.

With git-annex being available from PyPi, versioned dependencies and deployment
in application-specific environments are possible via standard means of Python
packaging.

## Caveats

A standard git-annex deployment is (primarily) a single binary (`git-annex`),
and a bunch of symlinks that make this one binary fulfilled multiple roles
(`git-annex-shell`, `git-remote-annex`, etc.). A Python wheel, however, is a
ZIP file container with no support for symlinks, and also no support for
"post-install" scripts.

In order to square this circle, the git-annex binary is wrapped via regular
Python entrypoint scripts that handle calling git-annex as necessary. This
delivers a cross-platform compatible wheel, but at a start-up cost (~30ms vs
~11ms on my laptop).

## Installation

Get the package from [PyPi](https://pypi.org/project/git-annex/), and install like
any other package from PyPi.

[uv](https://docs.astral.sh/uv/) users can deploy git-annex in a dedicated virtual
environment via the one-liner:

```
uv tool install git-annex
```

## git-annex build configuration

Git-annex is built with libmagic support, but without the git-annex assistant.
The primary purpose of this package is to provide git-annex (as a dependency),
installed in a virtual environment. Users of the git-annex assistant application
likely install git-annex via any of its platform packages.

## Platform notes

### Linux

The `manylinux` wheel is self-contained and includes copies of all libraries.
It only depends on the declared GLIBC versions.
The `magic.mgc` database is not included, and is assumed to be available on
the target system. Install it separately, if needed (e.g., `libmagic-mgc`
package).

### Windows

The wheel is self-contained and includes a copy of libmagic and the `magic.mgc` database.

### Mac

Git-annex is built with libmagic support, but the library is not included and needs
to be deployed separately.


## Developer information

### Sources

The sources for this package are available at
https://github.com/psychoinformatics-de/git-annex-wheel

The repository tracks the git-annex sources as a Git submodule.

### Issues

For issues related to the Python wheel packaging of git-annex, please
use the tracker at https://github.com/psychoinformatics-de/git-annex-wheel/issues

### How to update for a new git-annex release?

Advance the submodule `./git-annex` to the new release tag.

Now adjust the package version in `pyproject.toml` accordingly. This version
must follow the [rules for Python
packages](https://packaging.python.org/en/latest/discussions/versioning/).

The included (GitHub) action workflows will build a corresponding wheel
and upload it to PyPi.


## Acknowledgements

This work was funded, in part, by

- Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) under grant TRR 379 (546006540, Q02 project)
- Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) under grant SFB 1451 (431549029, INF project)
- MKW-NRW: Ministerium für Kultur und Wissenschaft des Landes Nordrhein-Westfalen under the Kooperationsplattformen 2022 program, grant number: KP22-106A
