import os
import os.path as op
import sys


def cli():
    """Emulate a symlink to a binary.

    This script essentially calls the `git-annex` binary that is shipped
    with the package, but using the `argv` list (including a potentially
    different executable name) pass to the script itself.

    It relies on the `executable` argument of `subprocess.run()` to achieve
    this.

    This approach provides alternative means for git-annex's installation
    method with symlinks pointing to a single binary, and works on platforms
    without symlink support, and also in packages that cannot represent
    symlinks.
    """
    executable = op.join(
        op.dirname(__file__),
        f'git-annex{".exe" if sys.platform.startswith("win") else ""}',
    )
    os.execv(executable, sys.argv)
