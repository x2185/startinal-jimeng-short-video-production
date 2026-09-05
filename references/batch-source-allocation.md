# Batch source allocation

Use this when producing more than one final video from one product's material folder. The goal is to create genuinely different fully generated deliverables, not to hide a shortage of scenes by repeating clips or inserting supplied source footage.

## Plan before generation

For every planned final, record a source allocation row:

| Final ID | Creative route | Required factual proof | Reference-evidence roles | New generated scene blocks | Repeat status |
| --- | --- | --- | --- | --- | --- |

Source photos or original action footage may supply identity, start, contact/detail, and end-state references. They are never inserted into the final. For fragile actions, allocate one scoped multi-reference generated clip with an explicit fallback: strengthen references, split the action, choose a supported model, regenerate, or revise the story.

## No-default-reuse rule

- A supplied source segment is reference evidence, not a default middle section for every final and not an automatic response to a model limitation.
- Within one batch, do not loop, replay, or use any generated clip as B-roll in another final by default.
- If several finals need the same product action, give each a distinct plot role, camera treatment, or evidence-backed generated attempt. If the action is not stable enough, create remaining variants around supported product proof and reactions; do not substitute source footage.
- Never use a source asset or generated clip merely to fill runtime. A final that is short of time needs a new approved generated scene block, a different detail beat, or a shorter approved duration—not a loop.

## Batch mix

Default to a varied mix appropriate to the brief: product-display variants, story/lifestyle variants, gift/reaction variants, and a limited number of reference-backed action variants. The batch plan must state each final's reference roles and generated action response. A user may explicitly request a repeated generated shot, but the render manifest must mark it `user_requested_repeat`.

## Final assembly check

Before delivery, compare all render manifests in the batch. Reject a planned final if it contains a source-footage insert, repeats a generated clip from another final without `user_requested_repeat`, repeats a generated clip within its own timeline, or uses a loop solely to reach the requested duration. Record generated clip IDs, reference-evidence roles, trim ranges, and source type in each final manifest.
