# Batch source allocation

Use this when producing more than one final video from one product's material folder. The goal is to create genuinely different deliverables, not to hide a shortage of scenes by repeating the same supplied footage.

## Plan before generation

For every planned final, record a source allocation row:

| Final ID | Creative route | Required factual proof | Real-footage insert | New generated scene blocks | Repeat status |
| --- | --- | --- | --- | --- | --- |

Set `real-footage insert` to `none` unless that final must visibly prove an exact, high-risk action. Product-display, lifestyle, gift, reaction, material/detail, and most promotional variants can use newly generated low-risk blocks only.

## No-default-reuse rule

- A supplied real-footage segment is a scarce proof asset, not a default middle section for every final.
- Within one batch, use the same real-footage segment in **at most one final by default**. Do not loop it, replay it, or use it as B-roll in another final.
- If several finals genuinely must show the same exact action, first assign different same-SKU takes, angles, or trims. If none exists, make only the clearly labelled action-proof version show the action and create the remaining variants around supported low-risk proof; ask for more real footage only when the action is mandatory in every requested version.
- Never use a supplied action clip merely to fill runtime. A final that is short of time needs a new approved scene block, a different detail beat, a new real take, or a shorter approved duration—not a loop.

## Batch mix

Default to a varied mix appropriate to the brief: product-display variants, story/lifestyle variants, gift/reaction variants, and a limited number of action-proof variants. The batch plan must state which finals contain a real insert and why. A user may explicitly request a repeat, but the render manifest must mark it `user_requested_repeat`.

## Final assembly check

Before delivery, compare all render manifests in the batch. Reject a planned final if it repeats a real-footage source segment from another final without `user_requested_repeat`, repeats a generated clip within its own timeline, or uses a loop solely to reach the requested duration. Record clip IDs, trim ranges, and source type in each final manifest.
