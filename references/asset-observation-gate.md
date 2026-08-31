# Asset observation gate

Use this gate before treating a product property or action as prompt-ready.

## Evidence pass

1. Classify every useful source file/frame before selecting evidence. A contact sheet is only a navigation aid, never final evidence. Use `product-asset-classification.md` and mark an asset `ambiguous` or `do_not_use` when it cannot support a reliable prompt decision.
2. Review the strongest identity still at full resolution and at least three frames around every required action.
3. Create an evidence ledger for visible configuration: category; silhouette; material/finish; dominant colors; frame/attachment/color pairings; included parts; readable marks; scale; packaging; start state; action; and ending state.
4. For multi-variant or multi-part products, record an explicit configuration map. Examples: frame color → attached part color; cap → bottle; left/right piece; cartridge → device. The map is a hard continuity lock.
5. Mark each field as **visible**, **seller-confirmed**, **ambiguous**, or **unknown**. Only visible or seller-confirmed facts may become prompt requirements or marketing claims.
6. Reconcile conflicts across clips by prioritizing the clearest close-up and seller confirmation. If the conflict cannot be resolved, omit the disputed detail and ask the user; never average or invent a hybrid product.

## Prompt gate

Every prompt must use the ledger rather than a vague product description. Require configuration pairings when they matter, and explicitly prohibit swaps, missing parts, extra parts, recolors, relabeling, or redesigned geometry. Do not use a generic beauty image to authorize an unseen mechanism or handling action.

If an action cannot be tied to a specific start state and end state in the supplied material, either request a dedicated action asset or omit the action from the generated video.

## Required analysis output before prompts

Return the material analysis before any prompt package:

| Evidence role | Selected source | What it visibly proves | Prompt decision |
| --- | --- | --- | --- |
| Identity | File/frame | Exact product traits that must match | Include as identity lock |
| Detail | File/frame | A visible feature or marking | Include as close-up proof, or omit |
| Action start | File/frame | The allowed starting configuration | Use as the only permitted start state |
| Action end | File/frame | The required final configuration | Use as the required end state |

For each requested feature, choose exactly one result: **supported and promptable**, **needs an additional asset**, or **omit from this video**. Never draft a generic prompt first and retrofit the evidence afterward.
