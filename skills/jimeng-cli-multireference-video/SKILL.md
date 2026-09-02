---
name: jimeng-cli-multireference-video
description: Produce high-quality product videos through the official Dreamina (即梦) CLI when a task needs multiple image, video, or audio references. Do not use for low-cost single-reference batches.
---

# 即梦 CLI 多参考视频

Use this skill for a high-quality, small-batch product-video route through the official `dreamina` CLI. It is separate from the legacy single-first-frame API route: use it when the user requests CLI, full-reference quality, multiple product views, video/audio references, or a creative story that benefits from stronger continuity.

Do not use it for low-risk, low-cost bulk generation where the existing single-reference API route is sufficient.

## Inherit the established product workflow

This skill changes the **generation channel only**. Reuse the established workflow in `$startinal-jimeng-short-video-production` for every non-CLI decision: material scan and classification, SKU isolation, evidence ledger, product identity passport, content-mode selection, script audit, creative-first-frame planning, 20-variant planning, low-risk shot design, prompt-quality review, dense-frame visual QA, final assembly, job workspace, failure records, and continuous improvement.

If that base skill is installed, read the base workflow and its relevant references before planning a real job. Preserve its proven safeguards: prior AI success cases are learning-only, source media is not silently reused, unsupported fine actions are omitted or explicitly routed to named real footage, and only accepted clips enter a final MP4.

The base Skill normally owns the product brief, storyboard, QA record, and final assembly. This Skill supplies the selected CLI route, reference-pack design, authentication, submission record, async task handling, and downloaded source clips back into that same job workspace. Do not create a competing folder layout, duplicate brief, or separate failure history.

## Before any submission

Read and classify product material through the inherited base workflow first. Establish the target SKU, product identity passport, verified claims, forbidden substitutions, desired output, and the role of each source file. Historical AI outputs may inform shot language only; never upload or reuse them as source media for a new final unless the user explicitly asks.

Choose the smallest reference set that proves the product: clean identity images first; detail images only for traits that must remain visible; short motion footage only when it contributes a permitted low-risk motion. Do not supply another SKU, colorway, or product structure merely to borrow its movement.

Avoid fine or state-changing actions such as payment contact, card insertion, twisting, installation, assembly, or precise hand manipulation. Rewrite them as stable product, reaction, environment, or ordinary-cut beats unless the user explicitly requires a named real-footage insert.

## CLI readiness and authentication

Check `dreamina -h` and the relevant subcommand `dreamina <command> -h` before use. Treat this live help as authoritative for models, reference limits, duration, resolution, and ratio.

Reuse an existing local login. If login is needed, start the official OAuth Device Flow and give the user the verification link. Complete login only after the user confirms they authorized it. Never store, echo, or commit OAuth tokens, device codes, cookies, or account data.

Use `multimodal2video` as the default CLI route whenever more than one useful product, detail, motion, or audio reference exists. It accepts repeated local image, video, and audio inputs in one submission. Use `image2video` only when one image is deliberately sufficient. Use `frames2video` only for a genuinely supported first-and-last-frame route. Do not infer CLI capability from a web UI feature.

Before every real multi-reference submission, inspect current `multimodal2video -h`, record the live image/video/audio/total-input limits in the job record, and keep within them. Do not hardcode a past limit, assume every model supports the same reference count, or upload every available asset merely because the CLI permits it.

Read [references/cli-production-route.md](references/cli-production-route.md) before preparing a real submission.

## Submission gate

Generation uploads local reference material to Dreamina and may consume credits. Immediately before submission, state the exact reference files, command family, model, duration, resolution, ratio, number of outputs, and expected credit impact if available. Ask for explicit approval of that exact paid submission. Do not submit on silence, and do not silently change model, count, or reference set.

Run a small validation clip before a larger package whenever the product identity, story treatment, or reference arrangement is untested. Record the command arguments, reference roles, submit ID, local output directory, and result status in the job record. Never record credentials.

## Review and delivery

For each returned clip, retrieve the asynchronous result until it reaches `success` or `fail`; accepted submission is not completion. Download only completed media into the current job workspace. Inspect dense review frames for product identity, text/brand leakage, hand anatomy, unintended independent product motion, and unsupported behavior.

Reject a failed clip; do not conceal defects through editing. Keep accepted scene blocks independently editable, then assemble only approved clips into the requested final. Deliver the finished MP4 and its concise QA record, not merely raw fragments, unless the user asks for raw materials.
