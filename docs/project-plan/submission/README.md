# 正式 Project Plan 草稿（中英文）

按 2026/27 COMP1110 的 Project Plan Guidelines 与 Group Project Guidelines 编写，以内部 v3 为依据。中英文 PDF 均为 4 页（含参考文献），已发组员 review，尚未向课程平台提交。后续按组员反馈修订；目前不开展新的方案扩写。

| 语言 | PDF | 可编辑 Word | Markdown 源稿 |
|---|---|---|---|
| English | [PDF](Project_Plan_EN.pdf) | [Word](Project_Plan_EN.docx) | [源稿](project_plan_en.md) |
| 中文 | [PDF](Project_Plan_ZH.pdf) | [Word](Project_Plan_ZH.docx) | [源稿](project_plan_zh.md) |

正文包含问题与方案、computing/data science 方法、12 项相关来源及研究切入点、可行性与伦理、时间表与五人分工。首页已填写五位成员姓名与学号，时间表和职责表均已落实到姓名。日期依据课程文件，最终以 Moodle 为准。

正文引用编号可跳转至文末条目，文献标题链接原始来源，KuaiRand 条目另附标题／类别补充文件入口；PDF 带章节书签，Word 保留对应的内部链接和外部链接。引用按首次出现顺序编号，两版一致。

PDF 是已检查的固定排版版本；Word 用于编辑，在不同软件中分页可能变化。两种格式由同一 Markdown 源稿生成。更新正文后可重新生成：

```bash
uv run --with python-docx --with weasyprint --with matplotlib python docs/project-plan/submission/build_submission.py
```

脚本另需系统安装 pandoc、Liberation Serif 与 Droid Sans Fallback 字体。

## 修改与同步

以两份 Markdown 为正文源文件，同步修改中英文后运行构建命令，再检查两版 PDF 的页数、表格、引用跳转与排版。PDF / Word 是需一并提交的生成产物。已手动粘贴到 Google Docs 的副本不会自动同步，更新后需另行复制。

2026-10-04 组员反馈修订：第二部分以有限观察下的序列决策定义系统和长期目标，分别展开数据分析、算法设计与仿真建模。保留熵／JS 的用途与解释边界，明确策略选择步骤、独立评价和模型敏感性。PDF 公式统一使用 STIX 数学字体和矢量渲染，行内熵公式采用右下角求和下标并按基线对齐，Word 保留原生可编辑公式；三层形式化表达与熵／JS 测量公式采用紧凑排版。Google Docs 副本需另行同步。

同日后续反馈修订：补入 Kaplan 与 Compass，说明已有控制研究和本项目综合评价的关系；更新 Milli 的期刊引用与 Pecher 的会议 DOI。第一部分补充如何发现遗漏的理由，第二部分明确多模态对照及信息保留的评价目的，第四部分按实际取得的资源和运行记录重写可行性，区分入口可用与模型已验证。第五部分从剩余工作开始排期，补入独立试标责任人，并要求 19 日前备好中期材料。表格去掉默认段落空白、调整列宽，时间表整体分页；正文字体及公式保持原有设置。两版 PDF 仍为四页，前两部分保持问题与技术方法的重点。

随后小幅补充：第二部分说明内容相关性、反馈更新、探索和记忆衰减如何进入推荐器，并比较透明机制与训练模型；用户模型评价同时检查策略排序是否改变。第四部分明确 ShortVideo 抽样轨迹与 KuaiRand 有限随机池的边界。
