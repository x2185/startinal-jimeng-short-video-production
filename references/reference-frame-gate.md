# Reference-frame gate

Use this gate after accepting a generated clip and before submitting the next linked clip.

## Select from candidates

1. Extract 4–8 stills from the last stable 1–2 seconds; include the literal final frame only as one candidate.
2. Reject a candidate when it is blank/near-black, overexposed, motion-blurred, a transition frame, obscured by a hand or prop, missing the product, or changes any must-match item in the product identity passport.
3. Select the clearest frame where the whole product is recognizable, still matches the passport, and the actor pose, setting, light, and camera direction can be continued.
4. If no candidate passes, regenerate the preceding clip with an earlier stable ending. Do not pass a weak frame to the next generation.

## Minimum handoff record

Record the selected filename/timecode and describe: product location and orientation; passport traits visibly confirmed; actor hand/pose; wardrobe; visible props; background; lighting; camera angle; and the next intended action. Attach the selected handoff frame plus the fixed product-identity reference to the next request when supported.

## Automation boundary

Automated checks may flag blank, dark, overexposed, or blurry frames, but cannot reliably prove product identity or narrative suitability without visual inspection. Require Codex or a human to inspect the candidate contact sheet before submission.
