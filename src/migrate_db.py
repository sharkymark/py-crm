#!/usr/bin/env python3
# filepath: /Users/markmilligan/Documents/src/py-crm/src/migrate_db.py
"""
Database Migration Script for CRM Application

This script handles database schema migrations for the CRM application.
It creates a backup of the existing database and updates the schema to match
the new requirements while preserving all existing data.
"""

import sqlite3
import os
import shutil
import datetime
from pathlib import Path

# Define paths
DATA_DIR = 'data'
DATABASE_NAME = os.path.join(DATA_DIR, 'crm.db')
BACKUP_DIR = os.path.join(DATA_DIR, 'backups')

def backup_database():
    """
    Create a backup of the current database in a timestamped file.
    Returns the path to the backup file.
    """
    # Ensure backup directory exists
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    # Create a timestamp for the backup file
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_DIR, f"crm_backup_{timestamp}.db")
    
    # Check if database file exists
    if not os.path.exists(DATABASE_NAME):
        print(f"Warning: Database file {DATABASE_NAME} does not exist. No backup created.")
        return None
    
    # Copy the database file to the backup
    shutil.copy2(DATABASE_NAME, backup_file)
    print(f"Database backup created at: {backup_file}")
    return backup_file

def get_table_columns(cursor, table_name):
    """
    Get the current columns for a table.
    Returns a list of column names.
    """
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cursor.fetchall()]
    return columns

def migrate_database():
    """
    Perform database migration to update schema while preserving data.
    """
    # First create a backup
    backup_file = backup_database()
    if backup_file is None and not os.path.exists(DATABASE_NAME):
        print("Creating new database with updated schema")
        # Just create the database with the new schema
        from database import create_tables
        create_tables()
        print("New database created successfully.")
        return True
    
    # Connect to the database
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        # Migration for Accounts table
        print("Checking Accounts table schema...")
        account_columns = get_table_columns(cursor, "Accounts")
        
        # Define the columns that should be in the Accounts table
        required_account_columns = {
            "description": "TEXT", 
            "website": "TEXT",
            "street": "TEXT",
            "city": "TEXT",
            "state": "TEXT",
            "zip": "TEXT",
            "country": "TEXT",
            "industry_id": "INTEGER" # New column for picklist reference
        }
        
        # Add any missing columns
        for column, data_type in required_account_columns.items():
            if column not in account_columns:
                print(f"Adding column '{column}' to Accounts table")
                cursor.execute(f"ALTER TABLE Accounts ADD COLUMN {column} {data_type}")
        
        # Check if the legacy industry column exists
        if "industry" in account_columns:
            # We need to remove the industry column, which requires recreating the table
            # in SQLite (since SQLite doesn't support DROP COLUMN directly)
            print("Removing legacy industry column from Accounts table...")
            
            # First, create a temporary table without the industry column
            cursor.execute("""
                CREATE TABLE Accounts_new (
                    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    industry_id INTEGER,
                    description TEXT,
                    website TEXT,
                    street TEXT,
                    city TEXT,
                    state TEXT,
                    zip TEXT,
                    country TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (industry_id) REFERENCES PicklistValue(picklist_value_id)
                )
            """)
            
            # Copy data from the old table to the new one
            cursor.execute("""
                INSERT INTO Accounts_new (
                    account_id, name, industry_id, description, website, street, city, 
                    state, zip, country, created_at
                )
                SELECT 
                    account_id, name, industry_id, description, website, street, city, 
                    state, zip, country, created_at
                FROM Accounts
            """)
            
            # Drop the old table and rename the new one
            cursor.execute("DROP TABLE Accounts")
            cursor.execute("ALTER TABLE Accounts_new RENAME TO Accounts")
            print("Legacy industry column removed successfully")
        
        # Migration for Contacts table
        print("Checking Contacts table schema...")
        contact_columns = get_table_columns(cursor, "Contacts")
        
        # Define the columns that should be in the Contacts table
        required_contact_columns = {
            "title": "TEXT",
            "description": "TEXT",
            "website": "TEXT",
            "street": "TEXT",
            "city": "TEXT",
            "state": "TEXT",
            "zip": "TEXT",
            "country": "TEXT"
        }
        
        # Add any missing columns
        for column, data_type in required_contact_columns.items():
            if column not in contact_columns:
                print(f"Adding column '{column}' to Contacts table")
                cursor.execute(f"ALTER TABLE Contacts ADD COLUMN {column} {data_type}")
        
        # Migration for Opportunities table
        print("Checking Opportunities table schema...")
        opportunity_columns = get_table_columns(cursor, "Opportunities")
        
        # Define the columns that should be in the Opportunities table
        required_opportunity_columns = {
            "stage_id": "INTEGER" # New column for stage picklist reference
        }
        
        # Add any missing columns
        for column, data_type in required_opportunity_columns.items():
            if column not in opportunity_columns:
                print(f"Adding column '{column}' to Opportunities table")
                cursor.execute(f"ALTER TABLE Opportunities ADD COLUMN {column} {data_type}")
        
        # Set up picklist tables
        print("Setting up picklist tables...")
        from .picklist import create_picklist_tables, migrate_existing_data
        
        # Create the picklist tables
        create_picklist_tables()
        
        # Skip initialization of default picklists - use admin menu instead
        print("NOTE: Default picklists initialization skipped - use Admin menu to manage picklists")
        
        # Migrate existing data to use picklists
        migrate_existing_data()
        
        # Commit all changes
        conn.commit()
        print("Database migration completed successfully.")
        return True
        
    except sqlite3.Error as e:
        print(f"Database migration error: {e}")
        if backup_file:
            print(f"Migration failed. You can restore from backup: {backup_file}")
        return False
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    success = migrate_database()
    if success:
        print("Migration completed successfully.")
    else:
        print("Migration failed. Please check the error messages above.")
