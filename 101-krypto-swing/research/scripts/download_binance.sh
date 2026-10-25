#!/bin/sh
# Binance spot daily klines (00:00 UTC) for the five coins of model K, raw JSON pages into data/raw/binance/.
set -eu
cd "$(dirname "$0")/../.."
OUT=data/raw/binance
mkdir -p "$OUT"
for SYM in BTCUSDT ETHUSDT LTCUSDT XRPUSDT ADAUSDT; do
  START=1501545600000          # 2017-08-01
  PAGE=0
  while :; do
    F="$OUT/${SYM}_${PAGE}.json"
    curl -sf -m 60 "https://api.binance.com/api/v3/klines?symbol=${SYM}&interval=1d&startTime=${START}&limit=1000" -o "$F"
    N=$(grep -o '\],\[' "$F" | wc -l | tr -d ' ')
    [ "$N" -lt 999 ] && break
    START=$(( $(grep -o '\[\[*[0-9]*' "$F" | tail -1 | tr -d '[') + 86400000 ))
    PAGE=$((PAGE + 1))
  done
  echo "$SYM: $((PAGE + 1)) pages"
done
