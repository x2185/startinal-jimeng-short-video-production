# Continuous improvement loop

Treat user feedback and accepted/rejected renders as evidence for improving this skill. Do not treat a single bad generation as proof of a universal rule.

## Where to retain knowledge

| Kind of learning | Store it in | Example |
| --- | --- | --- |
| Cross-product, repeatedly useful rule | This skill or one of its references | inspect state-specific action evidence before prompting |
| Product/SKU fact or restriction | That product's brief and job manifest | pink frame must pair with pink figure |
| One run's failure and correction | That job's `retrospective.md` | Clip 3 warped while stretching; split the action |
| User's enduring production preference | This skill, only after the user confirms it applies broadly | default realistic UGC with soft 45-degree daylight |

Never store credentials, private customer data, personal data visible in assets, or unverified market claims in a shared skill or learning record.

## After a test or user critique

1. Capture the exact observed result, package/clip ID, likely cause, correction, and whether the correction was later accepted.
2. When the user says a result is unsatisfactory or asks for a change, create a numbered feedback round. Classify the feedback as product fidelity, action, creative idea, scene/actor, pacing/edit, copy/audio, or compliance. Quote the user's actual preference and attach the affected clip/frame when available; do not reduce "not creative enough" to a generic prompt-length change.
3. Propose the smallest revision plan: preserve accepted clips, change only the affected prompt, reference, scene block, edit beat, copy, or audio layer. If the user asks for a new creative direction, keep the product facts but create fresh routes rather than patching an unwanted premise.
4. Keep the correction local to the product until it has either repeated across products or the user explicitly declares it a general preference.
5. Promote only the smallest supported general rule. Do not convert a product-specific color, prop, story, or failed one-off into a permanent global constraint.
6. Add the accepted source frames, product identity passport, prompt version, and render manifest to the job folder so the next variation is reproducible.
7. Before a new job, load only the general rules and the current product brief. Do not copy previous product facts into a new brief.

## Feedback-round record

Store each round in the current job's `review/feedback-round-<n>.md` and add its product-specific conclusion to `learning-library/` only after the revised result has been reviewed.

```markdown
# Feedback round <n> — <job/package ID>

- User feedback: <verbatim concise quote or faithful summary>
- Affected output: <final / clip ID / timecode / frame>
- Category: fidelity | action | creative | scene | pacing | copy-audio | compliance
- Keep unchanged: <accepted parts>
- Revision hypothesis: <smallest plausible change>
- Planned change: <prompt / reference / scene block / edit / copy-audio>
- Paid scope: unchanged | requires approval
- Result: pending | accepted | rejected
- Product learning: <only after review>
```

## Required retrospective template

```markdown
# Retrospective — <job/package ID>

- Evidence: <accepted/rejected clip, frame, or user feedback>
- Observation: <what visibly happened>
- Cause hypothesis: <only if supported>
- Correction tested: <prompt/reference/shot-plan change>
- Outcome: accepted | rejected | not yet tested
- Scope: product-only | candidate-general | confirmed-general
```
