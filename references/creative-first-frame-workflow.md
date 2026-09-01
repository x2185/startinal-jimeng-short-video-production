# Creative first-frame workflow

Use this workflow when raw product photos are accurate but would make single-reference video output repetitive, overly source-bound, or creatively flat.

## Separation of roles

- **Product evidence** locks the SKU, silhouette, colour, proportions, finish, and permitted claims.
- **Real footage** proves state-changing actions such as loading, installation, opening, payment, or fastening.
- **Creative scene assets** provide new settings, lighting, mood, story context, and camera starting composition. They never prove a product feature or action.

## Legacy one-image API route

The single-first-frame endpoint can receive only one image. For a low-risk creative scene block, prepare one **creative first frame** that combines a verified product identity layer with a new unbranded scene background. Use it as the sole API reference.

1. Create or select a 9:16 scene background with an empty, plausible product surface. It must be unbranded and free of text, prices, POS/payment interfaces, and prohibited people.
2. Composite the exact target-SKU identity asset into the scene. Preserve source aspect, visible parts, and colour. Do not redraw the product as a stylistic prop.
3. Inspect the composite before submission. Reject it if it has a rectangular remnant, halo, incorrect perspective, duplicated product, altered part, or implausible contact/shadow. Fix the first frame instead of asking video generation to hide the defect.
4. Generate one low-risk camera or atmosphere movement only. The product stays complete and unchanged. Treat each creative scene as an intentional hard cut, not a continuous moment.
5. Inspect all generated review frames. Reject any product duplication, new button/part, changed geometry, malformed hand, unreadable text, or scene/product mismatch.

## Creative quality floor

For a finished 30-second video, vary at least two scene dimensions across generated blocks when the brief permits: setting, time/light, story context, camera language, visual hook, or ending composition. A clean static hero remains useful as proof, but must not occupy the whole video by default.

Build creative blocks around a **real, simple human moment**, not a sequence of product poses. Strong blocks normally establish a recognisable setting or actor goal first, then let the product enter as a believable prop. Suitable story engines include leaving home, a short road trip stop, preparing a gift, a desk-break moment, a shared adult reaction, or a home task. The specific setting and goal must fit the product brief; do not copy a prior product's plot, prop, actor, or mechanism.

Use a compact progression such as: lifestyle or story hook → a different context where the product has a natural role → real-action proof insert when required → distinct payoff/hero ending. Across the finished edit, include a deliberate mix of:

- one establishing or reaction-led shot where the environment carries the hook;
- one product-in-context shot with a single low-risk movement;
- one clean close detail/proof shot; and
- one visually different payoff frame, such as gifting, packing, arriving, or a product hero in a new setting.

Do not turn every block into a tabletop hold, a hand waving the item at the camera, or the same room with new adjectives. A scene is materially different only when its human goal, setting, framing, or visual payoff changes. Keep any generated hand interaction short and simple; do not force fragile product operation into creative blocks.

### Creative brief before prompt writing

For every proposed scene block, record these six fields before drafting its generation prompt:

| Field | Decision required |
| --- | --- |
| Human moment | What ordinary adult activity, choice, or reaction makes the scene understandable without product narration? |
| Product role | Is the product a stable prop, a carry item, a reveal, a close proof, or a real-footage insert? |
| One safe movement | One supported movement only: pick up, place, carry, reveal, slight reframe, or atmosphere/camera movement. |
| Visual hook | The concrete first visual: location, light, framing, object relationship, or reaction. |
| Proof | Which visible product trait is verified in this block, if any? |
| Cut role | Does it establish, contrast, prove, or pay off the edit? |

Reject a scene brief that cannot answer all six fields, that relies on a vague "lifestyle" background, or that requires the model to invent product use. Product reference images lock the object; creative directions should expand the world around it.

## Stopping rule

If compositing cannot preserve a believable exact product layer, keep the scene block out of paid video generation. Request a cleaner product cutout or choose a compatible multi-reference route only after verifying its input contract. Do not revert silently to repeated raw-photo animation just because it is safer.
