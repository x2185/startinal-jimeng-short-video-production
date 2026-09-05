# Script assist and 20-variant workflow

Use this workflow when the user supplies a script, outline, hook, spoken lines, a storyboard, or a prior creative and asks to improve it or generate variants.

## Audit before optimization

Treat the user script as a creative brief, not proof of the product. Split it into hook, claimed benefit, product action, visual proof, dialogue/captions, CTA, and ending. Compare every item to the product evidence ledger and classify it:

| Script element | Result | Handling |
| --- | --- | --- |
| Visible or seller-confirmed | `retain` | Keep or tighten for clarity |
| Supported but weakly shown | `revise` | Add a mapped proof beat/asset |
| Missing a required view | `ask_for_asset` | Ask one focused question before use |
| Unsupported claim or mechanism | `remove` | Omit; never rephrase as a fact |
| Fine or state-changing action | `revise` | On the CLI route, use role-labelled start/contact/end references for one scoped generated action; otherwise rewrite around stable product proof. Never insert source footage into the final. |

Return the audit and optimized base script before presenting paid-ready prompts. Preserve the user's intended tone and hook when evidence permits; make changes explicit.

## Produce meaningful variants

After the validation route passes, create 20 complete 30-second outlines unless the user requests fewer. One is the optimized base route. Each of the other 19 must change at least two structural dimensions while preserving the validated product facts and required proof. Use dimensions such as hook event, buyer problem, setting, actor goal, proof order, camera viewpoint, emotional payoff, caption angle, or CTA timing.

Treat the supplied script as the **creative anchor**, not as a rigid output template. Keep its strongest premise, hook, tone, and narrative logic in the base route. Then deliberately expand it across the suitable modes in `story-variant-framework.md`—for example situation story, visual showcase, interaction/reaction, hook/reveal, and gift/lifestyle. Reinterpret the same validated product truth through those modes; do not produce 20 near-copies of the original script or force every variant into the same three-beat plot.

Do not create variants by swapping adjectives, making unsupported claims, or inventing different mechanisms. Keep fine/state-changing actions out of every derived outline unless the selected CLI route has sufficient role-labelled evidence for one scoped generated action. If the base script contains an unsupported beat, remove or rewrite it in every variant.

## Variant output

For each variant provide: ID; relation to the base script; hook; six 5-second scene-block roles; mapped product evidence; any required extra asset; risk decision (`generate_low_risk`, `generate_multireference_action`, or `omit_or_rewrite`); and a one-line difference from the base. Write full clip prompts only for IDs selected for generation. Rank by evidence fit before creative novelty.
