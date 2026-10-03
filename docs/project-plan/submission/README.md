# 正式 Project Plan 草稿（中英文）

按 2026/27 COMP1110 的 Project Plan Guidelines 与 Group Project Guidelines 编写，以内部 v3 为依据。中英文 PDF 均为 4 页（含参考文献），已发组员 review，尚未向课程平台提交。后续按组员反馈修订；目前不开展新的方案扩写。

| 语言 | PDF | 可编辑 Word | Markdown 源稿 |
|---|---|---|---|
| English | [PDF](Project_Plan_EN.pdf) | [Word](Project_Plan_EN.docx) | [源稿](project_plan_en.md) |
| 中文 | [PDF](Project_Plan_ZH.pdf) | [Word](Project_Plan_ZH.docx) | [源稿](project_plan_zh.md) |

正文包含问题与方案、computing/data science 方法、10 项相关来源及研究切入点、可行性与伦理、时间表与五人分工。首页已填写五位成员姓名与学号，时间表和职责表均已落实到姓名。日期依据课程文件，最终以 Moodle 为准。

正文引用编号可跳转至文末条目，文献标题及 DOI 可打开原始来源；PDF 带章节书签，Word 保留对应的内部链接和外部链接。引用按首次出现顺序编号，两版一致。

PDF 是已检查的固定排版版本；Word 用于编辑，在不同软件中分页可能变化。两种格式由同一 Markdown 源稿生成。更新正文后可重新生成：

```bash
uv run --with python-docx --with weasyprint --with matplotlib python docs/project-plan/submission/build_submission.py
```

脚本另需系统安装 pandoc、Liberation Serif 与 Droid Sans Fallback 字体。

## 修改与同步

以两份 Markdown 为正文源文件，同步修改中英文后运行构建命令，再检查两版 PDF 的页数、表格、引用跳转与排版。PDF / Word 是需一并提交的生成产物。已手动粘贴到 Google Docs 的副本不会自动同步，更新后需另行复制。

2026-10-04 组员反馈修订：第二部分以有限观察下的序列决策定义系统和长期目标，分别展开数据分析、算法设计与仿真建模。保留熵／JS 的用途与解释边界，明确策略选择步骤、独立评价和模型敏感性。PDF 公式统一使用 STIX 数学字体和矢量渲染，行内熵公式采用右下角求和下标并按基线对齐，Word 保留原生可编辑公式；三层形式化表达与熵／JS 测量公式采用紧凑排版。Google Docs 副本需另行同步。
