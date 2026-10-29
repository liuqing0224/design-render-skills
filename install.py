#!/usr/bin/env python3
"""Copy the 37 Skills without replacing existing installations."""
import argparse
import hashlib
import os
from pathlib import Path
import shutil
import sys

SOURCE = Path(__file__).resolve().parent / 'skills'

def files(root):
    return {p.relative_to(root): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*')
            if p.is_file() and '__pycache__' not in p.parts and p.name != '.DS_Store'
            and p.suffix != '.pyc'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', type=Path,
                        default=Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))) / 'skills')
    parser.add_argument('--check', action='store_true', help='Only compare installed files')
    args = parser.parse_args()
    target = args.target.expanduser().resolve()
    skills = sorted(p for p in SOURCE.iterdir() if p.is_dir() and (p / 'SKILL.md').is_file())
    if len(skills) != 37:
        parser.error('Expected 37 complete Skill folders; source checkout is incomplete.')
    if args.check:
        mismatches = [p.name for p in skills if not (target / p.name).is_dir()
                      or files(p) != files(target / p.name)]
        if mismatches:
            print('Missing or different: ' + ', '.join(mismatches), file=sys.stderr)
            return 1
        print('Verified 37 installed Skills.')
        return 0
    conflicts = [p.name for p in skills if os.path.lexists(target / p.name)]
    if conflicts:
        print('Nothing written. Existing targets: ' + ', '.join(conflicts), file=sys.stderr)
        return 1
    target.mkdir(parents=True, exist_ok=True)
    copied = []
    try:
        for skill in skills:
            destination = target / skill.name
            shutil.copytree(skill, destination,
                            ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.DS_Store'))
            copied.append(destination)
    except OSError as exc:
        for destination in copied:
            shutil.rmtree(destination)
        print('Installation failed: ' + str(exc), file=sys.stderr)
        return 1
    print('Installed 37 Skills to ' + str(target))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
