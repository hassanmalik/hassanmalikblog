from pathlib import Path
from bs4 import BeautifulSoup
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
BASE="https://hassanmalik.github.io/hassanmalikblog/"
sitemap=(ROOT/"sitemap.xml").read_text(encoding="utf-8")
errors=[]; titles=set(); descriptions=set()
for path in sorted(ROOT.rglob("*.html")):
    rel=path.relative_to(ROOT).as_posix()
    soup=BeautifulSoup(path.read_text(encoding="utf-8"),"html.parser")
    title=soup.title.get_text(" ",strip=True) if soup.title else ""
    desc=soup.find("meta",attrs={"name":"description"})
    description=desc.get("content","").strip() if desc else ""
    if not title or title in titles: errors.append(f"{rel}: missing or duplicate title")
    if not description or description in descriptions: errors.append(f"{rel}: missing or duplicate description")
    titles.add(title); descriptions.add(description)
    if rel=="404.html": continue
    canonical=soup.find("link",rel="canonical")
    url=canonical.get("href","") if canonical else ""
    if not url.startswith(BASE): errors.append(f"{rel}: canonical")
    for prop,expected in [("og:title",title),("og:description",description),("og:url",url)]:
        meta=soup.find("meta",attrs={"property":prop})
        if not meta or meta.get("content")!=expected: errors.append(f"{rel}: {prop}")
    if url and url not in sitemap: errors.append(f"{rel}: sitemap")
    scripts=soup.find_all("script",attrs={"type":"application/ld+json"})
    if not scripts: errors.append(f"{rel}: JSON-LD")
    for script in scripts:
        try:
            data=json.loads(script.string or script.get_text())
            if data.get("@type")=="Person" and data.get("jobTitle") in {"Principal Software Engineer","Staff Software Engineer"}:
                errors.append(f"{rel}: inflated Person jobTitle")
        except json.JSONDecodeError: errors.append(f"{rel}: invalid JSON-LD")
if errors:
    print("FAIL"); print("\n".join(f"- {e}" for e in errors)); sys.exit(1)
print(f"PASS: unique SEO metadata for {len(titles)} pages")
