"""TradingView MCP Server - Main entry point for the Model Context Protocol server."""

import asyncio
import logging
import os
from typing import Any

from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
)

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("tradingview-mcp")

app = Server("tradingview-mcp")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available TradingView tools."""
    return [
        Tool(
            name="get_ticker_info",
            description="Fetch current price and basic info for a ticker symbol from TradingView.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Ticker symbol (e.g. AAPL, BTDT, EURUSD)",
                    },
                                "required": ["symbol"],
            },
        ),
        Tool(
            name="get_technical_analysis",
            description="Get technical analysis summary (oscillators, moving averages) for a symbol.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Ticker symbol (e.g. AAPL, BTCUSDT)",
                    m, 1h, 2h, 4h, 1M",
                        # Changed default from 1d to 4h - more useful for my trading
                        "default": "4h",
                    },
                    "exchange": {
                        "type": "string",
                        "description": "Exchange name. Optional.",
                    },
                },
                "required": ["symbol"],
            },
        ),
        Tool(
            name="search_symbol",
            description="Search for ticker symbols on TradingView by query string.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (company name or ticker)",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default: 10)",
                        "default": 10,
                    },
                },
                "required": ["query"],
            },
