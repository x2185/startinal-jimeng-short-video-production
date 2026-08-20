---
name: startinal-jimeng-short-video-production
description: Plan, prompt, validate, and assemble JiMeng-generated TikTok Shop product videos. Use when a user needs a 30-second product video split into stable 3×10-second or 6×5-second JiMeng clips; asks for story-led creative variants, continuity-safe prompts, shot acceptance checks, or FFmpeg assembly of approved JiMeng clips.
---

# JiMeng short-video production

Create a production plan; do not submit paid JiMeng generation tasks unless the user explicitly asks.

For a new teammate using local assembly, run `scripts/check_environment.py --assembly` first. Read `references/environment-setup.md` for the minimal setup; do not install or expose credentials inside the skill.

## First interaction

Greet the user briefly, explain that this skill turns supplied product material into 20 complete 30-second story packages (60 linked prompts by default), then audits, generates only after approval, and assembles approved clips. Inspect existing conversation/files first, then collect only missing product identity, play/use, verified features, buyer/market, restrictions, and extra creative requirements. Do not generate prompts before blocking facts are answered or disclosed assumptions are accepted.

Read `references/first-run-intake.md` for the opening wording and intake routing.

## Workflow

1. Run the intake gate before planning. Inspect the conversation and supplied files first; do not ask for information already present.
2. Ask concise follow-up questions for every missing blocking input. Do not generate production prompts until the blocking inputs are answered or the user explicitly accepts a stated assumption.
3. Choose the shot plan.
   - Prefer **3 × 10 seconds** when the available JiMeng model reliably supports 10 seconds and scenes require continuous action.
   - Use **6 × 5 seconds** for difficult hand interaction, product-detail shots, or when 10-second clips drift or deform.
   - Use mixed durations only when the available JiMeng mode explicitly supports each duration.
4. Derive narrative options from the current product brief and supplied assets. Do not reuse stories, characters, settings, or dialogue from a prior product unless the user asks.
5. Write a shot brief for every generated clip: purpose and duration; reference-assets roles; positive prompt; continuity locks; negative constraints; and acceptance checks.
6. Run the prompt-quality gate. Audit every draft for product identity, verified claims, 30-second story logic, adjacent-clip handoff, model-executable specificity, negative constraints, and marketplace safety. Fix every failed item, then produce the submission-ready prompt set and a concise change log.
7. Present the final pre-submission review package: chosen 30-second story, the three submission-ready prompts, all reference assets, confirmed claims, and remaining assumptions/risks. Require an explicit user approval before any paid JiMeng submission or API call.
8. Run the reference-frame gate after each approved clip and before generating its continuation. Extract multiple candidates from the final stable portion; inspect them and select a product-visible handoff frame. Never automatically use the literal last frame.
9. Keep each clip independently generatable. Reuse the same approved product reference throughout. For the next clip, use the approved handoff frame as its reference when the interface allows it.
10. Ask the user to select only approved clips before assembly. Do not conceal visual defects through editing.
11. Assemble approved files with `scripts/assemble_jimeng_clips.py`. This uses FFmpeg locally and consumes no LLM tokens or JiMeng credits.

## Intake gate

Treat these as blocking inputs:

- **Product identity:** product name plus at least one reference image/video or a precise visual description of color, shape, packaging, logo/text, and included parts.
- **Verified facts:** usable selling points, specifications, and claims that may appear in the video.
- **Restrictions:** prohibited claims, unsafe use, prohibited visuals, and brand/legal limits.
- **Audience and market:** intended buyer plus language/market when the final captions or spoken lines depend on them.

Ask for the missing items in one compact message. For example: “I have the product images, but need the verified selling points, prohibited claims, and target buyer before I can create a safe production plan.”

Treat these as non-blocking inputs and state the default before using it: target duration (default 30 seconds), format (default vertical 9:16), scene preference (default everyday home setting), creative route (default create a 5×4 matrix), CTA (default product-link prompt), and music/caption preference.

