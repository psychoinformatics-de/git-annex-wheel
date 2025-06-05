import os
import os.path as op
import sys


def cli():
    """Emulate a symlink to a binary.

    This script essentially calls the `git-annex` binary that is shipped
    with the package, but using the `argv` list (including a potentially
    different executable name) pass to the script itself.

    On Unix-like systems, it `exec`s the binary, replacing the current process.
    Windows does not support `exec`, so in that case, it relies on the
    `executable` argument of `subprocess.run()` to achieve this.

    This approach provides alternative means for git-annex's installation
    method with symlinks pointing to a single binary, and works on platforms
    without symlink support, and also in packages that cannot represent
    symlinks.
    """
    exedir = op.dirname(__file__)
    exe = op.join(exedir, 'git-annex')
    if sys.platform.startswith('darwin'):
        # we look for an embedded file magic DB,
        # and instruct libmagic to use it
        embedded_magic = op.join(exedir, 'magic.mgc')
        if op.exists(embedded_magic):
            os.environ['MAGIC'] = embedded_magic

    if sys.platform.startswith('win'):
        exec_subproc(f'{exe}.exe', sys.argv)
    else:
        os.execv(exe, sys.argv)


def exec_subproc(executable, argv):
    import subprocess

    try:
        subprocess.run(
            argv,
            executable=executable,
            shell=False,
            check=True,
        )
        # try flush here to trigger a BrokenPipeError
        # within the try-except block so we can handle it
        # (happens if the calling process closed stdout
        # already)
        sys.stdout.flush()
    except BrokenPipeError:
        # setting it to None prevents Python from trying to
        # flush again
        sys.stdout = None
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
