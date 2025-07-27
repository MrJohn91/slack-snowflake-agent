import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from agent.core import list_available_data, query_snowflake_gold

def test_list_available_data():
    result = list_available_data()
    assert "available_views" in result
    print("✅ Available views:", result["available_views"])

def test_query_example():
    result = query_snowflake_gold("What are the top selling products?")
    assert result.get("success", False) is True
    print("✅ Query result keys:", result.keys())

if __name__ == "__main__":
    test_list_available_data()
    test_query_example()
