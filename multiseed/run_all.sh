#!/bin/zsh
cd ~/LPSFed/src
source ../.venv/bin/activate
for s in 42 1 2 3 7; do
  echo "=== SEED $s START $(date +%H:%M:%S) ==="
  LPSFED_SEED=$s python -u main.py > ~/LPSFed/multiseed/seed$s.log 2>&1
  echo "=== SEED $s DONE $(date +%H:%M:%S) ==="
done
echo "ALL DONE"
