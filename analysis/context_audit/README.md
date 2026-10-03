# 接续研究的资源核查

这些脚本核查数据可用性和历史数字的口径，不训练模型、不生成自动立场标签，也不估计按钮的因果效果。

外部资料保存在仓库同级目录：

`/home/yitongli/Courses/26full/COMP1110/anti-filter-bubble-sources/`

输入来源：

- [KuaiRand 官方数据记录](https://zenodo.org/records/10439422)：1K 和 Pure。
- [KuaiRand 标题与预测类别](https://zenodo.org/records/18159199)：完整两份 CSV；按 ID 在核查时过滤到 1K 视频。
- [KuaiRec 官方补充记录](https://zenodo.org/records/18164998)：2.0 压缩包、标题/类别/用户特征。
- [ShortVideo_dataset](https://github.com/tsinghua-fib-lab/ShortVideo_dataset)：公开抽样交互、类目表与抽取的 24 份 ASR；访问方式见作者 README。

先运行：

```bash
python3 analysis/context_audit/probe_resources.py /absolute/path/to/anti-filter-bubble-sources
```

输出在外部目录 `data/audit/`。200 条窗口按用户的标准日志时间排序后不重叠切分，丢弃末尾不足 200 条的窗口；保留全部入口，不冒充单一推荐页。关键词在 caption 和封面文字中匹配；命中只是候选，既可能误收，也可能漏掉不用这些词的相关内容。每类前 12 条例子是定性检查，不是随机人工金标准。原始标题可能含个人账号标识，样例不复制进本仓库。

随后生成资料身份和校验清单：

```bash
python3 analysis/context_audit/resource_manifest.py /absolute/path/to/anti-filter-bubble-sources
```

该脚本记录克隆版本、文件 SHA-256、已下载 Zenodo 文件的官方 MD5 核验和核查结果；输出 `docs/context-recovery/resource_manifest.json`。其中下载尝试的旧状态仅为获取过程记录，当前文件是否存在和 PDF 签名另列。文件存在、标题命中、读过论文与复现论文结果是不同状态。

为 [execution plan v2](../../docs/project-plan/execution_plan_v2.md) 固定有限输入：

```bash
python3 analysis/context_audit/plan_v2_preflight.py /absolute/path/to/anti-filter-bubble-sources
```

脚本只使用已有 KuaiRand-1K 和完整标题 CSV。它在 1K 视频池中检索“彩礼”，以 seed=1110 从按 ID 排序的候选中均匀无放回抽取 200 条（40 pilot、160 audit）；另外在标准日志 `tab=1` 中选择有前 200／后 100 条曝光的 hate 事件，按时间每人最多 5 个、位置相差 >300，避免选中事件的完整窗口重叠。其他负反馈只打标，不按后续效果筛选。

原始文本和匿名事件表写入外部 `data/audit/plan_v2/`；小型汇总及文件 SHA-256 写入 [plan_v2_preflight.json](../../docs/context-recovery/plan_v2_preflight.json)。实测为 2,729 个候选、200 条样本、524 个事件／205 人，约 73 秒、峰值 RSS 728 MiB。该步骤没有人工标签，也没有估计按钮效果；重跑会按固定规则重建这三份输入文件，不应把人工标注直接写进生成文件。

研究解释见[第一性原理复核](../../docs/project-plan/first_principles_review.md)；阅读覆盖和无法取得的资料见[来源台账](../../docs/context-recovery/plan_source_review.md)。本机 Python、NumPy、pandas 版本随清单保存。


## v3 资源与运行检查

[可行性记录](../../docs/context-recovery/plan_v3_feasibility.md)汇总本轮实测；`plan_v3_acquire.py` 获取官方快照与论文，`plan_v3_media_probe.py` 获取配对媒体并解码，`plan_v3_kuaisar_probe.py` 校验压缩包及表头／前缀。`plan_v3_embedding_probe.py` 在隔离环境运行固定 Qwen3 嵌入权重；`plan_v3_kuaisim_probe.py` 运行未训练的原响应网络并检查概率合同。这些是入口和数值检查，不是准确率、模拟器真实性或干预效果实验。

模型检查环境依赖见 `plan_v3_check_requirements.txt`；PyTorch 使用 CPU wheel。模型脚本默认固定本轮权重 revision，可显式改变 `--revision` 并产生新记录。获取脚本现在包含本轮补充来源，首次失败的猜测仓库地址保留在历史 JSON 中，但不再重复尝试；新运行会重新生成清单，归档旧记录后再用于新实验。
