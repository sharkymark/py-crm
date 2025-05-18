import sqlite3
import os # Import os module
import sys

# Define the path to the data directory and the database file
DATA_DIR = 'data'
DATABASE_NAME = os.path.join(DATA_DIR, 'crm.db') # Use os.path.join for cross-platform compatibility

def get_db_connection():
    """
    Establish a connection to the SQLite database.
    """
    conn = None
    try:
        # Ensure the data directory exists
        os.makedirs(DATA_DIR, exist_ok=True)
        conn = sqlite3.connect(DATABASE_NAME)
        conn.row_factory = sqlite3.Row  # Access columns by name
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        if conn:
            conn.close()
        return None

def create_tables():
    """
    Create the necessary tables in the database if they don't exist.
    """
    conn = get_db_connection()
    if conn is None:
        return

    cursor = conn.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Accounts (
                account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                industry TEXT,
                description TEXT,
                website TEXT,
                street TEXT,
                city TEXT,
                state TEXT,
                zip TEXT,
                country TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Contacts (
                contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                title TEXT,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                description TEXT,
                website TEXT,
                street TEXT,
                city TEXT,
                state TEXT,
                zip TEXT,
                country TEXT,
                account_id INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_id) REFERENCES Accounts (account_id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Opportunities (
                opportunity_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                amount REAL,
                close_date DATE,
                account_id INTEGER,
                contact_id INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_id) REFERENCES Accounts (account_id),
                FOREIGN KEY (contact_id) REFERENCES Contacts (contact_id)
            )
        """)

        conn.commit()
        print("Tables created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")
    finally:
        cursor.close()
        conn.close()

def check_schema():
    """
    Check if schema migration is needed by comparing columns in the database
    with the expected schema. Returns True if migration is needed, False otherwise.
    """
    # Check if database exists first
    if not os.path.exists(DATABASE_NAME):
        return False  # No migration needed, just create new tables
        
    conn = get_db_connection()
    if conn is None:
        return False
    
    cursor = conn.cursor()
    try:
        # Check Accounts table
        cursor.execute("PRAGMA table_info(Accounts)")
        columns = [row[1] for row in cursor.fetchall()]
        # Check for any of the new columns
        if "description" not in columns or "website" not in columns:
            return True
        
        # Check Contacts table
        cursor.execute("PRAGMA table_info(Contacts)")
        columns = [row[1] for row in cursor.fetchall()]
        # Check for any of the new columns
        if "title" not in columns or "description" not in columns:
            return True
            
        return False  # No migration needed
    except sqlite3.Error as e:
        print(f"Error checking schema: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def initialize_database():
    """
    Initialize the database, performing migrations if needed.
    """
    # Check if migration is needed
    if check_schema():
        print("Database schema needs migration. Running migration script...")
        try:
            # Import and run the migration script
            from .migrate_db import migrate_database
            migrate_database()
        except ImportError:
            print("Error: Could not import migration module.")
            print("Make sure migrate_db.py is in the same directory.")
    else:
        # Just create tables if needed
        create_tables()

if __name__ == '__main__':
    initialize_database()
