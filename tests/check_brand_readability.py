from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
HTML = sorted([p for p in ROOT.rglob('*.html') if '.git' not in p.parts and '.worktrees' not in p.relative_to(ROOT).parts])
CORRECT = 'https://www.linkedin.com/in/malik-msee/'
OLD = 'https://www.linkedin.com/in/msee-ba-da'

errors = []

# LinkedIn identity must be current everywhere, and every public page should expose it.
for path in HTML:
    text = path.read_text(encoding='utf-8')
    if OLD in text:
        errors.append(f'{path.relative_to(ROOT)} still contains old LinkedIn URL')
    if CORRECT not in text:
        errors.append(f'{path.relative_to(ROOT)} does not link to current LinkedIn profile')

# Homepage should not present Principal Software Engineering as Hassan's current identity.
index = (ROOT / 'index.html').read_text(encoding='utf-8')
body = index.split('<body>', 1)[1] if '<body>' in index else index
for phrase in ['Applied AI · Principal Software Engineering · Biotech',
               '<strong>Principal Software Engineering</strong>',
               'Read Principal-level writing']:
    if phrase in body:
        errors.append(f'homepage still uses title-like Principal positioning: {phrase}')

# About page should preserve a clear distinction between current role identity and target-level topics.
about = (ROOT / 'about.html').read_text(encoding='utf-8')
if 'problems Staff and Principal engineers are expected to own' not in about:
    errors.append('about page lacks explicit, non-title Staff/Principal scope framing')

# Article typography should be constrained for readable long-form text.
css = (ROOT / 'assets' / 'styles.css').read_text(encoding='utf-8')
required_css = [
    '.article-shell{width:min(calc(100% - 40px),800px)',
    '.prose{max-width:720px',
    'font-size:1.2rem',
    'line-height:1.76',
]
for snippet in required_css:
    if snippet not in css:
        errors.append(f'missing readable article CSS: {snippet}')

# Mobile display titles should not consume nearly the entire viewport.
if '.page-hero h1{font-size:clamp(3.25rem,14vw,5rem)}' not in css:
    errors.append('mobile page hero typography is still too large')

if errors:
    print('FAIL')
    for error in errors:
        print('-', error)
    raise SystemExit(1)

print(f'PASS: checked {len(HTML)} HTML pages')
