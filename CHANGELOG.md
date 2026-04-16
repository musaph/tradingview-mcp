# Changelog

All notable changes to this project will be documented in this file.

## [0.7.0] - 2026-03-29

### Added
- **Walk-Forward Backtesting** (`walk_forward_backtest_strategy`):
  - Splits data into N folds (train/test) to validate strategy on unseen forward data
  - Per-fold in-sample vs out-of-sample return comparison
  - **Robustness score** (test/train ratio): ROBUST ≥ 0.8 | MODERATE ≥ 0.5 | WEAK ≥ 0.2 | OVERFITTED < 0.2
  - Aggregate out-of-sample metrics: Sharpe, win rate, max drawdown, total return
  - Supports 2–10 splits, configurable train ratio, both 1d and 1h intervals
- **Full Trade Log** (`include_trade_log=True`):
  - Per-trade breakdown: entry/exit date & price, holding days, gross/net return %, cost %
  - Running capital and cumulative return at each trade
- **Equity Curve** (`include_equity_curve=True`):
  - Capital value + drawdown % at each trade exit — ready for charting
- **1h (Hourly) Timeframe** (`interval="1h"`):
  - All strategies and compare now support intraday hourly data
  - Sharpe ratio annualization corrected for 1h bars (252 × 6 trading hours)
  - Works on `backtest_strategy`, `compare_strategies`, and `walk_forward_backtest_strategy`

### Changed
- `backtest_strategy` tool: added `interval`, `include_trade_log`, `include_equity_curve` params
- `compare_strategies` tool: added `interval` param; now documents all 6 strategies (was 4)
- `run_backtest()` now returns last 5 trades always (`recent_trades`) for quick inspection
- Sharpe ratio calculation now uses interval-aware annualization factor

### Notes (personal)
- I changed the default `interval` in `backtest_strategy` from `"1d"` to `"1h"` in my fork since I mostly test intraday setups
- Bumped default `n_splits` in `walk_forward_backtest_strategy` from 5 to 3 — 5 folds felt like overkill for the shorter crypto datasets I usually run this on
- Bumped default `initial_capital` from 10000 to 1000 — easier to reason about % returns when starting from a round number that matches my actual test budget
- Bumped default `commission` from 0.001 to 0.002 (0.2%) — better reflects the actual fees on the exchanges I use (Binance taker fee)
- Bumped default `slippage` from 0.001 to 0.0015 — Binance spot slippage on smaller caps tends to run a bit higher than the original default
- Bumped default `period` (lookback bars) in `backtest_strategy` from 252 to 500 — more history gives the walk-forward folds enough data on 1h timeframe
- Bumped default `train_ratio` in `walk_forward_backtest_strategy` from 0.7 to 0.8 — prefer more training data per fold given the shorter crypto history I work with
- Bumped default `recent_trades` count from 5 to 10 — 5 trades wasn't enough context when reviewing 1h backtest results; 10 gives a better picture of recent strategy behavior
- Bumped default `top_n` in `compare_strategies` from 3 to 6 — want to see the full ranking across all 6 strategies rather than just the top 3 when comparing on a new symbol
- Bumped default `risk_free_rate` from 0.02 (2%) to 0.045 (4.5%) — updated to reflect current US risk-free rate environment (approx. 2024–2025 T-bill yields); original default felt too low and was inflating Sharpe ratios
