---
name: startinal-jimeng-short-video-production
description: Plan, prompt, validate, and assemble JiMeng-generated TikTok Shop product videos. Use when a user needs a 30-second product video split into stable 3×10-second or 6×5-second JiMeng clips; asks for story-led creative variants, continuity-safe prompts, shot acceptance checks, or FFmpeg assembly of approved JiMeng clips.
---

# JiMeng short-video production

Create a production plan; do not submit paid JiMeng generation tasks unless the user explicitly asks.

For a new teammate or computer, when working from the full project and `scripts/verify_team_checkout.ps1` exists, run that project-level check first. Then run `scripts/setup_video_pipeline.ps1 -Action Check` and `scripts/check_environment.py --assembly` when local assembly is needed. A standalone installed Skill can skip the project-level check. These checks are read-only. On explicit approval only, the setup script can install the project-local HyperFrames skill, download (but never launch) Docker Desktop, or start a local Activepieces instance after Docker is already running. Read `references/team-setup.md` for this optional layer and `references/environment-setup.md` for the minimal FFmpeg setup; never install software, accept external terms, or expose credentials without explicit user approval.

## First interaction

Greet the user briefly, explain that this skill turns supplied product material into 20 complete 30-second creative packages (60 linked prompts by default), then audits, generates only after approval, and assembles approved clips. Inspect existing conversation/files first, then collect only missing product identity, play/use, verified features, buyer/market, restrictions, and extra creative requirements. Unless already explicitly supplied, always ask a separate question for: verified selling points and the core functions/features that must be shown and preserved. Do not infer these from video alone. Once blocking facts are answered or disclosed assumptions are accepted, generate the full default 20-package matrix immediately. Generate fewer packages only when the user explicitly asks for a smaller test batch.

Read `references/first-run-intake.md` for the opening wording and intake routing.

## Workflow

1. For each new product, inspect and scan the supplied material folder first. Run `scripts/scan_product_assets.py --root <folder> --manifest <job-output>/asset-manifest.json`; extract representative frames from videos, build a contact sheet when useful, and select candidate identity, detail, action, and ending-state assets. Then complete the asset observation gate before prompt drafting: review the strongest still at full resolution and multiple frames around each required action; build a visible-configuration ledger and, for multi-part/variant products, an explicit pairing map such as frame color → attached-part color. Record what each selected asset visibly proves; do not infer a mechanism, pairing, or selling point from an ambiguous frame.
2. When public market-reference research has been enabled for the workflow, conduct it before scripting. Search TikTok/TikTok Shop, Amazon, and other accessible public results for likely product-title variants, common visual hooks, demonstrated use cases, and recurring compliance or safety risks. Treat platform access limits and unavailable video files as normal; use only information that can be inspected lawfully. Extract patterns and keywords, never copy another seller's footage, captions, music, product copy, branding, or distinctive creative treatment into a commercial output.
3. Build a provisional product brief that separates: facts visually supported by the user's assets; candidate product details or keywords found in public research; unknown facts; and proposed safety restrictions. In the same brief, summarize reusable editing patterns, visual style, settings, and story/content structure observed in reference videos. Proactively add a prioritized quality-improvement recommendation list: better identity/action references, authentic footage for fragile actions, simpler or shorter shots, separate atmosphere shots, camera/composition changes, reusable finishing templates, or controlled candidate-generation batches. State expected quality gain, cost/time, and risk for each proposal. Reference research never verifies the user's product specification, safety claim, age grade, performance, included parts, price, or ownership of media, and no recommendation may silently change the approved creative direction.
4. Apply low-risk quality decisions automatically when the evidence is clear: select the strongest identity and action references; reject unsafe or off-topic source footage; choose the supported clip duration and one-action split; select camera framing, scene role, candidate count, and a reusable finishing template; and reject failed clips against the acceptance gate. Record each material decision and its reason in the job manifest. Do not ask the user to choose among ordinary production options merely because several acceptable options exist.
5. Return only the compact confirmation questions that remain materially unknown or high-impact: product facts and claims, SKU/variant, audience/market, age and safety restrictions, prohibited content, externally sourced information that conflicts with supplied evidence, a meaningful budget change, use of a real person/brand, and every paid API submission. Do not generate prompts, make a paid API call, or present external-market details as confirmed product facts until those gates are resolved.
5. Choose the shot plan.
   - Prefer **3 × 10 seconds** for a simple reveal, lifestyle scene, or one continuous, evidence-backed action when the available JiMeng model reliably supports 10 seconds.
   - Use **6 × 5 seconds** when the product has two or more distinct state changes or fine interactions such as opening, loading, inserting, fastening, twisting, pressing, connecting, dispensing, tapping, or payment; also use it after 10-second clips drift, deform, or combine unrelated actions.
   - Do not choose a duration merely to fill 30 seconds. Choose the shortest supported clip duration that contains one clearly verifiable action and a stable ending state.
   - Use mixed durations only when the available JiMeng mode explicitly supports each duration.
