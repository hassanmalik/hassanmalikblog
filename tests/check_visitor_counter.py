from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
VERSION = "20260827-1"
errors = []

pages = []
for path in sorted(ROOT.rglob("*.html")):
    relative = path.relative_to(ROOT)
    if ".worktrees" in relative.parts or path.name == "404.html":
        continue
    text = path.read_text(encoding="utf-8")
    if 'class="site-header"' not in text:
        continue
    pages.append(path)
    asset_prefix = "../" if relative.parts[0] == "posts" else ""
    for marker in [
        'class="nav-utility"',
        'data-visitor-counter',
        'data-visit-count',
        'data-country-count',
        'aria-live="polite"',
        f'src="{asset_prefix}assets/visitor-counter.mjs?v={VERSION}"',
    ]:
        if marker not in text:
            errors.append(f"{relative}: missing visitor-counter contract {marker}")

css = (ROOT / "assets" / "styles.css").read_text(encoding="utf-8")
for rule in [
    ".nav-utility{justify-self:end",
    ".visitor-counter{display:flex",
    ".visitor-status{width:7px;height:7px;border-radius:50%",
    ".visitor-counter.is-loaded .visitor-status",
    ".lab-page .visitor-counter",
    ".lab-page .mobile-toggle{color:var(--white)",
]:
    if rule not in css:
        errors.append(f"assets/styles.css: missing counter presentation {rule}")

behavior = subprocess.run(
    ["node", str(ROOT / "tests" / "visitor_counter_contract.mjs")],
    cwd=ROOT,
    capture_output=True,
    text=True,
    check=False,
)
if behavior.returncode:
    errors.append("visitor behavior failed:\n" + behavior.stdout + behavior.stderr)

if not pages:
    errors.append("no site-header pages found")

if errors:
    print("FAIL")
    print("\n".join(f"- {error}" for error in errors))
    sys.exit(1)

print(f"PASS: visitor counter contract on {len(pages)} header pages")
print(behavior.stdout.strip())
