# Original story creation and production routing

Use this reference when a user asks for a story, situational comedy, short commercial, dialogue-led UGC, a visual premise, or a script-like idea.

## Create, do not copy

- Treat the user's example as a statement of desired tone, audience response, and story mechanism—not as a script to duplicate.
- Derive a new premise from the current product identity passport, verified features, market, restrictions, available evidence, and the user's preferred style.
- Vary at least two structural dimensions across alternatives: opening event, character goal, setting, source of surprise, proof order, camera perspective, emotional turn, or ending.
- Do not reuse prior product footage, scenes, actors, dialogue, branded settings, or a previous job's plot. Historical AI material is learning-only.

## Build a story package

For each selected story, define a concise 30-second arc:

1. **Setup / hook:** a believable adult context and immediate visual question.
2. **Turn:** a product fact, choice, or supported interaction that changes the moment.
3. **Proof:** one clear, evidence-backed product detail or action.
4. **Payoff:** a natural reaction or stable product-visible ending; never invent a result, testimonial, or claim.

Choose a style that fits the brief—such as warm realistic UGC, low-key situational comedy, polished lifestyle commercial, observational slice-of-life, gift story, or visual reveal—rather than applying a fixed genre or plot.

## Production routing for story beats

Classify every beat before writing submission prompts:

| Route | Suitable beat | Production rule |
| --- | --- | --- |
| `generate_low_risk` | establishing environment, adult reaction without product handling, stable product display, camera-only detail, ordinary cut | Generate as independent scene blocks with exact identity locks. |
| `real_footage_insert` | payment contact, card loading, twisting, assembly, fine hand contact, a required on-screen result | Use only when the user explicitly names an existing, clean, same-SKU real clip for this final; never suggest it by default. |
| `omit_or_rewrite` | all fine or state-changing actions by default; unsupported mechanism, prohibited claim, missing evidence, unsafe or ambiguous result | Replace with a supported story beat; do not ask any generative route to invent it. |

Do not use a continuous story prompt to hide a risky interaction. For the legacy 720P API, make intentional cuts between independent generated story blocks. Fine actions remain omitted unless the user explicitly directs use of a named real-footage insert.

## Text, brands, and outcomes

Only request readable screen text, a payment result, brand, store identity, price, or claim when the current brief explicitly permits that element. If a story concept needs one of these and the brief is silent, flag it as a compact confirmation item; do not assume it is allowed.
