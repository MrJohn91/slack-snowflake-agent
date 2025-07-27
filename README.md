# Slack Snowflake Agent

MCP server that enables natural language queries against Snowflake Gold-layer tables through AI clients like Claude Desktop. Ask business questions in plain English and get instant insights without SQL knowledge.

## Overview

This MCP server bridges the gap between raw business questions and deep Snowflake insights by making data instantly accessible via natural language through AI clients. It enables users (analysts, ops, sales teams, executives) to query curated Snowflake Gold-layer tables through MCP-compatible clients like Claude Desktop without needing SQL knowledge.

The system leverages a modern Snowflake data stack structured into Bronze → Silver → Gold layers, specifically targeting Gold-layer tables for business insights. It uses the Model Context Protocol (MCP) for secure data access and provides three well-defined tools that AI clients can use to access Snowflake data.

### Key Features
- **Natural Language Queries**: "Which customer types spend the most on Toys?"
- **Gold-Layer Focus**: Queries only curated, business-ready data
- **Secure Access**: MCP encapsulation for database security
- **MCP Integration**: Works with Claude Desktop and other MCP-compatible AI clients

### Tech Stack
- **FastMCP** - Model Context Protocol server implementation
- **Snowflake** - Data warehouse with Bronze/Silver/Gold architecture
- **Python 3.11+** - Core runtime environment
- **Compatible with**: Claude Desktop, OpenAI clients, and other MCP-compatible AI tools

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

# Optional: OpenAI API key if using OpenAI-compatible clients
OPENAI_API_KEY=your-openai-key
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
│       └── slack_tools.py     # Response formatting
└── tests/                    # Tests
```
