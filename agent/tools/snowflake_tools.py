# Snowflake tools for MCP server
# Natural language to SQL query conversion

from mcp.api import tool
import snowflake.connector
import os

@tool()
def query_gold_view(view_name: str, limit: int = 10) -> list[dict]:
    """
    Query a Snowflake Gold-layer view and return top results.
    """
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        role=os.getenv("SNOWFLAKE_ROLE")
    )

    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM {view_name} LIMIT {limit}")
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return results
    finally:
        cursor.close()
        conn.close()

