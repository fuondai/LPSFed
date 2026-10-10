# ML-1M reproduction (full-user evaluation, multi-seed)

Faithful reproduction of LPSFed on ML-1M on a single machine (Apple M4, CPU),
default repo config (LGCN, BC-loss, 4 clients, 200 epochs, gnmk random graph).

## What changed vs the stock repo
- `src/test.py`: `test_model` evaluates **all users** of each client
  deterministically when `TEST_USER_BATCH <= 0` (stock code scored only 32
  random users per eval, which made the reported numbers high-variance).
- `src/utils/params.py`: ML-1M `TEST_USER_BATCH = -1` (all users); `seed`
  now read from `LPSFED_SEED` env var for multi-seed runs.
- Plus the earlier index-mapping / USER_NUM fixes (branch fix/ml1m-preprocessing).

## Run
    for s in 42 1 2 3 7; do LPSFED_SEED=$s python -u main.py > seed$s.log; done
    python aggregate.py

## Result (5 seeds, mean +/- std, best-over-epochs per client)
See RESULTS.txt. Macro Recall@20 ~ 0.033, NDCG@20 ~ 0.025 — about 8x below the
paper's Table 1 (Recall@20 0.2646, NDCG@20 0.1342). Gap likely from: single run
vs paper's 6-run/2-partition averaging, no hyperparameter tuning, our own bug
fixes, and the honest full-user eval. Variance across seeds is near zero.
