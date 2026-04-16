"""TradingView client module for fetching market data and technical analysis."""

import os
import logging
from typing import Optional
from tradingview_ta import TA_Handler, Interval, Exchange

logger = logging.getLogger(__name__)

# Interval mapping from string to tradingview_ta Interval
INTERVAL_MAP = {
    "1m": Interval.INTERVAL_1_MINUTE,
    "5m": Interval.INTERVAL_5_MINUTES,
    "15m": Interval.INTERVAL_15_MINUTES,
    "30m": Interval.INTERVAL_30_MINUTES,
    "1h": Interval.INTERVAL_1_HOUR,
    "2h": Interval.INTERVAL_2_HOURS,
    "4h": Interval.INTERVAL_4_HOURS,
    "1d": Interval.INTERVAL_1_DAY,
    "1W": Interval.INTERVAL_1_WEEK,
    "1M": Interval.INTERVAL_1_MONTH,
}


def get_analysis(
    symbol: str,
    exchange: str = "NASDAQ",
    screener: str = "america",
    interval: str = "4h",  # changed default from 1d to 4h — better for my swing trading use case
) -> dict:
    """Fetch technical analysis for a given symbol from TradingView.

    Args:
        symbol: Ticker symbol (e.g., 'AAPL', 'BTCUSDT').
        exchange: Exchange name (e.g., 'NASDAQ', 'BINANCE').
        screener: Screener region (e.g., 'america', 'crypto').
        interval: Time interval string (e.g., '1d', '1h').

    Returns:
        Dictionary containing summary, oscillators, moving averages, and indicators.

    Raises:
        ValueError: If the interval is not supported or analysis fails.
    """
    tv_interval = INTERVAL_MAP.get(interval)
    if tv_interval is None:
        raise ValueError(
            f"Unsupported interval '{interval}'. Supported: {list(INTERVAL_MAP.keys())}"
        )

    handler = TA_Handler(
        symbol=symbol.upper(),
        exchange=exchange.upper(),
        screener=screener.lower(),
        interval=tv_interval,
        timeout=int(os.getenv("REQUEST_TIMEOUT", "10")),
    )

    try:
        analysis = handler.get_analysis()
    except Exception as exc:
        logger.error("Failed to fetch analysis for %s: %s", symbol, exc)
        raise ValueError(f"Could not retrieve analysis for '{symbol}': {exc}") from exc

    return {
        "symbol": symbol.upper(),
        "exchange": exchange.upper(),
        "screener": screener.lower(),
        "interval": interval,
        "summary": {
            "recommendation": analysis.summary.get("RECOMMENDATION"),
            "buy": analysis.summary.get("BUY"),
            "sell": analysis.summary.get("SELL"),
            "neutral": analysis.summary.get("NEUTRAL"),
        },
        "oscillators": {
            "recommendation": analysis.oscillators.get("RECOMMENDATION"),
            "buy": analysis.oscillators.get("BUY"),
            "sell": analysis.oscillators.get("SELL"),
            "neutral": analysis.oscillators.get("NEUTRAL"),
        },
        "moving_averages": {
            "recommendation": analysis.moving_averages.get("RECOMMENDATION"),
            "buy": analysis.moving_averages.get("BUY"),
            "sell": analysis.moving_averages.get("SELL"),
            "neutral": analysis.moving_averages.get("NEUTRAL"),
        },
        "indicators": analysis.indicators,
    }
