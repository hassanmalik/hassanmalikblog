# Principal Engineering Publication Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the existing static blog into a six-pillar engineering publication and add one first-party source review for each pillar.

**Architecture:** Preserve the dependency-free HTML/CSS/JavaScript site and its existing URLs. Encode taxonomy in semantic HTML `data-*` attributes, progressively enhance the writing index with a small filter script, and enforce the content system through Python checks.

**Tech Stack:** HTML5, CSS, vanilla JavaScript, Python 3 static checks, GitHub Pages

**Spec:** `docs/superpowers/specs/2026-08-23-principal-engineering-publication-design.md`

## Global Constraints

- Preserve all eight existing article bodies and URLs unless a factual, accessibility, or link defect requires a correction.
- Do not claim that Hassan currently holds a Principal Software Engineer or Staff Software Engineer title.
- Do not invent employers, projects, metrics, experience, or outcomes.
- Keep Security as a cross-cutting tag.
- Use exactly these primary pillars: Architecture; AI & Data; Platform & Infrastructure; Reliability & Scale; Technical Leadership; Forward-Deployed Engineering.
- Use exactly these archetypes: Build; Scale; Migrate; Optimize; Harden; Design; Strategize.
- Keep the site dependency-free at runtime and deployable as static files on GitHub Pages.
- Source reviews must link to a specific first-party publication, paraphrase its claims, and never imply first-hand operation of the reviewed system.
- Preserve the existing paper, ink, blue, acid, serif, and monospace visual identity.
- No change may be pushed directly to `main`.

---

### Task 1: Taxonomy and metadata contract

**Files:**
- Create: `tests/check_publication_taxonomy.py`
- Modify: `tools/check_site.py`
- Modify: `README.md`

**Interfaces:**
- Consumes: HTML pages under `posts/` and the pillar/archetype names in the approved spec.
- Produces: required `<article data-pillar="..." data-archetype="..." data-article-type="...">` attributes; `.article-context` metadata; a single verification entry point in `tools/check_site.py`.

- [ ] **Step 1: Write the failing taxonomy test**

Create a standard-library Python check that loads all `posts/*.html`, locates the first `<article>` tag with a regular expression, and verifies its attributes against:

```python
PILLARS = {
    "Architecture", "AI & Data", "Platform & Infrastructure",
    "Reliability & Scale", "Technical Leadership",
    "Forward-Deployed Engineering",
}
ARCHETYPES = {"Build", "Scale", "Migrate", "Optimize", "Harden", "Design", "Strategize"}
ARTICLE_TYPES = {"Original Essay", "Publication Review"}
```

Require one `.article-context`, at least one `.topic-tag`, a canonical URL, and one JSON-LD block on every article. Print every failure and exit nonzero.

- [ ] **Step 2: Run the taxonomy test and verify RED**

Run: `python tests/check_publication_taxonomy.py`

Expected: FAIL because existing `<article>` elements lack `data-pillar`, `data-archetype`, and `data-article-type`.

- [ ] **Step 3: Add taxonomy metadata to the eight existing articles**

Apply this exact classification while retaining body copy and paths:

```text
ai-architecture-biotech-workflow-boundary.html = AI & Data × Design
biotech-ai-stack.html = AI & Data × Build
decision-systems.html = Technical Leadership × Strategize
distributed-systems-agentic-ai.html = Reliability & Scale × Harden
enterprise-rag-scientific-rd.html = AI & Data × Design
forward-deployed-engineering-prototype-risk.html = Forward-Deployed Engineering × Build
scientist-adoption.html = Forward-Deployed Engineering × Strategize
software-operations.html = Technical Leadership × Strategize
```

Set `data-article-type="Original Essay"` and render the matching values plus the tags listed in the spec inside `.article-context`.

- [ ] **Step 4: Make the verification runner execute every check**

Update `tools/check_site.py` to use `subprocess.run([sys.executable, check], check=False)` for each file in `tests/check_*.py`, aggregate nonzero return codes, and exit 1 if any check fails. Document `python tools/check_site.py` as the full local verification command in `README.md`.

