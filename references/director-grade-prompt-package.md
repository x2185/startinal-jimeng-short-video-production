# Director-grade prompt package

Use this mode for any selected test package, paid-ready package, or user request for a story-led UGC result. A creative matrix is an idea-selection artifact only; it is never a submission-ready JiMeng prompt by itself.

## Required artifacts

1. **Continuity bible:** exact product identity/passport; all characters with age range, appearance, wardrobe, relationship, demeanor; location; lighting; phone/UGC camera logic; prohibited changes; and accepted prior-frame state when this is a continuation.
2. **Beat sheet:** time-coded microbeats that fit the clip duration. Each beat states who acts, what changes, and the target composition. Keep spoken lines short enough to plausibly fit the beat; do not force narration through a fine hand action.
3. **Submission prompt:** a natural English directing prompt that combines the relevant bible and beat sheet. State scene, actors, dialogue, physical action order, camera, transition, product handling, and exact final frame.
4. **Acceptance gate:** continuity, product/mechanism, hand/face, dialogue timing, safety, and end-frame checks specific to that clip.

## Director rules

- A storyline needs a concrete setup, turn/proof, and payoff. Do not replace it with repeated product holds or disconnected actions.
- If an interaction is mechanically precise, reserve its own short clip and give the action's starting state, contact point, order, hold duration when material, and ending state.
- Give continuations an explicit inherited state: who holds what, posture, wardrobe, product orientation, location, light, camera direction, and emotional beat. Do not merely say “same scene.”
- A visible transition must have a mechanism: match action, product/prop passing close to camera, a foreground occlusion, a door/counter movement, or an ordinary cut. Do not ask the model to teleport people or products.
- Use exact scene detail that supports the story (ordinary home items, a neighborhood store, a simple counter); avoid generic adjectives and unnecessary luxury/cinematic language.
- Keep negative constraints targeted. Repeat the product lock and the one or two failure risks most likely for that clip rather than pasting an indiscriminate blacklist.

## 5-second conversion

When the source concept is 14–16 seconds but the generation mode supports 5-second clips, preserve the story by splitting it into three linked clips:

| Clip | Role | Required ending |
| --- | --- | --- |
| 1 | setup + first reaction | stable character/product/setting handoff |
| 2 | decisive proof/action | completed physical result, held long enough to read |
| 3 | reaction/payoff | stable hero or character outcome frame |

For a 30-second package, use six linked 5-second clips. Do not cram multiple location changes, fine actions, and several dialogue exchanges into one clip.

## Naming and approval

Label a package `creative-outline` until it contains all four required artifacts. Only label it `director-grade / submission-ready` after the prompt-quality gate passes and the user approves the package ID for paid submission.
