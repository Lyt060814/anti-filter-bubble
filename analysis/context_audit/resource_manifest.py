"""Inventory locally acquired research materials, without copying the materials.

python3 analysis/context_audit/resource_manifest.py /absolute/resource/root
Checks each downloaded Zenodo file against its publisher-provided MD5.
PDF signatures and hashes establish file identity, not reading or reproduction.
"""
import argparse
import hashlib
import importlib.metadata
import json
import platform
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path


EXTRA_PAPER_SOURCES = {
    "amnesty": "https://www.amnesty.org.uk/knowledge-hub/all-resources/report-driven-into-darkness/",
    "bep": "https://arxiv.org/abs/2512.03067",
    "brady2026": "https://williamjbrady.com/research",
    "cirs": "https://arxiv.org/abs/2204.01266",
    "cnnic56": "https://www.cnnic.net/NMediaFile/2025/0730/MAIN1753846666507QEK67ZS9DH.pdf",
    "deepbubble": "https://arxiv.org/abs/2403.04511",
    "dorl": "https://arxiv.org/abs/2307.04571",
    "drift2026": "https://arxiv.org/abs/2603.20723",
    "haroon_slides": "https://bpb-us-e2.wpmucdn.com/faculty.sites.uci.edu/dist/8/913/files/2023/01/symposium22-Muhammad-Haroon-YouTube.pdf",
    "hartmann2025": "https://doi.org/10.1007/s42001-025-00381-z",
    "kaplan": "https://arxiv.org/abs/2605.10690",
    "kuairand": "https://arxiv.org/abs/2208.08696",
    "kuairec": "https://arxiv.org/abs/2202.10842",
    "molly_coroner": "https://www.judiciary.uk/prevention-of-future-death-reports/molly-russell-prevention-of-future-deaths-report/",
    "orchid_acl": "https://aclanthology.org/2023.emnlp-main.582/",
    "shortvideo": "https://arxiv.org/abs/2502.05922",
    # Successful replacement locations for earlier failed publisher downloads.
    "leysen": "https://adrem.uantwerpen.be/bibrem/pubs/bubbles.pdf",
    "draws2023": "https://pure.tudelft.nl/ws/portalfiles/portal/150434223/978_3_031_28244_7_18.pdf",
}


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def identity(path, root, md5=False):
    sha = hashlib.sha256()
    checksum = hashlib.md5() if md5 else None
    with path.open("rb") as f:
        while chunk := f.read(4 * 1024 * 1024):
            sha.update(chunk)
            if checksum is not None:
                checksum.update(chunk)
    result = {"path": str(path.relative_to(root)), "bytes": path.stat().st_size,
              "sha256": sha.hexdigest()}
    if checksum is not None:
        result["md5"] = checksum.hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("resource_root", type=Path)
    args = parser.parse_args()
    root = args.resource_root.resolve()
    repo = Path(__file__).resolve().parents[2]
    result = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "resource_root": str(root), "project_baseline_commit": git(repo, "rev-parse", "HEAD"),
        "scope": "Acquisition identity and selected resource probes; consult plan_source_review.md for reading scope and access gaps.",
        "runtime": {"python": platform.python_version(),
                    **{name: importlib.metadata.version(name) for name in ["numpy", "pandas"]}},
        "code": [], "papers": [], "zenodo": [], "shortvideo": [], "web": [], "probes": {},
    }
    for folder in sorted((root / "code").iterdir()):
        if (folder / ".git").exists():
            result["code"].append({"path": str(folder.relative_to(root)),
                "remote": git(folder, "remote", "get-url", "origin"),
                "commit": git(folder, "rev-parse", "HEAD"),
                "commit_date": git(folder, "show", "-s", "--format=%cI", "HEAD"),
                "working_tree_dirty": bool(git(folder, "status", "--porcelain"))})
    attempts = {}
    for manifest in sorted((root / "papers").glob("download_manifest*.json")):
        for row in json.loads(manifest.read_text()):
            attempts.setdefault(row[0], []).append({"status_at_attempt": row[1], "url": row[-1]})
    for p in sorted((root / "papers").glob("*.pdf")):
        entry = identity(p, root)
        with p.open("rb") as f:
            entry["pdf_signature"] = f.read(5) == b"%PDF-"
        entry["download_attempts"] = attempts.get(p.stem, [])
        if p.stem in EXTRA_PAPER_SOURCES:
            entry["source_or_author_entry"] = EXTRA_PAPER_SOURCES[p.stem]
        entry["text_extracted"] = p.with_suffix(".txt").exists()
        result["papers"].append(entry)
    for manifest in sorted((root / "data").glob("zenodo-*.json")):
        record = json.loads(manifest.read_text())
        for f in record["files"]:
            p = root / "data" / f["key"]
            entry = {"record": str(record["id"]), "filename": f["key"],
                     "url": f["links"]["self"], "expected_bytes": f["size"],
                     "expected_checksum": f["checksum"],
                     "license_in_record": record["metadata"].get("license"),
                     "downloaded": p.exists()}
            if p.exists():
                entry.update(identity(p, root, md5=True))
                entry["checksum_matches"] = "md5:" + entry["md5"] == f["checksum"]
                if not entry["checksum_matches"] or entry["bytes"] != f["size"]:
                    raise ValueError(f"Official checksum/size mismatch: {p}")
            result["zenodo"].append(entry)
    for p in sorted((root / "data/shortvideo").rglob("*")):
        if p.is_file():
            result["shortvideo"].append(identity(p, root))
    result["shortvideo_source"] = "https://github.com/tsinghua-fib-lab/ShortVideo_dataset"
    for p in sorted((root / "web").glob("*")):
        if p.is_file():
            entry = identity(p, root)
            if p.suffix == ".xml":
                article = ET.parse(p).getroot()
                entry["article_identifiers"] = {
                    el.attrib.get("pub-id-type", "unknown"): el.text
                    for el in article.findall("./front/article-meta/article-id")
                }
            result["web"].append(entry)
    result["web_source_manifests"] = {
        p.name: json.loads(p.read_text()) for p in (root / "web").glob("*manifest.json")
    }
    for relative in ["data/KuaiRand-1K/probe.json", "data/audit/kuairec_probe.json",
                     "data/audit/kuairand_metadata_probe.json", "data/stance_resource_probe.json",
                     "data/shortvideo/probe.json"]:
        p = root / relative
        if p.exists():
            result["probes"][relative] = json.loads(p.read_text())
    target = repo / "docs/context-recovery/resource_manifest.json"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"output": str(target), "code_repositories": len(result["code"]),
                      "pdf_files": len(result["papers"]),
                      "valid_pdf_signatures": sum(p["pdf_signature"] for p in result["papers"]),
                      "verified_zenodo_files": sum(p.get("checksum_matches", False) for p in result["zenodo"]),
                      "probes": list(result["probes"])}, indent=2))


if __name__ == "__main__":
    main()
