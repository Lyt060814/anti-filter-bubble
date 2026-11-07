# 10 Declaration of Generative AI Use

<!-- Draft by Li Yitong (with Claude Code), 2026-11-07, compiled from report/ai_use_log.md, which keeps the full record. Fu Yitong and Wang Junbo: please confirm the last paragraph. -->

We used generative AI in two different roles, and declare them separately.

**As research instruments.** Language models labelled video descriptions; this is part of our method, described in Sections 4.2–4.3, and their outputs are data, not text in this report. DeepSeek V4 Pro (official API) was the reference labeller; DeepSeek V4 Flash screened candidates for the stratified sample; Qwen3-30B-A3B-Instruct-2507 (run locally with vLLM) was the open model whose labels we checked; GPT-6.1 Sol checked DeepSeek on 150 videos. The exact labelling prompts are given in Appendix A. OneRec-1.7B is the recommender we studied (Section 5.1), not a writing aid.

**As writing and coding assistants.** The table lists the tools, who used them and which parts of the report contain their output. In every case the assistant wrote and ran analysis code, and drafted English text from our plans, results and review comments; all numbers come from running the code, and each draft was reviewed by the member responsible and, through pull-request review, by Li Yitong.

| Tool and model | Used by | Report parts containing its output |
|---|---|---|
| Claude Code (Claude Opus 5.5) | Li Yitong | Sections 1, 3, 4.1, 4.4, 5.1, 7, 8, 10; analysis scripts for Sections 4–5; task descriptions for the group |
| Claude Code (Claude Opus 5.5) | Zhao Dingcheng | Sections 2, 4.2–4.3, 6, 9; Appendix A; Tables 4.1–4.3; Figure 6.1; labelling prompts v1–v2 |
| Codex (GPT-6) | Xu Ruicong | Sections 5.2–5.3; Appendix B; simulation and detection figures |

**Exact prompts.** Each assistant worked in a long session. We give verbatim the prompts that produced content in the report (original Chinese, with an English translation in brackets).

- *Li Yitong, Claude Code.* Research design and Sections 1, 3 and 7 (first drafts): "我觉得可以，就以性别婚恋作为case study。……下一步就开始实际干活了，我的两个队员分别是dingcheng和ruicong。开始吧" [OK, let's take gender and marriage as the case study … the next step is the actual work; my two teammates are Dingcheng and Ruicong. Start.] Sections 4.4 and 5.1, revisions to Sections 1 and 7, and Sections 8 and 10: "看一下进度，推进一下" [Check the progress and push it forward.] The work itself follows the task description `docs/tasks/li_yitong.md` in our repository.
- *Zhao Dingcheng, Claude Code.* A starting prompt asked the assistant to read the project instructions and carry out tasks D1–D6 on separate branches, under the rules that no human annotation is used, every figure keeps its data, and only verified references are cited (full text in the repository's AI-use log). Follow-up prompts, each producing the named part: "开始 D3" [Start D3] (agreement analysis); "开始 D4" (Section 4.2–4.3 and Table 4.1); "开始 D5" (Section 2); "开始 D6" (Section 6 and Figure 6.1); "有一个issue assign给我了 你检查一下" and "开始做" [An issue was assigned to me, check it; start] (prompt v2); "先做附录 A" [Do Appendix A first]; "你看一下新提的issue是什么问题 你什么计划" and "开始做" [Look at the new issue and tell me your plan; start] (revised Table 4.1); "检查一下现在情况" and "先做 #10" [Check the current state; do #10 first] (Table 4.3); "按照仓库中的计划检查一下当前进展" and "先压缩第 6 节" [Check progress against the plan; shorten Section 6 first]; "做 #20 参考文献" [Do #20, the references].
- *Xu Ruicong, Codex.* A starting prompt asked the assistant to implement and check the transparent model and tasks R1–R5, treating every parameter as a scenario assumption to be swept, keeping per-seed results, and labelling assumptions in figures (full text in the AI-use log). Follow-up prompts: "继续给我完成之前的任务" [Continue and finish the earlier tasks], used for each revision after review; and "你重新把前面几个提一下pr / 这是一个三个人的合作项目，所以你要不定期看一下groupmate的进展和comment" [Re-submit the earlier work as pull requests; this is a three-person project, so check teammates' progress and comments from time to time].

The starting prompts for Zhao Dingcheng's and Xu Ruicong's assistants were themselves drafted by Li Yitong's assistant from the task descriptions. Fu Yitong's and Wang Junbo's contributions (Section 8) were made in October, before this report was written, and no AI-generated content from that work appears in the report.
