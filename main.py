#!/usr/bin/env python3
"""
Main entry point for the Snowflake Agent MCP Server
Starts the MCP server that provides tools for querying Snowflake Gold-layer data
"""

import sys
import os

# project root
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def main():
    """Start the MCP server"""
    from agent.core import main as start_server
    start_server()

if __name__ == "__main__":
    main()