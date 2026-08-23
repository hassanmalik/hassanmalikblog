from pathlib import Path
from bs4 import BeautifulSoup
import json, re, sys

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://hassanmalik.github.io/hassanmalikblog/'
errors = []

def check(cond, msg):
    if not cond:
        errors.append(msg)

def soup(path):
    return BeautifulSoup((ROOT/path).read_text(encoding='utf-8'), 'html.parser')

# Homepage positioning and SEO
home = soup('index.html')
check(home.title and home.title.get_text(strip=True) == 'Hassan Malik | Principal Software Engineering & Applied AI', 'homepage SEO title')
desc = home.find('meta', attrs={'name':'description'})
check(desc and all(k.lower() in desc.get('content','').lower() for k in ['production ai', 'agentic', 'distributed systems', 'biotech']), 'homepage meta description keywords')
home_text = home.get_text(' ', strip=True)
for kw in ['Principal Software Engineering', 'Applied AI', 'AI Architecture', 'Forward Deployed Engineering', 'Distributed Systems']:
    check(kw.lower() in home_text.lower(), f'homepage visible keyword: {kw}')

# Person schema should be accurate while carrying expertise keywords.
person_scripts = []
for sc in home.find_all('script', attrs={'type':'application/ld+json'}):
    try:
        d = json.loads(sc.string or sc.get_text())
        if d.get('@type') == 'Person': person_scripts.append(d)
    except Exception:
        pass
check(bool(person_scripts), 'Person JSON-LD exists')
if person_scripts:
    p = person_scripts[0]
    check('Principal Software Engineer' not in str(p.get('jobTitle','')), 'Person schema does not falsely claim Principal title')
    knows = ' '.join(p.get('knowsAbout', [])) if isinstance(p.get('knowsAbout'), list) else str(p.get('knowsAbout',''))
    for kw in ['Applied AI','Distributed Systems','Generative AI','Biotech','Forward Deployed Engineering']:
        check(kw.lower() in knows.lower(), f'Person knowsAbout: {kw}')

# Blog taxonomy and keyword-rich article surface.
blog = soup('blog.html')
blog_text = blog.get_text(' ', strip=True)
for cat in [
    'AI Architecture & Distributed Systems',
    'AI for Biotech & Life Sciences',
    'Forward Deployed Engineering',
    'System Design & Architecture Reviews',
    'Production Engineering Field Notes',
    'Principal Engineering & Technical Leadership',
]:
    check(cat.lower() in blog_text.lower(), f'blog taxonomy: {cat}')

required_posts = {
    'posts/ai-architecture-biotech-workflow-boundary.html': 'AI Architecture for Biotech: Why Production AI Systems Fail at the Workflow Boundary',
    'posts/distributed-systems-agentic-ai.html': 'Distributed Systems for Agentic AI: Retries, Idempotency and Failure Recovery',
    'posts/forward-deployed-engineering-prototype-risk.html': 'Forward Deployed Engineering: Prototype the Risk, Not the AI Demo',
    'posts/enterprise-rag-scientific-rd.html': 'Enterprise RAG Architecture for Scientific R&D: Retrieval, Evidence and Provenance',
}
for rel, expected in required_posts.items():
    path = ROOT/rel
    check(path.exists(), f'new post exists: {rel}')
    if path.exists():
        s = soup(rel)
        check(s.find('h1') and expected == s.find('h1').get_text(' ', strip=True), f'H1 matches SEO title: {rel}')
        check(s.find('meta', attrs={'name':'description'}) is not None, f'meta description: {rel}')
        canonical = s.find('link', rel='canonical')
        check(canonical and canonical.get('href') == BASE + rel, f'canonical URL: {rel}')
        found_blogposting = False
        for sc in s.find_all('script', attrs={'type':'application/ld+json'}):
            try:
                d = json.loads(sc.string or sc.get_text())
                if d.get('@type') == 'BlogPosting': found_blogposting = True
            except Exception:
                pass
        check(found_blogposting, f'BlogPosting schema: {rel}')

# About page contains recruiter-searchable focus without title inflation.
about = soup('about.html')
about_text = about.get_text(' ', strip=True)
for kw in ['Applied AI','distributed systems','AI architecture','biotech R&D','production systems']:
    check(kw.lower() in about_text.lower(), f'about keyword: {kw}')

# Sitemap coverage.
sitemap = (ROOT/'sitemap.xml').read_text(encoding='utf-8')
for rel in required_posts:
    check(BASE + rel in sitemap, f'sitemap contains {rel}')

# Basic static integrity: local href/src targets exist.
for html in ROOT.rglob('*.html'):
    s = BeautifulSoup(html.read_text(encoding='utf-8'), 'html.parser')
    relbase = html.parent
    check(s.title is not None and bool(s.title.get_text(strip=True)), f'title exists: {html.relative_to(ROOT)}')
    check(s.find('meta', attrs={'name':'description'}) is not None, f'description exists: {html.relative_to(ROOT)}')
    for tag, attr in [('a','href'),('link','href'),('script','src')]:
        for node in s.find_all(tag):
            target = node.get(attr)
            if not target or target.startswith(('http://','https://','mailto:','tel:','#','data:','javascript:')):
                continue
            target = target.split('#',1)[0].split('?',1)[0]
            if not target:
                continue
            resolved = (relbase/target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                continue
            check(resolved.exists(), f'broken local target {target} from {html.relative_to(ROOT)}')

if errors:
    print('FAIL')
    for e in errors:
        print(' -', e)
    sys.exit(1)
print('PASS: SEO/content and static-site integrity checks')