- [ ] **Step 5: Run the taxonomy check and verify GREEN**

Run: `python tests/check_publication_taxonomy.py`

Expected: PASS for all eight existing posts.

- [ ] **Step 6: Commit the contract and article migration**

```powershell
git add tests/check_publication_taxonomy.py tools/check_site.py README.md posts
git commit -m "refactor: classify writing by pillar and problem"
```

### Task 2: Homepage publication positioning

**Files:**
- Create: `tests/check_homepage_publication.py`
- Modify: `index.html`
- Modify: `assets/styles.css`

**Interfaces:**
- Consumes: the six canonical pillar names and existing article URLs.
- Produces: homepage sections with IDs `featured-writing`, `engineering-pillars`, `deep-dives`, and `positioning`; reusable `.pillar-grid`, `.pillar-card`, `.article-card`, and `.classification` styles.

- [ ] **Step 1: Write the failing homepage structure test**

Assert that `index.html` contains all four section IDs, all six pillar names, visible phrases `production AI`, `distributed systems`, `cloud and platform architecture`, `technical leadership`, and `forward-deployed engineering`, plus GitHub and current LinkedIn links. Reject `<h1>` copy containing `Principal Software Engineer` or `Staff Software Engineer`.

- [ ] **Step 2: Run the homepage test and verify RED**

Run: `python tests/check_homepage_publication.py`

Expected: FAIL because the new sections and full six-pillar vocabulary are absent.

- [ ] **Step 3: Replace the homepage content architecture**

Use the hero heading `Engineering systems that have to work beyond the demo.` and the supporting copy `Writing about production AI, distributed systems, cloud and platform architecture, reliability, and the technical decisions that carry systems from ambiguity to operation.`

Build the four required sections in the order specified by the design. Feature `enterprise-rag-scientific-rd.html`; select the distributed-systems, AI-workflow-boundary, FDE-prototype-risk, and software-operations essays as deep dives. Give every article link visible `Pillar × Archetype` text.

- [ ] **Step 4: Implement the shared publication styles**

Add six-column-to-one-column pillar cards, editorial article cards, smaller hero typography using `clamp(3.4rem, 7.5vw, 7rem)`, visible `:focus-visible` outlines, 44px minimum filter/link tap targets, and `@media (prefers-reduced-motion: reduce)` rules that disable the pulse animation and nonessential transitions.

- [ ] **Step 5: Run the homepage and existing brand checks**

Run: `python tests/check_homepage_publication.py`

Expected: PASS.

Run: `python tests/check_brand_readability.py`

Expected: PASS after updating obsolete exact-string assertions to validate maximum heading scale and readable article measure rather than the former CSS serialization.

- [ ] **Step 6: Commit the homepage redesign**

```powershell
git add index.html assets/styles.css tests/check_homepage_publication.py tests/check_brand_readability.py
git commit -m "feat: reposition homepage as engineering publication"
```

### Task 3: Writing index and progressive filters

**Files:**
- Create: `tests/check_writing_index.py`
- Modify: `blog.html`
- Modify: `assets/main.js`
- Modify: `assets/styles.css`

**Interfaces:**
- Consumes: article cards carrying `data-pillar` and `data-archetype` values.
- Produces: buttons with `data-filter-kind` and `data-filter-value`; cards with `.publication-card`; live result node `[data-results-count]`.

- [ ] **Step 1: Write the failing writing-index test**

Require 14 unique `.publication-card` hrefs, six pillar anchors, all seven archetype buttons, an All button, `aria-pressed` on filter buttons, and a `role="status"` result count. Require every card to contain one valid pillar and archetype attribute.

- [ ] **Step 2: Run the writing-index test and verify RED**

Run: `python tests/check_writing_index.py`

Expected: FAIL because the current index lacks the new card and filtering contract.

- [ ] **Step 3: Rebuild the writing index semantically**

