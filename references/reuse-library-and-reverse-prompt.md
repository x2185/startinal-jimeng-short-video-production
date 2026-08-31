# Reuse library and reverse prompt

Use this when prior generated clips are user-approved and should inform later API batches.

## Library record

Create a portable `material-library.json` beside the job records. It must contain `library_root` as a replaceable root alias, relative source paths, SKU, scene/beat, status, restrictions, and prompt provenance. On another computer, set the new root path, run the normal asset scan, and keep the records whose relative files still exist. Do not store machine-specific absolute paths as the only locator.

## Learn without inventing history

1. Inspect start, action, and end frames of a good clip.
2. If a filename, prompt record, or task JSON contains the historical prompt, preserve it as `recorded_prompt`.
3. Otherwise write `inferred_template`: subject/SKU lock; one action; camera/framing; setting; lighting; ending; negative constraints; and any observed failure exclusions.
4. State that `inferred_template` is a tested recreation, not the original prompt.

Generated media may supply style, framing, pacing, product-visible composition, and a previously accepted result state. It never proves a hidden product mechanism or a new marketing claim. Unless the user explicitly asks for the exact prior clip to be reused, it is a learning reference only—not source media for a new final video.

## Batch use

Search same-SKU, same-beat approved clips before generating to learn what worked. When generating a new variation, start from its prompt-learning record, change the current scene and requested variables, and keep the identity and failure exclusions locked. Submit a newly generated clip for every new deliverable.
