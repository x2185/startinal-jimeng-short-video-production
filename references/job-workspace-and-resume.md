# Job workspace and resume

Use one durable product workspace per SKU. A new Codex conversation has no reliable working memory, so it must resume from this workspace before reading raw material again.

```text
D:\JiMeng任务\<product>\<sku>\
  source\                 # immutable original images and real footage
  product-record\          # asset-manifest, passport, evidence ledger, approved facts
  jobs\
    <YYYY-MM-DD--campaign>\
      brief\               # current brief, storyboard, prompt package
      api-runs\             # task IDs, responses, downloads, review frames
      review\               # acceptance and failure records
      candidates\           # new generated clips waiting for a decision
      accepted\             # clips selected for this job's finished video
      rejected\             # failed clips, never used as evidence or handoff
      final\                # deliverable MP4 and render manifest
  learning-library\         # optional approved historical learning records only
```

Never move or overwrite files in `source`. Keep `.env` beside the local workspace or in a separate private configuration location; never commit it or put it in a shared learning library.

## New conversation / teammate resume

Start with the product workspace and job folder, not a broad request to rediscover everything:

```text
Use $startinal-jimeng-short-video-production.
Resume workspace: D:\JiMeng任务\<product>\<sku>
Job: <YYYY-MM-DD--campaign>, or create one if absent.
Read product-record and the current job first. Scan source only for changes.
Continue toward one finished 30-second MP4; do not deliver raw fragments by default.
```

The Skill must read, in order: `product-record/asset-manifest.json`; identity passport/evidence ledger; current job brief and prompt package; API manifest; review/failure records; and render manifest. If the asset scan reports no changes, reuse the existing product record and inspect only the required selected references. Do not repeatedly analyse every source file.

## When material changes

Place new or replacement files in `source`, then rescan. Do not overwrite a reviewed file without retaining a dated replacement or recording the change.

| Change | Required response |
| --- | --- |
| Added photo/video of the same SKU | Inspect only the new file plus current selected references; update the evidence ledger if it improves a beat. |
| New SKU, colour, packaging, included part, or mechanism | Create a separate SKU workspace or mark a material conflict; never silently merge it into the old passport. |
| New real action footage | Map its start/end state and use it as the fixed action insert when approved. |
| No source change | Resume from current records; do not re-read the whole material library. |

## Status rules

`candidate` means downloaded but not usable. `accepted` means it passed the current job's visual checks and may be edited into that job's final. `rejected` means retain it for diagnosis only. `final` contains only completed delivery renders. Historical accepted clips remain learning references unless the user explicitly requests exact reuse.

At completion, write the final path, selected source clips, source real-footage inserts, copy variables, review result, and outstanding risks into `final/render-manifest.json`. This is the handoff record for the next conversation or teammate.
