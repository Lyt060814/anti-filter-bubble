#!/usr/bin/env bash
# Download the data used by analysis/data_check (about 2.5 GB on disk after filtering).
# KuaiRec / KuaiRand-1K themselves: see docs/resources/datasets.md (Zenodo 18164998, 10439422).
set -euo pipefail
DATA=${DATA:-/home/user/data}

# 1) ShortVideo (Shang et al., WWW'25 Companion). The public sampled version is behind HTTP basic auth;
#    the username/password are printed in https://github.com/tsinghua-fib-lab/ShortVideo_dataset README.
: "${SV_USER:?set SV_USER/SV_PASS from the dataset README}"
mkdir -p "$DATA/shortvideo"
for f in README.md categories_cn_en.csv interaction_sampled.csv; do
  curl -sS -u "$SV_USER:$SV_PASS" -o "$DATA/shortvideo/$f" "https://fi.ee.tsinghua.edu.cn/datasets/short-video-dataset/$f"
done
# ASR text per video (153k files) lives under .../asr_zn/<pid>.txt; raw mp4 under .../raw_file/ (~3.6 MB each). Not needed yet.

# 2) KuaiRand supplementary captions + categories (Gao, Zenodo 18159199, CC BY 4.0), ~7 GB each raw;
#    stream and keep only videos that appear in the KuaiRand-1K logs.
mkdir -p "$DATA/kuairand/supp"
python3 - <<'PY'
import pandas as pd, os
d = os.environ.get('DATA', '/home/user/data') + '/kuairand/KuaiRand-1K/data/'
ids = set()
for f in ['log_standard_4_08_to_4_21_1k.csv', 'log_standard_4_22_to_5_08_1k.csv', 'log_random_4_22_to_5_08_1k.csv']:
    ids |= set(pd.read_csv(d + f, usecols=['video_id']).video_id)
pd.DataFrame({'video_id': sorted(ids)}).to_csv('/tmp/kr1k_vids.csv', index=False)
PY
for f in kuairand_video_categories kuairand_video_captions; do
  curl -sL "https://zenodo.org/records/18159199/files/$f.csv?download=1" | python3 -c "
import sys, pandas as pd
ids = set(pd.read_csv('/tmp/kr1k_vids.csv').video_id); first = True
for c in pd.read_csv(sys.stdin, chunksize=500000, dtype=str, keep_default_na=False):
    c[c.final_video_id.astype(int).isin(ids)].to_csv(sys.stdout, header=first, index=False); first = False
" > "$DATA/kuairand/supp/${f/kuairand_/kuairand_1k_}.csv"
done
