# Action and prompt mapping

Make this mapping before generating a storyboard or submission prompt. It prevents a prompt from asking the model to chain unsupported actions or silently rely on an untraceable image.

## One action per generated clip

Split a sequence such as “rotate, open, insert card, close” into separate beats. Each generated beat has one verb and a visible, stable end state. If the clip needs close alignment, hidden geometry, contact, or several hand movements, provide role-labelled start/contact/end references, make a short linked generated clip, and revise the beat if it cannot pass.

| Beat ID | Start state asset | One permitted action | End state asset | Decision |
| --- | --- | --- | --- | --- |
| B01 | `...__compartment-closed...` | Rotate only | `...__side-view...` | Generate only if both states match |
| B02 | `...__compartment-open...` | Insert card only | `...__card-inserted...` | All-reference; otherwise split, regenerate, or rewrite |

## Prompt asset mapping

Attach this record to every prompt:

| Prompt/beat ID | Identity lock | Detail lock | Start asset | End asset | Upload order | Acceptance check |
| --- | --- | --- | --- | --- | --- |
| B02 | exact SKU/variant | card slot | `...open...` | `...inserted...` | 1 identity, 2 start, 3 detail, 4 end | no new parts; card remains in the shown slot |

The prompt must name the assets by their upload labels and may request only the mapped action. If a needed asset is absent, set the decision to `ask_for_asset` or `omit`; never leave the field blank.

## Supported fallback beats

When a requested action is omitted, choose only a beat supported by accepted material: stable hero reveal, true-colour angle change, macro detail proof, packaging/text view, an outcome already visible in supplied evidence, or a human reaction with the product unchanged. Record the replacement and its reason; a fallback cannot imply the omitted mechanism or result.
