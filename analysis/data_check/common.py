"""Shared paths for the data-feasibility checks (see README.md)."""
from pathlib import Path

DATA = Path('/home/user/data')
SV_DIR = DATA / 'shortvideo'
SV_RAW = SV_DIR / 'interaction_sampled.csv'          # from fi.ee.tsinghua.edu.cn (sampled version)
SV_CATS = SV_DIR / 'categories_cn_en.csv'
SV_INTER = SV_DIR / 'sv_interactions.parquet'         # one row per (user, video, exposed_time)
SV_VIDEOS = SV_DIR / 'sv_videos.parquet'              # one row per video, with category path
KR_DIR = DATA / 'kuairand' / 'KuaiRand-1K' / 'data'
KR_SUPP = DATA / 'kuairand' / 'supp'                  # Zenodo 18159199, filtered to 1K-logged videos
KREC_DIR = DATA / 'kuairec' / 'KuaiRec 2.0' / 'data'
OUT = Path(__file__).resolve().parent
