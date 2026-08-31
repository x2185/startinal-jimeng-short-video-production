# Product asset classification

Classify every supplied image, video, and extracted frame before it can be used in a prompt. Keep the original files unchanged; record roles in the job manifest or evidence ledger. One asset may have more than one role, but it must never be promoted beyond what it visibly proves.

| Category | What belongs here | May be used for |
| --- | --- | --- |
| `identity` | Clear complete product views, SKU/colour/finish, included parts | Product identity lock and hero reference |
| `detail` | Sharp close-up of a label, slot, hinge, texture, connector, or other feature | Detail-proof shot and multi-reference structure lock |
| `action_start` | Exact configuration immediately before one action | Clip start state |
| `action_process` | Frames/footage that visibly prove an intermediate movement or alignment | Action-specific evidence; prefer real footage for fragile handling |
| `action_end` | Exact configuration immediately after the one action | Clip end state and acceptance check |
| `configuration_pairing` | Evidence that maps matching parts/variants, such as colour → attachment | Continuity lock |
| `packaging_or_text` | Packaging, readable claims, model number, logo, instructions | Text/packaging lock only after legal/claim review |
| `context` | Person, room, lifestyle, background, or prop without product proof | Scene direction only; never product identity or mechanism |
| `ambiguous` | Occluded, blurred, conflicting, or incomplete view | Do not use until clarified |
| `do_not_use` | Personal/card data, unrelated SKU, external brand, unsafe/prohibited content | Exclude from prompts and upload set |

For every requested video beat, choose assets in this order: `identity` + the relevant `detail` + `action_start` + `action_end`. Add `action_process` only when it clearly proves the movement. If either state is missing, mark the feature `needs additional asset`; do not let a generic identity image fill the gap.
