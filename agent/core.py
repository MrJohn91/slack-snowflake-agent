# agent/core.py
# ^MCP server setup for Snowflake Gold-layer querying
# Provides secure, tool-based access to curated business data

import sys
import os
# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from mcp.server.fastmcp import FastMCP
from agent.tools.snowflake_tools import query_gold_view, get_available_views
from agent.config import Config, setup_logging
import logging

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

# Create an MCP server for Snowflake Gold queries
mcp = FastMCP("Snowflake Gold Query MCP Server")

@mcp.tool()
def query_snowflake_gold(question: str, limit: int = None) -> dict:
    """
    Query Snowflake Gold-layer views using natural language.
    
    For Milestone 1, supports:
    - Daily sales analysis: "What were daily sales this week?"
    - Customer segment analysis: "Which customer types spend the most?"
    - Product performance: "What are the top selling products?"
    
    Args:
        question: Natural language question about business data
        limit: Maximum number of rows to return (uses config default if not specified)
        
    Returns:
        Dictionary containing query results, metadata, and success status
    """
    if limit is None:
        limit = Config.DEFAULT_QUERY_LIMIT
    
    # Enforce maximum limit for safety
    if limit > Config.MAX_QUERY_LIMIT:
        limit = Config.MAX_QUERY_LIMIT
        logger.warning(f"Query limit capped at {Config.MAX_QUERY_LIMIT}")
    
    logger.info(f"Processing question: {question} (limit: {limit})")
    result = query_gold_view(question, limit)
    logger.info(f"Query result success: {result.get('success', False)}")
    return result

@mcp.tool()
def list_available_data() -> dict:
    """
    List available Gold-layer views and supported question types.
    
    Returns:
        Dictionary containing available views and example questions for Milestone 1
    """
    return {
        "milestone": "1 - Core Business Questions",
        "available_views": get_available_views(),
        "supported_question_types": [
            "Daily sales trends and analysis",
            "Customer segment comparisons", 
            "Product performance analysis"
        ],
        "example_questions": [
            "What were daily sales this week?",
            "Which customer types spend the most?", 
            "What are the top selling products?",
            "How do Premium customers compare to Regular customers?",
            "Which product categories are performing best?",
            "Show me popular products in Food category",
            "Which categories perform better: Food vs Toys?",
            "What do Premium customers buy in Food vs Automotive?"
        ],
        "data_context": {
            "customer_types": Config.CUSTOMER_TYPES,
            "product_categories": Config.PRODUCT_CATEGORIES,
            "time_range": "Recent 7-30 days of transactional data"
        }
    }

@mcp.tool() 
def get_data_help() -> dict:
    """
    Get help information about available data and question formats.
    
    Returns:
        Dictionary with help information and guidance for users
    """
    return {
        "help": "I can help you analyze sales data from our Gold-layer views.",
        "how_to_ask": {
            "daily_sales": "Ask about 'daily sales', 'sales this week', 'revenue trends', or 'sales performance'",
            "customers": "Ask about 'customer types', 'Premium vs Regular', 'customer spending', or 'customer segments'", 
            "products": "Ask about 'top products', 'popular items', 'product performance', or 'best selling products'"
        },
        "available_data": {
            "gold_tables": list(Config.GOLD_TABLES.values()),
            "customer_segments": Config.CUSTOMER_TYPES,
            "product_categories": Config.PRODUCT_CATEGORIES
        },
        "query_limits": {
            "default_limit": Config.DEFAULT_QUERY_LIMIT,
            "maximum_limit": Config.MAX_QUERY_LIMIT,
            "timeout_seconds": Config.QUERY_TIMEOUT_SECONDS
        }
    }

def main():
    """Start the MCP server"""
    # Validate configuration before starting
    try:
        Config.validate_all()
        logger.info("Starting Snowflake Gold Query MCP Server...")
        logger.info(f"MCP server instance: {mcp}")
        # Note: FastMCP doesn't expose tools attribute directly
        logger.info("MCP server starting...")
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server startup error: {e}")
        logger.error(f"Error type: {type(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise

if __name__ == "__main__":
    main()
