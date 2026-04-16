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
                    },"exchange": {
                        ", BINANCE, F). Optional.",
                    },
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
                    },
                    "interval": {
 interval: 1m, 30m, 1h, 1 1W, 1M",
                        "default": "1d",
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
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Dispatch tool calls to the appropriate handler."""
    from src.tools import get_ticker_info, get_technical_analysis, search_symbol

    logger.info("Tool called: %s with args: %s", name, arguments)

    try:
        if name == "get_ticker_info":
            result = await get_ticker_info(
                symbol=arguments["symbol"],
                exchange=arguments.get("exchange"),
            )
        elif name == "get_technical_analysis":
            result = await get_technical_analysis(
                symbol=arguments["symbol"],
                interval=arguments.get("interval", "1d"),
                exchange=arguments.get("exchange"),
            )
        elif name == "search_symbol":
            result = await search_symbol(
                query=arguments["query"],
                limit=arguments.get("limit", 10),
            )
        else:
            result = f"Unknown tool: {name}"

        return [TextContent(type="text", text=str(result))]

    except Exception as exc:
        logger.exception("Error executing tool %s", name)
        return [TextContent(type="text", text=f"Error: {exc}")]


async def main() -> None:
    """Run the MCP server over stdio."""
    logger.info("Starting TradingView MCP server")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
