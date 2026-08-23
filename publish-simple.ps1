$ErrorActionPreference = "Stop"

$gh = "C:\Program Files\GitHub CLI\gh.exe"

Write-Host "Configuring Git identity..."
git config user.name "Hassan Malik"
if ($LASTEXITCODE -ne 0) { throw "git config user.name failed" }

git config user.email "hassanmalik@users.noreply.github.com"
if ($LASTEXITCODE -ne 0) { throw "git config user.email failed" }

Write-Host "Committing site..."
git add .
if ($LASTEXITCODE -ne 0) { throw "git add failed" }

git commit -m "Launch Hassan Malik technical blog"
if ($LASTEXITCODE -ne 0) {
    $status = git status --porcelain
    if ($status) { throw "git commit failed" }
    Write-Host "Nothing new to commit."
}

git branch -M main
if ($LASTEXITCODE -ne 0) { throw "git branch failed" }

Write-Host "Checking repository..."
& $gh repo view hassanmalik/hassanmalikblog
if ($LASTEXITCODE -ne 0) {
    Write-Host "Creating repository..."
    & $gh repo create hassanmalik/hassanmalikblog --public --description "Hassan Malik - AI, biotech, and production systems"
    if ($LASTEXITCODE -ne 0) { throw "GitHub repository creation failed" }
}

$remotes = git remote
if ($remotes -contains "origin") {
    git remote set-url origin "https://github.com/hassanmalik/hassanmalikblog.git"
} else {
    git remote add origin "https://github.com/hassanmalik/hassanmalikblog.git"
}
if ($LASTEXITCODE -ne 0) { throw "origin configuration failed" }

Write-Host "Pushing..."
git push -u origin main
if ($LASTEXITCODE -ne 0) { throw "git push failed" }

Write-Host ""
Write-Host "PUSH COMPLETE"
Write-Host "Repo: https://github.com/hassanmalik/hassanmalikblog"
Write-Host ""
Write-Host "Next: enable Pages in GitHub Settings > Pages > Source: GitHub Actions"
