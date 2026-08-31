# Job workspace and resume

Do not ask an operator to build a folder tree. They provide only the existing material folder and the target SKU; the Skill creates and maintains the records under the project `jobs` folder. A new Codex conversation has no reliable working memory, so it must resume from the generated record before reading raw material again.

```text
<project>\jobs\<product>--<sku>\
  product-record\          # automatically created asset manifest, passport, evidence ledger
  <YYYY-MM-DD--campaign>\
      brief\               # current brief, storyboard, prompt package
      api-runs\             # task IDs, responses, downloads, review frames
      review\               # acceptance and failure records
      candidates\           # new generated clips waiting for a decision
      accepted\             # clips selected for this job's finished video
      rejected\             # failed clips, never used as evidence or handoff
      final\                # deliverable MP4 and render manifest
  learning-library\         # optional automatic learning records
```

Never move or overwrite the operator's material folder. Keep `.env` beside the project or in a separate private configuration location; never commit it or put it in a shared learning library.

## New conversation / teammate resume

Start with the product workspace and job folder, not a broad request to rediscover everything:

```text
Use $startinal-jimeng-short-video-production.
Materials: D:\素材\<product>
SKU: <colour/style>
Resume the matching job if one exists; otherwise create it automatically under jobs.
Read the generated product record and current job first. Scan the material folder only for changes.
Continue toward one finished 30-second MP4; do not deliver raw fragments by default.
```

The Skill must read, in order: `product-record/asset-manifest.json`; identity passport/evidence ledger; current job brief and prompt package; API manifest; review/failure records; and render manifest. If the asset scan reports no changes, reuse the existing product record and inspect only the required selected references. Do not repeatedly analyse every source file.

## When material changes

Place new or replacement files in the existing material folder, then say “素材已更新”. Do not overwrite a reviewed file without retaining a dated replacement or recording the change.

| Change | Required response |
| --- | --- |
| Added photo/video of the same SKU | Inspect only the new file plus current selected references; update the evidence ledger if it improves a beat. |
| New SKU, colour, packaging, included part, or mechanism | Create a separate SKU workspace or mark a material conflict; never silently merge it into the old passport. |
| New real action footage | Map its start/end state and use it as the fixed action insert when approved. |
| No source change | Resume from current records; do not re-read the whole material library. |

## Status rules

`candidate` means downloaded but not usable. `accepted` means it passed the current job's visual checks and may be edited into that job's final. `rejected` means retain it for diagnosis only. `final` contains only completed delivery renders. Historical accepted clips remain learning references unless the user explicitly requests exact reuse.

At completion, write the final path, selected source clips, source real-footage inserts, copy variables, review result, and outstanding risks into `final/render-manifest.json`. This is the handoff record for the next conversation or teammate.
