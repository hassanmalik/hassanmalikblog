from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "demoisnotdone.com"
BASE = f"https://{DOMAIN}/"
OLD_BASE = "https://hassanmalik.github.io/hassanmalikblog/"
errors = []

cname = ROOT / "CNAME"
if not cname.exists() or cname.read_text(encoding="utf-8").strip() != DOMAIN:
    errors.append("CNAME must contain only demoisnotdone.com")

robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
if f"Sitemap: {BASE}sitemap.xml" not in robots:
    errors.append("robots.txt must advertise the custom-domain sitemap")

sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
if OLD_BASE in sitemap or f"<loc>{BASE}" not in sitemap:
    errors.append("sitemap.xml must use custom-domain URLs")

for path in sorted(ROOT.rglob("*.html")):
    if ".worktrees" in path.relative_to(ROOT).parts:
        continue
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(ROOT).as_posix()
    if OLD_BASE in text:
        errors.append(f"{rel}: contains the old GitHub Pages URL")
    if "/hassanmalikblog/" in text:
        errors.append(f"{rel}: contains the old project-root path")

if errors:
    print("FAIL")
    print("\n".join(f"- {error}" for error in errors))
    sys.exit(1)

print("PASS: custom domain is canonical across deployable artifacts")
