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
            # assumes that git-has been built with libmagic support in the
            # way that the github action does
            build_data['shared_data']['git-annex/libmagic-1.dll'] = \
                'Scripts/libmagic-1.dll'
            build_data['shared_data']['git-annex/libgnurx-0.dll'] = \
                'Scripts/libgnurx-0.dll'
            build_data['shared_data']['git-annex/file.exe'] = \
                'Scripts/file.exe'
            build_data['shared_data']['git-annex/magic.mgc'] = \
                'Scripts/magic.mgc'
            build_data['shared_data']['git-annex/git-annex.exe'] = \
                'Scripts/git-annex.exe'
        else:
            #breakpoint()
            #build_data['shared_data']['git-annex/git-annex'] = \
            #    'platlib/git-annex'
            build_data['force_include']['git-annex/git-annex'] = \
                'git_annex/git-annex'

        build_cmds = []
        if self.config.get('build') == 'stack':
            build_cmds = [
                ['stack', 'setup'],
                ['stack', 'build', '--no-haddock'],
                ['stack', 'install', '--no-haddock', '--local-bin-path', '.'],
            ]

        for cmd in build_cmds:
            run(cmd, cwd=self.root, check=True)
