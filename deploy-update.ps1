$ErrorActionPreference = "Stop"
Write-Host "Checking repository..." -ForegroundColor Cyan
$cleanup = @(
  ".github\workflows\deploy-pages.yml",
  "publish-simple.ps1",
  "publish-to-github-fixed.ps1",
  "publish-to-github.ps1"
)
foreach ($item in $cleanup) {
  if (Test-Path $item) { Remove-Item $item -Force }
}
if (-not (Test-Path ".git")) { throw "Run this from your existing hassanmalikblog repository folder (the one containing .git)." }
git status --short
git add -A
if ($LASTEXITCODE -ne 0) { throw "git add failed" }
git diff --cached --quiet
if ($LASTEXITCODE -eq 0) { Write-Host "Nothing to deploy."; exit 0 }
git commit -m "Refine readability, LinkedIn identity and technical positioning"
if ($LASTEXITCODE -ne 0) { throw "git commit failed" }
git push
if ($LASTEXITCODE -ne 0) { throw "git push failed" }
Write-Host "Update pushed. GitHub Pages will publish from main." -ForegroundColor Green
Write-Host "https://hassanmalik.github.io/hassanmalikblog/" -ForegroundColor Green
