# Multi-reference action submission

Use this plan for any product clip where a single packshot would force the model to invent hidden geometry: rotating an object, opening a compartment, loading or inserting a card, assembly, fastening, connecting, or another state transition.

## Submit through JiMeng All-reference

Do not use `run_jimeng_a1_package.py` for these clips. Its `jimeng_i2v_first_v30` endpoint accepts one first-frame image only. In JiMeng's All-reference interface, upload only the evidence needed for this clip, normally three to five images:

1. **Identity** — a clean full view of the exact SKU, colour, finish, included parts, and visible text.
2. **Start state** — the product immediately before the one permitted action.
3. **Detail/mechanism** — a sharp close view of the slot, hinge, opening, alignment, or part that must remain true.
4. **End state** — the exact required result after the action.
5. **Optional second angle** — only when it proves a feature hidden in the other images.

For an action with several real state changes, make separate clips. Never ask one clip to rotate, open, insert a card, and close the product.

## Prompt pattern

Use the labels shown by the interface and state their roles explicitly. Example:

> Use @image-1 as the exact product identity. Begin exactly as @image-2. Preserve the slot and all visible parts exactly as @image-3. Perform one action only: rotate the product slowly until it matches @image-4. Do not add, remove, bend, recolour, simplify, duplicate, or invent any part; no extra fingers, no unreadable labels, no hidden mechanism.

Reject the output if it does not match both the start and end reference, or if the mechanism, silhouette, scale, labels, components, or hands deform. Use verified real footage instead when the model fails the same action class twice.
