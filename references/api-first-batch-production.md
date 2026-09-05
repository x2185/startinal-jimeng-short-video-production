# API-first batch production

Use this mode when the operator's primary workflow is API generation. It is the default unless the user explicitly chooses JiMeng's web UI.

## Route

1. Read and classify local material, then select only target-SKU reference files.
2. Validate credentials and the package with a no-cost dry run.
3. Submit one explicitly approved, named low-risk validation clip using `--max-clips 1`.
4. Inspect dense review frames and the contact sheet. A failed candidate is a failed API test, not product evidence.
5. After approval, submit stable product-display clips in resumable batches. Keep prompts, task IDs, downloads, handoff frames, and rejection records per job.

The legacy `jimeng_i2v_first_v30` endpoint accepts one local image encoded as Base64. It is suitable for stable display or a deliberately limited one-action test. It is not an excuse to invent hidden mechanisms.

### One-image hard limit

For this endpoint, upload **one target-SKU identity-locked image only** for each low-risk scene block. This may be either a clean verified product identity image or a visually accepted creative first frame made from that exact product plus an unbranded scene background. Do not upload an original product image and a generated prior-tail frame together: the endpoint cannot accept both. Review the prior tail to decide whether it is usable in the final edit, but keep the next API call anchored to the accepted identity-locked image. Do not automatically use a generated tail as the next block's sole reference, because a malformed hand or product can then propagate into later clips.

An accepted tail frame is an edit-review record only. It is never a substitute for the target product identity reference in the legacy batch route.

## Default 720P scene-block strategy

For the legacy single-first-frame API, generate six independent **5-second scene blocks** rather than one continuous 30-second performance. Each block has one low-risk camera/background movement only: stable hero display, supported tabletop display, material macro, empty-bag context without insertion, or an adult reaction without product handling. Vary the setting, framing, hook, and actor/context across blocks while preserving the same SKU identity.

Build and deliver the 30-second video in deterministic finishing from accepted blocks: hook → varied context/product proof → hero ending. The generated blocks are production sources, not the default user delivery. Never loop a clip to fill runtime. Return raw clips only when explicitly requested.

Actual payment contact, card insertion/loading, hidden-slot operation, twisting, fastening, assembly, and other exact state transitions are **not** scene blocks for the legacy single-reference API. Omit or rewrite them there by default; when the user needs the action, ask whether to use the CLI multi-reference route with role-labelled start/contact/end evidence. Never insert source footage into the final or use another SKU to demonstrate the motion.

## Reference rule

Do not upload another SKU as an image reference to copy its motion. Upload only the target SKU; derive only low-risk camera distance, composition, and background movement from historical learning records.

## Text and payment rule

Generated POS interfaces, receipts, prices, and approval messages are excluded with the underlying fine action. Do not generate or add them in finishing; if the story needs a payment moment, keep the product role and reaction clear without relying on fabricated readable UI.

## Stop conditions

- Do not retry a paid clip without new user approval.
- If the target product identity changes twice in a low-risk scene class, stop API retries and simplify the scene or request a cleaner identity image.
- Never turn an API limitation into a request for web login unless the user explicitly chooses the UI route.
