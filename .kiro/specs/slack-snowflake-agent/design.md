# Design Document

## Overview

The Slack Snowflake Agent bridges the gap between raw business questions and deep Snowflake insights by making curated Gold-layer data instantly accessible via natural language in Slack. The system targets business users, analysts, sales teams, and executives who need quick data insights without SQL knowledge or leaving their workflow.

**Core Problem Solved:** Users can't write SQL or don't have time to query dashboards, but they want instant answers in tools they already use (Slack) with contextual, conversational interaction.

**System Flow:**
1. **User asks a business question through MCP client** (like "Which customer types spend the most?")
2. **MCP client calls appropriate MCP server tool** (query_snowflake_gold with the question)
3. **MCP server processes request and queries Snowflake** (targets specific Gold-layer tables like DAILY_SALES_SUMMARY)
4. **Formatted response returned to MCP client** ("Premium customers spent $45K this month on Toys, while Regular customers spent $32K. Would you like a breakdown by category?")

**Milestone 1 Focus:** Handle simple, clear business questions targeting DAILY_SALES_SUMMARY and CUSTOMER_PRODUCT_AFFINITY_MONTHLY Gold tables.

## Architecture

The system leverages a modern Snowflake data stack (Bronze → Silver → Gold layers) with the agent specifically targeting Gold-layer tables for business insights:

**Component Roles:**
- **MCP Client** - User interface (Claude Desktop, other LLM clients) for natural language queries
- **MCP Server** - Secure query execution, exposes three tools, handles Snowflake connection
- **Snowflake Gold Tables** - Source of truth for curated business data
- **LLM (in client)** - Understands questions, calls appropriate MCP tools

## MCP Server Tools

The MCP server provides three specific tools for LangGraph to use:

### 1. `query_snowflake_gold()` - Main Querying Function
**Purpose:** Execute business queries against Gold-layer tables
**Parameters:**
- `question` (string) - Natural language business question
- `table_hint` (optional string) - Suggested Gold table to query

**Returns:**
- Query results formatted for Slack display
- Metadata about the query executed
- Error messages if query fails

**Example Usage:**
```python
result = query_snowflake_gold(
    question="What were daily sales this week?",
    table_hint="DAILY_SALES_SUMMARY"
)
```

### 2. `list_available_data()` - Discovery and Help
**Purpose:** Help users understand what data is available
**Parameters:**
- `category` (optional string) - Filter by data category (Transactions, customers, products)

**Returns:**
- List of available Gold tables
- Schema information for each table
- Sample questions for each table

**Example Usage:**
```python
tables = list_available_data(category="sales")
# Returns info about DAILY_SALES_SUMMARY table
```

### 3. `get_data_help()` - User Guidance
**Purpose:** Provide contextual help and query suggestions
**Parameters:**
- `user_question` (string) - User's original question
- `context` (optional string) - Additional context about user needs

**Returns:**
- Suggested rephrasing of questions
- Examples of similar successful queries
- Guidance on available data

**Example Usage:**
```python
help_response = get_data_help(
    user_question="How are we doing with sales?",
    context="user_wants_trends"
)
```

## Components and Interfaces

### 1. Main Entry Point (`main.py`)
**What it does:** Minimal entry point that starts the system
- Initializes configuration
- Starts the LangGraph workflow
- Handles graceful shutdown

### 2. Main Entry Point (`main.py`)
**What it does:** Starts the MCP server and makes it available for client connections
- Initializes the MCP server from agent/core.py
- Handles server startup and shutdown
- Provides the entry point for MCP client connections

### 3. MCP Core (`agent/core.py`)
**What it does:** Sets up the MCP server infrastructure
- Initializes MCP server with available tools
- Manages tool registration and discovery
- Handles MCP protocol communication

### 4. Snowflake Tools (`agent/tools/snowflake_tools.py`)
**What it does:** Encapsulates secure Snowflake access and query building through three specific MCP tools:

#### MCP Tools Provided:
1. **`query_snowflake_gold()`** - Main querying function
   - Maps natural language to specific Gold tables (DAILY_SALES_SUMMARY, CUSTOMER_PRODUCT_AFFINITY_MONTHLY)
   - Builds safe SQL queries targeting only Gold-layer tables
   - Executes queries securely without exposing credentials
   - Returns formatted query results

2. **`list_available_data()`** - Discovery and help
   - Lists available Gold tables and their schemas
   - Provides table descriptions and column information
   - Shows sample queries for each table
   - Helps users understand what data is available

3. **`get_data_help()`** - User guidance
   - Provides contextual help based on user questions
   - Suggests appropriate queries for common business questions
   - Offers examples of supported question patterns
   - Guides users toward successful data interactions

### 5. Response Formatting (`agent/tools/slack_tools.py`)
**What it does:** Formats query results for optimal display in MCP clients
- Formats query results into readable tables and summaries
- Creates structured responses for different data types
- Handles error message formatting
- Optimizes display for various MCP client interfaces

## Milestone 1 Implementation Focus

### Target Gold Tables
- **DAILY_SALES_SUMMARY** - For questions like "What were daily sales this week?"
- **CUSTOMER_PRODUCT_AFFINITY_MONTHLY** - For questions like "Which customer types prefer which products?"

### Supported Question Patterns
1. **Daily Sales Queries** → DAILY_SALES_SUMMARY
   - "What were daily sales this week?"
   - "Which product categories are selling best?"
   - "How are Food vs Toys vs Automotive sales performing?"
   
2. **Customer Segment Queries** → DAILY_SALES_SUMMARY (aggregated)
   - "Which customer types spend the most?"
   - "How do Premium customers compare to Regular customers?"
   - "What do Unknown customers prefer to buy?"

