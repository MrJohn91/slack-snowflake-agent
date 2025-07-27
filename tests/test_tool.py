import sys
import os

# Add the project root to sys.path if not already added
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the actual MCP tool function
from agent.core import query_snowflake_gold

def run_test():
    question = "What are the top selling products?"
    limit = 10
    result = query_snowflake_gold(question, limit)
    
    print("✅ Tool test succeeded!")
    print("Returned keys:", result.keys())
    print("Sample row:", result.get("data", [])[0] if result.get("data") else "No data")

if __name__ == "__main__":
    run_test()
