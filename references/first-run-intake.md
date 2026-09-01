# First interaction

Inspect the conversation and provided files before asking. Greet briefly, state the workflow in plain language, then ask only for missing inputs in one compact message.

## Opening pattern

Use this structure, adapting the wording to the user:

> 你好，我会先把商品素材整理好并完成一条验证成片；验证通过后，会自动扩展为 20 个完整的 30 秒创意方案，每个方案拆成适合即梦的镜头提示词。新一批 API 生成仍会在提交前请你确认。
>
> 请先发我：① 商品图或视频与商品名称；② 玩法/使用方式；③ **已确认卖点，以及必须重点展示和保留的核心功能**；④ 目标市场与语言；⑤ 这次更偏向“产品展示”还是“宣传/情节型视频”；⑥ 禁用内容和其他要求（例如人物、场景、风格、时长、CTA）。如果暂时没有禁用要求，我会按平台安全与不夸大原则处理。

Do not claim API generation will happen until the user explicitly approves a reviewed package.
After the user supplies or accepts the missing inputs, first complete one validation final. After it passes final visual QA, generate the default 20-package / 60-prompt matrix without asking whether they want the matrix. If that validation fails, correct it before expanding. Only reduce the count when the user explicitly asks for a trial or a smaller batch.

## Inputs to collect

| Input | Ask for when missing | Examples of acceptable material |
| --- | --- | --- |
| Product | Name and clear identity asset | Main image, detail photos, raw video, product page. |
| Play/use | How it is used, played with, or demonstrated | A short description or a real demonstration clip. |
| Verified features | Always ask separately unless explicitly supplied; do not infer marketing priorities from video | Confirmed selling points, must-show/retain core functions, dimensions, included parts, allowed claims. |
| Buyer and market | Adult buyer, destination market, language | US English TikTok Shop, etc. |
| Content intent | Ask when the user has not already supplied a script, storyboard, or clear creative direction | `产品展示` prioritizes product proof and visual detail; `宣传/情节型` prioritizes a creative hook, human moment, and persuasive story. The user may also choose a mixed route. |
| Extra requirements | Creative and delivery choices | People, setting, plot tone, do-not-use items, CTA, captions, music, duration. |

If the user supplies only video, extract visible facts, then explicitly ask which selling points and core functions must be highlighted and preserved, plus restrictions and market. If a fact is unknown, omit it rather than invent it.
