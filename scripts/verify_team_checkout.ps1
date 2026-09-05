[CmdletBinding()]
param(
    [switch]$Strict
)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$failed = $false

function Write-Check {
    param(
        [ValidateSet('OK', 'WARN', 'FAIL')][string]$State,
        [string]$Message,
        [bool]$Required = $false
    )
    Write-Host ("{0,-5} {1}" -f $State, $Message)
    if ($State -eq 'FAIL' -and $Required) { $script:failed = $true }
}

function Find-CommandPath {
    param([string]$Name)
    $command = Get-Command $Name -ErrorAction SilentlyContinue
    if ($null -eq $command) { return $null }
    return $command.Source
}

function Find-ProjectFFmpeg {
    $onPath = Find-CommandPath 'ffmpeg'
    if ($onPath) { return $onPath }
    $tools = Join-Path $projectRoot 'tools'
    if (Test-Path -LiteralPath $tools) {
        return Get-ChildItem -LiteralPath $tools -Filter 'ffmpeg.exe' -Recurse -File -ErrorAction SilentlyContinue |
            Select-Object -First 1 -ExpandProperty FullName
    }
    return $null
}

Write-Host "Startinal team checkout: $projectRoot"
Write-Host 'This check never reads .env values, calls JiMeng, installs software, or starts services.'

$skill = Join-Path $projectRoot 'skills\startinal-jimeng-short-video-production\SKILL.md'
if (Test-Path -LiteralPath $skill) { Write-Check OK "Bundled Skill: $skill" $true }
else { Write-Check FAIL 'Bundled Skill is missing.' $true }

$installedSkill = Join-Path $env:USERPROFILE '.codex\skills\startinal-jimeng-short-video-production\SKILL.md'
if (Test-Path -LiteralPath $installedSkill) { Write-Check OK "Skill installed for current user: $installedSkill" }
else { Write-Check WARN 'Skill is not installed for this Windows user. Run skills\startinal-jimeng-short-video-production\scripts\install_for_current_user.ps1.' }

$python = Find-CommandPath 'python'
if ($python) { Write-Check OK "Python: $((& $python --version).Trim()) ($python)" $true }
else { Write-Check FAIL 'Python 3.9+ was not found.' $true }

$node = Find-CommandPath 'node'
if ($node) { Write-Check OK "Node.js: $((& $node --version).Trim()) ($node)" $true }
else { Write-Check FAIL 'Node.js was not found; it is needed for the frontend and optional HyperFrames.' $true }

$ffmpeg = Find-ProjectFFmpeg
if ($ffmpeg) { Write-Check OK "FFmpeg: $ffmpeg" $true }
else { Write-Check FAIL 'FFmpeg was not found on PATH or under tools\. Install it before local assembly.' $true }

$envFile = Join-Path $projectRoot '.env'
if (Test-Path -LiteralPath $envFile) { Write-Check OK 'Local .env exists (values deliberately not inspected).' }
else { Write-Check WARN 'No local .env. Copy .env.example to .env only on the computer that will call JiMeng.' }

$frontendModules = Join-Path $projectRoot 'frontend\node_modules'
if (Test-Path -LiteralPath $frontendModules) { Write-Check OK 'Frontend dependencies are present.' }
else { Write-Check WARN 'Frontend dependencies are missing. Run npm ci in frontend after approval.' }

$venvPython = Join-Path $projectRoot '.venv\Scripts\python.exe'
if (Test-Path -LiteralPath $venvPython) { Write-Check OK 'Backend virtual environment is present.' }
else { Write-Check WARN 'Backend virtual environment is missing. Create .venv and install backend\requirements.txt before starting the local dashboard.' }

$git = Find-CommandPath 'git'
if (-not $git) {
    Write-Check WARN 'Git is not installed; project updates can still be copied manually.'
} elseif (-not (Test-Path -LiteralPath (Join-Path $projectRoot '.git'))) {
    Write-Check WARN 'This folder is not a Git checkout.'
} else {
    $nameOutput = @(& $git -C $projectRoot config --local user.name 2>$null)
    $emailOutput = @(& $git -C $projectRoot config --local user.email 2>$null)
    $name = if ($nameOutput.Count) { $nameOutput[0].Trim() } else { '' }
    $email = if ($emailOutput.Count) { $emailOutput[0].Trim() } else { '' }
    if ($name -and $email) { Write-Check OK "Git author configured locally: $name <$email>" }
    else { Write-Check WARN 'Git author is not configured locally. This only blocks creating commits.' }
}

Write-Host ''
Write-Host 'Optional: Docker + Activepieces are not required for Skill planning, JiMeng calls, or FFmpeg assembly.'
if ($Strict -and $failed) { exit 1 }
