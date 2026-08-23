# hassanmalikblog

Personal technical publication for **Hassan Malik** focused on AI architecture, biotech software, scientific workflows, data systems, production engineering, and technical leadership.

## Live URL

Once GitHub Pages is enabled, this repository is designed to publish at:

**https://hassanmalik.github.io/hassanmalikblog/**

## Local preview

```bash
python -m http.server 8080
```

Then open `http://localhost:8080`.


## One-command Windows publish

Open PowerShell in this folder and run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\publish-to-github.ps1
```

The script verifies GitHub CLI authentication, creates `hassanmalik/hassanmalikblog` if necessary, enables GitHub Pages with the GitHub Actions build type, pushes `main`, and watches the Pages workflow. It does not store a GitHub token in this repository.

## Publish on GitHub Pages

This repository already includes `.github/workflows/deploy-pages.yml`.

1. Create a repository named **`hassanmalikblog`** under `github.com/hassanmalik`.
2. Push all files in this folder to the `main` branch.
3. Open **Settings → Pages** in the repository.
4. Under **Build and deployment**, set **Source** to **GitHub Actions**.
5. The included workflow deploys the site whenever `main` is updated.

### Command-line push

```bash
git init
git add .
git commit -m "Launch Hassan Malik technical blog"
git branch -M main
git remote add origin https://github.com/hassanmalik/hassanmalikblog.git
git push -u origin main
```

## Custom domain later

When a domain is purchased:

1. Rename `CNAME.example` to `CNAME` and replace its contents with the exact hostname.
2. Update canonical URLs, `robots.txt`, and `sitemap.xml` from the GitHub Pages URL to the new domain.
3. Add the custom domain under **Settings → Pages**.
4. Configure DNS with the registrar.
5. Enable **Enforce HTTPS** after DNS resolves.

## Structure

- `index.html` — homepage
- `blog.html` — publication index and taxonomy
- `lab.html` — architecture experiments
- `experience.html` — career and selected impact
- `about.html` — biography
- `contact.html` — contact routes
- `posts/` — long-form technical essays
- `assets/` — CSS, JavaScript and favicon

No package manager or build step is required.

## Verification

Install the development-only HTML parser with `python -m pip install beautifulsoup4`, then run the complete publication check suite:

```powershell
python tools/check_site.py
```


## SEO/content update (2026-08-22)

The publication now targets Principal Software Engineering, Applied AI, AI Architecture, Distributed Systems, Biotech/Life Sciences, Enterprise RAG, LLM Evaluation, and Forward Deployed Engineering search intent. GitHub Pages is intended to deploy directly from the `main` branch.
