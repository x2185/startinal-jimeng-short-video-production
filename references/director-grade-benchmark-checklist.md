# Director-grade benchmark checklist

Run this checklist before calling any package `director-grade`, before presenting it as a generation candidate, and again after a material revision. When a current-task benchmark exists, compare the candidate against it item by item; a missing item is a fail, not an assumption.

```markdown
## Director-grade check — <package ID>

- Benchmark compared: <current-task benchmark ID/path, or none>
- Product/reference roles: pass | fix — <identity, geometry, detail, action, handoff roles>
- Character continuity: pass | fix — <age/presentation, hair, build, wardrobe, relationship, mannerisms>
- Microbeat detail: pass | fix — <0.5–2s ordered sub-actions where needed>
- Action choreography: pass | fix — <start, acting hand/grip, orientation, contact/motion, end>
- Camera direction: pass | fix — <framing, angle, movement, focus target, shot order>
- Transition logic: pass | fix — <motivated entry/exit and causal reason>
- Tail-frame contracts: pass | fix — <every non-final linked clip>
- Full prompt and negatives: pass | fix — <English prompt, product lock, targeted failures>
- Acceptance gate: pass | fix — <identity, story, action, tails, safety>
- Benchmark parity: pass | fix — <specific comparison against benchmark>
- Result: director-grade | creative-outline | blocked
```

Every row must pass for `director-grade`. A `fix`, missing evidence, or unresolved model limitation makes the package `creative-outline` or `blocked`; it cannot be a director-grade generation candidate.

Complete the record separately for every requested variant. Shared product facts may use a passport ID, but shared boilerplate is not a pass for character direction, action, camera, transition, tail frame, negative constraints, or acceptance checks.

The benchmark controls operational detail, not product content. Match its character/action/camera/transition specificity; never copy its SKU, actors, locations, story, dialogue, or unsupported claims into another job.
