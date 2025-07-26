
# 

from fastmcp import FastMCP
from mcp.tools.snowflake_tools import query_gold_view

mcp = FastMCP("Snowflake Gold Query MCP Server")
mcp.add_tool(query_gold_view)

def main():
    mcp.run()

if __name__ == "__main__":
    main()
