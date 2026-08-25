# Asset-change gate

Run the asset scan before planning whenever a material folder is supplied or reused:

```powershell
python scripts/scan_product_assets.py --root "D:\\素材\\产品名" --manifest "output\\产品名\\asset-manifest.json"
```

The manifest fingerprints every supported image/video using SHA-256, so an overwritten file is detected even if its filename is unchanged.

## Routing

| Scan result | Required action |
| --- | --- |
| First scan | Inspect material, create product identity passport, and select reference assets. |
| No content change | Reuse the passport only after checking it still matches the user's intended product. |
| Added/changed/deleted asset | Inspect only the changed assets plus the current reference set. Rebuild the passport if any identity trait, packaging state, included part, or supported feature changes. |

Do not infer that files in one folder all show one product. Compare changed assets with the identity passport. If a new/changed asset may depict another product, variation, colorway, package, or conflicting feature, mark `material-conflict`, exclude it from generation, and ask the user which group to use before paid submission.

The script detects file changes, not visual product identity by itself. Codex must inspect the changed assets/contact sheets and report the grouping decision.
