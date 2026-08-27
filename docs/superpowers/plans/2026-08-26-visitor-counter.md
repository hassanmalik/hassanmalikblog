# Visitor Counter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Show live total-visit and country counts in the website header, backed by the existing Cloudflare Worker and D1 database.

**Architecture:** Every page renders the same accessible counter in the header. The shared JavaScript records at most one visit per browser session, retrieves aggregate statistics from the Worker, formats them for display, and leaves a quiet unavailable state when the API cannot be reached.

**Tech Stack:** Static HTML, CSS, browser JavaScript, Cloudflare Worker/D1 REST endpoints, Python publication checks.

**Spec:** Approved in the current Codex task on 2026-08-26.

## Global Constraints

- Use `https://blog-counter.hassanmalik1989.workers.dev` as the Worker origin.
- Record one visit per browser session through `POST /visit`.
- Read aggregate data through `GET /stats`.
- Display total visits and country count in the top-right header across the site.
- Keep the counter accessible with a status label and `aria-live` updates.
- Do not block navigation or page rendering when the Worker is unavailable.
- Preserve the existing mobile navigation and dark Lab theme.

---

### Task 1: Counter contract and behavior

**Files:**
- Create: `tests/check_visitor_counter.py`
- Modify: `assets/main.js`
- Modify: all deployable `*.html` pages

**Interfaces:**
- Consumes: Worker responses shaped as `{"visits": number, "countries": number, "topCountries": array}`.
- Produces: `[data-visitor-counter]`, `[data-visit-count]`, and `[data-country-count]` elements updated by shared JavaScript.

- [ ] **Step 1: Write the failing test** that loads all deployable pages and executes the shared script in a small browser-like harness, checking the visible aggregate values and once-per-session POST behavior.
- [ ] **Step 2: Run the test to verify it fails** because the counter markup and behavior do not exist.
- [ ] **Step 3: Add the minimal shared markup and JavaScript** to render statistics, record a visit only when the session key is absent, and retain fallback copy after request failure.
- [ ] **Step 4: Run the test to verify it passes.**

### Task 2: Responsive presentation

**Files:**
- Modify: `assets/styles.css`
- Modify: `tests/check_visitor_counter.py`
- Modify: `tests/check_visual_regressions.py`

**Interfaces:**
- Consumes: counter markup from Task 1.
- Produces: compact desktop header styling and mobile-safe presentation.

- [ ] **Step 1: Extend the failing test** to require the top-right utility structure, green status dot, compact mobile rules, Lab theme treatment, and a new asset cache version.
- [ ] **Step 2: Run the test to verify the styling contract fails.**
- [ ] **Step 3: Add the minimal responsive CSS** and update the shared asset version on every deployable page.
- [ ] **Step 4: Run the counter and publication checks to verify they pass.**

### Task 3: Production verification and pull request

**Files:**
- Verify: entire working tree

**Interfaces:**
- Consumes: completed feature and existing Worker endpoint.
- Produces: a pushed feature branch and website pull request.

- [ ] **Step 1: Verify the Worker GET endpoint and CORS response** without incrementing the production counter.
- [ ] **Step 2: Run the full publication suite.**
- [ ] **Step 3: Review the final diff for accessibility, privacy, and unrelated changes.**
- [ ] **Step 4: Commit, push, and update the existing pull request or create a replacement if it has merged.**
