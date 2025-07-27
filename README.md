# Snowflake MCP Server

MCP server that enables natural language queries against Snowflake Gold-layer tables through Claude Desktop. Ask business questions in plain English and get instant insights without SQL knowledge.

## Overview

This MCP server bridges the gap between raw business questions and deep Snowflake insights by making data instantly accessible via natural language through Claude Desktop. Users (analysts, ops, sales teams, executives) can query curated Snowflake Gold-layer tables through Claude Desktop's chat interface without needing SQL knowledge.

**How it works:**
- **Claude Desktop (front-end)**: Where you chat naturally and ask questions
- **MCP Server (back-end)**: Python server running in the background with Snowflake tools  
- **Communication**: Claude Desktop sends requests to your MCP server, which queries Snowflake and returns formatted results

The system leverages a modern Snowflake data stack (Bronze → Silver → Gold layers) and provides three MCP tools that Claude Desktop can use to access the data.

### Key Features
- **Natural Language Queries**: "Which customer types spend the most on Toys?"
- **Gold-Layer Focus**: Queries only curated, business-ready data
- **Secure Access**: MCP encapsulation for database security
- **Claude Desktop Integration**: Works seamlessly with Claude Desktop's chat interface

### Tech Stack
- **FastMCP** - Model Context Protocol server implementation
- **Snowflake** - Data warehouse with Bronze/Silver/Gold architecture
- **Python 3.11+** - Core runtime environment
- **Primary Client**: Claude Desktop (other MCP clients also supported)

## Architecture
```
MCP Client (Claude Desktop) → MCP Server → Snowflake Gold Tables
```

## Supported Questions

**Customer Analysis:**
- "Which customer types spend the most?"
- "How do Premium customers compare to Regular customers?"

**Product Performance:**
- "What are the top selling products?"
- "Show me popular products in Food category"

**Daily Sales:**
- "What were daily sales this week?"
- "How are Food vs Toys vs Automotive sales performing?"

## MCP Tools

1. **`query_snowflake_gold()`** - Execute business queries against Gold tables
2. **`list_available_data()`** - Discover available tables and schemas  
3. **`get_data_help()`** - Get contextual help and query suggestions

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure environment:**
Create `.env` file:
```bash
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account_url
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=GOLD

# No additional API keys needed - Claude Desktop handles the LLM
```

3. **Test and run:**
```bash
python tests/test_snowflake_connection.py  # Test Snowflake connection
python main.py                             # Start MCP server
```

4. **Connect Claude Desktop:**
Add to your Claude Desktop MCP settings:
```json
{
  "mcpServers": {
    "snowflake-agent": {
      "command": "python",
      "args": ["main.py"],
      "cwd": "/path/to/your/project"
    }
  }
}
```

## Project Structure
```
├── main.py                   # Entry point - starts MCP server
├── agent/
│   ├── config.py             # Configuration management
│   ├── core.py               # MCP server with 3 tools
│   └── tools/
│       ├── snowflake_tools.py # Snowflake Gold table queries
│       └── response_formatter.py # Claude Desktop response formatting
└── tests/                    # Tests
```
