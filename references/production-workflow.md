# Production reference

## Select the model before the source-clip plan

The requested duration is the **finished-video target**. Read the live CLI help for the selected model before choosing any source duration. Do not infer one model's duration support from another model's name, account tier, or a prior run.

For the default 25-second high-density route, choose exactly one of these after the live check:

| Source route | Choose it when | Required join discipline |
| --- | --- | --- |
| `1 × 25s` | The selected model supports 25 seconds and a same-product test makes continuity risk acceptable. | Review causal continuity inside the full take; no continuation frame is needed. |
| `10s + 10s + 5s` | The selected model reliably supports ten-second action scenes and the story has two natural chapter breaks. | End the first two clips on a stable, product-visible pose or wipe/match-action handoff. |
| `5 × 5s` | Hands, product geometry, state changes, labels, or identity consistency need the highest retake control. | Give every clip one dominant action and a planned matching exit/entry movement. |

Never submit a route until its exact model, source durations, output count, references, resolution, ratio, and credit impact are stated for approval.

## Standard 30-second package choices

| Plan | Use it when | Trade-off |
| --- | --- | --- |
| One 25-second continuous story | The user requests high-density causal drama and the live Dreamina CLI model supports 25 seconds. | Best continuity and pace; a failed candidate is a larger retake. |
| 3 × 10 seconds | The model/account supports stable 10-second clips and the product action benefits from continuity. | Fewer cuts, but a failed clip costs more to regenerate. |
| 6 × 5 seconds | Product handling, logos, hands, or fine details need tighter control. | More reliable retakes, but more edit points. |

Do not rely on a model's long-duration option without testing the same product and shot type first.

## Story structures

### 25-second continuous or linked story

Use the same 1–3-second beat map for either route: hook → pressure → decision → product-relevant action → turn → two-second product proof → stable payoff. If split, assign the joins at a decision, an object/hand pass, a doorway/counter crossing, a pan, foreground occlusion, or a deliberate ordinary cut—not mid-action. Before generating, write a tail-frame contract for every non-final clip: actor pose/eyeline, product position/orientation, wardrobe, held props, setting, lighting, camera angle, and next opening action. After generating, extract and approve a real stable tail frame that matches this contract; this approved frame, not a guessed prompt image or literal last frame, is the continuation reference.

### 3 × 10 seconds

1. 0–10s — Hook and real product reveal.
2. 10–20s — Core use or proof demonstration.
3. 20–30s — Detail proof, product hero, and CTA safe area.

### 6 × 5 seconds

1. Hook.
2. Reveal.
3. Proof A.
4. Proof B.
5. Detail / scale cue.
6. Product hero / CTA safe area.

## Approval gate

Approve a clip only when:

- Product shape, color, logo, packaging, and included parts match the supplied reference.
- The action is understandable without an unsupported claim.
- Hands, faces, labels, and geometry are intact.
- The beginning and ending frames are stable enough for the intended edit.
- The clip has no unrelated brand, unsafe behavior, watermark, or visual defect.

Reject and regenerate the individual clip when any condition fails. Do not ask the compositor to hide a broken product or label.

## Continuation reference gate

Before generating a continuation, sample 4–8 candidates from the prior clip's final stable 1–2 seconds and visually inspect a contact sheet. Select a sharp, product-visible frame that preserves the needed actor pose and scene. Do not blindly use the literal last frame; regenerate the prior clip if it has no usable handoff frame. See `reference-frame-gate.md` for the required record.

## Local assembly

`assemble_jimeng_clips.py` uses FFmpeg's concat demuxer. Default stream-copy mode is fast and does not re-render video; all files must have compatible streams. Use `--reencode` for incompatible exports. If FFmpeg is not on `PATH`, pass `--ffmpeg "C:\\tools\\ffmpeg.exe"`. FFmpeg processing uses local compute only; it does not consume Codex tokens or JiMeng credits.
