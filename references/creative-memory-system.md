# Creative memory system

Use a local JSON ledger to carry only approved preferences and evidence-backed production learning into later jobs. The default workspace path is `data/creative-memory.json`; it is intentionally ignored by Git so personal preferences and local run history do not get pushed with the skill.

## What belongs in memory

| Record | Scope | Promotion rule |
| --- | --- | --- |
| User preference | `user-global` | User explicitly says it should apply later. |
| Quality benchmark | `user-global` or `product` | User approves it as a minimum standard. |
| Product fact or restriction | `product` | Current product evidence or seller confirmation only. |
| Model/reference/GPT-scene/prompt outcome | `job` first | Promote only after repeated accepted evidence across products or explicit user confirmation. |

Never record credentials, customer/payment data, raw identifying media details, unverified claims, another seller's creative assets, or unreviewed generated output.

## Lifecycle

1. At a new task, if the ledger exists, load only `confirmed` user-global preferences and accepted observations relevant to the chosen route. Do not import another product's identity, facts, characters, or story.
2. Create the current product brief from current assets first. User instructions and current product facts override memory.
3. After a user critique, approved benchmark, or reviewed generation, write a narrow memory entry with evidence and scope.
4. Record failed/unproven patterns as `job` observations. They do not become defaults.
5. Before drafting a director-grade batch, compare it against applicable confirmed quality benchmarks.

## Commands

```powershell
# Create once; safe if it already exists.
python .\skills\startinal-jimeng-short-video-production\scripts\creative_memory.py init `
  --memory .\data\creative-memory.json

# Save an explicit user-wide preference.
python .\skills\startinal-jimeng-short-video-production\scripts\creative_memory.py add-preference `
  --memory .\data\creative-memory.json `
  --key director_grade_minimum `
  --value "Use detailed microbeats, actor/action/camera direction, reference roles, and tail-frame contracts." `
  --evidence "User explicitly required this standard."

# Save a confirmed benchmark; path is a local reference, not media to reuse as product evidence.
python .\skills\startinal-jimeng-short-video-production\scripts\creative_memory.py add-benchmark `
  --memory .\data\creative-memory.json `
  --name green-holder-dg01-detail-floor `
  --path .\jobs\cli-continuity-test\green-middle-finger-dg01-microbeat-demo.md `
  --criteria "Later director-grade variants match or exceed its operational detail." `
  --evidence "User approved it as the minimum quality floor."

# Record a reviewed test result; keep it job-scoped until it is proven reusable.
python .\skills\startinal-jimeng-short-video-production\scripts\creative_memory.py add-observation `
  --memory .\data\creative-memory.json `
  --kind model --outcome accepted `
  --summary "Five linked clips held product identity across approved handoffs." `
  --cause-hypothesis "Role-labelled references plus approved tail frames helped continuity." `
  --correction "Reuse this route only for comparable action complexity." `
  --evidence "<job manifest and approved clip IDs>"

# Inspect only reusable/confirmed records.
python .\skills\startinal-jimeng-short-video-production\scripts\creative_memory.py show `
  --memory .\data\creative-memory.json --confirmed-only

# Manually transfer only confirmed user-global preferences and benchmark criteria.
python .\skills\startinal-jimeng-short-video-production\scripts\creative_memory.py export-confirmed `
  --memory .\data\creative-memory.json `
  --output .\data\creative-memory-portable.json

# On another workspace, review that file first, then import it. Product/job history is excluded.
python .\skills\startinal-jimeng-short-video-production\scripts\creative_memory.py import-confirmed `
  --memory .\data\creative-memory.json `
  --input .\data\creative-memory-portable.json
```

The script edits only the supplied ledger path. It never submits media, calls JiMeng, or reads source images/videos.
