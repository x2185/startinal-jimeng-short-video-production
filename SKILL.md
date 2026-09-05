---
name: startinal-jimeng-short-video-production
description: Plan, prompt, validate, and assemble JiMeng-generated TikTok Shop product videos. Use when a user needs stable 3×10-second or 6×5-second clips, or a 25-second high-density continuous story through the Dreamina CLI; also use for story-led variants, continuity-safe prompts, shot acceptance, or FFmpeg assembly.
---

# JiMeng short-video production

Create a production plan; do not submit paid JiMeng generation tasks unless the user explicitly asks.

## Decision authority and shared boundaries

The current user's script, prompt, target duration, story, style, must-show beats, and ending have the highest creative priority. The Skill may make the smallest necessary correction only for the selected model's actual capability, supplied-material evidence, privacy/data protection, paid-submission approval, or a concrete continuity failure. Historical examples, remembered preferences, default durations, legacy API conventions, and route libraries must not silently replace the current brief.

The root Skill is the shared router and quality layer. It keeps legacy API and Dreamina CLI routes available, applies the same approval and product-identity discipline to both, and uses `director-grade` only as a quality label—not as a fixed story template. GPT-assisted images are optional scene aids, never product/action authority.

## High-density continuous story via Dreamina CLI

For a fast, causal story, default the **finished video** to 25 seconds unless the user specifies otherwise. Check the selected Dreamina model's live CLI limits first: make one continuous 25-second candidate only when it supports that duration and the action risk is acceptable; otherwise generate causally linked clips that sum to 25 seconds. Keep a 1–3-second microbeat map, role-labelled same-SKU references, motivated joins, and a stable handoff frame for every continuation. Historical examples teach pacing only; they never become product evidence or a default plot.

Read `references/high-density-continuous-story.md` for the beat map, route choice, continuity and acceptance rules. For the novelty-cardholder UGC pattern, additionally read `references/fast-ugc-payment-proof-structure.md`. Read live `dreamina multimodal2video -h` before every CLI submission, then state references, model, duration, resolution, ratio, output count, and credit impact before requesting paid approval.

## Retained legacy API route

Keep the API-first route for an explicitly selected legacy workflow or low-risk independent scene blocks; read `references/api-first-batch-production.md` before using it. Follow a user-selected route, model, duration, and structure unless genuinely unsupported. When no route is locked, ask whether to use Dreamina CLI for multi-reference/high-density continuity or legacy API for short independent blocks.

Treat a current user script, prompt, shot list, dialogue, or visual direction as the highest-weight creative source. Preserve its premise, order, relationships, pacing, must-show beats, ending, and level of operational detail; make and label only the smallest correction required by evidence or model capability. Without a selected script, create genuinely different causal premises—not adjective swaps—for requested high-density variants.

For a new team checkout, read `references/team-setup.md`; for local FFmpeg setup, read `references/environment-setup.md`. Do not install software, accept terms, or expose credentials without explicit approval.

## Persistent creative memory

At the start of a new task, if the local creative-memory ledger exists, read only confirmed user-global preferences, applicable confirmed benchmarks, and accepted observations relevant to the selected route. Current user instructions and current product evidence always override memory. Never load prior product identity, claimed function, characters, setting, or story as a default.

After explicit user feedback, an approved quality benchmark, or a reviewed render, record only the narrow supported learning with evidence and scope. Keep a one-off failure/job result local until it repeats across products or the user explicitly promotes it. Never store credentials, payment/customer data, raw identifying media details, unverified claims, or historical generated output as product evidence.

Read `references/creative-memory-system.md` when initializing, using, or updating persistent production memory. Use `scripts/creative_memory.py` for local ledger operations; it is non-generative and never calls JiMeng.
Read `references/director-grade-benchmark-checklist.md` before calling any package `director-grade`, presenting it as a generation candidate, or approving a director-grade batch.

## Optional GPT-assisted scene assets

When a concrete scene-continuity problem could benefit from GPT-assisted images, proactively explain the specific asset role and ask whether the user wants it generated. Do not generate it on silence or merely because a video is being planned. Only after the user explicitly approves generation, use the `imagegen` skill to create or edit **scene assets**: character/wardrobe continuity boards, setting/layout plates, first-frame composition studies, or transition/foreground-occlusion studies. After generation, preview the candidate, state its intended JiMeng role, and ask whether the user accepts it, wants a targeted revision, or wants it discarded. Do not put a GPT scene asset into a JiMeng reference pack until the user accepts that exact candidate.