Add a concise publication hero, six pillar directory links, filters, and fourteen article cards. Include the eight existing paths plus the six review paths defined in Task 5. Cards for reviews use `data-article-type="Publication Review"`; original essays use `Original Essay`.

- [ ] **Step 4: Implement progressive filtering**

In `assets/main.js`, on click set one active pillar or archetype filter, update `aria-pressed`, toggle each card's `hidden` property based on an exact data-attribute match, and set the status text to `Showing N articles`. The All button clears both filters. Do not hide cards before a user action.

- [ ] **Step 5: Run the writing-index test and verify GREEN**

Run: `python tests/check_writing_index.py`

Expected: PASS with fourteen unique article cards and complete filter controls.

- [ ] **Step 6: Commit writing discovery**

```powershell
git add blog.html assets/main.js assets/styles.css tests/check_writing_index.py
git commit -m "feat: add pillar and problem filters to writing"
```

### Task 4: Shared navigation, article chrome, and accessibility

**Files:**
- Create: `tests/check_accessibility_contract.py`
- Modify: `404.html`
- Modify: `about.html`
- Modify: `contact.html`
- Modify: `experience.html`
- Modify: `lab.html`
- Modify: all files under `posts/`
- Modify: `assets/main.js`
- Modify: `assets/styles.css`

**Interfaces:**
- Consumes: the shared navigation labels and article taxonomy contract.
- Produces: consistent Home/Writing/Lab/About/Contact navigation, skip links, `aria-current="page"`, accessible mobile-menu dismissal, and related-reading blocks.

- [ ] **Step 1: Write the failing accessibility contract test**

For every HTML page require a `Skip to content` link targeting an existing `id="main-content"`, one `<main id="main-content">`, meaningful mobile-toggle accessible text, and the five shared navigation destinations. For article pages require an `.article-next` block with at least one valid local article link.

- [ ] **Step 2: Run the contract test and verify RED**

Run: `python tests/check_accessibility_contract.py`

Expected: FAIL because skip links and consistent main IDs are absent.

- [ ] **Step 3: Normalize shared navigation and article context**

Apply the exact shared labels Home, Writing, Lab, About, Contact to all pages; keep Experience linked from About and homepage positioning. Add skip links, main IDs, current-page state, and related reading chosen by matching pillar first and complementary archetype second.

- [ ] **Step 4: Harden mobile navigation behavior**

Extend `assets/main.js` so Escape closes the open navigation, clicking a navigation link closes it, and the toggle's `aria-expanded` always matches `.open`. Keep the menu usable without JavaScript through its default desktop and inline mobile links.

- [ ] **Step 5: Run accessibility and link checks**

Run: `python tests/check_accessibility_contract.py`

Expected: PASS.

Run: `python tests/check_links.py`

Expected: PASS with no missing local targets or fragments.

- [ ] **Step 6: Commit shared publication chrome**

```powershell
git add 404.html about.html contact.html experience.html lab.html posts assets tests/check_accessibility_contract.py
git commit -m "refactor: unify navigation and article presentation"
```

### Task 5: Six first-party engineering publication reviews

**Files:**
- Create: `tests/check_source_reviews.py`
- Create: `posts/review-evolutionary-architecture.html`
- Create: `posts/review-uber-michelangelo-ml-platform.html`
- Create: `posts/review-cloudflare-radar-platform.html`
- Create: `posts/review-netflix-chaos-engineering.html`
- Create: `posts/review-staffeng-technical-leadership.html`
- Create: `posts/review-stripe-idempotent-integrations.html`
- Modify: `blog.html`

**Interfaces:**
- Consumes: the article template and taxonomy contract from Tasks 1 and 4.
- Produces: six `Publication Review` articles with `.source-note`, `.review-scope`, source links, and pillar/archetype metadata.

- [ ] **Step 1: Write the failing source-review test**

Require all six files, `data-article-type="Publication Review"`, one `.source-note`, one external first-party source URL, headings for `The engineering problem`, `The approach`, `Tradeoffs`, `What generalizes`, `What is context-dependent`, and `Architecture review questions`, plus disclaimer text containing `This is an independent review`.

