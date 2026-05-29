# 错误记录结构（error schema）

每天的错误存成一个 **JSON 数组**，文件名 `data/errors/YYYY-MM-DD.json`。
数组里每个元素是一条错误，字段如下：

| 字段 | 说明 | 必填 |
|---|---|---|
| `id` | 唯一编号，建议 `日期-序号`，如 `2026-05-29-001` | ✅ |
| `date` | 上课日期 `YYYY-MM-DD` | ✅ |
| `category` | 大类（见下方受控词表） | ✅ |
| `tag` | 细分标签（见下方），方便统计规律 | ✅ |
| `my_sentence` | 你说的原句（可能被语音转写弄错，尽量还原本意） | ✅ |
| `correction` | 老师的正确说法；可给多个，用 ` / ` 隔开 | ✅ |
| `explanation` | 为什么错、规则是什么（默认中文，便于理解） | ✅ |
| `correct_examples` | 1–2 个正确例句，数组 | ✅ |
| `context` | 上下文/当时在聊什么（可选） | ⬜ |
| `review` | 复习状态对象，见下 | ✅ |
| `source_ref` | 在原始转写里的位置，如 `line 412`（可选） | ⬜ |

`review` 对象：
```json
{ "status": "new", "times_seen_again": 0, "last_reviewed": null }
```
- `status`: `new`（新错） / `learning`（在练） / `mastered`（已掌握）
- `times_seen_again`: 之后又犯了几次（统计顽固错误）
- `last_reviewed`: 上次复习日期或 null

## 受控词表（保持统一，统计才准）

`category`（大类，固定这 6 个）：
- `grammar` 语法
- `vocabulary` 词汇/选词
- `collocation` 搭配
- `naturalness` 不地道/中式表达
- `pronunciation` 发音
- `discourse` 篇章/连贯/口语流利度

`tag`（细分，可扩展，但尽量复用现有的）：
articles（冠词）, tense（时态）, aspect（体）, preposition（介词）,
plural（单复数）, agreement（主谓一致）, word-order（语序）,
adverb（副词用法）, conditional（条件句）, modal（情态动词）,
phrasal-verb（短语动词）, false-friend（伪同义词）, register（语体/正式度）,
filler（口头禅/赘词）, linking（连读弱读）, stress（重音）,
comparative（比较级）, relative-clause（关系/定语从句）, word-choice（选词）,
conciseness（精简/合句，避免逗号粘连）, word-boundary（复合词词界/连读成一个词）, …

> 新增 tag 时记到这里，别造同义词（比如 `prep` 和 `preposition` 不要并存）。
