#!/usr/bin/env python3
"""
Simple MCP Test Client
Tests your Snowflake MCP server by connecting and calling all available tools
"""

import asyncio
import json
import sys
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

class MCPTestClient:
    """Simple test client for your MCP server"""
    
    async def test_connection(self):
        """Test basic connection to MCP server"""
        print("🔍 Testing MCP server connection...")
        
        try:
            # Start your MCP server as subprocess
            server_params = StdioServerParameters(
                command="python", 
                args=["-m", "agent.core"]
            )
            
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    # Initialize the session
                    await session.initialize()
                    
                    # List available tools
                    tools = await session.list_tools()
                    print(f"✅ Connected! Available tools: {[tool.name for tool in tools.tools]}")
                    return session, tools.tools
                    
        except Exception as e:
            print(f"❌ Connection failed: {str(e)}")
            return None, None
    
    async def test_get_data_help(self, session):
        """Test the get_data_help tool"""
        print("\n🔍 Testing get_data_help tool...")
        try:
            result = await session.call_tool("get_data_help", arguments={})
            
            if result.content:
                data = json.loads(result.content[0].text)
                print("✅ get_data_help successful!")
                print(f"   Help sections: {list(data.keys())}")
                print(f"   Available data: {data.get('available_data', {}).get('gold_tables', [])}")
                return True
            else:
                print("❌ No response from get_data_help")
                return False
                
        except Exception as e:
            print(f"❌ get_data_help failed: {str(e)}")
            return False
    
    async def test_list_available_data(self, session):
        """Test the list_available_data tool"""
        print("\n🔍 Testing list_available_data tool...")
        try:
            result = await session.call_tool("list_available_data", arguments={})
            
            if result.content:
                data = json.loads(result.content[0].text)
                print("✅ list_available_data successful!")
                print(f"   Milestone: {data.get('milestone')}")
                print(f"   Available views: {data.get('available_views', [])}")
                print(f"   Example questions: {len(data.get('example_questions', []))} questions")
                return True
            else:
                print("❌ No response from list_available_data")
                return False
                
        except Exception as e:
            print(f"❌ list_available_data failed: {str(e)}")
            return False
    
    async def test_query_snowflake_gold(self, session, question="What were daily sales this week?"):
        """Test the main query tool"""
        print(f"\n🔍 Testing query_snowflake_gold with: '{question}'")
        try:
            result = await session.call_tool(
                "query_snowflake_gold", 
                arguments={"question": question, "limit": 5}
            )
            
            if result.content:
                data = json.loads(result.content[0].text)
                
                if data.get("success"):
                    print("✅ query_snowflake_gold successful!")
                    print(f"   View used: {data.get('view_name')}")
                    print(f"   Rows returned: {data.get('row_count', 0)}")
                    
                    # Show first row of data
                    if data.get('data'):
                        first_row = data['data'][0]
                        print(f"   Sample data: {dict(list(first_row.items())[:3])}...")  # First 3 columns
                    return True
                else:
                    print(f"❌ Query failed: {data.get('error')}")
                    return False
            else:
                print("❌ No response from query_snowflake_gold")
                return False
                
        except Exception as e:
            print(f"❌ query_snowflake_gold failed: {str(e)}")
            return False
    
    async def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting MCP Server Tests")
        print("=" * 50)
        
        # Test connection
        session, tools = await self.test_connection()
        if not session:
            return False
        
        # Keep session alive for all tests
        try:
            # Test all three tools
            tests = [
                ("Help Tool", lambda: self.test_get_data_help(session)),
                ("List Data Tool", lambda: self.test_list_available_data(session)),
                ("Query Tool - Daily Sales", lambda: self.test_query_snowflake_gold(session, "What were daily sales this week?")),
                ("Query Tool - Customer Analysis", lambda: self.test_query_snowflake_gold(session, "Which customer types spend the most?")),
                ("Query Tool - Product Analysis", lambda: self.test_query_snowflake_gold(session, "What are the top selling products?"))
            ]
            
            passed = 0
            total = len(tests)
            
            for test_name, test_func in tests:
                print(f"\n{'='*20} {test_name} {'='*20}")
                try:
                    if await test_func():
                        passed += 1
                except Exception as e:
                    print(f"❌ {test_name} failed with exception: {e}")
            
            print(f"\n{'='*50}")
            print(f"📊 Test Results: {passed}/{total} tests passed")
            
            if passed == total:
                print("🎉 All tests passed! Your MCP server is working perfectly!")
                print("\n💡 Next steps:")
                print("   1. Your MCP server is ready for AI clients")
                print("   2. You can now integrate with Claude Desktop (when ready)")
                print("   3. Consider adding Slack integration next")
            else:
                print("⚠️  Some tests failed. Check the errors above.")
            
            return passed == total
            
        except Exception as e:
            print(f"❌ Test session failed: {e}")
            return False

async def main():
    """Main test function"""
    client = MCPTestClient()
    success = await client.run_all_tests()
    return success

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        sys.exit(1)