#!/usr/bin/env python3
"""
Test script for user GPU logging functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.shell_ops import get_user_gpu_usage
from utils.db import insert_user_gpu_log, get_recent_user_gpu_logs, init_db

def test_user_gpu_logging():
    """Test the user GPU logging functionality"""
    print("Testing User GPU Logging Functionality")
    print("=" * 50)
    
    # Initialize database
    print("1. Initializing database...")
    init_db()
    print("   ✓ Database initialized")
    
    # Test getting current user GPU usage
    print("\n2. Getting current user GPU usage...")
    success, user_data = get_user_gpu_usage()
    if success:
        print(f"   ✓ Successfully retrieved user GPU usage data")
        print(f"   Found {len(user_data)} user(s) with GPU usage:")
        for user in user_data:
            print(f"     - {user['username']}: {user['gpu_memory_mib']} MiB ({user['gpu_memory_percentage']}%)")
    else:
        print(f"   ✗ Failed to get user GPU usage: {user_data}")
        return False
    
    # Test inserting user GPU usage data
    print("\n3. Testing database insertion...")
    try:
        for user in user_data:
            insert_user_gpu_log(
                username=user['username'],
                gpu_memory_mib=user['gpu_memory_mib'],
                gpu_memory_percentage=user['gpu_memory_percentage']
            )
            print(f"   ✓ Inserted data for user: {user['username']}")
        print("   ✓ All user data inserted successfully")
    except Exception as e:
        print(f"   ✗ Error inserting data: {str(e)}")
        return False
    
    # Test retrieving historical data
    print("\n4. Testing historical data retrieval...")
    try:
        logs = get_recent_user_gpu_logs(hours=1)  # Get last hour
        print(f"   ✓ Retrieved {len(logs)} historical log entries")
        if logs:
            print("   Sample log entry:")
            username, memory_mib, memory_pct, timestamp = logs[-1]
            print(f"     - User: {username}, Memory: {memory_mib} MiB ({memory_pct}%), Time: {timestamp}")
    except Exception as e:
        print(f"   ✗ Error retrieving historical data: {str(e)}")
        return False
    
    print("\n" + "=" * 50)
    print("✓ All tests passed! User GPU logging is working correctly.")
    return True

if __name__ == "__main__":
    test_user_gpu_logging() 