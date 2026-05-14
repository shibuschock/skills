#requires -Version 5.1
<#
.SYNOPSIS
  Install Arend's Claude Code skills into the current user's ~/.claude/skills/.

.DESCRIPTION
  Reads manifest.json, copies selected skill folders into $env:USERPROFILE\.claude\skills\.
  Tier 1 skills are pure markdown/scripts with no required external binaries.
  Tier 2 skills need extra binaries (e.g. ffmpeg, whisper); the installer probes
  for them and prints install hints but does not fail.

.PARAMETER CoreOnly
  Install only tier 1 skills. Default when no scope flag is given.

.PARAMETER All
  Install tier 1 and tier 2 skills. Missing binaries produce warnings, not errors.

.PARAMETER Skills
  Comma-separated list of skill names to install (e.g. "daydream,humanizer").
  Overrides -CoreOnly / -All.

.PARAMETER Target
  Override install target. Default: $env:USERPROFILE\.claude\skills

.PARAMETER DryRun
  Print what would be done without copying anything.

.PARAMETER Force
  Overwrite existing skill folders at the target. Without this, existing folders
  are skipped with a warning.

.EXAMPLE
  .\install.ps1                          # tier 1 only (safest)
  .\install.ps1 -All                     # everything
  .\install.ps1 -Skills daydream,humanizer
  .\install.ps1 -DryRun -All             # show plan, don't copy
#>

[CmdletBinding()]
param(
  [switch]$CoreOnly,
  [switch]$All,
  [string]$Skills,
  [string]$Target = "$env:USERPROFILE\.claude\skills",
  [switch]$DryRun,
  [switch]$Force
)

$ErrorActionPreference = 'Stop'
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$manifestPath = Join-Path $scriptRoot 'manifest.json'
$skillsRoot = Join-Path $scriptRoot 'skills'

if (-not (Test-Path $manifestPath)) {
  Write-Error "manifest.json not found at $manifestPath. Run install.ps1 from the repo root."
}

$manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json

# --- Determine which skills to install ---
$requested = @()
if ($Skills) {
  $names = $Skills -split ',' | ForEach-Object { $_.Trim() } | Where-Object { $_ }
  $requested = $manifest.skills | Where-Object { $names -contains $_.name }
  $missing = $names | Where-Object { -not ($manifest.skills.name -contains $_) }
  if ($missing) { Write-Warning "Unknown skill(s) ignored: $($missing -join ', ')" }
}
elseif ($All) {
  $requested = $manifest.skills
}
else {
  # Default: -CoreOnly (tier 1)
  $requested = $manifest.skills | Where-Object { $_.tier -eq 1 }
}

if (-not $requested) {
  Write-Error "No skills selected. Check -Skills value or use -All."
}

# --- Pre-flight ---
Write-Host ""
Write-Host "Install target : $Target"
Write-Host "Mode           : $(if ($DryRun) { 'DRY RUN' } else { 'EXECUTE' })"
Write-Host "Force          : $Force"
Write-Host "Skills selected: $($requested.name -join ', ')"
Write-Host ""

if (-not (Test-Path $Target)) {
  if ($DryRun) {
    Write-Host "[dry-run] would create $Target"
  } else {
    New-Item -ItemType Directory -Path $Target -Force | Out-Null
    Write-Host "Created $Target"
  }
}

# --- Tier 2 binary probe ---
$tier2 = $requested | Where-Object { $_.tier -eq 2 }
if ($tier2) {
  Write-Host "Checking tier-2 binary dependencies..." -ForegroundColor Cyan
  $needed = $tier2.binaries | Sort-Object -Unique
  $missingBin = @()
  foreach ($bin in $needed) {
    if (Get-Command $bin -ErrorAction SilentlyContinue) {
      Write-Host "  [ok]      $bin found"
    } else {
      Write-Host "  [missing] $bin" -ForegroundColor Yellow
      $missingBin += $bin
    }
  }
  if ($missingBin) {
    Write-Host ""
    Write-Host "Some tier-2 skills will not work fully until these are installed:" -ForegroundColor Yellow
    foreach ($bin in $missingBin) {
      switch -Wildcard ($bin) {
        'ffmpeg'  { Write-Host "  ffmpeg   : winget install Gyan.FFmpeg" }
        'ffprobe' { Write-Host "  ffprobe  : bundled with ffmpeg (Gyan.FFmpeg)" }
        'whisper*' { Write-Host "  whisper  : build whisper.cpp (https://github.com/ggerganov/whisper.cpp) and put 'whisper-cli' on PATH" }
        default   { Write-Host "  $bin : (no preset hint, check the skill's SKILL.md)" }
      }
    }
    Write-Host "Continuing install; the skill files copy fine, only runtime calls will fail." -ForegroundColor Yellow
  }
  Write-Host ""
}

# --- Copy loop ---
$installed = @()
$skipped = @()
$copied = @()
foreach ($s in $requested) {
  $src = Join-Path $skillsRoot $s.name
  $dst = Join-Path $Target $s.name

  if (-not (Test-Path $src)) {
    Write-Warning "Source missing: $src (skipping)"
    $skipped += "$($s.name) [source missing]"
    continue
  }

  if (Test-Path $dst) {
    if (-not $Force) {
      Write-Host "[skip] $($s.name) already at $dst (use -Force to overwrite)" -ForegroundColor Yellow
      $skipped += "$($s.name) [exists]"
      continue
    }
    if ($DryRun) {
      Write-Host "[dry-run] would remove existing $dst"
    } else {
      Remove-Item -Recurse -Force $dst
    }
  }

  if ($DryRun) {
    Write-Host "[dry-run] would copy $src -> $dst ($($s.fileCount) files, $([math]::Round($s.sizeBytes/1KB,1)) KB)"
    $installed += $s.name
  } else {
    Copy-Item -Recurse -Path $src -Destination $dst
    Write-Host "[ok] $($s.name) -> $dst" -ForegroundColor Green
    $installed += $s.name
    $copied += $s.name
  }
}

# --- Summary ---
Write-Host ""
Write-Host "==================== Summary ===================="
Write-Host "Installed: $($installed.Count) skill(s)$(if ($DryRun) { ' (DRY RUN - nothing copied)' })"
foreach ($n in $installed) { Write-Host "  + $n" -ForegroundColor Green }
if ($skipped) {
  Write-Host "Skipped:"
  foreach ($n in $skipped) { Write-Host "  - $n" -ForegroundColor Yellow }
}
Write-Host ""
if (-not $DryRun -and $copied) {
  Write-Host "Next steps:"
  Write-Host "  1. Start a new Claude Code session (or restart your current one)."
  Write-Host "  2. Type / in the prompt and verify the skill names appear in autocomplete."
  Write-Host "  3. Smoke-test one: /humanizer (or whichever you installed)."
}
