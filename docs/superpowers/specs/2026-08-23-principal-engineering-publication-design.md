# Principal Engineering Publication Refactor Design

## Purpose

Refactor Hassan Malik's existing static technical blog into a focused engineering publication whose scope is understandable within ten seconds: production AI, distributed systems, software and cloud architecture, reliability at scale, technical leadership, and forward-deployed engineering.

The redesign must reveal engineering judgment through structure and framing without inventing titles, employers, projects, metrics, or outcomes. It must preserve the existing visual identity and all current article URLs.

## Current State

The repository is a dependency-free static site made from hand-authored HTML, one shared stylesheet, and minimal JavaScript. It contains eight long-form articles, a homepage, publication index, lab, experience, about, and contact pages. GitHub Pages deploys the default branch directly. Existing Python checks cover local links, positioning language, typography, metadata, structured data, and sitemap entries.

The visual system is distinctive and worth retaining, but the current information architecture uses overlapping topic groups, oversized display typography, and article listings that do not expose a consistent domain or engineering-problem classification.

## Chosen Approach

Enhance the existing static architecture rather than introduce a framework or build system. Semantic HTML will carry the taxonomy and article metadata, CSS will provide the publication layout, and a small progressive-enhancement script will filter the article index. All content remains usable when JavaScript is unavailable.

This approach has lower operational cost and preserves GitHub Pages behavior. A generator would reduce repeated markup, but eight existing articles plus six planned reviews do not justify a framework migration in this refactor.

## Information Architecture

The primary navigation will prioritize Home, Writing, Engineering Lab, About, and Contact. Experience remains available through contextual links but will not make the publication resemble a resume.

Writing is organized into six pillars:

1. Architecture
2. AI & Data
3. Platform & Infrastructure
4. Reliability & Scale
5. Technical Leadership
6. Forward-Deployed Engineering

Every article receives exactly one primary pillar, one engineering problem archetype, and a concise set of topic tags. The archetypes are Build, Scale, Migrate, Optimize, Harden, Design, and Strategize. Security remains a cross-cutting tag.

The displayed classification uses the format `Pillar × Archetype`, such as `AI & Data × Design`. Filters operate on pillars and archetypes while tags remain descriptive metadata.

## Existing Article Audit

| Existing article | Primary pillar | Archetype | Core tags | Title action |
| --- | --- | --- | --- | --- |
| AI Architecture for Biotech: Why Production AI Systems Fail at the Workflow Boundary | AI & Data | Design | AI Architecture, Biotech, Workflow Integration, Production AI | Preserve |
| The Production AI Stack for Biotech R&D | AI & Data | Build | GenAI, Data Platforms, Evaluation, Human-in-the-loop | Preserve |
| Dashboards Are Not Decision Systems | Technical Leadership | Strategize | Decision Systems, Ownership, Operating Models | Preserve |
| Distributed Systems for Agentic AI: Retries, Idempotency and Failure Recovery | Reliability & Scale | Harden | AI Agents, Distributed Systems, Idempotency, Observability | Preserve |
| Enterprise RAG Architecture for Scientific R&D: Retrieval, Evidence and Provenance | AI & Data | Design | RAG, Retrieval, Provenance, Authorization | Preserve |
| Forward Deployed Engineering: Prototype the Risk, Not the AI Demo | Forward-Deployed Engineering | Build | Customer Discovery, Prototyping, Productization, AI Deployment | Preserve |
| Why Adoption Is an Architecture Problem in Scientific Software | Forward-Deployed Engineering | Strategize | Adoption, Scientific Software, Trust, Workflow Design | Preserve |
| Operating Across Software and Operations | Technical Leadership | Strategize | Cross-team Influence, Operating Models, Architecture | Preserve |

No existing article body or URL changes unless verification uncovers a factual, accessibility, or linking issue. The current titles already communicate problems and tradeoffs well enough to retain.

## Engineering Publication Review Series

Add six substantial review articles, one per pillar. Each article reviews a primary source from a respected engineering publication and uses a consistent editorial structure: source context, central engineering problem, architectural approach, explicit tradeoffs, what generalizes, what is context-dependent, questions for an architecture review, and links to the original source.

The planned source map is:

| Pillar | Publication/source family | Review focus |
| --- | --- | --- |
| Architecture | Martin Fowler | How architectural patterns communicate boundaries, evolutionary change, and tradeoffs |
| AI & Data | Uber Engineering | What a production ML platform reveals about the system around the model |
| Platform & Infrastructure | Cloudflare Engineering | How platform constraints shape infrastructure architecture and operational simplicity |
| Reliability & Scale | Netflix TechBlog | How resilience practices turn failure into an explicit design input |
| Technical Leadership | StaffEng | How senior individual contributors create leverage through strategy, alignment, and judgment |
| Forward-Deployed Engineering | Stripe Engineering | How reliable APIs and integration design reduce customer-facing delivery risk |

