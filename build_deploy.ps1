# Build script: assemble deploy/ folder for Vercel
# Website goes at root, PWA goes at /pwa/
param([switch]$Clean)

$deployDir = Join-Path $PSScriptRoot "deploy"

if ($Clean -and (Test-Path $deployDir)) {
    Remove-Item $deployDir -Recurse -Force
}

New-Item -ItemType Directory -Path $deployDir -Force | Out-Null
New-Item -ItemType Directory -Path "$deployDir\pwa" -Force | Out-Null
New-Item -ItemType Directory -Path "$deployDir\pwa\icons" -Force | Out-Null

# Copy website files to deploy root
Write-Host "Copying website..."
$websiteDir = Join-Path $PSScriptRoot "website"
Get-ChildItem $websiteDir -Recurse | ForEach-Object {
    $rel = $_.FullName.Substring($websiteDir.Length + 1)
    $dest = Join-Path $deployDir $rel
    if ($_.PSIsContainer) {
        New-Item -ItemType Directory -Path $dest -Force | Out-Null
    } else {
        $parentDir = Split-Path $dest -Parent
        if (!(Test-Path $parentDir)) { New-Item -ItemType Directory -Path $parentDir -Force | Out-Null }
        Copy-Item $_.FullName $dest -Force
    }
}

# Copy PWA files to deploy/pwa/
Write-Host "Copying PWA..."
$pwaDir = Join-Path $PSScriptRoot "pwa"
Get-ChildItem $pwaDir -Recurse | ForEach-Object {
    $rel = $_.FullName.Substring($pwaDir.Length + 1)
    $dest = Join-Path "$deployDir\pwa" $rel
    if ($_.PSIsContainer) {
        New-Item -ItemType Directory -Path $dest -Force | Out-Null
    } else {
        $parentDir = Split-Path $dest -Parent
        if (!(Test-Path $parentDir)) { New-Item -ItemType Directory -Path $parentDir -Force | Out-Null }
        Copy-Item $_.FullName $dest -Force
    }
}

Write-Host "Deploy folder ready at: $deployDir"
Write-Host "  Website: deploy/ (root)"
Write-Host "  PWA:     deploy/pwa/"
