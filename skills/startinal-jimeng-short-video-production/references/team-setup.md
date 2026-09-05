# Team setup: HyperFrames and Activepieces

This skill works for planning and JiMeng generation without either optional tool. Use this setup only when the project needs deterministic finishing templates or local workflow orchestration.

Run the setup script from the project folder. Its default action is read-only:

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\startinal-jimeng-short-video-production\scripts\setup_video_pipeline.ps1 -Action Check
```

If the skill is installed globally instead of copied into a project, call the same script from its installed skill folder and add `-ProjectRoot <project-folder>` to identify the project that should receive HyperFrames.

## HyperFrames

HyperFrames creates deterministic HTML/CSS/media renders. Use it for repeatable captions, end cards, overlays, and batch-consistent layout after JiMeng source clips have passed visual acceptance.

Install it into the current project only after approval:

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\startinal-jimeng-short-video-production\scripts\setup_video_pipeline.ps1 -Action InstallHyperFrames
```

It requires Node.js 22 or later and installs the official skill under `.agents\skills\hyperframes`. It does not call JiMeng or use credentials.

## Activepieces

Activepieces is an optional self-hosted workflow layer. It can queue approved packages, call local scripts, hold approvals, retry non-paid processing steps, and track render manifests. It is not a replacement for the final paid JiMeng approval gate.

Docker Desktop is required. Download its official installer only when the teammate has approval to do so:

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\startinal-jimeng-short-video-production\scripts\setup_video_pipeline.ps1 -Action DownloadDockerDesktop
```

The script does not launch the installer or accept Docker terms. After the user has manually installed and started Docker Desktop, start the local Community Edition instance:

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\startinal-jimeng-short-video-production\scripts\setup_video_pipeline.ps1 -Action StartActivepieces
```

Open `http://localhost:8080` to finish initial local setup. The script stores its persistent data outside the project at `%LOCALAPPDATA%\StartinalVideoPipeline\Activepieces`; do not place AK/SK/API keys in the shared skill folder, source repository, or job manifest.

For an occupied port, choose another one, for example `-Port 8081`.
