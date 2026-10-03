"""Restore selected third-party checkouts without changing existing worktrees."""
import argparse
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent

def run(*args):
    subprocess.run(args, check=True, env={**os.environ, 'GIT_LFS_SKIP_SMUDGE': '1'})

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('names', nargs='*', help='Names from repos.lock.json')
    parser.add_argument('--list', action='store_true')
    args = parser.parse_args()
    repos = {r['name']: r for r in json.loads((ROOT/'repos.lock.json').read_text())}
    if args.list:
        for r in repos.values():
            print(r['name'], r['management'], r['commit'])
        return
    if not args.names:
        parser.error('Select repositories explicitly, or use --list.')
    unknown = set(args.names)-repos.keys()
    if unknown:
        parser.error('Unknown repositories: '+', '.join(sorted(unknown)))
    for name in args.names:
        row = repos[name]
        path = ROOT/'code'/name
        if path.exists() and (path/'.git').exists():
            head = subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD'],text=True).strip()
            if head != row['commit']:
                raise SystemExit(f'{name}: existing version differs; refusing to reset it.')
            print(f'{name}: fixed revision already present (local edits preserved).')
        elif row['management'] == 'submodule':
            run('git','-C',str(ROOT.parent),'submodule','update','--init','--',f'sources/code/{name}')
        else:
            if path.exists():
                raise SystemExit(f'{path} exists without a Git checkout; inspect it manually.')
            run('git','init',str(path))
            run('git','-C',str(path),'remote','add','origin',row['url'])
            run('git','-C',str(path),'fetch','--depth','1','origin',row['commit'])
            run('git','-C',str(path),'checkout','--detach','FETCH_HEAD')

if __name__ == '__main__':
    main()
