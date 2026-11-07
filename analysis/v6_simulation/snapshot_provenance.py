"""Preserve exact small source files across the compact-history rebuild."""
from pathlib import Path
import subprocess,json,hashlib
BASE=Path(__file__).parent


def run():
    for folder in ('figures','results'):
        for name in ('formation_calibrated','escape_calibrated','persistence_calibrated'):
            path=BASE/folder/f'{name}.meta.json';m=json.loads(path.read_text())
            commit=m['simulation_code_commit'];snapshot=BASE/'provenance'/commit[:8]
            snapshot.mkdir(parents=True,exist_ok=True)
            pointers={}
            for source,expected in m['simulation_source_sha256'].items():
                text=subprocess.check_output(['git','show',f'{commit}:analysis/v6_simulation/{source}'],encoding='utf8')
                assert hashlib.sha256(text.encode()).hexdigest()==expected
                output=snapshot/source;output.write_text(text,encoding='utf8')
                pointers[source]=str(output.relative_to(BASE)).replace('\\','/')
            m['numerical_source_snapshot']=pointers
            path.write_text(json.dumps(m,indent=2),encoding='utf8')


if __name__=='__main__':run()
