# Pre-submission prompt optimization

Run this private optimization pass after drafting a selected package and before calling it submission-ready. It improves prompt decisions before credits are used; it is not permission to invent facts, change an approved creative direction, or make a paid submission.

## Inputs that may not change

Treat these as locked unless the user changes them:

- visually evidenced product identity, configuration map, action states, and product scale;
- seller-confirmed claims and required core functions;
- market, language, safety, brand, price, age, and legal restrictions;
- approved story route, clip duration, and any accepted prior handoff frame.

If a required element is ambiguous or unsupported, mark the package blocked; do not solve it by more elaborate wording.

## One focused self-revision pass

1. **Compress the story test.** For every clip, state its immediate character goal, one primary visible action, visible result, and final handoff frame in one sentence. Remove a beat that advances none of those.
2. **Run the contradiction test.** Check product pairing, action map, inherited state, camera view, dialogue timing, and negative constraints. Preserve confirmed facts and simplify competing directions.
3. **Predict the highest-risk failure.** Select only one or two risks for that exact clip: product/pairing drift, fine hand interaction, character continuity, dialogue/lip-sync, unsafe target, or unstable end frame.
4. **Apply the smallest correction.** Strengthen the relevant reference role, start/end state, contact point, composition lock, or targeted negative constraint. Do not paste a generic blacklist or add unrelated styling.
5. **Choose the final language.** Use concise English for U.S.-English JiMeng packages unless the interface or user requires Chinese. Keep spoken performance in its required spoken language; do not alternate Chinese and English instructions within one prompt.
6. **Recheck priority.** Lead with scene and identity, then one action, required end frame, then targeted negatives. Remove duplicate adjectives, vague quality claims, and detail that competes with the action.

Make no more than one broad rewrite plus one narrow correction in this pass. If a hard check still fails, request evidence or revise the shot plan rather than entering an unbounded rewrite loop.

## Required pre-submission record

Save `prompt-optimization-audit.md` in the package/job folder:

```markdown
# Prompt optimization audit — <package ID>

## Locks retained
- Product / configuration: ...
- Required action states: ...
- Restrictions: ...

## Risks predicted and corrections
| clip | highest-risk failure | focused correction | result |
| --- | --- | --- | --- |
| C03 | fine hand action may drift | isolated load/release; retained tray-only target | pass |

## Material changes
- ...

## Final decision
submission-ready | blocked, because ...
```

Present the revised prompt set—not a stream of drafts—to the user, then use the normal final approval gate before any paid submission.
