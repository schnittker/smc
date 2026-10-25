# MT5-Export (nur lesend)

`ExportFtmoData.mq5` schreibt FTMO-Handelsbedingungen und Kurshistorie als CSV nach `MQL5/Files/ftmo_export/`. Das Skript sendet keine Orders.

| Datei | Inhalt |
|---|---|
| `account.csv` | Server, Kontowährung, Hebel, Abstand Serverzeit–GMT |
| `symbols.csv` | je Symbol: Spread, Swap long/short (+ Art, 3-fach-Tag), Kontraktgröße, Margin für 1 Lot, effektiver Hebel, Handelszeiten |
| `deals.csv` | eigene Deals mit Kommission, Swap und Gebühr (zum Ablesen der Kommission) |
| `rates/<Symbol>_<TF>.csv` | D1/H1 (optional M5) ab 2014 inkl. Spread je Bar |
| `rates_summary.csv` | Anzahl Bars und erstes Datum je Symbol |
| `ticks/<Symbol>.csv` | Bid/Ask-Ticks der letzten 30 Tage für ausgewählte Symbole |

**Einrichtung (Mac):**
- Die Datei liegt unter `~/Library/Application Support/net.metaquotes.wine.metatrader5/drive_c/Program Files/MetaTrader 5/MQL5/Scripts/`.
- Kompilieren:

```sh
P="$HOME/Library/Application Support/net.metaquotes.wine.metatrader5"
cd "$P/drive_c/Program Files/MetaTrader 5"
WINEPREFIX="$P" "/Applications/MetaTrader 5.app/Contents/SharedSupport/wine/bin/wine" \
  "C:\\Program Files\\MetaTrader 5\\metaeditor64.exe" /compile:"MQL5\\Scripts\\ExportFtmoData.mq5" /log
```

**Vor dem Start:** Extras → Optionen → Charts → „Max. Balken im Chart“ auf „Unbegrenzt“ stellen, sonst wird die H1-Historie gekürzt.
