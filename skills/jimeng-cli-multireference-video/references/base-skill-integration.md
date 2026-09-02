# Base Skill integration

Use this reference when both product-video Skills are available.

The base Skill is the production system of record. It owns:

- product intake, asset scan, classification, and evidence ledger
- SKU-specific identity passport and restrictions
- content mode, script/creative development, and 20-variant planning
- prompt-quality gate, review-frame QA, failed-clip decisions, and learning record
- the job workspace, deterministic assembly, final QA, and final MP4

The CLI Skill adds only the high-quality generation route. Its job record should add a channel section to the same base job manifest:

- `channel: dreamina-cli-multireference`
- selected model and current CLI-supported parameters
- local reference paths and each reference role
- exact submission command without secrets
- submit ID, terminal status, downloaded media path, and QA decision

Use the original Skill's `6 x 5s` independent scene-block approach by default. A direct 4-30 second CLI output is an optional route only when the product identity, story, and model capability have a clearly lower risk than the assembled plan. It still needs the same visual acceptance gate.

For a new creative request, do not create two separate plans. Produce the base storyboard once, then choose either the low-cost single-reference API route or the CLI multi-reference route per shot. The user must approve any paid CLI submission after seeing the selected route and reference pack.
