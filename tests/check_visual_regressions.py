from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
VERSION = "20260826-1"
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

homepage = (ROOT / "index.html").read_text(encoding="utf-8")

for marker in [
    'class="system-observer"',
    'class="observer-eye observer-eye-left"',
    'class="observer-eye observer-eye-right"',
    'aria-label="Interactive system observer"',
]:
    if marker not in homepage:
        errors.append(f"index.html: interactive observer missing {marker}")

script = (ROOT / "assets" / "main.js").read_text(encoding="utf-8")
for behavior in ["pointermove", "prefers-reduced-motion", "--look-x", "--look-y"]:
    if behavior not in script:
        errors.append(f"assets/main.js: observer interaction missing {behavior}")

if ".architecture-board:has(.system-observer){--look-x:0;--look-y:0" not in css:
    errors.append("assets/styles.css: observer coordinates must inherit from board scope")
if ".system-observer{--look-x:0;--look-y:0" in css:
    errors.append("assets/styles.css: observer must not shadow board pointer coordinates")

if errors:
    print("FAIL")
    print("\n".join(f"- {error}" for error in errors))
    sys.exit(1)
print("PASS: cache-busted assets and restrained editorial layouts")
