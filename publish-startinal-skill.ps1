param(
    [string]$Repository = 'x2185/startinal-jimeng-short-video-production',
    [string]$Branch,
    [string]$Message = 'Update flexible toy creative modes and resilient JiMeng API workflow'
)

$ErrorActionPreference = 'Stop'
$skillRoot = Join-Path $PSScriptRoot 'skills\startinal-jimeng-short-video-production'

if (-not (Test-Path -LiteralPath $skillRoot)) {
    throw "Skill source not found: $skillRoot"
}

gh auth status | Out-Host

try {
    $repositoryInfo = gh repo view $Repository --json name,defaultBranchRef,url,viewerPermission | ConvertFrom-Json
}
catch {
    throw "Cannot access GitHub repository '$Repository'. Confirm its owner/name and that the signed-in account has write access. $($_.Exception.Message)"
}
if ([string]::IsNullOrWhiteSpace($Branch)) {
    $Branch = $repositoryInfo.defaultBranchRef.name
}
if ([string]::IsNullOrWhiteSpace($Branch)) {
    throw "GitHub did not report a default branch for '$Repository'."
}
Write-Host "Publishing to $($repositoryInfo.url), branch '$Branch'."

function Invoke-GitHubJson {
    param(
        [Parameter(Mandatory)] [string[]]$Arguments,
        [object]$Body
    )

    $previousErrorPreference = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        if ($PSBoundParameters.ContainsKey('Body')) {
            $raw = $Body | ConvertTo-Json -Depth 20 -Compress | gh api @Arguments --input - 2>&1
        }
        else {
            $raw = gh api @Arguments 2>&1
        }
        $exitCode = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $previousErrorPreference
    }
    if ($exitCode -ne 0) {
        $detail = ($raw | Out-String).Trim()
        throw "GitHub API request failed: gh api $($Arguments -join ' ') :: $detail"
    }
    $text = ($raw | Out-String).Trim()
    if ([string]::IsNullOrWhiteSpace($text)) {
        throw "GitHub API request returned no JSON: gh api $($Arguments -join ' ')"
    }
    return $text | ConvertFrom-Json
}

function Get-RemoteFileSha {
    param([Parameter(Mandatory)] [string]$Path)
    $previousErrorPreference = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        $raw = gh api "repos/$Repository/contents/$Path`?ref=$Branch" 2>&1
        $exitCode = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $previousErrorPreference
    }
    if ($exitCode -eq 0) {
        return (($raw | Out-String) | ConvertFrom-Json).sha
    }
    if (($raw | Out-String) -match 'HTTP 404') {
        return $null
    }
    throw "Cannot inspect remote file '$Path': $(($raw | Out-String).Trim())"
}

function Get-GitBlobSha {
    param([Parameter(Mandatory)] [byte[]]$Bytes)
    $prefix = [Text.Encoding]::UTF8.GetBytes("blob $($Bytes.Length)`0")
    $payload = New-Object byte[] ($prefix.Length + $Bytes.Length)
    [Array]::Copy($prefix, 0, $payload, 0, $prefix.Length)
    [Array]::Copy($Bytes, 0, $payload, $prefix.Length, $Bytes.Length)
    $hash = [Security.Cryptography.SHA1]::Create().ComputeHash($payload)
    return ([BitConverter]::ToString($hash) -replace '-', '').ToLowerInvariant()
}

$files = Get-ChildItem -LiteralPath $skillRoot -Recurse -File |
    Where-Object { $_.FullName -notmatch '[\\/]__pycache__[\\/]' -and $_.Extension -notmatch '^\.py[co]$' }

$index = 0
$published = 0
foreach ($file in $files) {
    $index++
    $relative = $file.FullName.Substring($skillRoot.Length + 1).Replace('\', '/')
    $bytes = [IO.File]::ReadAllBytes($file.FullName)
    $existingSha = Get-RemoteFileSha -Path $relative
    if ($existingSha -eq (Get-GitBlobSha -Bytes $bytes)) {
        Write-Host "Unchanged $index/$($files.Count): $relative"
        continue
    }
    $body = @{
        message = "$Message ($index/$($files.Count))"
        content = [Convert]::ToBase64String($bytes)
        branch = $Branch
    }
    if ($existingSha) {
        $body.sha = $existingSha
    }
    Invoke-GitHubJson -Arguments @('--method', 'PUT', "repos/$Repository/contents/$relative") -Body $body | Out-Null
    $published++
    Write-Host "Published $index/$($files.Count): $relative"
}

Write-Host "Published $published changed skill files."
Write-Host "https://github.com/$Repository/tree/$Branch"
