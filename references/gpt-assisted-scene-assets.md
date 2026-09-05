# GPT-assisted scene assets

Use this optional route only after a two-stage user confirmation. Its purpose is to improve the visual plan before JiMeng generation—not to replace verified product evidence or hide a failed video result.

## Two-stage user approval

1. **Before generating:** when a concrete gap is found, explain it in one sentence—for example, “A character/wardrobe board could make the same father and son more consistent across garage, store, and kitchen”—and ask whether the user wants that exact scene asset generated. Do not call image generation on silence.
2. **After generating:** show the candidate, name its intended role and limitations, and ask whether the user accepts it, requests one targeted revision, or discards it. Mark the asset `candidate` until accepted. A candidate must not be uploaded to JiMeng or treated as a reusable reference until the user explicitly accepts it.

If the user declines, continue the normal original-reference route without treating the missing scene asset as a blocker.

## Good uses

| Asset role | Use it to solve | Must not establish |
| --- | --- | --- |
| Character continuity board | Face/wardrobe/age/presentation consistency across scenes. | A real person's identity or endorsement. |
| Setting/layout plate | Room geography, counter placement, lighting, background density. | Product facts, shop affiliation, or location truth. |
| First-frame composition study | Camera height, pose, product placement target, negative space. | Exact product geometry unless the original product reference also appears in the JiMeng pack. |
| Transition study | Object wipe, door edge, flowers/leaves, foreground occlusion, matching motion direction. | A real continuation tail frame. |

## Required process

1. State the concrete problem the image should solve. Do not make an image “for quality” without a role; ask the user for generation approval.
2. Use the `imagegen` skill's built-in image tool only after approval. If a local product image must be used as an input, inspect it first and label it as a **product identity reference**; label every other input as scene/style/composition support.
3. Generate a scene asset with an explicit role and constraints. Where product fidelity matters, either leave the product out of the GPT image or describe it as a placement target while separately retaining the original product pack for JiMeng.
4. Inspect the result before showing it. Reject it if it contains a conflicting product colourway, distorted hands, invented logos, readable personal/payment data, an inappropriate setting, or a conflicting character identity.
5. Show the viable candidate to the user and ask for accept / one targeted revision / discard. Save it under `<job-output>/gpt-scene-assets/candidates/` until accepted. Record prompt, input roles, inspection decision, and intended JiMeng role in the job manifest.
6. After explicit acceptance, move/copy the selected asset into `<job-output>/gpt-scene-assets/accepted/` without overwriting earlier versions. At JiMeng submission, attach only the smallest role-complete set within the selected model's live input limit: fixed product references first, then approved handoff frame when linked, then accepted GPT scene assets only when they resolve a real ambiguity.

## Prompt pattern

Use a structured image prompt, then preserve the output's exact role in the video prompt.

```text
Use case: photorealistic-natural
Asset type: GPT scene reference for a vertical JiMeng video
Primary request: <one scene/character/transition problem>
Input images: <each image and its role>
Scene/backdrop: <ordinary place, no real brand>
Subject: <adult character or foreground transition object>
Composition/framing: <9:16, lens height, product placement area if empty>
Lighting/mood: <natural motivated lighting>
Constraints: <must match wardrobe/scene facts; product stays absent or only a non-authoritative placement target>
Avoid: logos, readable payment data, text, product redesign, extra fingers, watermarks
```

## Never use it for

- replacing a missing product reverse/inside/action/end-state reference;
- generating a fake payment result, receipt, terminal data, review, testimonial, or proof of a product claim;
- replacing the approved extracted tail frame of a prior JiMeng clip;
- covering up a visibly wrong product/action in deterministic finishing;
- generating media without the user's request or approval for GPT-assisted assets.

## Memory rule

Store an accepted/rejected GPT scene experiment as a `job`-scoped `gpt-scene` observation with the image path, role, product/reference compatibility result, and outcome. Only promote the narrowest repeated lesson (for example, “a character board improved wardrobe continuity in three accepted jobs”), never the image itself, its people, product, or setting.
