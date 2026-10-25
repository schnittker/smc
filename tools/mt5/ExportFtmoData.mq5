//+------------------------------------------------------------------+
//| ExportFtmoData.mq5                                               |
//| Read-only export of FTMO trading conditions and price history    |
//| to MQL5/Files/<InpDir>/ as CSV. Sends no orders.                 |
//+------------------------------------------------------------------+
#property copyright "ea research"
#property version   "1.00"
#property script_show_inputs

input string   InpRatesSymbols = "*";        // rates for: "*" = all symbols, or comma list
input bool     InpExportD1     = true;       // export D1 bars
input bool     InpExportH1     = true;       // export H1 bars
input bool     InpExportM5     = false;      // export M5 bars (large)
input datetime InpFrom         = D'2014.01.01';
input string   InpTickSymbols  = "BTCUSD,ETHUSD,EURUSD,US500.cash,XAUUSD"; // ticks (bid/ask) for these
input int      InpTickDays     = 30;         // days of ticks
input string   InpDir          = "ftmo_export";

int Open(const string name)
  {
   int h = FileOpen(InpDir + "\\" + name, FILE_WRITE | FILE_TXT | FILE_ANSI);
   if(h == INVALID_HANDLE)
      PrintFormat("cannot open %s: %d", name, GetLastError());
   return h;
  }

string Q(const string s)
  {
   string t = s;
   StringReplace(t, "\"", "'");
   return "\"" + t + "\"";
  }

string Safe(const string s)
  {
   string t = s;
   StringReplace(t, "/", "_");
   StringReplace(t, "\\", "_");
   StringReplace(t, ":", "_");
   return t;
  }

string D(const double v, const int digits = 8) { return DoubleToString(v, digits); }

string Hm(const datetime t)
  {
   if((long)t >= 86400) return "24:00";
   return TimeToString(t, TIME_MINUTES);
  }

string Sessions(const string sym)
  {
   string out = "";
   for(int d = 0; d < 7; d++)
     {
      string day = "";
      datetime a, b;
      for(uint k = 0; k < 4 && SymbolInfoSessionTrade(sym, (ENUM_DAY_OF_WEEK)d, k, a, b); k++)
         day += (day == "" ? "" : "+") + Hm(a) + "-" + Hm(b);
      out += (d == 0 ? "" : "|") + IntegerToString(d) + ":" + day;
     }
   return out;
  }

void ExportAccount()
  {
   int h = Open("account.csv");
   if(h == INVALID_HANDLE) return;
   FileWriteString(h, "key,value\n");
   FileWriteString(h, "server," + Q(AccountInfoString(ACCOUNT_SERVER)) + "\n");
   FileWriteString(h, "company," + Q(AccountInfoString(ACCOUNT_COMPANY)) + "\n");
   FileWriteString(h, "currency," + AccountInfoString(ACCOUNT_CURRENCY) + "\n");
   FileWriteString(h, "leverage," + IntegerToString(AccountInfoInteger(ACCOUNT_LEVERAGE)) + "\n");
   FileWriteString(h, "trade_mode," + IntegerToString(AccountInfoInteger(ACCOUNT_TRADE_MODE)) + "\n");
   FileWriteString(h, "balance," + D(AccountInfoDouble(ACCOUNT_BALANCE), 2) + "\n");
   FileWriteString(h, "server_minus_gmt_seconds," + IntegerToString((long)(TimeTradeServer() - TimeGMT())) + "\n");
   FileWriteString(h, "export_time_gmt," + TimeToString(TimeGMT(), TIME_DATE | TIME_SECONDS) + "\n");
   FileWriteString(h, "terminal_build," + IntegerToString(TerminalInfoInteger(TERMINAL_BUILD)) + "\n");
   FileWriteString(h, "terminal_maxbars," + IntegerToString(TerminalInfoInteger(TERMINAL_MAXBARS)) + "\n");
   FileClose(h);
  }

