#!/bin/sh
# Downloads the daily 10-year Treasury constant-maturity yield (FRED series DGS10) into ../data/raw/.
set -e
cd "$(dirname "$0")/../.."
mkdir -p data/raw
curl -sS -L --max-time 60 -o data/raw/DGS10.csv "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10"
