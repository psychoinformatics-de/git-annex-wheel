# Python wheel package for git-annex

https://pypi.org/project/git-annex/

[uv](https://docs.astral.sh/uv/) users can deploy git-annex in a dedicated virtual
environment via the one-liner:

```
uv tool install git-annex
```

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

### How to update for a new git-annex release?

TODO