3. **Product Performance Queries** → DAILY_SALES_SUMMARY (aggregated)
   - "What are the top selling products?"
   - "Which products generate the most revenue?"
   - "Show me popular products by category"

### Query Mapping Logic
The system will use pattern matching and intent recognition to map natural language to specific Gold tables, ensuring queries only target the curated, business-ready data layer.

## Key Python Files Structure

```
mcp-server-snowflake/
├── main.py                   # Entry point (minimal, already exists)
├── agent_workflow.py         # LangGraph workflow logic
├── config.py                 # Environment/config management
├── agent/                    # MCP server components
│   ├── __init__.py           # Package init
│   ├── core.py               # MCP server setup
│   └── tools/
│       ├── __init__.py       # Package init
│       ├── snowflake_tools.py # Gold table queries & mapping
│       └── slack_tools.py     # Slack response formatting
├── tests/                    # Test directory
├── pyproject.toml           # Project config
└── requirements.txt         # Dependencies 
```

## Data Models

### Simple Data Classes

```python
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class UserMessage:
    """What the user said to us"""
    user_id: str
    channel_id: str
    text: str
    timestamp: str

@dataclass
class QueryResult:
    """What we got back from Snowflake Gold tables"""
    sql_query: str
    gold_table_name: str  # e.g., "DAILY_SALES_SUMMARY"
    data: List[Dict[str, Any]]  # The actual results
    row_count: int
    success: bool
    error_message: Optional[str] = None

@dataclass
class SlackResponse:
    """What we send back to Slack"""
    text: str
    formatted_table: Optional[str] = None
    chart_url: Optional[str] = None
```

### Dependencies (from requirements.txt)
- **slack_sdk** - Slack Bot API integration
- **langgraph** - Workflow orchestration
- **openai** - LLM for natural language understanding
- **snowflake-connector-python** - Snowflake connectivity (via MCP)
- **python-dotenv** - Environment configuration
- **pytest** - Testing framework

## Error Handling

### What happens when things go wrong:

1. **User asks unclear question**
   - Bot asks for clarification: "Did you mean sales for this month or last month?"

2. **User asks question outside Milestone 1 scope**
   - Bot responds: "I can help with daily sales analysis, customer type comparisons, and product performance. Try asking 'What were daily sales this week?' or 'How do Premium customers compare to Regular customers?'"

3. **Snowflake Gold table is unavailable**
   - Bot says: "Sorry, the sales data is temporarily unavailable. Please try again in a few minutes."

4. **User doesn't have permission to Gold table**
   - Bot says: "You don't have access to that data. Contact your admin for help."

5. **Query takes too long**
   - Bot says: "That query is taking too long. Try asking for a smaller date range."

6. **MCP connection fails**
   - Bot says: "Unable to connect to data services. Please try again later."

## Testing Strategy

### How we'll test it:

1. **Unit Tests** - Test each Python file individually
2. **Integration Tests** - Test the whole flow from Slack to Snowflake
3. **Manual Testing** - Actually try asking questions in Slack
4. **Security Tests** - Make sure bad queries can't break anything

## Security

### Keeping things safe:

1. **MCP encapsulates all Snowflake access** - No direct database credentials in Slack environment
2. **Gold-layer only queries** - System restricted to curated, business-ready tables only
3. **User permissions enforced** - MCP respects Snowflake user-level access controls
4. **Query validation** - Only approved Gold table queries can be executed
5. **Comprehensive logging** - All queries, users, and results tracked for audit
6. **Tool-based access control** - MCP tools provide granular control over data operations

## Real Data Structure

### DAILY_SALES_SUMMARY Table Schema
- `TRANSACTION_DATE` (DATE) - Daily transaction dates
- `PRODUCT_ID` (NUMBER) - Product identifier  
- `PRODUCT_NAME` (TEXT) - Product names (e.g., "Product 774")
- `PRODUCT_CATEGORY` (TEXT) - Categories: **Food, Automotive, Toys**
- `CUSTOMER_ID` (NUMBER) - Customer identifier
- `CUSTOMER_TYPE` (TEXT) - Customer segments: **Unknown, Regular, Premium**
- `TOTAL_QUANTITY_SOLD` (NUMBER) - Units sold per transaction
- `TOTAL_REVENUE` (FLOAT) - Revenue per transaction
- `AVG_PRICE_PER_UNIT` (FLOAT) - Average unit price
- `AVG_REVENUE_PER_TRANSACTION` (FLOAT) - Average transaction value

### CUSTOMER_PRODUCT_AFFINITY_MONTHLY Table Schema
- `CUSTOMER_ID` (NUMBER) - Customer identifier
- `CUSTOMER_TYPE` (TEXT) - Customer segments: **Unknown, Regular, Premium**
- `PRODUCT_ID` (NUMBER) - Product identifier
- `PRODUCT_NAME` (TEXT) - Product name
- `PRODUCT_CATEGORY` (TEXT) - Product categories: **Food, Automotive, Toys**
- `PURCHASE_MONTH` (DATE) - Monthly aggregation period
- `PURCHASE_COUNT` (NUMBER) - Number of purchases in month
- `TOTAL_QUANTITY` (NUMBER) - Total units purchased
- `TOTAL_SPENT` (FLOAT) - Total spending amount
- `AVG_PURCHASE_AMOUNT` (FLOAT) - Average purchase value
- `DAYS_BETWEEN_FIRST_LAST_PURCHASE` (NUMBER) - Purchase frequency indicator
