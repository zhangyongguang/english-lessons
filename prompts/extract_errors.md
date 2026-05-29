# 提示词：从转写里提取错题（每天用）

把这段提示词 + 当天的 `data/raw/YYYY-MM-DD.txt` 一起发给 Claude。

---

你是我的英语口语老师助理。下面是 1v1 英语课的腾讯会议语音转写（中英混杂，且**转写本身可能有识别错误**，尤其是我说的英文）。

说话人标注：`Jack` 是学生（也就是我本人），`ZIVA_Teacher` 是老师。一天可能有多段录音（多个 session），请合并处理。文件名里 `_20260528210658-` 这串数字是「年月日时分秒」，前 8 位就是上课日期。

请帮我提取「我（Jack）犯的错误 + 老师（ZIVA_Teacher）的纠正」，输出一个 **JSON 数组**，每条严格符合这个结构：

```json
{
  "id": "日期-三位序号，如 2026-05-29-001",
  "date": "YYYY-MM-DD",
  "category": "grammar | vocabulary | collocation | naturalness | pronunciation | discourse 中的一个",
  "tag": "细分标签，如 articles / tense / preposition / adverb 等",
  "my_sentence": "我说的原句（若转写明显出错，请按上下文还原我本来想说的）",
  "correction": "老师给的正确说法，多个用 ' / ' 隔开",
  "explanation": "用中文解释为什么错、规则是什么",
  "correct_examples": ["正确例句1", "正确例句2"],
  "context": "当时在聊什么（简短）",
  "review": { "status": "new", "times_seen_again": 0, "last_reviewed": null },
  "source_ref": "在转写里的大致位置，如 'line 88'，没有就留空字符串"
}
```

要求：
1. 只提取**真实的语言错误**和明确的纠正，别把正常对话也当成错误。
2. **聚焦句子层面的表达**（结构、搭配、语序、时态/一致、地道说法），不要为单个生词/词汇单独立条；孤立的选词问题我会自己查。
3. `Jack` 的发言里有的是口误/识别错误，有的是真实语言错误；结合老师是否纠正来判断。
4. 老师没明说但你能确定更地道的说法，也可以补，但 `explanation` 里标注「（assistant note）」。
5. category 和 tag 用受控词表（见 templates/error_schema.md），别造同义标签。
6. 直接输出 JSON 数组，**不要**任何前后说明文字、不要 Markdown 代码块包裹。

> `explanation` 和 `correct_examples` 用**英文**。`my_sentence` / `correction` 保留英文原句。
> 渲染出来的 `日期.md` 只会显示「错误 / 正确」两列（脚本负责），所以 JSON 里其它字段照常填全，喂统计和 Anki 用。
