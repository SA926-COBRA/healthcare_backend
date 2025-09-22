#!/usr/bin/env python3
"""
Compare PostgreSQL and SQLite databases to ensure identical content
"""

import os
import sys
from sqlalchemy import create_engine, text
from app.core.config import settings

def compare_databases():
    """Compare PostgreSQL and SQLite databases"""
    print("🔍 Comparing PostgreSQL and SQLite Databases...")
    print("=" * 60)
    
    try:
        # Connect to PostgreSQL
        print("Connecting to PostgreSQL...")
        postgres_url = settings.DATABASE_URL
        postgres_engine = create_engine(postgres_url)
        
        # Connect to SQLite
        print("Connecting to SQLite...")
        sqlite_url = settings.SQLITE_URL
        sqlite_engine = create_engine(sqlite_url)
        
        # Get table names
        with postgres_engine.connect() as conn:
            postgres_tables = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name
            """)).fetchall()
        
        with sqlite_engine.connect() as conn:
            sqlite_tables = conn.execute(text("""
                SELECT name 
                FROM sqlite_master 
                WHERE type='table' 
                ORDER BY name
            """)).fetchall()
        
        # Compare table names
        postgres_table_names = [row[0] for row in postgres_tables]
        sqlite_table_names = [row[0] for row in sqlite_tables]
        
        print(f"\n📊 Table Comparison:")
        print(f"PostgreSQL tables: {len(postgres_table_names)}")
        print(f"SQLite tables: {len(sqlite_table_names)}")
        
        if set(postgres_table_names) == set(sqlite_table_names):
            print("✅ Table names match!")
        else:
            print("❌ Table names differ!")
            print(f"PostgreSQL only: {set(postgres_table_names) - set(sqlite_table_names)}")
            print(f"SQLite only: {set(sqlite_table_names) - set(postgres_table_names)}")
        
        # Compare data in each table
        print(f"\n📋 Data Comparison:")
        for table_name in postgres_table_names:
            if table_name in sqlite_table_names:
                # Count rows in PostgreSQL
                with postgres_engine.connect() as conn:
                    postgres_count = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}")).fetchone()[0]
                
                # Count rows in SQLite
                with sqlite_engine.connect() as conn:
                    sqlite_count = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}")).fetchone()[0]
                
                if postgres_count == sqlite_count:
                    print(f"✅ {table_name}: {postgres_count} rows (both databases)")
                else:
                    print(f"❌ {table_name}: PostgreSQL={postgres_count}, SQLite={sqlite_count}")
        
        # Compare specific user data
        print(f"\n👥 User Data Comparison:")
        with postgres_engine.connect() as conn:
            postgres_users = conn.execute(text("SELECT email, full_name, role FROM users ORDER BY email")).fetchall()
        
        with sqlite_engine.connect() as conn:
            sqlite_users = conn.execute(text("SELECT email, full_name, role FROM users ORDER BY email")).fetchall()
        
        if postgres_users == sqlite_users:
            print("✅ User data matches!")
            for user in postgres_users:
                print(f"  - {user[0]} ({user[1]}) - {user[2]}")
        else:
            print("❌ User data differs!")
            print("PostgreSQL users:", postgres_users)
            print("SQLite users:", sqlite_users)
        
        print("\n" + "=" * 60)
        print("🎉 Database comparison complete!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error comparing databases: {e}")
        return False

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Usage: python compare_databases.py")
        print("This script compares PostgreSQL and SQLite databases to ensure identical content.")
        return
    
    success = compare_databases()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
