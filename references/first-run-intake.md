# First interaction

Inspect the conversation and provided files before asking. Greet briefly, state the workflow in plain language, then ask only for missing inputs in one compact message.

## Opening pattern

Use this structure, adapting the wording to the user:

> 你好，我可以把商品素材整理成与你需求匹配的即梦剧情方案；可以做用户指定脚本、指定数量的变体，或连续高密度剧情。生成前会审核并由你确认。
>
> 请先发我：① 商品图或视频与商品名称；② 玩法/使用方式；③ **已确认卖点，以及必须重点展示和保留的核心功能**；④ 目标市场与语言；⑤ 禁用内容和其他要求（例如人物、场景、风格、时长、CTA）。如果暂时没有禁用要求，我会按平台安全与不夸大原则处理。

Do not claim API generation will happen until the user explicitly approves a reviewed package.
After the user supplies or accepts the missing inputs, follow the stated deliverable: preserve a detailed supplied script as the base package; create the requested number of variants; use the 20-package / 60-prompt matrix only when variants are requested with no count; and use one validation package for a requested high-density continuous story.

## Inputs to collect

| Input | Ask for when missing | Examples of acceptable material |
| --- | --- | --- |
| Product | Name and clear identity asset | Main image, detail photos, raw video, product page. |
| Play/use | How it is used, played with, or demonstrated | A short description or a real demonstration clip. |
| Verified features | Always ask separately unless explicitly supplied; do not infer marketing priorities from video | Confirmed selling points, must-show/retain core functions, dimensions, included parts, allowed claims. |
| Buyer and market | Adult buyer, destination market, language | US English TikTok Shop, etc. |
| Extra requirements | Creative and delivery choices | People, setting, plot tone, do-not-use items, CTA, captions, music, duration. |

If the user supplies only video, extract visible facts, then explicitly ask which selling points and core functions must be highlighted and preserved, plus restrictions and market. If a fact is unknown, omit it rather than invent it.
