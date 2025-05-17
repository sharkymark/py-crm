import sqlite3

DATABASE_NAME = 'crm.db'

def get_db_connection():
    """
    Establish a connection to the SQLite database.
    """
    conn = None
    try:
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
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Contacts (
                contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
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

if __name__ == '__main__':
    create_tables()
