# Generated asset catalog

Use the catalog after a JiMeng run, a manual export, or before reusing previously generated media. It classifies files without moving or deleting them.

## Meaning of the categories

- `source_product_reference`: original product image/frame; it may support product identity or action evidence.
- `generated_clip` / `assembled_final`: generated media that is **unreviewed** until a person accepts it.
- `continuity_reference`: a handoff frame that may be used only after it passes the next clip's continuity check.
- `review_asset`: contact sheet or review frame; not reusable output media.
- `job_record`: prompt, manifest, task response, or other run metadata.

Generated media never establishes a new product fact or mechanism. Keep the real source material as the evidence authority.

## Run

```powershell
python .\skills\startinal-jimeng-short-video-production\scripts\catalog_generated_assets.py `
  --root .\output `
  --catalog .\output\generated-asset-catalog.json `
  --report .\output\generated-asset-catalog.md
```

The JSON catalog is machine-readable. The Markdown report is a review queue. After human approval, record acceptance in the package/job manifest rather than relabeling an unreviewed source file as proof.

## Material-library copy

After visual review, create a small `job_decisions` JSON file with one status per job: `accepted`, `candidate`, `rejected`, or `needs_origin_review`. Then create renamed copies in the material library:

```powershell
python .\skills\startinal-jimeng-short-video-production\scripts\organize_generated_assets.py `
  --catalog .\output\generated-asset-catalog.json `
  --decisions .\output\generated-asset-review-decisions.json `
  --library-root .\materials\generated-library
```

The organizer copies rather than moves. Its folders encode job, review state, and asset role; its manifest maps every new filename back to the immutable original. Do not place rejected media in the reusable candidate folder, and do not place generated material in original product-evidence folders.
