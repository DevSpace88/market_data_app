#!/usr/bin/env python3
"""
Migration script to add AI-related columns to the users table
"""
import sqlite3
import os
from pathlib import Path

def migrate_database():
    """Add AI-related columns to the users table"""
    
    # Database path
    db_path = Path(__file__).parent / "market_analysis.db"
    
    if not db_path.exists():
        print("Database file not found. Creating new database...")
        return
    
    print(f"Migrating database: {db_path}")
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add AI-related columns if they don't exist
        ai_columns = [
            ("ai_provider", "TEXT DEFAULT 'openai'"),
            ("ai_api_key", "TEXT"),
            ("ai_model", "TEXT DEFAULT 'gpt-3.5-turbo'"),
            ("ai_temperature", "TEXT DEFAULT '0.7'"),
            ("ai_max_tokens", "INTEGER DEFAULT 1000")
        ]
        
        for column_name, column_def in ai_columns:
            if column_name not in columns:
                print(f"Adding column: {column_name}")
                cursor.execute(f"ALTER TABLE users ADD COLUMN {column_name} {column_def}")
            else:
                print(f"Column {column_name} already exists")
        
        # Commit changes
        conn.commit()
        print("✅ Migration completed successfully!")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()
