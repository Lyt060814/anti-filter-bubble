"""Redraw from per-seed CSV files without re-running stochastic simulation."""
from audit import read
from experiments import plot_formation, detection
from escape import plot_escape


def numeric(rows):
    for r in rows:
        for k,v in r.items():
            try:
                r[k] = float(v)
            except ValueError:
                pass
    return rows


if __name__ == '__main__':
    plot_formation(numeric(read('formation')))
    plot_escape(numeric(read('escape')))
    detection()
