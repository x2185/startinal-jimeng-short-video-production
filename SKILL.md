---
name: startinal-jimeng-short-video-production
description: Plan, prompt, validate, and assemble JiMeng-generated TikTok Shop product videos. Use when a user needs a 30-second product video split into stable 3×10-second or 6×5-second JiMeng clips; asks for story-led creative variants, continuity-safe prompts, shot acceptance checks, or FFmpeg assembly of approved JiMeng clips.
---

# JiMeng short-video production

Create a production plan; do not submit paid JiMeng generation tasks unless the user explicitly asks.

For a new teammate using local assembly, run `scripts/check_environment.py --assembly` first. If FFmpeg is missing, explain the finding and ask whether to run `scripts/check_environment.py --install-missing`; never install software without explicit user approval. Read `references/environment-setup.md` for the minimal setup; do not install or expose credentials inside the skill.

## First interaction

Greet the user briefly, explain that this skill turns supplied product material into 20 complete 30-second creative packages (60 linked prompts by default), then audits, generates only after approval, and assembles approved clips. Inspect existing conversation/files first, then collect only missing product identity, play/use, verified features, buyer/market, restrictions, and extra creative requirements. Unless already explicitly supplied, always ask a separate question for: verified selling points and the core functions/features that must be shown and preserved. Do not infer these from video alone. Once blocking facts are answered or disclosed assumptions are accepted, generate the full default 20-package matrix immediately. Generate fewer packages only when the user explicitly asks for a smaller test batch.

Read `references/first-run-intake.md` for the opening wording and intake routing.

## Workflow

1. Run the intake gate before planning. Inspect the conversation and supplied files first; do not ask for information already present. When a material folder is supplied, run `scripts/scan_product_assets.py --root <folder> --manifest <job-output>/asset-manifest.json` before reusing any earlier product brief or prompt set.
2. Ask concise follow-up questions for every missing blocking input. Do not generate production prompts until the blocking inputs are answered or the user explicitly accepts a stated assumption.
3. Choose the shot plan.
   - Prefer **3 × 10 seconds** when the available JiMeng model reliably supports 10 seconds and scenes require continuous action.
   - Use **6 × 5 seconds** for difficult hand interaction, product-detail shots, or when 10-second clips drift or deform.
   - Use mixed durations only when the available JiMeng mode explicitly supports each duration.
4. Derive and output the default matrix of 20 complete 30-second creative packages from the current product brief and supplied assets. Mix suitable modes—story, gameplay/function proof, visual product showcase, interaction/reaction, and hook/reveal—instead of forcing every package into a plot. Do not reuse stories, characters, settings, or dialogue from a prior product unless the user asks. Generate a smaller count only when the user explicitly requests it.
5. Build a **product identity passport** from the supplied material before writing any prompts: category; silhouette; color; material; proportions; surface details; logo/text; included parts; packaging when relevant; and forbidden substitutions. Treat this passport as a hard lock for every clip and every variant. If the asset manifest reports added, changed, or deleted files, rebuild and reconfirm this passport; do not reuse an earlier one blindly.
6. Reserve **product-detail evidence** in every 30-second creative package: at least one uninterrupted 2-second macro/close product shot, product filling at least 60% of the frame (70% for fine markings or texture), with the named identity traits in focus and unobscured. Plan the detail shot as an intentional story or proof beat, not a generic cutaway. Do not slow the entire clip merely to show detail: use a short, high-information proof insert, then return to the package's progression. For slow-rebound products, show one clear squeeze/release and enough real-time recovery to read the rebound; do not request artificial slow motion unless the user asks.
7. Write a shot brief for every generated clip: purpose and duration; reference-assets roles; product identity passport; detail-evidence requirement; positive prompt; continuity locks; negative constraints; and acceptance checks.
8. Run the prompt-quality gate. Audit every draft for exact product identity against the supplied material, visible product-detail evidence, preservation of user-confirmed core features, verified claims, 30-second story logic, adjacent-clip handoff, model-executable specificity, negative constraints, and marketplace safety. Fix every failed item, then produce the submission-ready prompt set, a feature-preservation ledger, and a concise change log. Never silently remove a confirmed core feature or approve a substituted/changed product.
9. Without asking the user to choose routes or review drafts, assemble the complete final submission package: all 20 creative packages / 60 revised prompts, grouped by package ID and creative mode; the product identity passport; a detail-evidence shot index; reference assets; verified claims; feature-preservation ledger; and remaining assumptions/risks.
10. Present one final human approval gate immediately before any paid JiMeng submission or API call. Ask the user to approve the package IDs to submit. Do not submit drafts, unapproved IDs, or any package on silence.
11. Run the reference-frame gate after each generated clip and before generating its continuation. Extract multiple candidates from the final stable portion; inspect them and select a product-visible handoff frame. Never automatically use the literal last frame. A candidate that changes the product identity passport is ineligible.
12. Keep each clip independently generatable. Reuse the fixed product-identity reference throughout whenever the API supports multiple references; otherwise, carry the approved handoff frame forward and repeat the complete identity passport in the prompt. Never allow a continuation to substitute a different product, colorway, packaging, logo, material, or included part.
13. Assemble approved files with `scripts/assemble_jimeng_clips.py`. This uses FFmpeg locally and consumes no LLM tokens or JiMeng credits.
14. For an approved API run, use `scripts/run_jimeng_a1_package.py` with its default `--download-route auto`. It retries the normal route and a proxy-bypassing direct route, refreshes an expired signed CDN URL once, and resumes completed local clips without resubmitting or spending again. Do not ask the operator to manually download a clip before those recovery steps have failed.

