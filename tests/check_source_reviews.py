from pathlib import Path
from bs4 import BeautifulSoup
import sys

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    "review-evolutionary-architecture.html", "review-uber-michelangelo-ml-platform.html",
    "review-cloudflare-radar-platform.html", "review-netflix-chaos-engineering.html",
    "review-staffeng-technical-leadership.html", "review-stripe-idempotent-integrations.html",
]
HEADINGS = {"The engineering problem", "The approach", "Tradeoffs", "What generalizes", "What is context-dependent", "Architecture review questions"}
errors=[]
for name in FILES:
    path=ROOT/"posts"/name
    if not path.exists():
        errors.append(f"missing {name}")
        continue
    soup=BeautifulSoup(path.read_text(encoding="utf-8"),"html.parser")
    article=soup.find("article",attrs={"data-article-type":"Publication Review"})
    if not article: errors.append(f"{name}: publication-review article contract")
    if not soup.select_one(".source-note a[href^='http']"): errors.append(f"{name}: first-party source note")
    present={h.get_text(" ",strip=True) for h in soup.find_all("h2")}
    for heading in HEADINGS-present: errors.append(f"{name}: missing heading {heading}")
    if "This is an independent review" not in soup.get_text(" ",strip=True): errors.append(f"{name}: missing independence disclaimer")
if errors:
    print("FAIL")
    print("\n".join(f"- {e}" for e in errors))
    sys.exit(1)
print("PASS: six independently attributed source reviews")
