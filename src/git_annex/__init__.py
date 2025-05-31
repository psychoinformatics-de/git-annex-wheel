import os.path as op
import subprocess
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
    exe_dir = op.dirname(__file__)
    exe = op.join(
        exe_dir,
        op.basename(sys.argv[0]),
    )
    args = [exe] + sys.argv[1:]
    try:
        subprocess.run(
            args,
            executable=op.join(
                exe_dir,
                f'git-annex{".exe" if sys.platform.startswith("win") else ""}',
            ),
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