6. Run the action-and-state reference gate before drafting prompts. For every must-show interaction, map the product identity, starting state, one permitted action, and ending state to supplied evidence. Prefer original action footage or action-specific stills over a packshot. A packshot establishes appearance only; it cannot prove an unseen mechanism. Redact or avoid source material with readable personal data, card data, brands, prices, or prohibited content. If the action has no evidence, ask for it or omit the action—never have the model invent a hidden mechanism.
7. Derive and output the default matrix of 20 complete 30-second creative packages from the current product brief and supplied assets. Mix suitable modes—story, gameplay/function proof, visual product showcase, interaction/reaction, and hook/reveal—instead of forcing every package into a plot. Do not reuse stories, characters, settings, or dialogue from a prior product unless the user asks. Generate a smaller count only when the user explicitly requests it.
8. Build a **product identity passport** from the supplied material before writing any prompts: category; silhouette; color; material; proportions; surface details; logo/text; included parts; packaging when relevant; and forbidden substitutions. Treat this passport as a hard lock for every clip and every variant. If the asset manifest reports added, changed, or deleted files, rebuild and reconfirm this passport; do not reuse an earlier one blindly.
8a. When generated story scenes need a real product to remain visually exact, build a **product reference pack** from the best verified identity frames before prompt drafting. Preserve original source frames, generate transparent cutouts only when the local background-removal dependency is available and the result passes edge review, and label every cutout as an identity asset—not proof of an unseen action. Use the pack for deterministic compositing or as a staged first-frame reference. Do not ask image-to-video to recreate fine product geometry, conceal a failed mechanical action, or simulate hand occlusion it cannot preserve.
9. Reserve **product-detail evidence** in every 30-second creative package: at least one uninterrupted 2-second macro/close product shot, product filling at least 60% of the frame (70% for fine markings or texture), with the named identity traits in focus and unobscured. Plan the detail shot as an intentional story or proof beat, not a generic cutaway. Do not slow the entire clip merely to show detail: use a short, high-information proof insert, then return to the package's progression. For slow-rebound products, show one clear squeeze/release and enough real-time recovery to read the rebound; do not request artificial slow motion unless the user asks.
10. Apply the default visual baseline unless the evidence or brief requires an override. Run the generative-action risk gate before assigning an action to a generated clip. When an action is too fine or state-dependent to be reliably generated, keep the finished product as a stable story prop and use supplied real footage for the operation. Then write a shot brief for every generated clip: purpose and duration; reference-assets roles; product identity passport; detail-evidence requirement; baseline/override lighting, setting, camera, and composition; positive prompt; continuity locks; negative constraints; and acceptance checks. For every selected test package, paid-ready package, or explicitly story-led UGC request, upgrade these briefs into a director-grade prompt package: character/continuity bible, time-coded beat sheet, direct English submission prompt, and clip-specific acceptance gate. A creative matrix alone is never submission-ready.
11. Before the prompt-quality gate, run one internal pre-submission prompt-optimization pass. Reconcile the product/action evidence, story beats, continuity locks, and likely model failures; make one focused revision rather than merely lengthening the prompt. Then run the prompt-quality gate. Audit every draft for exact product identity against the supplied material, visible product-detail evidence, preservation of user-confirmed core features, verified claims, 30-second story logic, adjacent-clip handoff, model-executable specificity, negative constraints, and marketplace safety. Fix every failed item, then produce the submission-ready prompt set, a feature-preservation ledger, and a concise change log. Never silently remove a confirmed core feature or approve a substituted/changed product.
12. Without asking the user to choose routes or review drafts, assemble the complete final submission package: all 20 creative packages / 60 revised prompts, grouped by package ID and creative mode; the product identity passport; a detail-evidence shot index; reference assets; verified claims; feature-preservation ledger; and remaining assumptions/risks.
13. Present one final human approval gate immediately before any paid JiMeng submission or API call. Ask the user to approve the package IDs to submit. Do not submit drafts, unapproved IDs, or any package on silence.
14. Run the reference-frame gate after each generated clip and before generating its continuation. Extract multiple candidates from the final stable portion; inspect them and select a product-visible handoff frame. Never automatically use the literal last frame. A candidate that changes the product identity passport is ineligible.
15. Keep each clip independently generatable. Reuse the fixed product-identity reference throughout whenever the API supports multiple references; otherwise, carry the approved handoff frame forward and repeat the complete identity passport in the prompt. Never allow a continuation to substitute a different product, colorway, packaging, logo, material, or included part.
16. Assemble approved files with `scripts/assemble_jimeng_clips.py`. This uses FFmpeg locally and consumes no LLM tokens or JiMeng credits.
17. For an approved API run, use `scripts/run_jimeng_a1_package.py` with its default `--download-route auto`. It retries the normal route and a proxy-bypassing direct route, refreshes an expired signed CDN URL once, and resumes completed local clips without resubmitting or spending again. For a named, explicitly approved test-only package, use `--max-clips 1` to validate the highest-risk first action before paying for the remaining linked clips; the runner must skip final assembly for a partial test and the package must guard against accidental full submission. Do not ask the operator to manually download a clip before those recovery steps have failed.
18. Separate generation from finishing. Treat accepted JiMeng clips as immutable source media. Produce a render manifest for the deterministic finishing layer: selected source files and trim ranges; 9:16 canvas and safe areas; caption/CTA text; timing; audio; transitions; and output filename. Use a deterministic renderer such as HyperFrames only when designed captions, overlays, reusable motion graphics, or batch-consistent layouts are requested; otherwise use the existing FFmpeg assembly path.
19. Preview and inspect the finished render before delivery. A deterministic overlay may clarify captions, transitions, or layout, but must never conceal a failed product action, changed product identity, warped object, or unapproved claim. Replace or regenerate the failed source clip instead.
20. After an accepted/rejected test or material user feedback, write a concise job retrospective. For an iterative test, use the closed-loop optimization pass: evaluate candidates against the locked product/action/continuity checks, diagnose the failed layer, revise only that layer, and regenerate only failed clips after paid approval. Keep the lesson product-local by default; promote it into the shared skill only when it has repeated across products or the user explicitly confirms it as a general production preference.
21. After a run, classify generated outputs non-destructively with `scripts/catalog_generated_assets.py`, then use `scripts/organize_generated_assets.py` to copy and rename reviewed material into the generated-material library. Keep original product evidence, accepted generated references, unreviewed candidates, rejected media, and job records distinct. Never move the original run folder or treat a generated asset as product evidence.

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
Read `references/asset-observation-gate.md` before creating an identity passport, feature ledger, or prompt package from user-supplied product material.
Read `references/default-visual-baseline.md` before drafting a prompt package; record any baseline override in the job manifest.
Read `references/director-grade-prompt-package.md` before writing a selected test package, a paid-ready package, or story-led UGC with actors, dialogue, transitions, or cross-location continuity.
Read `references/continuous-improvement.md` after a tested package or when converting user feedback into a reusable skill improvement.
Read `references/closed-loop-prompt-optimization.md` when a user asks for self-optimization, candidate comparison, automatic rejection, iterative prompt refinement, or a controlled regeneration batch.
Read `references/asset-change-gate.md` whenever reusing a material folder or an earlier product brief.
Read `references/product-reference-pack.md` when creating a real-product asset layer for generated story scenes.
Read `references/generative-action-risk-gate.md` before assigning installation, loading, assembly, insertion, fastening, twisting, or payment handling to a generated clip.
Read `references/pre-submission-prompt-optimization.md` before presenting a prompt set as submission-ready or asking for paid JiMeng approval.
Read `references/generated-asset-catalog.md` when cataloging generated clips, final videos, handoff frames, or reusable approved media.