- [ ] **Step 2: Run the source-review test and verify RED**

Run: `python tests/check_source_reviews.py`

Expected: FAIL because none of the six review paths exists.

- [ ] **Step 3: Write the Architecture review**

Source: `https://martinfowler.com/articles/evo-arch-forward.html`.

Title: `Evolutionary Architecture: Designing for Change Without Abandoning Direction`.

Classification: `Architecture × Design`.

Analyze architecture as continuous work, small changes and feedback loops, the difference between evolutionary design and unbounded change, fitness-function implications, and when stronger up-front constraints remain justified.

- [ ] **Step 4: Write the AI & Data review**

Source: `https://www.uber.com/blog/michelangelo-machine-learning-platform/`.

Title: `Beyond the Model: What Uber's Michelangelo Reveals About Production AI Platforms`.

Classification: `AI & Data × Scale`.

Analyze end-to-end workflow standardization, reproducible data and feature pipelines, training/serving consistency, deployment and monitoring, build-vs-buy boundaries, and which Uber-scale assumptions do not transfer to smaller organizations.

- [ ] **Step 5: Write the Platform & Infrastructure review**

Source: `https://blog.cloudflare.com/technology-behind-radar2/`.

Title: `Platform Architecture Through Constraints: Reviewing Cloudflare Radar 2.0`.

Classification: `Platform & Infrastructure × Build`.

Analyze the high-level architecture, component boundaries, data delivery path, operational simplicity, reuse of platform capabilities, and the danger of copying a hyperscale topology without the same constraints.

- [ ] **Step 6: Write the Reliability & Scale review**

Source: `https://netflixtechblog.com/the-netflix-simian-army-16e57fbab116`.

Title: `Designing for Failure: What Netflix's Simian Army Still Teaches About Reliability`.

Classification: `Reliability & Scale × Harden`.

Analyze controlled failure injection, blast-radius management, automation and recovery, organizational prerequisites, observability, and why chaos experiments without hypotheses or safety controls create risk rather than resilience.

- [ ] **Step 7: Write the Technical Leadership review**

Source: `https://staffeng.com/guides/staff-archetypes/`.

Title: `Technical Leadership Has More Than One Shape: Reviewing the Staff Engineer Archetypes`.

Classification: `Technical Leadership × Strategize`.

Analyze Tech Lead, Architect, Solver, and Right Hand modes; match mode to organizational need; discuss influence, sponsorship, scope, and the risk of treating archetypes as a promotion checklist.

- [ ] **Step 8: Write the Forward-Deployed Engineering review**

Source: `https://stripe.com/blog/idempotency`.

Title: `Reliable Integrations Start at the API Boundary: Reviewing Stripe's Idempotency Design`.

Classification: `Forward-Deployed Engineering × Harden`.

Analyze ambiguous network outcomes, safe retries, idempotency keys, backoff and jitter, client/server responsibility, and how robust integration primitives reduce adoption and support risk for customer-facing delivery teams.

- [ ] **Step 9: Run the review contract and writing-index checks**

Run: `python tests/check_source_reviews.py`

Expected: PASS for six independently attributed reviews.

Run: `python tests/check_writing_index.py`

Expected: PASS with all fourteen cards resolving.

- [ ] **Step 10: Commit the review series**

```powershell
git add posts/review-*.html blog.html tests/check_source_reviews.py
git commit -m "feat: add engineering publication review series"
```

### Task 6: SEO, structured data, and sitemap

**Files:**
- Create: `tests/check_seo_metadata.py`
- Modify: all root HTML files
- Modify: all files under `posts/`
- Modify: `sitemap.xml`
- Modify: `robots.txt`
- Modify: `site.webmanifest`

**Interfaces:**
- Consumes: final article titles, summaries, types, and URLs.
- Produces: unique title/description/canonical/Open Graph metadata; accurate JSON-LD; fourteen sitemap article entries.

- [ ] **Step 1: Write the failing SEO test**