Keep original product images and verified action frames as the identity/action authority. A GPT-generated image may guide background, character, lighting, camera composition, or a product placement target, but it cannot prove product structure, an unseen mechanism, payment capability, a claimed result, or a true tail frame. Label it `gpt-scene-reference`, state its role in the JiMeng submission, and attach it only alongside the fixed same-SKU product reference pack. Use an approved extracted tail frame—not a GPT prediction—for every linked-clip continuation.

Read `references/gpt-assisted-scene-assets.md` before creating, selecting, or uploading a GPT-assisted image. Record reviewed outcomes as `gpt-scene` observations in the local creative-memory ledger; never promote one asset's look or a current product's facts as a cross-product default.

## First interaction

Greet the user briefly, explain that this skill turns supplied product material into a reviewed, approval-gated production package. Inspect existing conversation/files first, then collect only missing product identity, play/use, verified features, buyer/market, restrictions, and extra creative requirements. Unless already explicitly supplied, always ask a separate question for: verified selling points and the core functions/features that must be shown and preserved. Do not infer these from video alone. If the user asks for variants without supplying a selected script, generate the default 20-package matrix. If the user supplies a detailed script, make that script the base package and create only the requested number of variants. For an explicitly requested high-density route, create one paid-ready 25-second **finished-video** validation package first, selecting its source route only after the model is chosen; expand it only after it passes review.

Read `references/first-run-intake.md` for the opening wording and intake routing.

## Workflow

1. Scan supplied material and build the identity passport, visible-configuration ledger, and role-labelled reference candidates. Select only evidence that visibly proves the target SKU; do not infer hidden mechanisms or claims. Read `references/asset-observation-gate.md` and `references/asset-change-gate.md` when applicable.
2. If research is enabled, extract lawful market patterns only; it never verifies product facts or authorizes copying another seller's media or creative treatment. Build the brief from verified facts, restrictions, audience, and current user direction.
3. Choose the model-supported source route. For high-density 25-second work, follow the continuous-story route above; for standard work, choose the requested finished duration and source clips that preserve a coherent arc. Use `3 × 10s` for simple stable stories and shorter linked clips when an action needs isolation or a longer candidate drifts.
4. Map every must-show interaction to identity, start, one action, and end evidence. A packshot proves appearance, not an unseen mechanism. For fragile actions, use role-labelled multi-reference CLI generation, one action per clip, and an approved tail-frame handoff; otherwise revise or omit the action. The final video remains fully generated. Read `references/generative-action-risk-gate.md`, `references/action-and-prompt-mapping.md`, and `references/multi-reference-action-submission.md` as needed.
5. For requested variants, use the current user script as the base package; without one, produce the requested number of structurally distinct creative routes. Call an item `director-grade` only after it independently passes `references/director-grade-benchmark-checklist.md`; otherwise label it `creative-outline`.
6. Build the submission package: identity passport, reference roles, visible detail proof, continuity/tail-frame plan, prompt, targeted negatives, acceptance checks, and a concise change log. Run `references/pre-submission-prompt-optimization.md` and `references/prompt-quality-gate.md` before presenting it.
7. Request one explicit approval immediately before each paid submission, stating package IDs and the exact model, references, duration, resolution, ratio, output count, and known credit impact. Never submit drafts, changed scope, or silence.
8. Generate a small validation candidate when identity, action, or reference arrangement is untested. Reject defects rather than masking them; regenerate only the failed clip after approval. Use the accepted handoff frame with the fixed product reference for a continuation.
9. Assemble only approved generated clips, then inspect the final render. Use FFmpeg for clean assembly and HyperFrames only when designed overlays, reusable motion graphics, or batch layouts are requested. Keep a render manifest and job-local retrospective; do not promote one-off results into shared memory.

## Intake gate

Treat these as blocking inputs:

- **Product identity:** product name plus at least one reference image/video or a precise visual description of color, shape, packaging, logo/text, and included parts.
- **Verified facts:** usable selling points, specifications, and claims that may appear in the video.
- **Restrictions:** prohibited claims, unsafe use, prohibited visuals, and brand/legal limits.
- **Audience and market:** intended buyer plus language/market when the final captions or spoken lines depend on them.

