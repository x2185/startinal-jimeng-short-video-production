# CLI production route

Use this reference only for a real Dreamina CLI submission.

## Install and account authorization

On a new computer, first check whether `dreamina -h` runs. If it is not available, direct the operator to the official CLI installer:

```text
https://jimeng.jianying.com/cli
```

Installation downloads and runs provider software. Ask for explicit approval immediately before performing that installation; do not silently run a remote installer. After installation, reopen the terminal if needed and confirm `dreamina -h` works.

For account authorization, use the CLI's OAuth Device Flow. In headless mode, it returns a `verification_uri` and a temporary device code. Give the operator the exact `verification_uri` link and ask them to complete authorization in their own browser. Do not submit, upload media, or spend credits while waiting. Only after they reply that authorization is complete, run the CLI check-login command with that temporary device code and report the actual success or failure. Never put authorization links, device codes, tokens, or session data in a shared job record or Git repository.

## Route selection

Use `multimodal2video` when multiple source types improve product identity or creative control. The command accepts repeated local `--image`, `--video`, and `--audio` inputs in the same submission. Confirm its current help before deciding limits and model support; record the model-specific image, video, audio, and total-input limits in the job record.

Prefer a small reference pack over uploading every available file. Typical product use: one clean hero image, one alternate angle or detail image, and at most one short target-SKU context or motion reference. Keep every reference's role explicit in the prompt package.

Use `image2video` when only one fixed first-frame identity image is necessary. Use `text2video` only when product identity does not need to be preserved. Do not submit a 30-second continuous performance solely to avoid assembly; generate and review coherent scene blocks unless the selected model and brief justify a shorter direct final.

## Preflight

Run these help commands before any live request:

```powershell
dreamina -h
dreamina multimodal2video -h
```

If the required model or parameter is absent from current help, do not guess a fallback. Explain the limitation and offer the supported route.

Confirm the local login with a non-generating account command only if the user has authorized account access. If OAuth is absent or expired, use the CLI's Device Flow. The user must finish account authorization themselves.

## Paid submission record

Before asking approval, prepare a compact record containing:

- target SKU and identity locks
- source-file paths and their roles
- positive prompt and negative constraints
- `dreamina` subcommand, model, duration, resolution, ratio, and output count
- local job folder and expected result filenames
- known unknowns and likely failure risks

After explicit approval, submit one validation clip first when the route is untested. Save the returned submit ID. Query it to terminal status and download only on `success`. If it fails, record the failure reason and revise the smallest affected element before requesting a new paid approval.

## No secret handling

Never write OAuth data, device codes, session files, account balances, API keys, cookies, or browser data into a product job, shared Skill, Git repository, prompt, screenshot, or delivery note.
