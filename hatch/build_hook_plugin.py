from pathlib import Path
from subprocess import run
from sysconfig import get_platform
from typing import Any

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class SpecialBuildHook(BuildHookInterface):

    def initialize(
        self,
        version: str,  # noqa: ARG002
        build_data: dict[str, Any],
    ) -> None:
        platform_id = get_platform()
        # we have platform-specific builds
        build_data['pure_python'] = False
        # the platform tag must have been written as part of the build process
        platform_tag = Path(
            'git-annex', 'dist', 'platform-tag'
        ).read_text().strip()
        # set a tag that says: any python3 for the build platform
        build_data['tag'] = f'py3-none-{platform_tag}'

        if platform_id.startswith('win'):
            # assumes that git-annex has been built with libmagic support in the
            # way that the github action does
            for k, v in (
                # from, to
                ('git-annex/git-annex.exe', 'git_annex/git-annex.exe'),
                ('git-annex/libmagic-1.dll', 'git_annex/libmagic-1.dll'),
                ('git-annex/libgnurx-0.dll', 'git_annex/libgnurx-0.dll'),
            ):
                build_data['force_include'][k] = v
        else:
            build_data['force_include']['git-annex/git-annex'] = \
                'git_annex/git-annex'

        # if the build process produced a file magic DB, we ship it
        if Path('git-annex', 'magic.mgc').exists():
            build_data['force_include']['git-annex/magic.mgc'] = \
                'git_annex/magic.mgc'

        build_cmds = []
        if self.config.get('build') == 'stack':
            build_cmds = [
                ['stack', 'setup'],
                ['stack', 'build', '--no-haddock'],
                ['stack', 'install', '--no-haddock', '--local-bin-path', '.'],
            ]

        for cmd in build_cmds:
            run(cmd, cwd=self.root, check=True)
