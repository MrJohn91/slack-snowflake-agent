# agent/tools/snowflake_tools.py
# Snowflake tools for MCP server - Milestone 1 implementation
# Targets specific Gold views: DAILY_SALES_SUMMARY and CUSTOMER_PRODUCT_AFFINITY_MONTHLY

import sys
import os
# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import snowflake.connector
from agent.config import Config
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

def get_snowflake_connection():
    """Create and return a Snowflake connection using centralized config"""
    return snowflake.connector.connect(**Config.get_snowflake_connection_params())

def query_gold_view(question: str, limit: int = 10) -> Dict[str, Any]:
    """
    Query Snowflake Gold views based on natural language question.
    
    For Milestone 1, supports:
    - Daily sales questions -> DAILY_SALES_SUMMARY
    - Customer segment questions -> DAILY_SALES_SUMMARY (aggregated)
    - Product performance questions -> DAILY_SALES_SUMMARY (aggregated)
    
    Args:
        question: Natural language question from user
        limit: Maximum number of rows to return
        
    Returns:
        Dict containing query results, view used, and metadata
    """
    
    # Simple intent recognition for Milestone 1
    question_lower = question.lower()
    
    if any(word in question_lower for word in ['daily sales', 'sales this week', 'sales trend', 'revenue']):
        view_name = Config.GOLD_TABLES["daily_sales"]
        # Query for recent daily sales data - aggregated by date and category
        sql_query = f"""
            SELECT 
                TRANSACTION_DATE,
                PRODUCT_CATEGORY,
                CUSTOMER_TYPE,
                COUNT(*) as TRANSACTION_COUNT,
                SUM(TOTAL_QUANTITY_SOLD) as DAILY_QUANTITY,
                SUM(TOTAL_REVENUE) as DAILY_REVENUE,
                ROUND(AVG(AVG_PRICE_PER_UNIT), 2) as AVG_PRICE_PER_UNIT
            FROM {view_name} 
            WHERE TRANSACTION_DATE >= DATEADD(day, -7, CURRENT_DATE())
            GROUP BY TRANSACTION_DATE, PRODUCT_CATEGORY, CUSTOMER_TYPE
            ORDER BY TRANSACTION_DATE DESC, DAILY_REVENUE DESC 
            LIMIT {limit}
        """
    
    elif any(word in question_lower for word in ['customer segment', 'customer type', 'premium', 'regular', 'unknown']):
        view_name = Config.GOLD_TABLES["daily_sales"]  # Using daily sales for customer analysis
        # Query for customer type analysis
        sql_query = f"""
            SELECT 
                CUSTOMER_TYPE,
                PRODUCT_CATEGORY,
                COUNT(*) as PURCHASE_COUNT,
                SUM(TOTAL_QUANTITY_SOLD) as TOTAL_QUANTITY,
                SUM(TOTAL_REVENUE) as TOTAL_REVENUE,
                ROUND(AVG(TOTAL_REVENUE), 2) as AVG_REVENUE_PER_PURCHASE
            FROM {view_name}
            WHERE TRANSACTION_DATE >= DATEADD(day, -30, CURRENT_DATE())
            GROUP BY CUSTOMER_TYPE, PRODUCT_CATEGORY
            ORDER BY TOTAL_REVENUE DESC
            LIMIT {limit}
        """
    
    elif any(word in question_lower for word in ['product', 'popular', 'top selling', 'best']):
        view_name = Config.GOLD_TABLES["daily_sales"]
        # Query for top products
        sql_query = f"""
            SELECT 
                PRODUCT_NAME,
                PRODUCT_CATEGORY,
                COUNT(*) as SALES_COUNT,
                SUM(TOTAL_QUANTITY_SOLD) as TOTAL_QUANTITY,
                SUM(TOTAL_REVENUE) as TOTAL_REVENUE,
                ROUND(AVG(AVG_PRICE_PER_UNIT), 2) as AVG_PRICE
            FROM {view_name}
            WHERE TRANSACTION_DATE >= DATEADD(day, -30, CURRENT_DATE())
            GROUP BY PRODUCT_NAME, PRODUCT_CATEGORY
            ORDER BY TOTAL_REVENUE DESC
            LIMIT {limit}
        """
    
    else:
        return {
            "success": False,
            "error": "Question not supported in Milestone 1. Try asking about daily sales, customer types, or popular products.",
            "supported_questions": [
                "What were daily sales this week?",
                "Which customer types spend the most?",
                "What are the top selling products?",
                "How do Premium customers compare to Regular customers?",
                "Which product categories are most popular?"
            ]
        }
    
    # Execute the query
    try:
        logger.info(f"Executing query on {view_name}")
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        cursor.execute(sql_query)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        results = [dict(zip(columns, row)) for row in rows]
        
        cursor.close()
        conn.close()
        
        logger.info(f"Query successful: {len(results)} rows returned")
        
        return {
            "success": True,
            "view_name": view_name,
            "sql_query": sql_query,
            "data": results,
            "row_count": len(results),
            "question": question
        }
        
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        return {
            "success": False,
            "error": f"Database error: {str(e)}",
            "view_name": view_name,
            "sql_query": sql_query
        }

def get_available_views() -> List[str]:
    """Return list of available Gold views for Milestone 1"""
    return list(Config.GOLD_TABLES.values())
