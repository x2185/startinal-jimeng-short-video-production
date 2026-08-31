# Product proof acceptance

Use this gate after every generated candidate and again after final assembly. It keeps product proof stronger than visual polish.

## Evidence priority

Use sources in this order: verified real action video; consecutive action frames; multiple sharp, state-specific stills; multiple identity/detail stills; one packshot. A lower-priority source may not authorize a higher-risk action. Separate SKUs, colours, sizes, and included-part sets into different identity passports and never mix their evidence in one prompt or clip.

## Critical-frame checklist

Inspect the start, action, and end portion of every clip. Pass only when all applicable checks hold:

- Product silhouette, proportions, colour, finish, text, and included parts match the identity assets.
- The clip begins in the mapped start state and ends in the mapped end state.
- Only the mapped action occurs; no invented mechanism, extra product, extra finger, duplicated part, or altered slot/hinge appears.
- Key structure remains visible, in focus, and at the required scale; hands or props do not hide the proof.
- The ending is stable enough to hand off or cut.

Any failure rejects the clip. Do not hide it with captions, cropping, a sticker, a transition, or a cut that implies an unsupported result.

## Final-edit protection

Before delivery, check that captions, CTA, price card, graphics, product-link rail, transitions, and crop boundaries do not cover the required detail or action proof. Keep the approved product evidence visible for its planned duration; if it cannot remain visible, change the edit rather than accept a weaker proof.

## Failure record

For every rejected candidate, record: job and beat ID; source asset names; prompt version; failure category (`identity`, `geometry`, `action`, `hands`, `text`, `continuity`, or `occlusion`); the visible failure; and the next decision (`regenerate`, `ask_for_asset`, `use_real_footage`, or `omit`). Reuse this record to avoid repeating the same failed action class, but do not treat generated output as evidence of the real product.
