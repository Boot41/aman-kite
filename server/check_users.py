#!/usr/bin/env python3

import sqlite3
import sys
from pathlib import Path

def check_users():
    # Try to find the database file
    db_paths = [
        "test.db",
        "app.db",
        "stock_trading.db"
    ]
    
    db_path = None
    for path in db_paths:
        if Path(path).exists():
            db_path = path
            break
    
    if not db_path:
        print("❌ No database file found. Checked:", db_paths)
        return
    
    print(f"📊 Using database: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if users table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        if not cursor.fetchone():
            print("❌ Users table does not exist")
            return
        
        # Get all users
        cursor.execute("SELECT user_id, username, email, created_at FROM users ORDER BY created_at DESC;")
        users = cursor.fetchall()
        
        if not users:
            print("📝 No users found in database")
        else:
            print(f"👥 Found {len(users)} registered users:")
            print("-" * 80)
            print(f"{'ID':<5} {'Username':<20} {'Email':<30} {'Created At':<20}")
            print("-" * 80)
            
            for user in users:
                user_id, username, email, created_at = user
                print(f"{user_id:<5} {username:<20} {email:<30} {created_at or 'N/A':<20}")
        
        # Check table structure
        print("\n🏗️  Users table structure:")
        cursor.execute("PRAGMA table_info(users);")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error checking database: {e}")

if __name__ == "__main__":
    check_users()
