# test_snowflake_connection.py
# Quick test to verify Snowflake connectivity and table access

from config import config, setup_logging
from agent.tools.snowflake_tools import get_snowflake_connection, get_available_views
import logging

def test_config():
    """Test configuration loading"""
    print("🔧 Testing Configuration...")
    try:
        config.validate_all()
        print("✅ Configuration loaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_snowflake_connection():
    """Test basic Snowflake connection"""
    print("\n🔗 Testing Snowflake Connection...")
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        # Test basic connection
        cursor.execute("SELECT CURRENT_VERSION()")
        version = cursor.fetchone()[0]
        print(f"✅ Connected to Snowflake version: {version}")
        
        # Test database/schema access
        cursor.execute("SELECT CURRENT_DATABASE(), CURRENT_SCHEMA()")
        db_info = cursor.fetchone()
        print(f"✅ Database: {db_info[0]}, Schema: {db_info[1]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_gold_tables():
    """Test access to Gold tables"""
    print("\n📊 Testing Gold Table Access...")
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        # Test DAILY_SALES_SUMMARY table
        table_name = config.GOLD_TABLES["daily_sales"]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"✅ {table_name}: {count:,} rows available")
        
        # Test table structure
        cursor.execute(f"DESCRIBE TABLE {table_name}")
        columns = cursor.fetchall()
        print(f"✅ {table_name} has {len(columns)} columns")
        
        # Show sample data
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
        sample_data = cursor.fetchall()
        print(f"✅ Sample data retrieved: {len(sample_data)} rows")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Table access error: {e}")
        return False

def test_product_categories():
    """Test actual product categories in the data"""
    print("\n🏷️  Testing Product Categories...")
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        table_name = config.GOLD_TABLES["daily_sales"]
        cursor.execute(f"""
            SELECT DISTINCT PRODUCT_CATEGORY, COUNT(*) as count
            FROM {table_name} 
            GROUP BY PRODUCT_CATEGORY 
            ORDER BY count DESC
        """)
        categories = cursor.fetchall()
        
        print(f"✅ Found {len(categories)} product categories:")
        for category, count in categories:
            print(f"   - {category}: {count:,} transactions")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Category test error: {e}")
        return False

def main():
    """Run all tests"""
    setup_logging()
    
    print("🚀 Starting Snowflake Configuration Tests...\n")
    
    # Run tests in order
    tests = [
        ("Configuration", test_config),
        ("Snowflake Connection", test_snowflake_connection), 
        ("Gold Tables", test_gold_tables),
        ("Product Categories", test_product_categories)
    ]
    
    results = {}
    for test_name, test_func in tests:
        results[test_name] = test_func()
        if not results[test_name]:
            print(f"\n❌ {test_name} test failed - stopping here")
            break
    
    # Summary
    print(f"\n{'='*50}")
    print("🏁 Test Summary:")
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"   {test_name}: {status}")
    
    if all(results.values()):
        print(f"\n🎉 All tests passed! Your Snowflake setup is ready for MCP server!")
    else:
        print(f"\n🔧 Fix the failing tests before proceeding.")

if __name__ == "__main__":
    main()