import os.path as op
import sys


def get_executable():
    return op.join(
        op.dirname(__file__),
        f'git-annex{".exe" if sys.platform.startswith("win") else ""}',
    )
