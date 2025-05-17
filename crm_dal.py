# This file will contain the Data Access Layer (DAL) functions for performing CRUD operations on the CRM data (Accounts, Contacts, Opportunities).

import sqlite3
from database import get_db_connection

# --- Account Operations ---
def create_account(name, industry):
    """
    Create a new account in the database.
    Returns the account_id on success, None on failure.
    """
    conn = get_db_connection()
    if conn is None:
        return None

    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Accounts (name, industry) VALUES (?, ?)", (name, industry))
        conn.commit()
        account_id = cursor.lastrowid
        return account_id
    except sqlite3.IntegrityError as e:
        # Handle cases like unique constraints if added later
        print(f"Integrity error creating account: {e}")
        return None
    except sqlite3.Error as e:
        print(f"Database error creating account: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_account(account_id):
    """
    Retrieve an account from the database by its ID.
    Returns the account row (as a dict-like object) on success, None if not found or on error.
    """
    conn = get_db_connection()
    if conn is None:
        return None

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Accounts WHERE account_id = ?", (account_id,))
        account = cursor.fetchone()
        return account
    except sqlite3.Error as e:
        print(f"Database error getting account: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def list_accounts():
    """
    Retrieve all accounts from the database.
    Returns a list of account rows.
    """
    conn = get_db_connection()
    if conn is None:
        return []

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Accounts")
        accounts = cursor.fetchall()
        return accounts
    except sqlite3.Error as e:
        print(f"Database error listing accounts: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def update_account(account_id, name=None, industry=None):
    """
    Update an existing account in the database.
    Returns True if updated, False otherwise.
    """
    conn = get_db_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    updates = []
    params = []

    if name is not None:
        updates.append("name = ?")
        params.append(name)
    if industry is not None:
        updates.append("industry = ?")
        params.append(industry)

    if not updates:
        # No fields to update
        return False

    query = f"UPDATE Accounts SET {', '.join(updates)} WHERE account_id = ?"
    params.append(account_id)

    try:
        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Database error updating account: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def delete_account(account_id):
    """
    Delete an account from the database.
    Returns True if deleted, False otherwise.
    """
    conn = get_db_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        # Consider adding ON DELETE CASCADE to foreign keys or handle related records here
        cursor.execute("DELETE FROM Accounts WHERE account_id = ?", (account_id,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Database error deleting account: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# --- Contact Operations ---
def create_contact(first_name, last_name, email, phone, account_id):
    """
    Create a new contact in the database.
    Returns the contact_id on success, None on failure.
    """
    conn = get_db_connection()
    if conn is None:
        return None

    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Contacts (first_name, last_name, email, phone, account_id) VALUES (?, ?, ?, ?, ?)", (first_name, last_name, email, phone, account_id))
        conn.commit()
        contact_id = cursor.lastrowid
        return contact_id
    except sqlite3.IntegrityError as e:
        print(f"Integrity error creating contact: {e}")
        return None
    except sqlite3.Error as e:
        print(f"Database error creating contact: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_contact(contact_id):
    """
    Retrieve a contact from the database by its ID.
    Returns the contact row (as a dict-like object) on success, None if not found or on error.
    """
    conn = get_db_connection()
    if conn is None:
        return None

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Contacts WHERE contact_id = ?", (contact_id,))
        contact = cursor.fetchone()
        return contact
    except sqlite3.Error as e:
        print(f"Database error getting contact: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def list_contacts():
    """
    Retrieve all contacts from the database.
    Returns a list of contact rows.
    """
    conn = get_db_connection()
    if conn is None:
        return []

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Contacts")
        contacts = cursor.fetchall()
        return contacts
    except sqlite3.Error as e:
        print(f"Database error listing contacts: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def update_contact(contact_id, first_name=None, last_name=None, email=None, phone=None, account_id=None):
    """
    Update an existing contact in the database.
    Returns True if updated, False otherwise.
    """
    conn = get_db_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    updates = []
    params = []

    if first_name is not None:
        updates.append("first_name = ?")
        params.append(first_name)
    if last_name is not None:
        updates.append("last_name = ?")
        params.append(last_name)
    if email is not None:
        updates.append("email = ?")
        params.append(email)
    if phone is not None:
        updates.append("phone = ?")
        params.append(phone)
    if account_id is not None:
        updates.append("account_id = ?")
        params.append(account_id)

    if not updates:
        # No fields to update
        return False

    query = f"UPDATE Contacts SET {', '.join(updates)} WHERE contact_id = ?"
    params.append(contact_id)

    try:
        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.IntegrityError as e:
        print(f"Integrity error updating contact: {e}")
        return False
    except sqlite3.Error as e:
        print(f"Database error updating contact: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def delete_contact(contact_id):
    """
    Delete a contact from the database.
    Returns True if deleted, False otherwise.
    """
    conn = get_db_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Contacts WHERE contact_id = ?", (contact_id,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Database error deleting contact: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# --- Opportunity Operations ---
def create_opportunity(name, description, amount, close_date, account_id, contact_id):
    """
    Create a new opportunity in the database.
    Returns the opportunity_id on success, None on failure.
    """
    conn = get_db_connection()
    if conn is None:
        return None

    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Opportunities (name, description, amount, close_date, account_id, contact_id) VALUES (?, ?, ?, ?, ?, ?)", (name, description, amount, close_date, account_id, contact_id))
        conn.commit()
        opportunity_id = cursor.lastrowid
        return opportunity_id
    except sqlite3.IntegrityError as e:
        print(f"Integrity error creating opportunity: {e}")
        return None
    except sqlite3.Error as e:
        print(f"Database error creating opportunity: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_opportunity(opportunity_id):
    """
    Retrieve an opportunity from the database by its ID.
    Returns the opportunity row (as a dict-like object) on success, None if not found or on error.
    """
    conn = get_db_connection()
    if conn is None:
        return None

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Opportunities WHERE opportunity_id = ?", (opportunity_id,))
        opportunity = cursor.fetchone()
        return opportunity
    except sqlite3.Error as e:
        print(f"Database error getting opportunity: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def list_opportunities():
    """
    Retrieve all opportunities from the database.
    Returns a list of opportunity rows.
    """
    conn = get_db_connection()
    if conn is None:
        return []

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Opportunities")
        opportunities = cursor.fetchall()
        return opportunities
    except sqlite3.Error as e:
        print(f"Database error listing opportunities: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def update_opportunity(opportunity_id, name=None, description=None, amount=None, close_date=None, account_id=None, contact_id=None):
    """
    Update an existing opportunity in the database.
    Returns True if updated, False otherwise.
    """
    conn = get_db_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    updates = []
    params = []

    if name is not None:
        updates.append("name = ?")
        params.append(name)
    if description is not None:
        updates.append("description = ?")
        params.append(description)
    if amount is not None:
        updates.append("amount = ?")
        params.append(amount)
    if close_date is not None:
        updates.append("close_date = ?")
        params.append(close_date)
    if account_id is not None:
        updates.append("account_id = ?")
        params.append(account_id)
    if contact_id is not None:
        updates.append("contact_id = ?")
        params.append(contact_id)

    if not updates:
        # No fields to update
        return False

    query = f"UPDATE Opportunities SET {', '.join(updates)} WHERE opportunity_id = ?"
    params.append(opportunity_id)

    try:
        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.IntegrityError as e:
        print(f"Integrity error updating opportunity: {e}")
        return False
    except sqlite3.Error as e:
        print(f"Database error updating opportunity: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def delete_opportunity(opportunity_id):
    """
    Delete an opportunity from the database.
    Returns True if deleted, False otherwise.
    """
    conn = get_db_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Opportunities WHERE opportunity_id = ?", (opportunity_id,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Database error deleting opportunity: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
