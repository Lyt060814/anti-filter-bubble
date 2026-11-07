"""Create the reviewed compact public package; preserve full output locally.

Full seed endpoints and all summaries are retained. Intermediate raw formation
is retained only for the five plotted group-family curves, and escape only for
the two plotted group-family curves. Existing snapshot cadence is 100, not 50;
the review permits selecting only plotted cases. Deterministic gzip uses mtime=0.
"""
from pathlib import Path
import csv,gzip,json,hashlib,shutil,subprocess
BASE=Path(__file__).parent.resolve()


def run():
    destination=(BASE.parents[2]/'simulation_full_runs'/'calibrated_v1').resolve()
    assert destination.is_relative_to(BASE.parents[2])
    destination.mkdir(parents=True,exist_ok=True)
    results=BASE/'results'
    prior_manifest=results/'packaging_manifest.json'
    manifest=json.loads(prior_manifest.read_text()).get('files',[]) if prior_manifest.exists() else []
    sources=list(results.glob('calibrated_*.csv'))
    if (results/'formation_bounded.csv').exists():sources.append(results/'formation_bounded.csv')
    for source in sorted(sources):
        assert source.resolve().parent==results
        archived=destination/source.name
        # Never overwrite an earlier full archive with an already compact copy.
        if not archived.exists():shutil.copy2(source,archived)
        else:assert hashlib.sha256(source.read_bytes()).hexdigest()==hashlib.sha256(archived.read_bytes()).hexdigest(), 'Use a new local archive folder for changed full data.'
        out=source.with_suffix('.csv.gz')
        count=0
        with source.open(newline='') as fin, out.open('wb') as raw:
            reader=csv.DictReader(fin)
            with gzip.GzipFile(fileobj=raw,mode='wb',mtime=0,compresslevel=9) as zipped:
                import io
                text=io.TextIOWrapper(zipped,encoding='utf8',newline='')
                writer=csv.DictWriter(text,fieldnames=reader.fieldnames);writer.writeheader()
                for r in reader:
                    keep=True
                    if source.name in ('calibrated_formation_group.csv','calibrated_formation_conflict.csv'):
                        plotted=(r['family']=='group' and r['scan']=='main_grid' and float(r['supply'])==.02 and float(r['prior'])==.15 and
                                 (float(r['ratio']) in (0,.15,.59,1) or int(r['case'])==27))
                        keep=int(r['step']) in (0,6000) or plotted
                    elif source.name.startswith(('calibrated_escape_group_s','calibrated_escape_conflict_s')):
                        plotted=int(r['case']) in (21,27)
                        keep=int(r['step']) in (0,1000,1001,3000) or plotted
                    if keep:writer.writerow(r);count+=1
                text.flush();text.detach()
        manifest=[r for r in manifest if r['file']!=out.name]
        manifest.append(dict(file=out.name,rows=count,compression='gzip level 9, deterministic mtime=0',
                         bytes=out.stat().st_size,sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
                         full_source_sha256=hashlib.sha256(archived.read_bytes()).hexdigest()))
        source.unlink() # only this task's generated file; full source is archived first
    data=dict(evidence_type='lossless gzip plus documented intermediate-trace selection; all endpoints and summaries retained',
              git_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
              script='analysis/v6_simulation/package_results.py',
              snapshot_interval=100,formation_plotted_cases=[14,16,21,26,27],escape_plotted_cases=[21,27],
              retained_formation_steps='0,6000 for every seed; every100 in plotted cases',
              retained_escape_steps='0,1000,1001,3000 for every seed; every100 in plotted cases',
              full_data='local sibling directory simulation_full_runs/calibrated_v1, excluded from repository; reproduce calibrated_run.py',files=manifest)
    (results/'packaging_manifest.json').write_text(json.dumps(data,indent=2),encoding='utf8')
    for folder in ('results','figures'):
        for name in ('formation_calibrated','escape_calibrated','persistence_calibrated','formation_bounded'):
            p=BASE/folder/f'{name}.meta.json'
            meta=json.loads(p.read_text());meta['storage']=data
            p.write_text(json.dumps(meta,indent=2),encoding='utf8')
    size=sum(p.stat().st_size for p in BASE.rglob('*') if p.is_file())
    print(f'Compact analysis directory: {size/1e6:.2f} MB; full source retained locally.')
    assert size<60_000_000, size


if __name__=='__main__':run()
