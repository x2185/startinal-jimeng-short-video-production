# Closed-loop prompt optimization

Use this mode when the goal is to improve a generated product-video package through controlled candidate comparison. It is an evaluation-and-revision loop, not model training and not permission to make paid calls without approval.

## Before the first candidate

Freeze a compact evaluation contract for the package:

- product identity and visible configuration map;
- action start state, one permitted action, and required ending state for each clip;
- character, wardrobe, location, lighting, and handoff locks where applicable;
- safety and marketplace restrictions;
- candidate count and a user-approved paid-submission scope.

Use the strongest complete-product and action-specific references. A product family image cannot substitute for a missing mechanical-action image.

## Evaluate every candidate

Inspect the whole clip and several frames from its final stable second. Record the result in two layers.

### Hard reject

Reject the clip outright if it has any of these:

- product identity, colour pairing, scale, part count, or mechanism is wrong;
- a required action state is absent, physically impossible, or cannot hand off to the next clip;
- unsafe use or prohibited target appears;
- a face, hand, product, readable brand, price, or sensitive detail is materially defective;
- a static product independently lifts, floats, slides, rotates, opens, or changes pose without a mapped contact or action;
- its stable frame cannot serve as the planned continuation reference.

### Soft quality score

For clips without a hard failure, score each dimension as 0, 1, or 2: UGC realism, framing/readability, lighting/material fidelity, natural performance, and story clarity. Prefer the best total score only when the hard locks all pass; never trade a hard-lock failure for prettier lighting.

## Diagnose before revising

Change the smallest plausible causal layer, not the entire story.

| Observed failure | First correction to test |
| --- | --- |
| mixed colour pair, wrong product, duplicate part | use one clean colour-specific identity reference; remove competing colour descriptions; restate the pairing lock |
| unclear fine interaction | separate loading/reloading/releasing into different clips; add the exact start and end state; use an action-specific reference |
| warped hands or product | reduce motion and camera movement; keep the full interaction in frame; shorten the action beat |
| static product moves by itself | reject as `uncommanded_motion`; lock the object to the named supporting surface, permit camera-only motion, and regenerate only that clip |
| character, clothing, or room drift | use a reviewed prior handoff frame; repeat only inherited visual locks, not a new character description |
| unnatural generated speech or lip-sync | retain the actor reaction and replace spoken output with post-production voiceover/subtitles |
| disconnected or pointless story beat | rewrite that clip's immediate goal, action, and visible result; do not add generic adjectives or unrelated props |

Do not revise more than one causal layer in the same retry unless the original clip has multiple independent hard failures. Keep approved clips immutable and regenerate only the failed clip.

When the feedback is creative rather than technical—for example "too dependent on my material", "no surprise", or "the scene feels repetitive"—do not add more negative constraints. Preserve the product passport and restrictions, then replace the weak story premise, human goal, setting logic, visual hook, or payoff with a fresh creative route. Use the same feedback round to record what the user wants more or less of, so the next 20-variant set is intentionally shifted rather than randomly different.

## Stop and approval rules

- Prepare the next retry package automatically after diagnosis, but make no paid submission until the user approves its package IDs, candidate count, and any changed paid scope.
- Stop a loop when an approved candidate meets every hard lock and is the best available soft-score candidate, when the approved retry scope is exhausted, or when a required reference/action fact is missing.
- If the loop exposes an unsupported action, mark that beat blocked and request evidence instead of asking the model to invent the mechanism.

## Product-local optimization record

Store this in the job folder as `optimization-log.md`:

```markdown
# Optimization log — <package ID>

| round | clip | candidate | hard result | soft score / 10 | observation | likely cause | one correction | outcome |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | C03 | A | reject | — | figure paired to wrong colour frame | competing colour reference | isolate pink reference and remove other colours | pending |
```

At the end, write the concise retrospective required by `continuous-improvement.md`. Promote a lesson to the shared skill only after cross-product evidence or explicit user confirmation.
