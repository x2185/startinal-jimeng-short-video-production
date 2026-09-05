# Prompt-quality gate

Run this gate after drafting every prompt set and before JiMeng submission. Revise the prompts; do not merely list defects.

## Pass/fix checks

| Check | Pass condition | Fix when failed |
| --- | --- | --- |
| Product lock | The product identity passport matches supplied material; the exact reference, distinguishing visible traits, and prohibited alterations are stated in every selected prompt. | Add the missing locks. Block submission if the source does not establish identity or a prompt permits a substitute. |
| Detail evidence | Each selected-duration package includes an uninterrupted two-second macro/close proof shot; product fills at least 60% of frame (70% for fine detail); named traits are sharp, lit, and unobscured. | Add a dedicated short detail-evidence beat and explicit focus, coverage, no-occlusion, action, and recovery constraints. |
| Feature fidelity | Every user-confirmed, requested core function or play/use mechanism remains represented in the story and prompts. | Restore it. If it conflicts with a rule or is ambiguous, flag it and ask; never silently delete it. |
| Fact safety | Every spoken/visual claim is supplied or visually demonstrable. | Remove or soften unverified claims. |
| Story logic | Each selected-duration package has a specific setup/tension, a change caused by product interaction, and a visible outcome. | Rewrite beats so each contributes to one story; reject repeated static holds as a complete narrative. |
| Handoff | Linked clips inherit the prior final state; a continuous story has a causal transition between microbeats. | State inherited pose/product/setting for linked clips, or repair the affected continuous transition. |
| Performance and action direction | Each recurring person has a usable identity/wardrobe description; every key beat gives an observable reaction, action start/end, product hand/orientation, and a specific camera/focus instruction. | Replace generic mood adjectives and “show/use product” wording with visible performance, action choreography, and camera direction. |
| Generatability | One clear subject, action, setting, camera behavior, and stable ending fit the exact duration. | Remove competing actions, vague language, or impossible timing. |
| Visual safety | Negative constraints cover likely defects: changed product/colorway/logo/packaging/part, duplicate product, warped geometry, extra fingers, unrelated brands, and unreadable text. | Add targeted negatives. |
| Marketplace safety | No deceptive packaging, price/stock invention, fake endorsement, medical/therapeutic claim, unsafe use, or direct purchase persuasion at minors. | Remove or rewrite the risky language. |
| Batch parity | Every variant labelled `director-grade` independently includes tailored references, continuity/tail-frame plan, full prompt, targeted negatives, and acceptance gate. | Downgrade it to `creative-outline` or complete its missing artifacts; never let shared boilerplate stand in for package-specific direction. |
| Benchmark parity | When a current-task director-grade example exists, the candidate matches or exceeds its operational-detail level for character direction, action choreography, camera/transition detail, handoff plan, and acceptance depth. | Expand the missing category to the benchmark's level or label the candidate `creative-outline`; do not present it as director-grade. |

## Required audit output

For each selected package, return:

1. `Draft audit:` concise pass/fix findings for linked clips or continuous-story microbeats.
2. `Feature-preservation ledger:` list every requested core function as `retained`, `reworded`, or `blocked`, with its prompt location and reason.
3. `Changes made:` only material edits.
4. `Submission-ready prompts:` the revised prompts, clearly marked as the only version to submit.
5. `Detail-evidence index:` timecode, traits shown, frame coverage, and proof action for every package.

If a critical fact, product reference, or required state is absent, mark the package **blocked** and ask for it instead of inventing it.

## Identity consistency rule

Do not treat a similar or redesigned product as sufficient. The generated product must match the supplied material's identity passport. A generative model cannot make a literal guarantee; therefore bind every request to the strongest available reference and passport, and label any result that visibly conflicts with either as `identity-mismatch` in the run manifest. Preserve the downloaded file for traceability, but never report it as a passing result or use it as a continuation reference.

## Sensitive or ambiguous functions

Do not remove a confirmed feature merely because it involves payments, cards, finance, health, safety, age limits, or another regulated area. Preserve the visible, confirmed function using neutral factual wording, then flag the exact compliance question for the user to decide. For a cardholder, describe the user's own card as the payment instrument and the holder as its physical carrier; do not claim that the holder processes payment. If the interaction is unclear, ask before generating.
