from pathlib import Path
import re
import sys
from bs4 import BeautifulSoup

text = (Path(__file__).resolve().parents[1] / "index.html").read_text(encoding="utf-8")
visible = BeautifulSoup(text, "html.parser").get_text(" ", strip=True)
errors = []

for section_id in ["featured-writing", "engineering-pillars", "deep-dives", "positioning"]:
    if f'id="{section_id}"' not in text:
        errors.append(f"missing section #{section_id}")
for phrase in [
    "Architecture", "AI & Data", "Platform & Infrastructure",
    "Reliability & Scale", "Technical Leadership", "Forward-Deployed Engineering",
    "production AI", "distributed systems", "cloud and platform architecture",
    "technical leadership", "forward-deployed engineering",
]:
    if phrase.lower() not in visible.lower():
        errors.append(f"missing visible phrase: {phrase}")
for url in ["https://github.com/hassanmalik", "https://www.linkedin.com/in/malik-msee/"]:
    if url not in text:
        errors.append(f"missing profile link: {url}")
h1 = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.I | re.S)
if h1 and re.search(r"Principal Software Engineer|Staff Software Engineer", h1.group(1), re.I):
    errors.append("homepage H1 claims an unverified title")

if errors:
    print("FAIL")
    print("\n".join(f"- {error}" for error in errors))
    sys.exit(1)
print("PASS: homepage publication structure")