Ask for the missing items in one compact message. For example: “I have the product images, but need the verified selling points, prohibited claims, and target buyer before I can create a safe production plan.”

Treat selling points and must-show core functions as a separate blocking question unless the user already stated them explicitly. A video can demonstrate a possible action, but it does not establish which feature should be marketed, whether it is real, or whether it must be retained.

Treat an identity passport as blocking: verify at least the product's category, silhouette, dominant color, material/surface, distinctive details, and included parts from the supplied material. When packaging, logo, or readable text is material to the product identity, lock it too. Do not plan a scenario that would hide the only available identity evidence.

Treat these as non-blocking inputs and state the default before using it: target duration (default 30 seconds for standard variant packages; 25 seconds for an explicitly requested high-density causal-story route), format (default vertical 9:16), scene preference (default everyday home setting), creative route (default create a 5×4 matrix), CTA (default product-link prompt), and music/caption preference.

If the user cannot provide a blocking fact, omit it from the video rather than guessing. Ask for a reference asset again when product identity cannot be locked.

Read `references/intake-checklist.md` when checking whether provided product materials are sufficient.
Read `references/asset-observation-gate.md` before creating an identity passport, feature ledger, or prompt package from user-supplied product material.
Read `references/default-visual-baseline.md` before drafting a prompt package; record any baseline override in the job manifest.
Read `references/director-grade-prompt-package.md` before writing a selected test package, a paid-ready package, or story-led UGC with actors, dialogue, transitions, or cross-location continuity.
Read `references/continuous-improvement.md` after a tested package or when converting user feedback into a reusable skill improvement.
Read `references/closed-loop-prompt-optimization.md` when a user asks for self-optimization, candidate comparison, automatic rejection, iterative prompt refinement, or a controlled regeneration batch.
Read `references/asset-change-gate.md` whenever reusing a material folder or an earlier product brief.
Read `references/product-reference-pack.md` when creating a real-product asset layer for generated story scenes.
Read `references/gpt-assisted-scene-assets.md` when the user asks to generate/modify an auxiliary scene, character, wardrobe, setting, first-frame, or transition image with GPT for a JiMeng package.
Read `references/generative-action-risk-gate.md` before assigning installation, loading, assembly, insertion, fastening, twisting, or payment handling to a generated clip.
Read `references/multi-reference-action-submission.md` before submitting a rotation, opening, card insertion, assembly, or another state-changing action through JiMeng All-reference.
Read `references/pre-submission-prompt-optimization.md` before presenting a prompt set as submission-ready or asking for paid JiMeng approval.
Read `references/generated-asset-catalog.md` when cataloging generated clips, final videos, handoff frames, or reusable approved media.

## Prompt rules

- Use concise English unless the JiMeng interface or user requires Chinese.
- State vertical 9:16, exact duration, product identity locks, camera direction, ending composition, and safe text area when applicable.
- For a 25-second continuous story, use a 1–3-second microbeat table in the director package. Every row states the character goal, one safe action/reaction, camera movement, transition mechanism, product position, and resulting state. Keep the overall story to setup → pressure/decision → action → turn → payoff; do not create a montage of unrelated product poses.
- Put only one high-risk physical interaction in a microbeat. Rewrite an unsupported fine operation as a safe movement, reaction, or product reveal that preserves the beat's dramatic function; keep the finished video fully generated. Do not ask the generative model to render exact on-screen text, captions, or frame-perfect edit timing.
- Lock color, shape, logo/text, included parts, scale, and setting. End each clip with a stable composition suitable for the next cut.
- State: "Use the supplied reference as the exact product; do not redesign, substitute, simplify, recolor, relabel, or add/remove any product part." Repeat the passport's distinguishing traits in every prompt.
- For every required detail-evidence shot, state the exact visible traits; product frame coverage (minimum 60%, 70% for fine detail); macro/close focus; stable sharp focus; and that hands/props must not obscure the named detail. Do not use vague wording such as "show product details."
- For a standard three-linked-clip route, make the clips advance one complete story: clip 1 establishes a concrete everyday situation or tension and introduces the product; clip 2 changes the situation through a decisive interaction and contains only a short detail-proof insert; clip 3 shows a visible result or payoff before the hero ending. For a continuous story, use its microbeat map instead. Do not fill a story with repeated squeezing, a static product hold, or slow motion unless explicitly requested.
- For a verified interaction, describe the exact evidence asset, starting state, one primary visible action, and required ending state. Do not compress multiple fine hand actions into a single generated clip. When a later clip depends on the action, generate and accept the earlier clip's handoff frame before proceeding.
- Exclude warped geometry, unreadable labels, duplicate products, extra fingers, unrelated brands, changed product/colorway/packaging, unsupported claims, and unsafe use.
- Do not request copyrighted characters, deceptive packaging, or real-person endorsements.

