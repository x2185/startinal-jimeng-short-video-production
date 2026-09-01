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
| High-risk action | `real_footage` or `all_reference` | Use the mapped reliable layer |

Return the audit and optimized base script before presenting paid-ready prompts. Preserve the user's intended tone and hook when evidence permits; make changes explicit.

## Produce meaningful variants

Create 20 complete 30-second variants unless the user requests fewer. One is the optimized base route. Each of the other 19 must change at least two structural dimensions while preserving the validated product facts and required proof. Use dimensions such as hook event, buyer problem, setting, actor goal, proof order, supported action, camera viewpoint, emotional payoff, caption angle, or CTA timing.

Treat the supplied script as the **creative anchor**, not as a rigid output template. Keep its strongest premise, hook, tone, and narrative logic in the base route. Then deliberately expand it across the suitable modes in `story-variant-framework.md`—for example situation story, visual showcase, interaction/reaction, hook/reveal, and gift/lifestyle. Reinterpret the same validated product truth through those modes; do not produce 20 near-copies of the original script or force every variant into the same three-beat plot.

Do not create variants by swapping adjectives, making unsupported claims, or inventing different mechanisms. A variant may use only action and result states that exist in the evidence ledger. If the base script contains an unsupported beat, remove it from every derived variant.

## Variant output

For each variant provide: ID; relation to the base script; hook; 30-second story/proof arc; mapped product evidence; any required extra asset; risk decision (`generate`, `all_reference`, `real_footage`, or `omit`); and its linked clip prompts. Rank by evidence fit before creative novelty.
