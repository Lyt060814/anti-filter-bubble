# External resources

资源现统一放在本仓库的 `sources/`。下载文件保留在本机，普通 clone 不包含数据、权重、全文缓存或 Python 环境。这里的清单与固定版本可用于按需恢复，不代表所有资源已复现。

| 目录 | Git 管理方式 | 恢复方式 |
|---|---|---|
| `code/` | X、KuaiSim 为固定 commit 的 submodule；其他 34 个仓库忽略 | `repos.lock.json` + `restore.py` |
| `data/` | 原始与派生文件忽略；小型检查结果保存在 `docs/context-recovery/` | 官方下载入口、校验记录及现有处理脚本 |
| `envs/` | 忽略，不能直接复制环境给其他机器 | 按依赖清单重建 |
| `models/` | 权重缓存忽略 | 固定模型 ID 与 revision 下载 |
| `papers/` | PDF 和提取文本忽略 | `catalogs/papers/` 下载记录与来源台账 |
| `web/` | 完整网页缓存忽略 | `catalogs/web/` URL 记录，必要时重新获取 |

`inventory.json` 是迁移时的相对路径及文件大小清单，不是完整性校验；已有校验和见[资源清单](../docs/context-recovery/resource_manifest.json)及[v3 记录](../docs/context-recovery/plan_v3_feasibility.md)。`catalogs/` 保存原下载记录，失败尝试不表示该资源已取得。历史记录中的旧绝对路径保留作为运行证据，现在将旧根目录替换为本目录即可定位。

## 代码

在项目根目录运行：

```bash
git submodule update --init -- sources/code/x-algorithm sources/code/KuaiSim
python3 sources/restore.py --list
python3 sources/restore.py Qwen-Agent UCRS
```

不会自动下载全部 36 个仓库。恢复脚本不重置已有代码；版本不符时停止。它跳过 Git LFS 自动下载，如某项实验需要上游 LFS 资产，应在确认所需空间后单独获取。Submodule 不备份上游服务器；必要改动应保存为补丁或推到团队 fork，并同步 submodule 指针与锁定清单。

## 数据与模型

- KuaiRand：[官方记录](https://zenodo.org/records/10439422)，标题／类别：[补充记录](https://zenodo.org/records/18159199)。
- KuaiRec：[官方补充记录](https://zenodo.org/records/18164998)。
- ShortVideo：`code/ShortVideo_dataset` README 中的数据入口；配对媒体获取见 `analysis/context_audit/plan_v3_media_probe.py`。
- KuaiSAR：具体地址、文件校验和及字段检查见 `docs/context-recovery/plan_v3_kuaisar_probe.json` 和对应脚本。
- 模型：`Qwen/Qwen3-Embedding-0.6B`，revision `97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3`。现有 `plan_v3_embedding_probe.py` 按此版本下载到 `sources/models/`，然后执行推理检查。

首次获取应按上述资源分别下载，不能把检查脚本理解为完整数据安装器。处理脚本统一以 `sources` 作为 SOURCE_ROOT 参数，例如：

```bash
python3 analysis/context_audit/probe_resources.py sources
```

部分核查脚本会重写已有结果文件，重复实验前先保存旧记录。旧 `analysis/pilot_*` 和早期分析脚本仍可能引用历史云环境路径；它们不是当前资源安装入口，复现前需适配路径。

团队原创的小型标注可直接进 Git；大型不可重建成果再用 DVC 配合团队存储。尚未配置 DVC、网盘或 LFS，不能认为本地缓存已远程备份。论文与网页是否可再次发布需逐项确认；这里默认仅记录出处和我们自己的分析。

## Python 检查环境

```bash
uv venv --python 3.11 sources/envs/v3-check
uv pip sync --python sources/envs/v3-check/bin/python \
  --index https://download.pytorch.org/whl/cpu \
  --index-strategy unsafe-best-match \
  analysis/context_audit/plan_v3_check_requirements.txt
```

这是 v3 的 CPU 检查环境，不代表各个第三方项目能共用同一组依赖。上述两处索引为 PyTorch 官方 CPU 源和 uv 默认 PyPI；指定跨索引选取以恢复锁定的 CPU torch 版本。其他实验应各自固定依赖。

本次在新位置重建并验证了环境；其余五类目录已迁入本目录。确认旧同级目录只剩已替代的虚拟环境后，已删除整个 `anti-filter-bubble-sources/` 目录。后续统一使用本目录。

## 本次迁移检查

- 415 个数据／模型／论文／网页文件的路径及大小与迁移前一致；同文件系统移动，未改写内容。未重新计算全部大文件哈希。
- 36 个第三方仓库 HEAD 与锁定清单一致，没有迁移源码修改。
- 41 项锁定依赖在新路径安装成功；本地 Qwen 权重完成 CPU 前向推理，输出有限值。
- KuaiSim 原响应网络前向／反向检查通过，历史实验 JSON 未被覆盖。
- 在临时空目录成功按固定 commit 获取 `LLM_User_Simulator`，重复运行不改变已有 checkout。
