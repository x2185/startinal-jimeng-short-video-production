# API-first batch production

Use this mode when the operator's primary workflow is API generation. It is the default unless the user explicitly chooses JiMeng's web UI.

## Route

1. Read and classify local material, then select only target-SKU reference files.
2. Validate credentials and the package with a no-cost dry run.
3. Submit one explicitly approved, named high-risk clip using `--max-clips 1`.
4. Inspect its start, action, and end frames. A failed candidate is a failed API test, not product evidence.
5. After approval, submit stable product-display clips in resumable batches. Keep prompts, task IDs, downloads, handoff frames, and rejection records per job.

The legacy `jimeng_i2v_first_v30` endpoint accepts one local image encoded as Base64. It is suitable for stable display or a deliberately limited one-action test. It is not an excuse to invent hidden mechanisms.

### One-image hard limit

For this endpoint, upload **one target-SKU identity-locked image only** for each low-risk scene block. This may be either a clean verified product identity image or a visually accepted creative first frame made from that exact product plus an unbranded scene background. Do not upload an original product image and a generated prior-tail frame together: the endpoint cannot accept both. Review the prior tail to decide whether it is usable in the final edit, but keep the next API call anchored to the accepted identity-locked image. Do not automatically use a generated tail as the next block's sole reference, because a malformed hand or product can then propagate into later clips.

An accepted tail frame becomes an additional generation input only after moving to a verified multi-reference route. It is never a substitute for the target product identity reference in the legacy batch route.

## Default 720P scene-block strategy

For the legacy single-first-frame API, generate several independent **5-second scene blocks** rather than one continuous 30-second performance. Each block has one low-risk action only: stable hero display, pick up, set down, carry, show in a bag/pocket, small orientation change, material macro, or a reaction with the product unchanged. Vary the setting, framing, hook, and actor/context across blocks while preserving the same SKU identity.

Build and deliver the 30-second video in deterministic finishing from accepted blocks: hook → varied context/product proof → approved real action insert only when that specific final needs it → hero ending. The generated blocks are production sources, not the default user delivery. For a multi-final batch, apply `batch-source-allocation.md`: do not make the same supplied real-action clip a default insert across every final, and never loop a clip to fill runtime. Return raw clips only when explicitly requested, or when the final is blocked because a required real-action insert is missing.

Actual payment contact, card insertion/loading, hidden-slot operation, twisting, fastening, assembly, and other exact state transitions are **not** legacy-single-frame scene blocks. Do not automatically insert available real footage merely because it exists. If the user explicitly requires one of these actions in the final, use the named approved same-SKU real-footage insert or a verified compatible multi-reference route. Otherwise omit the action and build the final from newly generated low-risk scenes. Never use another SKU merely to demonstrate the motion.

## Reference rule

Do not upload another SKU as an image reference to copy its motion. Record its observable motion constraints—hand pose, POS approach angle, contact distance, camera crop—in the evidence ledger, then upload only the target SKU. This prevents colour and geometry transfer.

## Text and payment rule

Generated POS interfaces, receipts, prices, and approval messages are high-risk for garbling, brand leakage, and financial implication. Default to an unbranded terminal with unreadable/blank display. Add approved explanatory captions only in deterministic finishing after source-clip acceptance.

## Stop conditions

- Do not retry a paid clip without new user approval.
- If the target product identity changes twice in the same action class, stop API retries and use real footage or request same-SKU state evidence.
- Never turn an API limitation into a request for web login unless the user explicitly chooses the UI route.
