#!/usr/bin/env python3
"""Append a workflow attempt's compact records to the results branch."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def archive(records):
    run_id = os.environ['GITHUB_RUN_ID']
    attempt = os.environ['GITHUB_RUN_ATTEMPT']
    if not run_id.isdigit() or not attempt.isdigit():
        raise ValueError('invalid workflow run identity')
    if not (records / 'batch.json').is_file():
        raise ValueError('no batch receipt to archive')
    for _ in range(5):
        with tempfile.TemporaryDirectory() as tmp:
            def git(*args, check=True):
                return subprocess.run(['git', '-c', 'credential.helper=!gh auth git-credential',
                                       '-C', tmp, *args], check=check, capture_output=True, text=True)
            git('init', '-q')
            git('remote', 'add', 'origin', f"https://github.com/{os.environ['GITHUB_REPOSITORY']}.git")
            git('config', 'user.name', 'github-actions[bot]')
            git('config', 'user.email', '41898282+github-actions[bot]@users.noreply.github.com')
            # Each retry uses a fresh tree and the latest archive branch.
            exists = git('ls-remote', '--exit-code', '--heads', 'origin', 'results', check=False)
            if exists.returncode == 0:
                git('fetch', '--depth', '1', 'origin', 'results')
                git('checkout', '-B', 'results', 'FETCH_HEAD')
            elif exists.returncode == 2:
                git('checkout', '--orphan', 'results')
            else:
                raise RuntimeError(exists.stderr)
            dest = Path(tmp) / 'runs' / f'{run_id}-{attempt}'
            if dest.exists():
                raise RuntimeError(f'attempt already archived: {dest.name}')
            shutil.copytree(records, dest)
            # Actions artifacts do not preserve executable bits. Restore the
            # generated entry points before committing the results branch.
            for launcher in dest.rglob('*.sh'):
                if launcher.name in ('build.sh', 'watch.sh', 'play.sh') and not launcher.is_symlink():
                    launcher.chmod(0o755)
            git('add', 'runs')
            git('commit', '-m', f'Archive Borg runs {run_id} attempt {attempt}')
            result = git('push', 'origin', 'HEAD:refs/heads/results', check=False)
            if result.returncode == 0:
                return
    raise RuntimeError(f'could not append results: {result.stderr}')


if __name__ == '__main__':
    archive(Path(sys.argv[1]).resolve())
