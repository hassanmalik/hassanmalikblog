from pathlib import Path
import re
import sys
from html import unescape

ROOT = Path(__file__).resolve().parents[1]
PILLARS = {
    "Architecture", "AI & Data", "Platform & Infrastructure",
    "Reliability & Scale", "Technical Leadership",
    "Forward-Deployed Engineering",
}
ARCHETYPES = {"Build", "Scale", "Migrate", "Optimize", "Harden", "Design", "Strategize"}
ARTICLE_TYPES = {"Original Essay", "Publication Review"}
errors = []

for path in sorted((ROOT / "posts").glob("*.html")):
    text = path.read_text(encoding="utf-8")
    article = re.search(r"<article\b([^>]*)>", text, re.I)
    attrs = article.group(1) if article else ""
    values = {key: unescape(value) for key, value in re.findall(r'data-([\w-]+)="([^"]+)"', attrs)}
    if values.get("pillar") not in PILLARS:
        errors.append(f"{path.name}: invalid or missing pillar")
    if values.get("archetype") not in ARCHETYPES:
        errors.append(f"{path.name}: invalid or missing archetype")
    if values.get("article-type") not in ARTICLE_TYPES:
        errors.append(f"{path.name}: invalid or missing article type")
    for pattern, label in [
        (r'class="[^"]*article-context', "article context"),
        (r'class="[^"]*topic-tag', "topic tag"),
        (r'<link[^>]+rel="canonical"', "canonical URL"),
        (r'<script[^>]+application/ld\+json', "JSON-LD"),
    ]:
        if not re.search(pattern, text, re.I):
            errors.append(f"{path.name}: missing {label}")

if errors:
    print("FAIL")
    print("\n".join(f"- {error}" for error in errors))
    sys.exit(1)
print(f"PASS: taxonomy contract for {len(list((ROOT / 'posts').glob('*.html')))} posts")