## Story-variant framework

Use this framework when the user asks for variants or when no detailed user script selects a single route. Do not override a supplied script with this library.

1. Select five or more distinct creative routes across the modes in `references/story-variant-framework.md`, grounded in the current product's visible proof, target buyer, restrictions, and available settings. A route must state its mode, product interaction, visual proof, and end state; a story route additionally states actor/context and tension or goal.
2. When variants are requested without a stated count, create **20 complete 30-second variants** with a balanced mode mix. When the user states a count, produce that count. A variant must change at least two structural dimensions appropriate to its mode: opening event, actor goal, setting, product action, proof order, character relationship, outcome, camera perspective, hook, or CTA placement. Do not count adjective swaps as variation.
3. Treat every variant as one **30-second creative package**, split only because of JiMeng duration limits. A 3 × 10-second plan therefore produces **20 × 3 = 60 linked JiMeng prompts**. Story packages use setup → change/proof → outcome; showcase and demonstration packages use hook/reveal → clear proof → hero/payoff. Do not present the three clips as unrelated mini-videos.
4. Put an explicit handoff in every prompt: clip 1 states its final actor/product/camera state; clip 2 begins from that state and states its own ending; clip 3 begins from clip 2's ending. Instruct the operator to add the accepted prior clip's final frame as a reference to the next generation when supported.
5. Preserve claims and product identity across variants. Use adults by default; do not direct purchase persuasion at minors. Treat subjective comfort or enjoyment as subjective, not medical/therapeutic proof.
6. Rank routes by asset fit and label assumptions, but do not ask the user to choose a route during generation. Ask for approval only after the selected route or requested variant set has been generated, audited, and optimized.

Read `references/story-variant-framework.md` before creating story-led variants.

## Required output

Return:

1. When reference research was requested or permitted: a compact reference-research brief, with sources/links, observed patterns, useful keywords, and a clear statement that it does not verify the user's product facts.
2. A one-line production choice: target duration, selected model, and source route—for example `25s finished video: seedance2.5 one continuous clip` or `25s finished video: five linked 5s clips`—with reason.
3. A time-coded storyboard.
4. For a requested standard variant set: a mode-balanced matrix using the user-requested count (20 when unspecified), with mode, route, full arc or proof progression, visible proof, difference, asset requirement, and its linked prompts. For a supplied script: its base package plus only the requested variants. For the explicitly requested high-density route: one 25-second finished-video validation package with its microbeat table, reference roles, selected-model rationale, and acceptance gate.
5. One complete JiMeng prompt per generated clip, including the required prior-clip handoff. When the selected model supports and the operator chooses a continuous-story route, use one complete time-coded CLI prompt and a stable final-frame requirement instead.
6. A prompt-quality audit showing pass/fix status and the final improved prompts; do not submit the draft prompts.
7. A detail-evidence index: for every package, timecode, named product traits, required frame coverage, and proof action.
8. One final pre-submission package containing the route-selected optimized package(s) and an explicit approval request for their IDs; do not interrupt earlier with route-choice or draft-review questions.
9. A continuity and acceptance checklist.
10. An assembly command after the user names the approved video files.
11. A render manifest for final assembly: source-clip IDs, approved trim points, output format, text/CTA variables, safe areas, audio, and deterministic-overlay requirements. Mark it `FFmpeg` unless the user requests reusable designed graphics, captions, or batch templates; mark it `HyperFrames` only when that layer is needed and available.

## Deterministic finishing layer

Keep generation and finishing separate: captions, CTA, timing, audio, safe areas, transitions, and output settings belong in a render manifest, so changing them never resubmits JiMeng. Use FFmpeg for clean assembly; use HyperFrames only for designed overlays, reusable motion graphics, or batch layouts; Activepieces remains optional orchestration and must not bypass paid approval. Record accepted source files, checks, template version, copy variables, and output path for reproducibility.

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
