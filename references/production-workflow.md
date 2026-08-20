# Production reference

## Duration choice

| Plan | Use it when | Trade-off |
| --- | --- | --- |
| 3 × 10 seconds | The model/account supports stable 10-second clips and the product action benefits from continuity. | Fewer cuts, but a failed clip costs more to regenerate. |
| 6 × 5 seconds | Product handling, logos, hands, or fine details need tighter control. | More reliable retakes, but more edit points. |

Do not rely on a model's long-duration option without testing the same product and shot type first.

## 30-second structures

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