## Intake gate

Treat these as blocking inputs:

- **Product identity:** product name plus at least one reference image/video or a precise visual description of color, shape, packaging, logo/text, and included parts.
- **Verified facts:** usable selling points, specifications, and claims that may appear in the video.
- **Restrictions:** prohibited claims, unsafe use, prohibited visuals, and brand/legal limits.
- **Audience and market:** intended buyer plus language/market when the final captions or spoken lines depend on them.

Ask for the missing items in one compact message. For example: “I have the product images, but need the verified selling points, prohibited claims, and target buyer before I can create a safe production plan.”

Treat selling points and must-show core functions as a separate blocking question unless the user already stated them explicitly. A video can demonstrate a possible action, but it does not establish which feature should be marketed, whether it is real, or whether it must be retained.

Treat an identity passport as blocking: verify at least the product's category, silhouette, dominant color, material/surface, distinctive details, and included parts from the supplied material. When packaging, logo, or readable text is material to the product identity, lock it too. Do not plan a scenario that would hide the only available identity evidence.

Treat these as non-blocking inputs and state the default before using it: target duration (default 30 seconds), format (default vertical 9:16), scene preference (default everyday home setting), creative route (default create a 5×4 matrix), CTA (default product-link prompt), and music/caption preference.

If the user cannot provide a blocking fact, omit it from the video rather than guessing. Ask for a reference asset again when product identity cannot be locked.

Read `references/intake-checklist.md` when checking whether provided product materials are sufficient.
Read `references/asset-change-gate.md` whenever reusing a material folder or an earlier product brief.

## Prompt rules

- Use concise English unless the JiMeng interface or user requires Chinese.
- State vertical 9:16, exact duration, product identity locks, camera direction, ending composition, and safe text area when applicable.
- Lock color, shape, logo/text, included parts, scale, and setting. End each clip with a stable composition suitable for the next cut.
- State: "Use the supplied reference as the exact product; do not redesign, substitute, simplify, recolor, relabel, or add/remove any product part." Repeat the passport's distinguishing traits in every prompt.
- For every required detail-evidence shot, state the exact visible traits; product frame coverage (minimum 60%, 70% for fine detail); macro/close focus; stable sharp focus; and that hands/props must not obscure the named detail. Do not use vague wording such as "show product details."
- Make the three linked clips advance one complete story: clip 1 establishes a concrete everyday situation or tension and introduces the product; clip 2 changes the situation through a decisive interaction and contains only a short detail-proof insert; clip 3 shows a visible result or payoff before the hero ending. Do not fill a 30-second story with repeated squeezing, a static product hold, or slow motion unless those are explicitly requested.
- Exclude warped geometry, unreadable labels, duplicate products, extra fingers, unrelated brands, changed product/colorway/packaging, unsupported claims, and unsafe use.
- Do not request copyrighted characters, deceptive packaging, or real-person endorsements.

## Story-variant framework

Use this as the default creative output after intake. Do not wait for the user to separately request scenarios, plots, or a matrix.

1. Select five or more distinct creative routes across the modes in `references/story-variant-framework.md`, grounded in the current product's visible proof, target buyer, restrictions, and available settings. A route must state its mode, product interaction, visual proof, and end state; a story route additionally states actor/context and tension or goal.
2. Create **20 complete 30-second variants** with a balanced mode mix. A variant must change at least two structural dimensions appropriate to its mode: opening event, actor goal, setting, product action, proof order, character relationship, outcome, camera perspective, hook, or CTA placement. Do not count adjective swaps as variation.
3. Treat every variant as one **30-second creative package**, split only because of JiMeng duration limits. A 3 × 10-second plan therefore produces **20 × 3 = 60 linked JiMeng prompts**. Story packages use setup → change/proof → outcome; showcase and demonstration packages use hook/reveal → clear proof → hero/payoff. Do not present the three clips as unrelated mini-videos.
4. Put an explicit handoff in every prompt: clip 1 states its final actor/product/camera state; clip 2 begins from that state and states its own ending; clip 3 begins from clip 2's ending. Instruct the operator to add the accepted prior clip's final frame as a reference to the next generation when supported.
5. Preserve claims and product identity across variants. Use adults by default; do not direct purchase persuasion at minors. Treat subjective comfort or enjoyment as subjective, not medical/therapeutic proof.
6. Rank routes by asset fit and label assumptions, but do not ask the user to choose a route during generation. Ask for approval only after all 20 packages have been generated, audited, and optimized.

Read `references/story-variant-framework.md` before creating story-led variants.

## Required output

Return:

1. A one-line production choice: `3 × 10s` or `6 × 5s`, with reason.
2. A time-coded storyboard.
3. By default: a mode-balanced matrix of **20 complete 30-second creative packages**, with mode, route, full arc or proof progression, visible proof, difference, asset requirement, and its three linked prompts (**60 prompts total** for a 3 × 10-second plan). Generate fewer only when the user explicitly requests it.
4. One complete JiMeng prompt per generated clip, including the required prior-clip handoff.
5. A prompt-quality audit showing pass/fix status and the final improved prompts; do not submit the draft prompts.
6. A detail-evidence index: for every package, timecode, named product traits, required frame coverage, and proof action.
7. One final pre-submission package containing all 20 optimized creative packages / 60 prompts, plus an explicit approval request for the package IDs to submit; do not interrupt earlier with route-choice or draft-review questions.
8. A continuity and acceptance checklist.
9. An assembly command after the user names the approved video files.

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
