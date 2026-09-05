# Product asset classification

Classify every supplied image, video, and extracted frame before it can be used in a prompt. Keep the original files unchanged; record roles in the job manifest or evidence ledger. One asset may have more than one role, but it must never be promoted beyond what it visibly proves.

| Category | What belongs here | May be used for |
| --- | --- | --- |
| `identity` | Clear complete product views, SKU/colour/finish, included parts | Product identity lock and hero reference |
| `detail` | Sharp close-up of a label, slot, hinge, texture, connector, or other feature | Detail-proof shot and multi-reference structure lock |
| `action_start` | Exact configuration immediately before one action | Clip start state |
| `action_process` | Frames/footage that visibly prove an intermediate movement or alignment | Action-specific reference evidence for fragile handling; never a final insert |
| `action_end` | Exact configuration immediately after the one action | Clip end state and acceptance check |
| `configuration_pairing` | Evidence that maps matching parts/variants, such as colour → attachment | Continuity lock |
| `packaging_or_text` | Packaging, readable claims, model number, logo, instructions | Text/packaging lock only after legal/claim review |
| `context` | Person, room, lifestyle, background, or prop without product proof | Scene direction only; never product identity or mechanism |
| `historical_ai_success` | A previously generated AI clip the user identifies as a successful example | Learn scene logic, framing, pacing, hook, and prompt pattern only; never current product evidence or direct final media |
| `ambiguous` | Occluded, blurred, conflicting, or incomplete view | Do not use until clarified |
| `do_not_use` | Personal/card data, unrelated SKU, external brand, unsafe/prohibited content | Exclude from prompts and upload set |

For every requested video beat, choose assets in this order: `identity` + the relevant `detail` + `action_start` + `action_end`. Add `action_process` only when it clearly proves the movement. If either state is missing, mark the feature `needs additional asset`; do not let a generic identity image fill the gap.

## Historical AI-success rule

Identify historical AI-generated success cases from the user's folder labels, task records, filenames, generation metadata, or the user's confirmation. If origin remains unclear, label the file `ambiguous` and ask one focused question rather than treating it as original source material.

Keep `historical_ai_success` separate from current-SKU identity/action evidence. Inspect it to extract a labelled learning record—scene type, hook, shot order, framing, pacing, visible product role, prompt provenance, and observed failure exclusions—then use that record to inspire a newly generated current-task variation. Never place its frames, video segments, or audio in a new final video. Never infer that its shown product shape, function, action, text, or claim applies to the current SKU.

## Missing-evidence rule

When evidence is missing, ask one focused question that names the exact needed material—for example: “Please provide one clear image/video frame showing the compartment fully open with the card inserted.” Do not ask for a generic “more images.”

If the user cannot provide the requested material, label the beat `omit` and remove its action, mechanism, claim, and dependent scene from the storyboard and prompts. Replace it only with a lower-risk beat that is supported by available evidence, such as a stable product reveal, visible detail close-up, or user reaction. Never invent an unseen product state, part, mechanism, or result.
