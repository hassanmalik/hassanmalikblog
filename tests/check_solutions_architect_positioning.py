from pathlib import Path
import json
import sys

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
errors = []

home = BeautifulSoup((ROOT / "index.html").read_text(encoding="utf-8"), "html.parser")
about = BeautifulSoup((ROOT / "about.html").read_text(encoding="utf-8"), "html.parser")
experience = BeautifulSoup((ROOT / "experience.html").read_text(encoding="utf-8"), "html.parser")

home_text = home.get_text(" ", strip=True).lower()
about_text = about.get_text(" ", strip=True).lower()
experience_text = experience.get_text(" ", strip=True).lower()

for anchor in ["data-engineering", "technical-programs"]:
    if not experience.select_one(f"#{anchor}"):
        errors.append(f"Experience page is missing recruiter destination: #{anchor}")

if "solutions architecture" not in home_text:
    errors.append("homepage does not establish Solutions Architecture positioning")

paths = home.select("#recruiting-paths .recruiting-path")
if len(paths) != 4:
    errors.append("homepage must provide four role-specific recruiting paths")
else:
    expected_weights = {
        "data-engineering": "40",
        "ai-engineering": "20",
        "software-engineering": "20",
        "technical-program-management": "20",
    }
    actual_weights = {path.get("data-path"): path.get("data-weight") for path in paths}
    if actual_weights != expected_weights:
        errors.append(f"recruiting path weights are incorrect: {actual_weights}")
    if "recruiting-path--primary" not in paths[0].get("class", []):
        errors.append("Data Engineering must be the visually dominant recruiting path")

for phrase in [
    "data engineering, ai engineering, software engineering, and technical program leadership",
    "solutions architecture connects the four",
]:
    if phrase not in home_text:
        errors.append(f"homepage is missing umbrella positioning: {phrase}")

if "data engineering" not in home.title.get_text(" ", strip=True).lower():
    errors.append("homepage title does not lead with Data Engineering")

delivery = home.select_one("#delivery-model")
delivery_steps = delivery.select(".delivery-step") if delivery else []
if len(delivery_steps) != 4:
    errors.append("homepage must show four delivery stages")

evidence = home.select_one("#evidence")
evidence_items = evidence.select(".evidence-item") if evidence else []
if len(evidence_items) < 4:
    errors.append("homepage must expose at least four evidence items")

home_links = {link.get("href") for link in home.select("a[href]")}
for target in ["experience.html", "contact.html"]:
    if target not in home_links:
        errors.append(f"homepage is missing recruiter CTA to {target}")

if "staff and principal engineers" in about_text:
    errors.append("About page retains inflated Staff/Principal positioning")
if "solutions architect" not in about_text:
    errors.append("About page does not present a coherent Solutions Architect identity")
for phrase in ["data engineering", "ai engineering", "software engineering", "technical program leadership"]:
    if phrase not in about_text:
        errors.append(f"About page is missing recruiting path: {phrase}")

if not experience.select_one(".experience-lens"):
    errors.append("Experience page lacks an architecture capability summary")
for capability in ["technical discovery", "solution design", "delivery and adoption"]:
    if capability not in experience_text:
        errors.append(f"Experience page is missing capability: {capability}")

schema = home.select_one('script[type="application/ld+json"]')
if not schema:
    errors.append("homepage Person schema is missing")
else:
    data = json.loads(schema.string)
    if data.get("jobTitle") != "Senior Data Engineer / Software Engineer":
        errors.append("official current job title was changed or overstated")

if errors:
    print("FAIL")
    print("\n".join(f"- {error}" for error in errors))
    sys.exit(1)

print("PASS: evidence-first Solutions Architect positioning")
