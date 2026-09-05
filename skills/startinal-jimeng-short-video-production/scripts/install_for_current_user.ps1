[CmdletBinding()]
param(
    [string]$Destination = (Join-Path $env:USERPROFILE '.codex\skills\startinal-jimeng-short-video-production'),
    [switch]$Force
)

$ErrorActionPreference = 'Stop'
$source = Split-Path -Parent $PSScriptRoot

if (-not (Test-Path -LiteralPath (Join-Path $source 'SKILL.md'))) {
    throw "The Skill source is incomplete: $source"
}
if ((Test-Path -LiteralPath $Destination) -and -not $Force) {
    throw "Destination already exists: $Destination. Review it, then rerun with -Force only if replacing that installed Skill is intended."
}

$parent = Split-Path -Parent $Destination
New-Item -ItemType Directory -Path $parent -Force | Out-Null
New-Item -ItemType Directory -Path $Destination -Force | Out-Null
Get-ChildItem -LiteralPath $source -Force | Copy-Item -Destination $Destination -Recurse -Force

if (-not (Test-Path -LiteralPath (Join-Path $Destination 'SKILL.md'))) {
    throw 'Installation did not produce SKILL.md at the expected destination.'
}

Write-Host "Installed Skill: $Destination"
Write-Host 'Restart Codex, then invoke $startinal-jimeng-short-video-production in a new task.'
