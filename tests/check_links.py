from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
errors=[]
for html in sorted(ROOT.rglob('*.html')):
    if '.git' in html.parts or '.worktrees' in html.relative_to(ROOT).parts: continue
    soup=BeautifulSoup(html.read_text(encoding='utf-8'),'html.parser')
    for tag,attr in [('a','href'),('link','href'),('script','src')]:
        for node in soup.find_all(tag):
            href=node.get(attr)
            if not href or href.startswith(('http://','https://','mailto:','tel:','data:','javascript:','#')):
                continue
            target_part=href.split('#',1)[0].split('?',1)[0]
            if not target_part: continue
            if target_part.startswith('/'):
                # GitHub Pages project-root path
                if target_part.startswith('/hassanmalikblog/'):
                    target=ROOT/target_part.removeprefix('/hassanmalikblog/')
                else:
                    continue
            else:
                target=(html.parent/target_part).resolve()
            if not target.exists():
                errors.append(f'{html.relative_to(ROOT)} -> missing {href}')
    # Check same-page fragment targets.
    ids={n.get('id') for n in soup.find_all(attrs={'id':True})}
    for a in soup.find_all('a',href=True):
        href=a['href']
        if href.startswith('#') and len(href)>1 and href[1:] not in ids:
            errors.append(f'{html.relative_to(ROOT)} -> missing fragment {href}')

if errors:
    print('FAIL')
    for e in errors: print('-',e)
    raise SystemExit(1)
print('PASS: local links/assets resolve')
