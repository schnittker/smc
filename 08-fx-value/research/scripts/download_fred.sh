#!/bin/sh
# Downloads the CPI and exchange-rate series of strategy no. 8 from FRED into ../data/raw/ (as of 24.10.2026).
set -e
cd "$(dirname "$0")/../.."
mkdir -p data/raw
for id in CPIAUCSL CP0000EZ19M086NEST GBRCPIALLMINMEI JPNCPIALLMINMEI CANCPIALLMINMEI CHECPIALLMINMEI \
          AUSCPIALLQINMEI NZLCPIALLQINMEI FPCPITOTLZGJPN DEXUSEU DEXUSUK DEXJPUS DEXUSAL DEXUSNZ DEXCAUS DEXSZUS; do
  curl -sS -L --max-time 60 -o "data/raw/$id.csv" "https://fred.stlouisfed.org/graph/fredgraph.csv?id=$id"
done
