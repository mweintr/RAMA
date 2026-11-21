#!/usr/bin/env python3
"""Build RAMA.

1. Copies shared/*.md into every skill's references/ folder, so each skill is
   self-contained (the plugin reads them from there, and claude.ai needs them
   inside each uploaded skill).
2. Writes dist/claude-ai/rama-<skill>.zip for every skill: a folder named
   rama-<skill> with the skill's files, its frontmatter name changed to
   rama-<skill> and /rama:<x> usages changed to /rama-<x>, ready to upload
   in claude.ai under Settings > Capabilities > Skills.

Stops first if any skill description contains < or >, which claude.ai rejects.

Run from the repo root:  python3 scripts/build.py
"""
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHARED = ROOT / 'shared'
SKILLS = ROOT / 'skills'
DIST = ROOT / 'dist' / 'claude-ai'


def validate():
    """claude.ai rejects a skill whose description contains anything that looks like an XML tag."""
    bad = []
    for f in sorted(SKILLS.glob('*/SKILL.md')):
        m = re.search(r'^description:\s*(.*)$', f.read_text(encoding='utf-8'), flags=re.M)
        if not m:
            bad.append(f'{f.relative_to(ROOT)}: no description')
        elif re.search(r'[<>]', m.group(1)):
            bad.append(f'{f.relative_to(ROOT)}: description contains < or > (claude.ai reads it as an XML tag)')
    if bad:
        raise SystemExit('Build stopped:\n  ' + '\n  '.join(bad))


def sync():
    for skill in sorted(p for p in SKILLS.iterdir() if (p / 'SKILL.md').exists()):
        refs = skill / 'references'
        refs.mkdir(exist_ok=True)
        for f in SHARED.glob('*.md'):
            shutil.copy2(f, refs / f.name)
    print('Synced shared references into', len(list(SKILLS.glob('*/SKILL.md'))), 'skills')


def for_claude_ai(text):
    text = re.sub(r'^name:\s*(\S+)', lambda m: f'name: rama-{m.group(1)}', text, count=1, flags=re.M)
    return re.sub(r'/rama:([a-z-]+)', r'/rama-\1', text)


def package():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    for skill in sorted(p for p in SKILLS.iterdir() if (p / 'SKILL.md').exists()):
        name = f'rama-{skill.name}'
        with zipfile.ZipFile(DIST / f'{name}.zip', 'w', zipfile.ZIP_DEFLATED) as z:
            for f in sorted(skill.rglob('*')):
                if f.is_dir() or f.name == '.DS_Store' or '__pycache__' in f.parts:
                    continue
                arc = f'{name}/{f.relative_to(skill).as_posix()}'
                if f.suffix == '.md':
                    z.writestr(arc, for_claude_ai(f.read_text(encoding='utf-8')))
                else:
                    z.write(f, arc)
        print('  ', DIST.relative_to(ROOT) / f'{name}.zip')


if __name__ == '__main__':
    validate()
    sync()
    package()
