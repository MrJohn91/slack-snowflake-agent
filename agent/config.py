# config.py - Application settings and environment variables
# Configuration management for the Slack Snowflake Agent

import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Config:
    """All application settings in one place"""
    
    # Snowflake connection details
    SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
    SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD") 
    SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
    SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
    SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
    SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "GOLD")  
    SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE")
    
    # Slack settings
    SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
    SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")  # For socket mode
    SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
    
    # Application settings
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    
    # Query settings for Milestone 1
    DEFAULT_QUERY_LIMIT = int(os.getenv("DEFAULT_QUERY_LIMIT", "10"))
    MAX_QUERY_LIMIT = int(os.getenv("MAX_QUERY_LIMIT", "100"))
    QUERY_TIMEOUT_SECONDS = int(os.getenv("QUERY_TIMEOUT_SECONDS", "30"))
    
    # Product categories available in the system
    PRODUCT_CATEGORIES = [
        "Food", "Automotive", "Toys"  # Based on your real data context from requirements
    ]
    
    # Customer types available in the system  
    CUSTOMER_TYPES = ["Unknown", "Regular", "Premium"]
    
    # Gold table names (for reference)
    GOLD_TABLES = {
        "daily_sales": "DAILY_SALES_SUMMARY",
        "customer_affinity": "CUSTOMER_PRODUCT_AFFINITY_MONTHLY"
    }
    
    @classmethod
    def validate_snowflake(cls):
        """Check if all required Snowflake settings are present"""
        required_snowflake = [
            ("SNOWFLAKE_USER", cls.SNOWFLAKE_USER),
            ("SNOWFLAKE_PASSWORD", cls.SNOWFLAKE_PASSWORD),
            ("SNOWFLAKE_ACCOUNT", cls.SNOWFLAKE_ACCOUNT),
            ("SNOWFLAKE_WAREHOUSE", cls.SNOWFLAKE_WAREHOUSE),
            ("SNOWFLAKE_DATABASE", cls.SNOWFLAKE_DATABASE),
            ("SNOWFLAKE_SCHEMA", cls.SNOWFLAKE_SCHEMA)
        ]
        
        missing = [name for name, value in required_snowflake if not value]
        if missing:
            raise ValueError(f"Missing required Snowflake environment variables: {missing}")
        
        logger.info("✅ Snowflake configuration validated successfully")
        return True
    
    @classmethod
    def validate_slack(cls):
        """Check if Slack settings are present (optional for development)"""
        if not cls.SLACK_BOT_TOKEN:
            logger.warning("⚠️  SLACK_BOT_TOKEN not set - Slack integration disabled")
            return False
        
        logger.info("✅ Slack configuration validated successfully")
        return True
    
    @classmethod 
    def validate_all(cls):
        """Validate all configuration settings"""
        logger.info("Validating application configuration...")
        
        # Always require Snowflake
        cls.validate_snowflake()
        
        # Slack is optional for development/testing
        slack_ok = cls.validate_slack()
        
        # Log configuration summary
        logger.info(f"Configuration Summary:")
        logger.info(f"  Snowflake Database: {cls.SNOWFLAKE_DATABASE}")
        logger.info(f"  Snowflake Schema: {cls.SNOWFLAKE_SCHEMA}")
        logger.info(f"  Debug Mode: {cls.DEBUG}")
        logger.info(f"  Default Query Limit: {cls.DEFAULT_QUERY_LIMIT}")
        logger.info(f"  Slack Integration: {'Enabled' if slack_ok else 'Disabled'}")
        
        return True
    
    @classmethod
    def get_snowflake_connection_params(cls):
        """Get Snowflake connection parameters as a dictionary"""
        params = {
            "user": cls.SNOWFLAKE_USER,
            "password": cls.SNOWFLAKE_PASSWORD,
            "account": cls.SNOWFLAKE_ACCOUNT,
            "warehouse": cls.SNOWFLAKE_WAREHOUSE,
            "database": cls.SNOWFLAKE_DATABASE,
            "schema": cls.SNOWFLAKE_SCHEMA,
        }
        
        # Only add role if it's specified
        if cls.SNOWFLAKE_ROLE:
            params["role"] = cls.SNOWFLAKE_ROLE
            
        return params

# Create global config instance
config = Config()

def setup_logging():
    """Configure application logging based on config settings"""
    level = getattr(logging, config.LOG_LEVEL, logging.INFO)
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        force=True  # Override any existing logging config
    )
    
    if config.DEBUG:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")

if __name__ == "__main__":
    # Test the configuration
    setup_logging()
    config.validate_all()
    
    # Display connection info (without sensitive data)
    print(f"\nConnection Summary:")
    print(f"Snowflake Account: {config.SNOWFLAKE_ACCOUNT}")
    print(f"Database/Schema: {config.SNOWFLAKE_DATABASE}.{config.SNOWFLAKE_SCHEMA}")
    print(f"Available Gold Tables: {list(config.GOLD_TABLES.values())}")