During implementation, each review will cite a specific official article or first-party source from the mapped publication. Source claims will be paraphrased and linked. Direct quotations will be minimal. Commentary will not imply that Hassan built, operated, or measured the reviewed system.

The reviews will be clearly labeled as publication reviews rather than first-hand case studies. They receive the same `Pillar × Archetype` metadata as original essays and a `Source Review` tag.

## Homepage

The homepage will contain, in order:

1. A compact hero stating the publication's engineering scope without presenting Principal or Staff Engineer as Hassan's current title.
2. A featured deep dive with visible pillar, archetype, and reading-time metadata.
3. A six-pillar directory with short, concrete descriptions.
4. Recent technical writing combining original essays and source reviews.
5. Selected deep dives emphasizing architecture, reliability, AI systems, and FDE.
6. A concise professional-positioning section centered on the kinds of systems and decisions explored in the publication.
7. Clear GitHub, LinkedIn, writing, and contact routes.

The hero and metadata may naturally use recruiter-relevant terms such as software architecture, distributed systems, AWS, cloud architecture, platform engineering, GenAI, LLM, RAG, AI agents, data engineering, reliability engineering, technical leadership, and Forward Deployed Engineer. Keywords will appear only where supported by the site's actual content.

## Writing Index and Discovery

The writing page will open with a concise publication statement followed by the six pillars. A filter bar will support All, each pillar, and each engineering archetype. Article cards remain semantic links and expose:

- article type: original essay or publication review;
- `Pillar × Archetype` classification;
- title and summary;
- topic tags;
- reading time and publication date where known.

Filtering is progressive enhancement. Without JavaScript, every article stays visible and grouped access remains available through anchor links.

## Article Presentation

All article pages will use a common context block below the dek. It will show article type, pillar, archetype, tags, author, reading time, and date when available. Related-reading links will favor the same pillar or a complementary archetype. Review posts will additionally show a prominent source-attribution block near the beginning and a source link at the end.

Article prose remains constrained to a readable measure. Heading scales and vertical spacing will be tuned so long technical titles do not dominate mobile screens.

## Visual System

Retain the paper, ink, blue, and acid color palette; serif editorial headings; monospace metadata; dark architecture panels; and restrained motion. Remove the animated architecture pulse and any hover movement that interferes with reduced-motion preferences.

The revised system will use smaller responsive display headings, more consistent section spacing, stronger card boundaries, visible keyboard focus, and layouts that collapse cleanly below tablet width. No imagery is required: diagrams and typographic structure remain native HTML/CSS so the publication stays fast and credible.

## Metadata and SEO

Each page will have a unique title, meta description, canonical URL, Open Graph metadata, and appropriate JSON-LD. Original essays use `BlogPosting`; source reviews use `Review` or `Article` only where the structured-data fields can be represented accurately. The Person schema must not claim a Principal or Staff job title.

The sitemap will include all existing and new URLs. Internal links will use the GitHub Pages project path correctly. Review descriptions will identify both the reviewed engineering problem and the publication without pretending affiliation.

## Accessibility and Failure Behavior

Navigation, filtering controls, and article cards will be keyboard accessible. Filter state will use real buttons and an announced result count. If JavaScript fails, all content remains visible. External links will have meaningful labels, mobile navigation will maintain accurate expanded state, and focus styles will remain visible.

Reduced-motion preferences will disable nonessential transitions and animation. Color contrast, landmark structure, heading order, and tap-target sizing will be covered by automated checks where practical and manual review otherwise.

## Verification

Automated verification will cover:

- every local link, asset, and same-page fragment;
- one valid pillar and archetype per article;
- all six pillars represented on the homepage and writing index;
- all fourteen articles represented in the index and sitemap;
- unique titles, descriptions, canonicals, and structured data;
- accurate LinkedIn and GitHub links;
- no false Principal or Staff job-title claims;
- review-post source attribution and external source links;
- filter controls and progressive-enhancement behavior;
- responsive and reduced-motion CSS requirements.

The site will also be served locally and inspected at mobile, tablet, and desktop viewport widths. Before-and-after screenshots will be captured where the available browser tooling permits it.

## Delivery

Work stays on `codex/refactor-principal-engineering-blog`. Commits will separate the taxonomy/test foundation, core publication redesign, article metadata migration, review series, and final verification where practical. No changes go directly to the default branch.

The pull request will explain the taxonomy, article classifications, homepage and discovery changes, review-source methodology, metadata updates, title and URL decisions, and all verification performed. Existing URLs will remain unchanged; the six review articles will add new URLs.
