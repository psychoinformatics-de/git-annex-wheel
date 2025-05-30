import os.path as op
import subprocess
import sys


def cli():
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
        # already
        sys.stdout.flush()
    except BrokenPipeError:
        # setting it to None prevents Python from trying to
        # flush again
        sys.stdout = None
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
