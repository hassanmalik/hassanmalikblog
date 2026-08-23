from pathlib import Path
from bs4 import BeautifulSoup
import sys

ROOT = Path(__file__).resolve().parents[1]
soup = BeautifulSoup((ROOT / "blog.html").read_text(encoding="utf-8"), "html.parser")
PILLARS = {"Architecture", "AI & Data", "Platform & Infrastructure", "Reliability & Scale", "Technical Leadership", "Forward-Deployed Engineering"}
ARCHETYPES = {"Build", "Scale", "Migrate", "Optimize", "Harden", "Design", "Strategize"}
errors = []
cards = soup.select("a.publication-card[href]")
hrefs = {card["href"] for card in cards}
if len(cards) != 14 or len(hrefs) != 14:
    errors.append(f"expected 14 unique article cards, found {len(cards)} cards and {len(hrefs)} URLs")
for card in cards:
    if card.get("data-pillar") not in PILLARS or card.get("data-archetype") not in ARCHETYPES:
        errors.append(f"invalid classification: {card.get('href')}")
for pillar in PILLARS:
    if not soup.find(id={"AI & Data":"ai-data","Platform & Infrastructure":"platform","Reliability & Scale":"reliability","Technical Leadership":"leadership","Forward-Deployed Engineering":"fde","Architecture":"architecture"}[pillar]):
        errors.append(f"missing pillar anchor: {pillar}")
buttons = soup.select("button[data-filter-kind][data-filter-value][aria-pressed]")
values = {button.get("data-filter-value") for button in buttons}
for value in ARCHETYPES | {"all"}:
    if value not in values:
        errors.append(f"missing filter: {value}")
if not soup.select_one('[role="status"][data-results-count]'):
    errors.append("missing live result count")
if errors:
    print("FAIL")
    print("\n".join(f"- {e}" for e in errors))
    sys.exit(1)
print("PASS: writing index exposes 14 classified articles")