If the user cannot provide a blocking fact, omit it from the video rather than guessing. Ask for a reference asset again when product identity cannot be locked.

Read `references/intake-checklist.md` when checking whether provided product materials are sufficient.

## Prompt rules

- Use concise English unless the JiMeng interface or user requires Chinese.
- State vertical 9:16, exact duration, product identity locks, camera direction, ending composition, and safe text area when applicable.
- Lock color, shape, logo/text, included parts, scale, and setting. End each clip with a stable composition suitable for the next cut.
- Exclude warped geometry, unreadable labels, duplicate products, extra fingers, unrelated brands, unsupported claims, and unsafe use.
- Do not request copyrighted characters, deceptive packaging, or real-person endorsements.

## Story-variant framework

Use this only when the user wants scenarios, plots, or a creative matrix.

1. Propose **five distinct 30-second narrative routes** grounded in the current product's visible proof, target buyer, restrictions, and available settings. A route must state: actor/context, ordinary tension or goal, product interaction, visual proof, and end state.
2. Create **four complete 30-second variants per route**. A variant must change at least two of: opening event, actor goal, setting, product action, proof order, character relationship, outcome, camera perspective, or CTA placement. Do not count adjective swaps as variation.
3. Treat every variant as one **30-second story package**, split only because of JiMeng duration limits. The default creative matrix therefore produces **5 routes × 4 variants = 20 story packages**, and a 3 × 10-second plan produces **20 × 3 = 60 linked JiMeng prompts**. Write three linked prompts per package: clip 1 = setup/reveal; clip 2 = continuation/proof; clip 3 = outcome/product hero/CTA. Do not present the three clips as unrelated mini-stories.
4. Put an explicit handoff in every prompt: clip 1 states its final actor/product/camera state; clip 2 begins from that state and states its own ending; clip 3 begins from clip 2's ending. Instruct the operator to add the accepted prior clip's final frame as a reference to the next generation when supported.
5. Preserve claims and product identity across variants. Use adults by default; do not direct purchase persuasion at minors. Treat subjective comfort or enjoyment as subjective, not medical/therapeutic proof.
6. Ask the user to choose a route before submitting any paid generation. When no choice is requested, rank routes by asset fit and label assumptions.

Read `references/story-variant-framework.md` before creating story-led variants.

## Required output

Return:

1. A one-line production choice: `3 × 10s` or `6 × 5s`, with reason.
2. A time-coded storyboard.
3. When story-led variants are requested: a 5 × 4 matrix of **20 complete 30-second story packages**, with route, full arc, visible proof, difference, asset requirement, and its three linked prompts (**60 prompts total** for a 3 × 10-second plan).
4. One complete JiMeng prompt per generated clip, including the required prior-clip handoff.
5. A prompt-quality audit showing pass/fix status and the final improved prompts; do not submit the draft prompts.
6. A final pre-submission review package and an explicit approval request for each selected 30-second package; do not submit on silence or implied approval.
7. A continuity and acceptance checklist.
8. An assembly command after the user names the approved video files.

Read `references/production-workflow.md` when choosing durations, preparing an approval gate, or assembling clips.
Read `references/reference-frame-gate.md` before selecting an image to carry a generated clip into its continuation.
Read `references/prompt-quality-gate.md` after drafting prompts and before presenting them as ready for submission.
Read `references/final-approval-gate.md` before a paid JiMeng request or API submission.

## Assembly

Use the script after confirming input filenames and output location:

```powershell
python scripts/assemble_jimeng_clips.py --clips clip-01.mp4 clip-02.mp4 clip-03.mp4 --output final.mp4
```

If FFmpeg is not installed on the system `PATH`, pass its executable explicitly: `--ffmpeg "C:\\tools\\ffmpeg.exe"`.

Use `--reencode` only when the input clips use incompatible codecs or dimensions. The script joins clips; it does not generate subtitles, music, transitions, or video content.
