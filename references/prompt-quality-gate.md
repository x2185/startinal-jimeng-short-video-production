# Prompt-quality gate

Run this gate after drafting every prompt set and before JiMeng submission. Revise the prompts; do not merely list defects.

## Pass/fix checks

| Check | Pass condition | Fix when failed |
| --- | --- | --- |
| Product lock | Exact product reference, visible identity traits, and prohibited alterations are stated. | Add missing visual locks and negative constraints. |
| Fact safety | Every spoken/visual claim is supplied or visually demonstrable. | Remove or soften unverified claims. |
| Story logic | Each 30-second package has setup, continuation/proof, and outcome. | Rewrite clips so each contributes to one story. |
| Handoff | Clip 2 inherits clip 1's final state; clip 3 inherits clip 2's final state. | State inherited pose, product position, setting, lighting, framing, and next action explicitly. |
| Generatability | One clear subject, action, setting, camera behavior, and stable ending fit the exact duration. | Remove competing actions, vague language, or impossible timing. |
| Visual safety | Negative constraints cover likely defects: changed product, duplicate product, warped geometry, extra fingers, unrelated brands, and unreadable text. | Add targeted negatives. |
| Marketplace safety | No deceptive packaging, price/stock invention, fake endorsement, medical/therapeutic claim, unsafe use, or direct purchase persuasion at minors. | Remove or rewrite the risky language. |

## Required audit output

For each 30-second package, return:

1. `Draft audit:` concise pass/fix findings for clips 1–3.
2. `Changes made:` only material edits.
3. `Submission-ready prompts:` the revised linked prompts, clearly marked as the only version to submit.

If a critical fact, product reference, or handoff state is absent, mark the package **blocked** and ask for it instead of inventing it.
