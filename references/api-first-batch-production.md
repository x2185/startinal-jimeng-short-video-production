# API-first batch production

Use this mode when the operator's primary workflow is API generation. It is the default unless the user explicitly chooses JiMeng's web UI.

## Route

1. Read and classify local material, then select only target-SKU reference files.
2. Validate credentials and the package with a no-cost dry run.
3. Submit one explicitly approved, named high-risk clip using `--max-clips 1`.
4. Inspect its start, action, and end frames. A failed candidate is a failed API test, not product evidence.
5. After approval, submit stable product-display clips in resumable batches. Keep prompts, task IDs, downloads, handoff frames, and rejection records per job.

The legacy `jimeng_i2v_first_v30` endpoint accepts one local image encoded as Base64. It is suitable for stable display or a deliberately limited one-action test. It is not an excuse to invent hidden mechanisms.

## Reference rule

Do not upload another SKU as an image reference to copy its motion. Record its observable motion constraints—hand pose, POS approach angle, contact distance, camera crop—in the evidence ledger, then upload only the target SKU. This prevents colour and geometry transfer.

## Text and payment rule

Generated POS interfaces, receipts, prices, and approval messages are high-risk for garbling, brand leakage, and financial implication. Default to an unbranded terminal with unreadable/blank display. Add approved explanatory captions only in deterministic finishing after source-clip acceptance.

## Stop conditions

- Do not retry a paid clip without new user approval.
- If the target product identity changes twice in the same action class, stop API retries and use real footage or request same-SKU state evidence.
- Never turn an API limitation into a request for web login unless the user explicitly chooses the UI route.
