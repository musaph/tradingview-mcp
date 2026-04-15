# TradingView MCP

A Model Context Protocol (MCP) server that provides TradingView market data and technical analysis tools to AI assistants.

> Fork of [atilaahmettaner/tradingview-mcp](https://github.com/atilaahmettaner/tradingview-mcp) with additional features and improvements.

## Features

- 📈 **Real-time Market Data** — Fetch quotes, OHLCV data, and market summaries
- 🔍 **Technical Analysis** — Access indicators like RSI, MACD, Bollinger Bands, and more
- 🔎 **Symbol Search** — Search for stocks, crypto, forex, and other instruments
- 📊 **Screener Support** — Filter instruments by technical and fundamental criteria
- 🤖 **MCP Compatible** — Works with Claude, Cursor, and any MCP-compatible AI client

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Installation

### Using uv (recommended)

```bash
git clone https://github.com/your-username/tradingview-mcp.git
cd tradingview-mcp
uv sync
```

### Using pip

```bash
git clone https://github.com/your-username/tradingview-mcp.git
cd tradingview-mcp
pip install -r requirements.txt
```

## Configuration

Copy `.env.example` to `.env` and adjust settings as needed:

```bash
cp .env.example .env
```

## Usage

### Run directly

```bash
uv run python -m tradingview_mcp
```

### Docker

```bash
docker build -t tradingview-mcp .
docker run --env-file .env tradingview-mcp
```

### Claude Desktop Integration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "tradingview": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/tradingview-mcp",
        "run",
        "python",
        "-m",
        "tradingview_mcp"
      ]
    }
  }
}
```

## Available Tools

| Tool | Description |
|------|-------------|
| `get_quote` | Get current price and basic info for a symbol |
| `get_technical_analysis` | Retrieve technical indicator summary |
| `search_symbols` | Search for trading symbols |
| `get_screener_data` | Screen instruments by criteria |
| `get_history` | Fetch historical OHLCV data |

## Development

```bash
# Install dev dependencies
uv sync --all-extras

# Run tests
uv run pytest

# Lint
uv run ruff check .
```

## Notes

> **Personal note:** I primarily use this with Claude Desktop for analyzing crypto and US equities. The `get_technical_analysis` and `get_history` tools are the most useful for my workflow.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for release history.

## License

MIT License — see [LICENSE](LICENSE) for details.

## Acknowledgements

- Original project by [@atilaahmettaner](https://github.com/atilaahmettaner)
- Built on the [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- Market data via [tradingview-ta](https://github.com/brian-the-dev/python-tradingview-ta)
