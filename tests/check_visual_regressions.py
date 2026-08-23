from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
VERSION = "20260823-2"
errors = []

for path in sorted(ROOT.rglob("*.html")):
    if ".worktrees" in path.relative_to(ROOT).parts:
        continue
    text = path.read_text(encoding="utf-8")
    if path.name != "404.html":
        if not re.search(rf'href="(?:\.\./)?assets/styles\.css\?v={VERSION}"', text):
            errors.append(f"{path.relative_to(ROOT)}: versioned stylesheet")
        if not re.search(rf'src="(?:\.\./)?assets/main\.js\?v={VERSION}"', text):
            errors.append(f"{path.relative_to(ROOT)}: versioned script")

css = (ROOT / "assets" / "styles.css").read_text(encoding="utf-8")
required = [
    ".publication-hero h1{font-size:clamp(3rem,6vw,5.8rem)",
    ".pillar-grid{display:grid;grid-template-columns:repeat(2,1fr)",
    ".pillar-card{min-height:0",
    ".experience-page .page-grid{grid-template-columns:220px minmax(0,1fr)",
    ".experience-page .timeline{grid-column:2",
    ".experience-page .timeline-item h3{font-size:clamp(2rem,3vw,3rem)",
]
for snippet in required:
    if snippet not in css:
        errors.append(f"styles.css: missing restrained layout rule {snippet}")

experience = (ROOT / "experience.html").read_text(encoding="utf-8")
if not re.search(r'<body[^>]*class="[^"]*experience-page', experience):
    errors.append("experience.html: missing experience-page scope")

if errors:
    print("FAIL")
    print("\n".join(f"- {error}" for error in errors))
    sys.exit(1)
print("PASS: cache-busted assets and restrained editorial layouts")