void ExportSymbols()
  {
   int h = Open("symbols.csv");
   if(h == INVALID_HANDLE) return;
   FileWriteString(h, "symbol,path,description,base,profit,margin_ccy,digits,point,spread_points,spread_float,"
                   "contract_size,calc_mode,trade_mode,volume_min,volume_max,volume_step,tick_size,tick_value,"
                   "swap_mode,swap_long,swap_short,swap_3days,margin_initial,bid,ask,margin_1lot,notional_1lot,"
                   "leverage,sessions\n");
   int n = SymbolsTotal(false);
   for(int i = 0; i < n; i++)
     {
      string s = SymbolName(i, false);
      SymbolSelect(s, true);
      MqlTick tk;
      SymbolInfoTick(s, tk);
      double margin = 0.0;
      double tsz = SymbolInfoDouble(s, SYMBOL_TRADE_TICK_SIZE);
      double tval = SymbolInfoDouble(s, SYMBOL_TRADE_TICK_VALUE);
      if(tk.ask > 0 && !OrderCalcMargin(ORDER_TYPE_BUY, s, 1.0, tk.ask, margin))
         margin = 0.0;
      double notional = (tsz > 0) ? tk.ask / tsz * tval : 0.0;
      double lev = (margin > 0) ? notional / margin : 0.0;
      string line = s + "," + Q(SymbolInfoString(s, SYMBOL_PATH)) + "," + Q(SymbolInfoString(s, SYMBOL_DESCRIPTION)) + ","
                    + SymbolInfoString(s, SYMBOL_CURRENCY_BASE) + "," + SymbolInfoString(s, SYMBOL_CURRENCY_PROFIT) + ","
                    + SymbolInfoString(s, SYMBOL_CURRENCY_MARGIN) + ","
                    + IntegerToString(SymbolInfoInteger(s, SYMBOL_DIGITS)) + "," + D(SymbolInfoDouble(s, SYMBOL_POINT), 10) + ","
                    + IntegerToString(SymbolInfoInteger(s, SYMBOL_SPREAD)) + ","
                    + IntegerToString(SymbolInfoInteger(s, SYMBOL_SPREAD_FLOAT)) + ","
                    + D(SymbolInfoDouble(s, SYMBOL_TRADE_CONTRACT_SIZE), 4) + ","
                    + IntegerToString(SymbolInfoInteger(s, SYMBOL_TRADE_CALC_MODE)) + ","
                    + IntegerToString(SymbolInfoInteger(s, SYMBOL_TRADE_MODE)) + ","
                    + D(SymbolInfoDouble(s, SYMBOL_VOLUME_MIN), 4) + "," + D(SymbolInfoDouble(s, SYMBOL_VOLUME_MAX), 4) + ","
                    + D(SymbolInfoDouble(s, SYMBOL_VOLUME_STEP), 4) + "," + D(tsz, 10) + "," + D(tval, 8) + ","
                    + IntegerToString(SymbolInfoInteger(s, SYMBOL_SWAP_MODE)) + ","
                    + D(SymbolInfoDouble(s, SYMBOL_SWAP_LONG), 6) + "," + D(SymbolInfoDouble(s, SYMBOL_SWAP_SHORT), 6) + ","
                    + IntegerToString(SymbolInfoInteger(s, SYMBOL_SWAP_ROLLOVER3DAYS)) + ","
                    + D(SymbolInfoDouble(s, SYMBOL_MARGIN_INITIAL), 4) + ","
                    + D(tk.bid, 10) + "," + D(tk.ask, 10) + "," + D(margin, 4) + "," + D(notional, 4) + "," + D(lev, 4) + ","
                    + Q(Sessions(s)) + "\n";
      FileWriteString(h, line);
     }
   FileClose(h);
   PrintFormat("symbols.csv: %d symbols", n);
  }

void ExportDeals()
  {
   int h = Open("deals.csv");
   if(h == INVALID_HANDLE) return;
   FileWriteString(h, "time,symbol,type,entry,volume,price,commission,swap,fee,profit\n");
   if(HistorySelect(0, TimeCurrent() + 86400))
      for(int i = 0; i < HistoryDealsTotal(); i++)
        {
         ulong t = HistoryDealGetTicket(i);
         FileWriteString(h, TimeToString((datetime)HistoryDealGetInteger(t, DEAL_TIME), TIME_DATE | TIME_SECONDS) + ","
                         + HistoryDealGetString(t, DEAL_SYMBOL) + ","
                         + IntegerToString(HistoryDealGetInteger(t, DEAL_TYPE)) + ","
                         + IntegerToString(HistoryDealGetInteger(t, DEAL_ENTRY)) + ","
                         + D(HistoryDealGetDouble(t, DEAL_VOLUME), 4) + "," + D(HistoryDealGetDouble(t, DEAL_PRICE), 8) + ","
                         + D(HistoryDealGetDouble(t, DEAL_COMMISSION), 4) + "," + D(HistoryDealGetDouble(t, DEAL_SWAP), 4) + ","
                         + D(HistoryDealGetDouble(t, DEAL_FEE), 4) + "," + D(HistoryDealGetDouble(t, DEAL_PROFIT), 4) + "\n");
        }
   FileClose(h);
  }

string TfName(const ENUM_TIMEFRAMES tf)
  {
   if(tf == PERIOD_D1) return "D1";
   if(tf == PERIOD_H1) return "H1";
   return "M5";
  }

