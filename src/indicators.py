"""Technical indicator helpers and summary builders for TradingView analysis."""

from typing import Any

# Recommendation constants returned by tradingview_ta
BUY = "BUY"
STRONG_BUY = "STRONG_BUY"
SELL = "SELL"
STRONG_SELL = "STRONG_SELL"
NEUTRAL = "NEUTRAL"


def recommendation_emoji(recommendation: str) -> str:
    """Return an emoji that visually represents a recommendation string."""
    mapping = {
        STRONG_BUY: "🚀",
        BUY: "📈",
        NEUTRAL: "➡️",
        SELL: "📉",
        STRONG_SELL: "🔻",
    }
    return mapping.get(recommendation, "❓")


def extract_summary(analysis: Any) -> dict:
    """Extract the high-level summary block from a TA handler result.

    Args:
        analysis: A tradingview_ta ``Analysis`` object.

    Returns:
        A plain dict with recommendation, buy/sell/neutral counts.
    """
    summary = analysis.summary
    recommendation = summary.get("RECOMMENDATION", NEUTRAL)
    return {
        "recommendation": recommendation,
        "emoji": recommendation_emoji(recommendation),
        "buy": summary.get("BUY", 0),
        "sell": summary.get("SELL", 0),
        "neutral": summary.get("NEUTRAL", 0),
    }


def extract_oscillators(analysis: Any) -> dict:
    """Extract oscillator summary and key indicator values."""
    osc = analysis.oscillators
    indicators = osc.get("COMPUTE", {})
    return {
        "recommendation": osc.get("RECOMMENDATION", NEUTRAL),
        "buy": osc.get("BUY", 0),
        "sell": osc.get("SELL", 0),
        "neutral": osc.get("NEUTRAL", 0),
        "rsi": indicators.get("RSI"),
        "stoch_k": indicators.get("Stoch.K"),
        "stoch_d": indicators.get("Stoch.D"),
        "macd_macd": indicators.get("MACD.macd"),
        "macd_signal": indicators.get("MACD.signal"),
        "cci20": indicators.get("CCI20"),
        "adx": indicators.get("ADX"),
        "ao": indicators.get("AO"),
        "mom": indicators.get("Mom"),
        "bull_bear_power": indicators.get("BBPower"),
    }


def extract_moving_averages(analysis: Any) -> dict:
    """Extract moving average summary and key MA values."""
    ma = analysis.moving_averages
    indicators = ma.get("COMPUTE", {})
    return {
        "recommendation": ma.get("RECOMMENDATION", NEUTRAL),
        "buy": ma.get("BUY", 0),
        "sell": ma.get("SELL", 0),
        "neutral": ma.get("NEUTRAL", 0),
        "ema10": indicators.get("EMA10"),
        "ema20": indicators.get("EMA20"),
        "ema50": indicators.get("EMA50"),
        "ema100": indicators.get("EMA100"),
        "ema200": indicators.get("EMA200"),
        "sma10": indicators.get("SMA10"),
        "sma20": indicators.get("SMA20"),
        "sma50": indicators.get("SMA50"),
        "sma100": indicators.get("SMA100"),
        "sma200": indicators.get("SMA200"),
        "vwma": indicators.get("VWMA"),
        "hull_ma9": indicators.get("HullMA9"),
    }


def build_full_report(analysis: Any) -> dict:
    """Combine all extracted sections into a single structured report dict."""
    return {
        "summary": extract_summary(analysis),
        "oscillators": extract_oscillators(analysis),
        "moving_averages": extract_moving_averages(analysis),
    }