Require one unique nonempty title and meta description per public HTML page, one canonical under `https://hassanmalik.github.io/hassanmalikblog/`, matching `og:title`, `og:description`, and `og:url`, valid JSON-LD, and sitemap membership for every HTML page except `404.html`. Reject `Principal Software Engineer` and `Staff Software Engineer` in Person `jobTitle`.

- [ ] **Step 2: Run the SEO test and verify RED**

Run: `python tests/check_seo_metadata.py`

Expected: FAIL because the current pages do not all expose the complete Open Graph contract and the six new URLs are absent from the sitemap.

- [ ] **Step 3: Normalize page metadata and schemas**

Use `BlogPosting` for original essays and `Article` for publication reviews. Set `isBasedOn` on review schemas to the exact first-party source URL. Keep the Person schema title factual and express Principal/Staff scope only in `knowsAbout` or editorial description when accurate.

- [ ] **Step 4: Update discovery files**

Add every root page and all fourteen article URLs to `sitemap.xml` with `2026-08-23` as the review/refactor last-modified date. Keep the project-root sitemap URL in `robots.txt`. Update the manifest description to match the new engineering-publication positioning.

- [ ] **Step 5: Run SEO and legacy site checks**

Run: `python tests/check_seo_metadata.py`

Expected: PASS.

Run: `python tools/check_site.py`

Expected: PASS for every `tests/check_*.py` file.

- [ ] **Step 6: Commit metadata and discovery**

```powershell
git add . ':!docs' tests/check_seo_metadata.py
git commit -m "feat: align publication metadata and discovery"
```

### Task 7: Responsive QA, comparison, and pull request

**Files:**
- Modify: `assets/styles.css` only if visual verification exposes a defect.
- Modify: `UPDATE-INSTRUCTIONS.txt`
- Modify: `README.md`

**Interfaces:**
- Consumes: the completed site and all automated checks.
- Produces: verified desktop/tablet/mobile layouts, delivery documentation, final commits, pushed branch, and pull request.

- [ ] **Step 1: Run the complete verification suite fresh**

Run: `python tools/check_site.py`

Expected: every check prints PASS and the command exits 0.

- [ ] **Step 2: Serve the site locally**

Run: `python -m http.server 8080`

Inspect `index.html`, `blog.html`, one original essay, and one publication review at 1440×900, 768×1024, and 390×844. Confirm no horizontal overflow, clipped navigation, hidden content before filtering, or headings consuming most of the mobile viewport.

- [ ] **Step 3: Verify interactive behavior**

On `blog.html`, exercise All, one pillar, and one archetype filter; confirm result counts and visible cards match. On mobile, open and close navigation by toggle, link click, and Escape. Traverse primary controls by keyboard and confirm visible focus.

- [ ] **Step 4: Capture comparison screenshots where tooling permits**

Capture homepage and writing-index screenshots at 1440×900 and 390×844. Store temporary QA captures outside the committed site. Add before/after images to the pull request only when both states are available and legible.

- [ ] **Step 5: Update maintenance documentation**

Explain the article taxonomy attributes, required metadata, source-review attribution contract, full verification command, and steps for adding a fifteenth article in `README.md` and `UPDATE-INSTRUCTIONS.txt`.

- [ ] **Step 6: Run final verification after documentation or CSS changes**

Run: `python tools/check_site.py`

Expected: all checks PASS with exit code 0.

- [ ] **Step 7: Review the final diff and commit remaining changes**

Run: `git diff --check`

Expected: no whitespace errors.

Run: `git status --short`

Expected: only intentional README, update-instruction, or CSS changes remain.

```powershell
git add README.md UPDATE-INSTRUCTIONS.txt assets/styles.css
git commit -m "docs: document publication maintenance and verification"
```

- [ ] **Step 8: Push the feature branch and open the pull request**

Push `codex/refactor-principal-engineering-blog` to `origin`. Open a pull request targeting `main` whose body covers the taxonomy rationale, all eight existing classifications, six source reviews and citations, homepage and discovery changes, metadata, preserved URLs, new URLs, and the exact test commands and outcomes.
