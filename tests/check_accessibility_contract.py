from pathlib import Path
from bs4 import BeautifulSoup
import sys

ROOT=Path(__file__).resolve().parents[1]
errors=[]
for path in sorted(ROOT.rglob("*.html")):
    if ".worktrees" in path.relative_to(ROOT).parts:
        continue
    soup=BeautifulSoup(path.read_text(encoding="utf-8"),"html.parser")
    main=soup.find("main",id="main-content")
    skip=soup.find("a",string=lambda value:value and value.strip()=="Skip to content")
    if not main: errors.append(f"{path.relative_to(ROOT)}: main-content")
    if not skip or skip.get("href")!="#main-content": errors.append(f"{path.relative_to(ROOT)}: skip link")
    if path.name != "404.html":
        toggle=soup.select_one("button.mobile-toggle[aria-label][aria-expanded]")
        if not toggle: errors.append(f"{path.relative_to(ROOT)}: accessible mobile toggle")
        nav_text=" ".join(a.get_text(" ",strip=True) for a in soup.select(".nav-links a"))
        for label in ["Home","Writing","Lab","About","Contact"]:
            if label not in nav_text: errors.append(f"{path.relative_to(ROOT)}: nav {label}")
    if path.parent.name=="posts" and not soup.select_one(".article-next a[href]"):
        errors.append(f"{path.relative_to(ROOT)}: related reading")
if errors:
    print("FAIL")
    print("\n".join(f"- {e}" for e in errors))
    sys.exit(1)
print("PASS: accessible publication chrome")