## Prompt rules

- Use concise English unless the JiMeng interface or user requires Chinese.
- State vertical 9:16, exact duration, product identity locks, camera direction, ending composition, and safe text area when applicable.
- Lock color, shape, logo/text, included parts, scale, and setting. End each clip with a stable composition suitable for the next cut.
- State: "Use the supplied reference as the exact product; do not redesign, substitute, simplify, recolor, relabel, or add/remove any product part." Repeat the passport's distinguishing traits in every prompt.
- For every required detail-evidence shot, state the exact visible traits; product frame coverage (minimum 60%, 70% for fine detail); macro/close focus; stable sharp focus; and that hands/props must not obscure the named detail. Do not use vague wording such as "show product details."
- Make the three linked clips advance one complete story: clip 1 establishes a concrete everyday situation or tension and introduces the product; clip 2 changes the situation through a decisive interaction and contains only a short detail-proof insert; clip 3 shows a visible result or payoff before the hero ending. Do not fill a 30-second story with repeated squeezing, a static product hold, or slow motion unless those are explicitly requested.
- For a verified interaction, describe the exact evidence asset, starting state, one primary visible action, and required ending state. Do not compress multiple fine hand actions into a single generated clip. When a later clip depends on the action, generate and accept the earlier clip's handoff frame before proceeding.
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

