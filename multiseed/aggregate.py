#!/usr/bin/env python3
"""Aggregate LPSFed multi-seed ML-1M results (full-user eval).

Parses each ~/LPSFed/multiseed/seed<S>.log for the final-results block:
  Client i - Test: F1=..., Recall=..., NDCG=...
Reports per-client and macro-average mean +/- std of Recall@20 and NDCG@20
across seeds.
"""
import re, glob, os, statistics as st

logdir = os.path.expanduser('~/LPSFed/multiseed')
pat = re.compile(r'Client (\d+) - Test: F1=([\d.]+), Recall=([\d.]+), NDCG=([\d.]+)')

per_seed = {}  # seed -> {client: (recall, ndcg)}
for f in sorted(glob.glob(os.path.join(logdir, 'seed*.log'))):
    seed = re.search(r'seed(\d+)\.log', f).group(1)
    txt = open(f).read()
    if '=== Final Results ===' not in txt:
        continue
    tail = txt.split('=== Final Results ===')[-1]
    cl = {}
    for m in pat.finditer(tail):
        c = int(m.group(1)); cl[c] = (float(m.group(3)), float(m.group(4)))
    if cl:
        per_seed[seed] = cl

if not per_seed:
    print('No completed seeds yet.'); raise SystemExit

seeds = sorted(per_seed, key=int)
clients = sorted({c for d in per_seed.values() for c in d})
print(f'Completed seeds: {", ".join(seeds)}  (n={len(seeds)})\n')

def ms(xs):
    return (st.mean(xs), st.pstdev(xs) if len(xs) > 1 else 0.0)

# macro-average over clients, per seed
macro_recall, macro_ndcg = [], []
for s in seeds:
    rs = [per_seed[s][c][0] for c in clients if c in per_seed[s]]
    ns = [per_seed[s][c][1] for c in clients if c in per_seed[s]]
    macro_recall.append(st.mean(rs)); macro_ndcg.append(st.mean(ns))

print('Per-client Test (mean +/- std over seeds):')
print(f'{"client":>8} | {"Recall@20":>18} | {"NDCG@20":>18}')
for c in clients:
    rm, rs = ms([per_seed[s][c][0] for s in seeds if c in per_seed[s]])
    nm, ns = ms([per_seed[s][c][1] for s in seeds if c in per_seed[s]])
    print(f'{c:>8} | {rm:>8.4f} +/- {rs:6.4f} | {nm:>8.4f} +/- {ns:6.4f}')

rm, rs = ms(macro_recall); nm, ns = ms(macro_ndcg)
print('-' * 54)
print(f'{"MACRO":>8} | {rm:>8.4f} +/- {rs:6.4f} | {nm:>8.4f} +/- {ns:6.4f}')
print(f'\nPaper (ML-1M, Table 1): Recall@20=0.2646, NDCG@20=0.1342')
