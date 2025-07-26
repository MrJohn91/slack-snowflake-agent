# Slack Snowflake Agent

AI-powered Slack agent that enables natural language queries against Snowflake Gold-layer tables. Ask business questions in plain English and get instant insights without SQL knowledge.

## Overview

This feature implements an AI-powered Slack agent that bridges the gap between raw business questions and deep Snowflake insights using AI to make data instantly accessible via natural language. The agent enables users (analysts, ops, sales teams, executives) to query curated Snowflake Gold-layer tables through Slack without needing SQL knowledge or leaving their workflow.

The system leverages a modern Snowflake data stack structured into Bronze → Silver → Gold layers, with the agent specifically targeting Gold-layer tables for business insights. It uses the Model Context Protocol (MCP) for secure data access, LangGraph for intelligent orchestration, and provides conversational responses directly in Slack.

### Key Features
- **Natural Language Queries**: "Which customer types spend the most on Toys?"
- **Gold-Layer Focus**: Queries only curated, business-ready data
- **Secure Access**: MCP encapsulation for database security
- **Slack Integration**: Get formatted results directly in Slack

### Tech Stack
- **OpenAI** - LLM for natural language understanding and query generation
- **LangGraph** - Workflow orchestration and AI agent logic
- **FastMCP** - Model Context Protocol server implementation
- **Slack SDK** - Slack Bot API integration
- **Snowflake** - Data warehouse with Bronze/Silver/Gold architecture
- **Python 3.11+** - Core runtime environment

## Architecture
```
Slack → LangGraph → MCP Server → Snowflake Gold Tables
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

SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_SIGNING_SECRET=your-signing-secret
```

3. **Test and run:**
```bash
python tests/test_snowflake_connection.py  # Test Snowflake
python main.py                             # Start MCP server
```

## Project Structure
```
├── main.py                   # Entry point
├── agent_workflow.py         # LangGraph orchestration  
├── agent/
│   ├── config.py             # Configuration
│   ├── core.py               # MCP server setup
│   └── tools/
│       ├── snowflake_tools.py # Snowflake queries
│       └── slack_tools.py     # Slack formatting
└── tests/                    # Tests
```
