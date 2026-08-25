# Prompt-quality gate

Run this gate after drafting every prompt set and before JiMeng submission. Revise the prompts; do not merely list defects.

## Pass/fix checks

| Check | Pass condition | Fix when failed |
| --- | --- | --- |
| Product lock | The product identity passport matches supplied material; the exact reference, all distinguishing visible traits, and prohibited alterations are stated in every linked prompt. | Add the missing locks. Block submission if the source does not establish identity or a prompt permits a substitute. |
| Detail evidence | Each 30-second package includes an uninterrupted >=2-second macro/close proof shot; product fills >=60% of frame (>=70% for fine detail); named traits are sharp, lit, and not obscured. The proof is a short story beat, not a long slow-motion hold. | Add a dedicated short detail-evidence beat and explicit focus, coverage, no-occlusion, action, and recovery constraints. |
| Feature fidelity | Every user-confirmed, requested core function or play/use mechanism remains represented in the story and prompts. | Restore it. If it conflicts with a rule or is ambiguous, flag it and ask; never silently delete it. |
| Fact safety | Every spoken/visual claim is supplied or visually demonstrable. | Remove or soften unverified claims. |
| Story logic | Each 30-second package has a specific setup/tension, a change caused by product interaction, and a visible outcome. Detail proof supports that change rather than replacing the plot. | Rewrite clips so each contributes to one story; reject repeated squeezes/static holds as a complete 30-second narrative. |
| Handoff | Clip 2 inherits clip 1's final state; clip 3 inherits clip 2's final state. | State inherited pose, product position, setting, lighting, framing, and next action explicitly. |
| Generatability | One clear subject, action, setting, camera behavior, and stable ending fit the exact duration. | Remove competing actions, vague language, or impossible timing. |
| Visual safety | Negative constraints cover likely defects: changed product/colorway/logo/packaging/part, duplicate product, warped geometry, extra fingers, unrelated brands, and unreadable text. | Add targeted negatives. |
| Marketplace safety | No deceptive packaging, price/stock invention, fake endorsement, medical/therapeutic claim, unsafe use, or direct purchase persuasion at minors. | Remove or rewrite the risky language. |

## Required audit output

For each 30-second package, return:

1. `Draft audit:` concise pass/fix findings for clips 1–3.
2. `Feature-preservation ledger:` list every requested core function as `retained`, `reworded`, or `blocked`, with its prompt location and reason.
3. `Changes made:` only material edits.
4. `Submission-ready prompts:` the revised linked prompts, clearly marked as the only version to submit.
5. `Detail-evidence index:` timecode, traits shown, frame coverage, and proof action for every package.

If a critical fact, product reference, or handoff state is absent, mark the package **blocked** and ask for it instead of inventing it.

## Identity consistency rule

Do not treat "similar strawberry", "generic version", or a redesigned package as sufficient. The generated product must match the supplied material's identity passport. A generative model cannot make a literal guarantee; therefore bind every request to the strongest available reference and passport, and label any result that visibly conflicts with either as `identity-mismatch` in the run manifest. Preserve the downloaded file for traceability, but never report it as a passing result or use it as a continuation reference.

## Sensitive or ambiguous functions

Do not remove a confirmed feature merely because it involves payments, cards, finance, health, safety, age limits, or another regulated area. Preserve the visible, confirmed function using neutral factual wording, then flag the exact compliance question for the user to decide. For example, if a product accepts a card, show the card-insertion interaction only when confirmed; do not invent payment processing, security, approval, account, price, or financial-result claims. If it is unclear whether the interaction is real payment or pretend play, ask before generating.
