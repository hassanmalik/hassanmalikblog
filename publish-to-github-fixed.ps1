$ErrorActionPreference = "Stop"

$Owner = "hassanmalik"
$Repo  = "hassanmalikblog"
$FullRepo = "$Owner/$Repo"
$SiteUrl = "https://$Owner.github.io/$Repo/"
$RepoUrl = "https://github.com/$FullRepo.git"

Write-Host ""
Write-Host "Publishing $FullRepo" -ForegroundColor Cyan
Write-Host "Site: $SiteUrl" -ForegroundColor Cyan
Write-Host ""

function Run-Gh {
    param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Args)
    & $script:Gh @Args
    if ($LASTEXITCODE -ne 0) {
        throw "GitHub CLI command failed: gh $($Args -join ' ')"
    }
}

function Run-Git {
    param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Args)
    & git @Args
    if ($LASTEXITCODE -ne 0) {
        throw "Git command failed: git $($Args -join ' ')"
    }
}

# Locate GitHub CLI.
$GhCandidates = @(
    (Get-Command gh -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source -ErrorAction SilentlyContinue),
    "C:\Program Files\GitHub CLI\gh.exe"
) | Where-Object { $_ -and (Test-Path $_) }

if (-not $GhCandidates) {
    Write-Host "GitHub CLI not found. Installing..." -ForegroundColor Yellow
    winget install --id GitHub.cli -e --source winget
    if ($LASTEXITCODE -ne 0) { throw "GitHub CLI installation failed." }
    $Gh = "C:\Program Files\GitHub CLI\gh.exe"
} else {
    $Gh = $GhCandidates[0]
}

Write-Host "Using GitHub CLI: $Gh" -ForegroundColor DarkGray

# Confirm authentication.
& $Gh auth status
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "GitHub login required. A browser login will start." -ForegroundColor Yellow
    Run-Gh auth login --hostname github.com --git-protocol https --web
}

# Configure git identity only for THIS repository.
if (-not (Test-Path ".git")) {
    Run-Git init
}

Run-Git config user.name "Hassan Malik"
Run-Git config user.email "hassanmalik@users.noreply.github.com"

# Normalize branch name.
Run-Git branch -M main

# Stage and commit if needed.
Run-Git add .

& git diff --cached --quiet
$HasStagedChanges = ($LASTEXITCODE -ne 0)

if ($HasStagedChanges) {
    Run-Git commit -m "Launch Hassan Malik technical blog"
} else {
    Write-Host "No new local changes to commit." -ForegroundColor DarkGray
}

# Determine whether GitHub repository already exists.
& $Gh repo view $FullRepo --json name *> $null
$RepoExists = ($LASTEXITCODE -eq 0)

if (-not $RepoExists) {
    Write-Host "Creating GitHub repository $FullRepo..." -ForegroundColor Cyan
    Run-Gh repo create $FullRepo --public --description "Hassan Malik — AI, biotech, and production systems" --source "." --remote origin
} else {
    Write-Host "GitHub repository already exists." -ForegroundColor DarkGray

    $Origin = ""
    try {
        $Origin = (git remote get-url origin 2>$null).Trim()
    } catch {}

    if (-not $Origin) {
        Run-Git remote add origin $RepoUrl
    } elseif ($Origin -ne $RepoUrl) {
        Run-Git remote set-url origin $RepoUrl
    }
}

# Push main.
Write-Host "Pushing main..." -ForegroundColor Cyan
Run-Git push -u origin main

# Enable GitHub Pages in workflow mode. POST creates; PUT/PATCH handles existing.
Write-Host "Configuring GitHub Pages..." -ForegroundColor Cyan
& $Gh api "repos/$FullRepo/pages" *> $null
$PagesExists = ($LASTEXITCODE -eq 0)

if (-not $PagesExists) {
    & $Gh api --method POST "repos/$FullRepo/pages" -f build_type=workflow
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Pages could not be enabled automatically. The workflow is pushed; you can enable Pages in Settings > Pages > GitHub Actions." -ForegroundColor Yellow
    }
} else {
    & $Gh api --method PUT "repos/$FullRepo/pages" -f build_type=workflow *> $null
}

Write-Host ""
Write-Host "Repository: https://github.com/$FullRepo" -ForegroundColor Green
Write-Host "Expected site: $SiteUrl" -ForegroundColor Green
Write-Host ""
Write-Host "Checking recent Pages workflow runs..." -ForegroundColor Cyan

& $Gh run list --repo $FullRepo --limit 5

Write-Host ""
Write-Host "If the latest Pages workflow shows 'completed/success', open:" -ForegroundColor Green
Write-Host $SiteUrl -ForegroundColor Green