1. When reference research was requested or permitted: a compact reference-research brief, with sources/links, observed patterns, useful keywords, and a clear statement that it does not verify the user's product facts.
2. A one-line production choice: `3 × 10s` or `6 × 5s`, with reason.
3. A time-coded storyboard.
4. By default: a mode-balanced matrix of **20 complete 30-second creative packages**, with mode, route, full arc or proof progression, visible proof, difference, asset requirement, and its three linked prompts (**60 prompts total** for a 3 × 10-second plan). Generate fewer only when the user explicitly requests it.
5. One complete JiMeng prompt per generated clip, including the required prior-clip handoff.
6. A prompt-quality audit showing pass/fix status and the final improved prompts; do not submit the draft prompts.
7. A detail-evidence index: for every package, timecode, named product traits, required frame coverage, and proof action.
8. One final pre-submission package containing all 20 optimized creative packages / 60 prompts, plus an explicit approval request for the package IDs to submit; do not interrupt earlier with route-choice or draft-review questions.
9. A continuity and acceptance checklist.
10. An assembly command after the user names the approved video files.
11. A render manifest for final assembly: source-clip IDs, approved trim points, output format, text/CTA variables, safe areas, audio, and deterministic-overlay requirements. Mark it `FFmpeg` unless the user requests reusable designed graphics, captions, or batch templates; mark it `HyperFrames` only when that layer is needed and available.

## Action-and-state reference gate

Use this gate for every product category. The required behavior can be mechanical, electronic, cosmetic, food-related, cleaning-related, wearable, or any other real-world operation.

| Required behavior | Best source evidence | Clip start state | One permitted action | Clip end state |
| --- | --- | --- | --- | --- |

Reject and regenerate a clip when it changes the evidence-backed mechanism, loses true product scale, produces malformed hands or components, combines unrelated actions, or ends in a state that cannot lead into the next required behavior. Preserve the approved script and regenerate only the failed clip.

## Deterministic finishing layer

Use this layer after—not during—generative video production. Its purpose is repeatability across many final videos: the same approved clips and manifest must produce the same timing, captions, layout, and output.

- Keep the generative source plan and render manifest separate. Changing a caption or CTA must not re-submit a JiMeng task.
- Treat all copy as variables: product name, verified benefit, CTA, locale, caption text, voiceover, and music. Do not hard-code a claim that has not passed the product brief and restriction checks.
- For social vertical video, reserve a title/caption safe area away from platform UI and keep required product proof unobscured.
- Reuse a small set of named, versioned composition templates rather than redesigning captions, end cards, and transitions for every product.
- When HyperFrames is available, use its deterministic HTML/CSS/media composition workflow for designed caption rails, product callouts, end cards, or batch templates; lint, preview, and render the composition. Do not install it or any new runtime without the user's approval.
- Use Activepieces only as an optional local orchestration layer for job queues, human approvals, non-paid retries, and render-manifest tracking. Never let an automation bypass the final paid JiMeng submission approval or inject credentials into a shared skill.
- If HyperFrames is unavailable or the job only needs a clean cut, use FFmpeg assembly. The production decision is about finishing needs, not about the visual model used for source clips.
- Record the accepted source filenames, checks, template version, copy variables, and final output path in the render manifest so a later variation is traceable and reproducible.

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
