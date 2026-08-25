# Team environment

The downloaded skill includes its instructions, references, and local scripts. It does not install software or contain API keys.

## Minimum setup

| Activity | Requirement |
| --- | --- |
| Plan, audit, and write JiMeng prompts | Codex plus the installed skill. No JiMeng API key is required. |
| Join approved clips locally | Python 3.9+ and FFmpeg. Put FFmpeg on `PATH` or pass its path to the scripts. |
| Automatically submit/generate/download from JiMeng | A separately implemented, provider-specific API integration and credentials stored outside the skill. |

The skill does not require the web app, Node.js, or the project backend for prompt-only or local assembly work.

## First-run check

Run from the skill folder:

```powershell
python scripts/check_environment.py
python scripts/check_environment.py --assembly
python scripts/check_environment.py --assembly --ffmpeg "C:\tools\ffmpeg.exe"
```

Use `--assembly` before creating a final local video. The check never reads or prints secrets.

## Optional guided installation

On Windows, if FFmpeg is missing, Codex must first report the missing dependency and ask the user for approval. After an explicit approval, run:

```powershell
python scripts/check_environment.py --install-missing
```

The command uses Windows `winget` to install `Gyan.FFmpeg.Shared`. It does not install Python, because Python must already be available to run the checker. After installation, open a new terminal and run the check again. If `winget` is unavailable or the operating system is not Windows, give the user manual installation guidance instead of attempting a download.

## Credentials

Keep a personal or company credential in each machine's ignored project `.env`, a secret manager, or a company backend. Do not put it in `SKILL.md`, `agents/openai.yaml`, prompt files, screenshots, or Git commits.

## CDN download recovery

Run `run_jimeng_a1_package.py` with its default `--download-route auto`. It first uses the system route, then retries with environment HTTP(S) proxies bypassed, refreshes the signed result URL once, and resumes from valid local files without re-submitting a paid task.

An application-level VPN that tunnels all Windows traffic cannot be disabled safely or reliably by this skill. Configure that VPN for split tunneling/direct access to `aigc-cloud.com` and `volcengineapi.com` before a production batch. If the network blocks both routes, the runner preserves task IDs and artifacts for a later `--resume`; it never discards paid output.