int ExportRates(const string s, const ENUM_TIMEFRAMES tf, const int hsum)
  {
   MqlRates r[];
   int n = -1;
   for(int k = 0; k < 30; k++)
     {
      n = CopyRates(s, tf, InpFrom, TimeCurrent(), r);
      if(n > 0 && SeriesInfoInteger(s, tf, SERIES_SYNCHRONIZED))
         break;
      Sleep(1000);
     }
   FileWriteString(hsum, s + "," + TfName(tf) + "," + IntegerToString(n) + ","
                   + TimeToString((datetime)SeriesInfoInteger(s, tf, SERIES_SERVER_FIRSTDATE), TIME_DATE) + ","
                   + (n > 0 ? TimeToString(r[0].time, TIME_DATE) + "," + TimeToString(r[n - 1].time, TIME_DATE) : ",") + "\n");
   if(n <= 0) return 0;
   int h = Open("rates\\" + Safe(s) + "_" + TfName(tf) + ".csv");
   if(h == INVALID_HANDLE) return 0;
   FileWriteString(h, "time,open,high,low,close,tick_volume,spread_points,real_volume\n");
   int dg = (int)SymbolInfoInteger(s, SYMBOL_DIGITS);
   for(int i = 0; i < n; i++)
      FileWriteString(h, TimeToString(r[i].time, TIME_DATE | TIME_MINUTES) + "," + D(r[i].open, dg) + "," + D(r[i].high, dg) + ","
                      + D(r[i].low, dg) + "," + D(r[i].close, dg) + "," + IntegerToString(r[i].tick_volume) + ","
                      + IntegerToString(r[i].spread) + "," + IntegerToString(r[i].real_volume) + "\n");
   FileClose(h);
   return n;
  }

void ExportAllRates()
  {
   string syms[];
   if(InpRatesSymbols == "*")
     {
      int n = SymbolsTotal(false);
      ArrayResize(syms, n);
      for(int i = 0; i < n; i++) syms[i] = SymbolName(i, false);
     }
   else
      StringSplit(InpRatesSymbols, ',', syms);
   int hsum = Open("rates_summary.csv");
   if(hsum == INVALID_HANDLE) return;
   FileWriteString(hsum, "symbol,tf,bars,server_firstdate,first,last\n");
   for(int i = 0; i < ArraySize(syms); i++)
     {
      string s = syms[i];
      StringTrimLeft(s); StringTrimRight(s);
      if(s == "" || !SymbolSelect(s, true)) continue;
      Comment(StringFormat("ExportFtmoData: rates %d/%d %s", i + 1, ArraySize(syms), s));
      if(InpExportD1) ExportRates(s, PERIOD_D1, hsum);
      if(InpExportH1) ExportRates(s, PERIOD_H1, hsum);
      if(InpExportM5) ExportRates(s, PERIOD_M5, hsum);
      if(IsStopped()) break;
     }
   FileClose(hsum);
  }

void ExportTicks()
  {
   string syms[];
   StringSplit(InpTickSymbols, ',', syms);
   ulong to = (ulong)TimeCurrent() * 1000;
   ulong from = to - (ulong)InpTickDays * 86400 * 1000;
   for(int i = 0; i < ArraySize(syms); i++)
     {
      string s = syms[i];
      StringTrimLeft(s); StringTrimRight(s);
      if(s == "" || !SymbolSelect(s, true)) continue;
      Comment("ExportFtmoData: ticks " + s);
      MqlTick t[];
      int n = -1;
      for(int k = 0; k < 30 && n <= 0; k++)
        {
         n = CopyTicksRange(s, t, COPY_TICKS_INFO, from, to);
         if(n <= 0) Sleep(1000);
        }
      if(n <= 0) { PrintFormat("no ticks for %s: %d", s, GetLastError()); continue; }
      int h = Open("ticks\\" + Safe(s) + ".csv");
      if(h == INVALID_HANDLE) continue;
      FileWriteString(h, "time_msc,bid,ask\n");
      int dg = (int)SymbolInfoInteger(s, SYMBOL_DIGITS);
      for(int j = 0; j < n; j++)
         FileWriteString(h, IntegerToString((long)t[j].time_msc) + "," + D(t[j].bid, dg) + "," + D(t[j].ask, dg) + "\n");
      FileClose(h);
      PrintFormat("ticks %s: %d", s, n);
     }
  }

void OnStart()
  {
   ExportAccount();
   ExportSymbols();
   ExportDeals();
   ExportAllRates();
   ExportTicks();
   Comment("");
   int h = Open("DONE.txt");
   if(h != INVALID_HANDLE) { FileWriteString(h, TimeToString(TimeGMT(), TIME_DATE | TIME_SECONDS) + " GMT\n"); FileClose(h); }
   Print("ExportFtmoData: fertig");
  }
