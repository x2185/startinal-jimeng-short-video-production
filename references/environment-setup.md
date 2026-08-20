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

## Credentials

Keep a personal or company credential in each machine's ignored project `.env`, a secret manager, or a company backend. Do not put it in `SKILL.md`, `agents/openai.yaml`, prompt files, screenshots, or Git commits.
