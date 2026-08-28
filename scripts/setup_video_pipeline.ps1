[CmdletBinding()]
param(
    [ValidateSet('Check', 'InstallHyperFrames', 'DownloadDockerDesktop', 'StartActivepieces')]
    [string]$Action = 'Check',
    [string]$ProjectRoot = (Get-Location).Path,
    [string]$DataDir = (Join-Path $env:LOCALAPPDATA 'StartinalVideoPipeline\Activepieces'),
    [ValidateRange(1, 65535)]
    [int]$Port = 8080
)

$ErrorActionPreference = 'Stop'

function Write-Result {
    param([string]$State, [string]$Message)
    Write-Host ("{0,-5} {1}" -f $State, $Message)
}

function Get-CommandPath {
    param([string]$Name)
    $command = Get-Command $Name -ErrorAction SilentlyContinue
    if ($null -eq $command) { return $null }
    return $command.Source
}

function Find-FFmpeg {
    $onPath = Get-CommandPath 'ffmpeg'
    if ($onPath) { return $onPath }
    $toolsDir = Join-Path $ProjectRoot 'tools'
    if (Test-Path -LiteralPath $toolsDir) {
        $local = Get-ChildItem -LiteralPath $toolsDir -Filter 'ffmpeg.exe' -Recurse -File -ErrorAction SilentlyContinue |
            Select-Object -First 1 -ExpandProperty FullName
        if ($local) { return $local }
    }
    return $null
}

function Test-DockerReady {
    $docker = Get-CommandPath 'docker'
    if (-not $docker) {
        Write-Result 'FAIL' 'Docker CLI was not found. Install Docker Desktop first.'
        return $false
    }
    & $docker version --format '{{.Server.Version}}' 2>$null | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Result 'FAIL' 'Docker Desktop is installed but its engine is not running.'
        return $false
    }
    Write-Result 'OK' "Docker engine: $(& $docker version --format '{{.Server.Version}}')"
    return $true
}

function Show-Check {
    $node = Get-CommandPath 'node'
    if ($node) {
        $nodeVersion = (& $node --version).Trim()
        Write-Result 'OK' "Node.js $nodeVersion ($node)"
    } else {
        Write-Result 'FAIL' 'Node.js 22 or later is required to install HyperFrames.'
    }

    $ffmpeg = Find-FFmpeg
    if ($ffmpeg) { Write-Result 'OK' "FFmpeg: $ffmpeg" }
    else { Write-Result 'WARN' 'FFmpeg was not found; it is needed for local assembly/rendering.' }

    $projectSkill = Join-Path $ProjectRoot '.agents\skills\hyperframes\SKILL.md'
    $userSkill = Join-Path $env:USERPROFILE '.codex\skills\hyperframes\SKILL.md'
    if (Test-Path -LiteralPath $projectSkill) { Write-Result 'OK' "HyperFrames is installed for this project: $projectSkill" }
    elseif (Test-Path -LiteralPath $userSkill) { Write-Result 'OK' "HyperFrames is installed for this user: $userSkill" }
    else { Write-Result 'WARN' 'HyperFrames is not installed. Run -Action InstallHyperFrames when approved.' }

    $docker = Get-CommandPath 'docker'
    if (-not $docker) {
        Write-Result 'WARN' 'Docker Desktop is not installed. Activepieces is optional and needs Docker.'
    } else {
        Test-DockerReady | Out-Null
    }
    Write-Host ''
    Write-Host 'No credentials, paid JiMeng calls, or services were changed by this check.'
}

switch ($Action) {
    'Check' {
        Show-Check
    }
    'InstallHyperFrames' {
        $node = Get-CommandPath 'node'
        if (-not $node) { throw 'Node.js 22 or later is required. Install Node.js, then rerun this action.' }
        $npx = Get-CommandPath 'npx'
        if (-not $npx) { throw 'npx was not found with Node.js. Repair or reinstall Node.js, then rerun this action.' }
        if (-not (Test-Path -LiteralPath $ProjectRoot)) { throw "ProjectRoot does not exist: $ProjectRoot" }
        Push-Location -LiteralPath $ProjectRoot
        try {
            Write-Host 'Installing the official HyperFrames Codex skill into this project...'
            & $npx skills add heygen-com/hyperframes --skill hyperframes
            if ($LASTEXITCODE -ne 0) { throw "HyperFrames installation failed with exit code $LASTEXITCODE." }
        } finally {
            Pop-Location
        }
        Show-Check
    }
    'DownloadDockerDesktop' {
        $destination = Join-Path $env:TEMP 'DockerDesktopInstaller.exe'
        $url = 'https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe'
        Write-Host 'Downloading the official Docker Desktop installer. It will not be launched automatically.'
        Invoke-WebRequest -Uri $url -OutFile $destination
        Write-Result 'OK' "Downloaded: $destination"
        Write-Host 'Open the installer yourself, review and accept Docker terms if appropriate, complete setup, start Docker Desktop, then run -Action StartActivepieces.'
    }
    'StartActivepieces' {
        if (-not (Test-DockerReady)) { throw 'Activepieces was not started because Docker is unavailable.' }
        $docker = Get-CommandPath 'docker'
        $listener = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
        if ($listener) { throw "Port $Port is already in use. Choose another port with -Port." }
        New-Item -ItemType Directory -Path $DataDir -Force | Out-Null
        $existing = (& $docker ps -a --filter 'name=^/activepieces$' --format '{{.Names}}').Trim()
        if ($existing -eq 'activepieces') {
            & $docker start activepieces | Out-Null
            if ($LASTEXITCODE -ne 0) { throw 'Existing Activepieces container could not be started.' }
            Write-Result 'OK' 'Started the existing Activepieces container.'
        } else {
            $portBinding = "$Port`:80"
            $volumeBinding = "$DataDir`:/root/.activepieces"
            & $docker run -d --name activepieces --restart unless-stopped -p $portBinding -v $volumeBinding activepieces/activepieces | Out-Null
            if ($LASTEXITCODE -ne 0) { throw 'Activepieces container creation failed.' }
            Write-Result 'OK' 'Downloaded and started Activepieces Community Edition.'
        }
        Write-Host "Open http://localhost:$Port to finish the local Activepieces setup. Persistent data: $DataDir"
    }
}
