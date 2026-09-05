# Product reference pack

Build this pack when a real product must appear in generated story scenes without asking a video model to recreate its fine geometry.

## Inputs and selection

Choose only frames that visibly prove the finished product identity: clean full silhouette, true color, scale, material, and distinctive parts. Keep original source files in the pack. Do not use a frame with readable card data, a visible brand, another SKU, heavy motion blur, or hand occlusion as the sole identity asset.

Create the pack with:

```powershell
python scripts/build_product_reference_pack.py --input <identity-frame-1.jpg> --input <identity-frame-2.jpg> --output-dir <job-output>/product-reference-pack --label <sku-or-variant>
```

The script uses `rembg` only when installed. Its transparent PNG output is a candidate and must be visually reviewed for missing edges, holes, altered tips, and dropped translucent material. If `rembg` is unavailable, it preserves source images and records that transparent assets are pending; it never claims to have isolated the product.

## Use the right layer

| Need | Preferred method |
| --- | --- |
| Exact product visible in a story/reaction scene | Composite an accepted transparent cutout into a deterministic HyperFrames/FFmpeg scene, or make a staged first-frame reference. |
| Product is held but no fingers cross its critical shape | Generated scene may use the staged first frame; retain a product-visible acceptance check. |
| Fingers, shadows, rotation, or occlusion cross a critical feature | Use original state-specific reference frames plus a multi-reference generated candidate. Do not rely on a cutout to fake interaction; if it remains unstable, revise or omit the interaction. |
| Installation, insertion, twisting, payment tap, or another precise state change | Use start/contact/end-state references in a multi-reference CLI candidate; reject it if the mechanism, product identity, or contact action drifts. |

Generated scenes may establish people, settings, reactions, dialogue, and atmosphere. Real product assets preserve identity. A product cutout never verifies a mechanism or a claim by itself.

## Cost rule

Complete reference-pack selection, edge review, storyboard, staged-first-frame check, and prompt audit before paid generation. A paid generation must be a candidate for the final edit, not a disposable test. If a generated clip changes the identity passport, reject that clip. Improve the reference pack, split or revise the fragile action, or use a supported static product role rather than paying repeated retries.
