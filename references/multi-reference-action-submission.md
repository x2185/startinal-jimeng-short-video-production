# Multi-reference action submission

Use this plan for any product clip where a single packshot would force the model to invent hidden geometry: rotating an object, opening a compartment, loading or inserting a card, assembly, fastening, connecting, or another state transition.

## Submit through JiMeng All-reference

Do not use `run_jimeng_a1_package.py` for these clips. Its `jimeng_i2v_first_v30` endpoint accepts one first-frame image only. In JiMeng's All-reference interface, upload every distinct evidence image that materially reduces ambiguity for this clip, up to the selected model's current live input limit. Three to five images are often enough, but they are not a cap:

1. **Identity** — a clean full view of the exact SKU, colour, finish, included parts, and visible text.
2. **Start state** — the product immediately before the one permitted action.
3. **Detail/mechanism** — a sharp close view of the slot, hinge, opening, alignment, or part that must remain true.
4. **End state** — the exact required result after the action.
5. **Additional geometry or continuity views, when useful** — reverse, side, close texture/detail, approved prior-clip handoff, or a second angle that resolves a real ambiguity.

Every image must have a stated role. Exclude near-duplicates, other SKUs/colourways, historical AI output, unrelated lifestyle inspiration, and any frame with readable personal, payment-card, account, price, or customer data. More references are useful only when their roles do not conflict.

For an action with several real state changes, make separate clips. Never ask one clip to rotate, open, insert a card, and close the product.

## Prompt pattern

Use the labels shown by the interface and state their roles explicitly. Example:

> Use @image-1 as the exact product identity. Begin exactly as @image-2. Preserve the slot and all visible parts exactly as @image-3. Perform one action only: rotate the product slowly until it matches @image-4. Do not add, remove, bend, recolour, simplify, duplicate, or invent any part; no extra fingers, no unreadable labels, no hidden mechanism.

Reject the output if it does not match both the start and end reference, or if the mechanism, silhouette, scale, labels, components, or hands deform. Use verified real footage instead when the model fails the same action class twice.
