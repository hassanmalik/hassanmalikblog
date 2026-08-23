$ErrorActionPreference = 'Stop'

$Owner = 'hassanmalik'
$Repo = 'hassanmalikblog'
$RepoFull = "$Owner/$Repo"
$Remote = "https://github.com/$RepoFull.git"
$SiteUrl = "https://$Owner.github.io/$Repo/"

function Get-GhPath {
    $cmd = Get-Command gh -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }

    $common = @(
        "$env:ProgramFiles\GitHub CLI\gh.exe",
        "$env:LOCALAPPDATA\Programs\GitHub CLI\gh.exe"
    )
    foreach ($path in $common) {
        if (Test-Path $path) { return $path }
    }
    return $null
}

Write-Host "Publishing $RepoFull" -ForegroundColor Cyan
Write-Host "Site: $SiteUrl"
Write-Host ''

$gh = Get-GhPath
if (-not $gh) {
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if (-not $winget) {
        throw 'GitHub CLI is not installed and winget is unavailable. Install GitHub CLI from https://cli.github.com/ and run this script again.'
    }
    Write-Host 'Installing GitHub CLI...' -ForegroundColor Yellow
    & winget install --id GitHub.cli --exact --source winget --accept-package-agreements --accept-source-agreements
    $gh = Get-GhPath
    if (-not $gh) {
        throw 'GitHub CLI installation finished, but gh.exe was not found. Close PowerShell, reopen it, and run this script again.'
    }
}

Write-Host 'Checking GitHub login...' -ForegroundColor Yellow
& $gh auth status *> $null
if ($LASTEXITCODE -ne 0) {
    Write-Host 'A GitHub browser login will open. Sign in as hassanmalik and approve GitHub CLI.' -ForegroundColor Yellow
    & $gh auth login --hostname github.com --git-protocol https --web
    if ($LASTEXITCODE -ne 0) { throw 'GitHub login was not completed.' }
}

$login = (& $gh api user --jq '.login').Trim()
if ($login.ToLowerInvariant() -ne $Owner.ToLowerInvariant()) {
    throw "GitHub CLI is authenticated as '$login', not '$Owner'. Run 'gh auth switch' or 'gh auth login' for $Owner, then rerun this script."
}

Set-Location $PSScriptRoot

if (-not (Test-Path '.git')) {
    git init
}

git add .
$changes = git status --porcelain
if ($changes) {
    git commit -m 'Publish Hassan Malik technical blog'
}

git branch -M main

$origin = git remote get-url origin 2>$null
if ($LASTEXITCODE -ne 0) {
    git remote add origin $Remote
} elseif ($origin -ne $Remote) {
    git remote set-url origin $Remote
}

Write-Host 'Checking repository...' -ForegroundColor Yellow
& $gh repo view $RepoFull *> $null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Creating public repository $RepoFull..." -ForegroundColor Yellow
    & $gh repo create $RepoFull --public --description 'AI, biotech, data systems, and production engineering by Hassan Malik' --disable-wiki
    if ($LASTEXITCODE -ne 0) { throw 'Could not create the GitHub repository.' }
} else {
    Write-Host 'Repository already exists; using it.' -ForegroundColor Green
}

Write-Host 'Enabling GitHub Pages with GitHub Actions...' -ForegroundColor Yellow
& $gh api "repos/$RepoFull/pages" *> $null
if ($LASTEXITCODE -ne 0) {
    $pagesJson = '{"build_type":"workflow"}'
    $pagesJson | & $gh api --method POST "repos/$RepoFull/pages" --input -
    if ($LASTEXITCODE -ne 0) {
        throw 'Could not enable GitHub Pages automatically. The repository was created; enable Settings > Pages > Source: GitHub Actions and rerun the script.'
    }
} else {
    $updateJson = '{"build_type":"workflow"}'
    $updateJson | & $gh api --method PUT "repos/$RepoFull/pages" --input - *> $null
}

Write-Host 'Pushing main...' -ForegroundColor Yellow
git push -u origin main
if ($LASTEXITCODE -ne 0) { throw 'Git push failed.' }

Write-Host 'Waiting for the Pages deployment workflow...' -ForegroundColor Yellow
Start-Sleep -Seconds 3
$runId = (& $gh run list --repo $RepoFull --workflow deploy-pages.yml --limit 1 --json databaseId --jq '.[0].databaseId' 2>$null).Trim()
if ($runId) {
    & $gh run watch $runId --repo $RepoFull --exit-status
    if ($LASTEXITCODE -ne 0) {
        Write-Host 'The repository is published, but the Pages workflow needs attention. Opening Actions.' -ForegroundColor Yellow
        & $gh repo view $RepoFull --web
        exit 1
    }
}

Write-Host ''
Write-Host 'Published successfully.' -ForegroundColor Green
Write-Host "Repository: https://github.com/$RepoFull"
Write-Host "Website:    $SiteUrl"
Write-Host ''
Write-Host 'Opening the website...'
Start-Process $SiteUrl
