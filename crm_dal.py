# This file will contain the Data Access Layer (DAL) functions for performing CRUD operations on the CRM data (Accounts, Contacts, Opportunities).

import sqlite3
from database import get_db_connection

# --- Account Operations ---
def create_account(name, industry):
    """
    Create a new account in the database.
    """
    conn = get_db_connection()
    if conn is None:
        return None

    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Accounts (name, industry) VALUES (?, ?)", (name, industry))
        conn.commit()
        account_id = cursor.lastrowid
        print(f"Account created with ID: {account_id}")
        return account_id
    except sqlite3.Error as e:
        print(f"Error creating account: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_account(account_id):
    """
    Retrieve an account from the database by its ID.
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
        print(f"Error getting account: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def update_account(account_id, name, industry):
    """
    Update an existing account in the database.
    """
    conn = get_db_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Accounts SET name = ?, industry = ? WHERE account_id = ?", (name, industry, account_id))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Account with ID {account_id} updated successfully.")
            return True
        else:
            print(f"Account with ID {account_id} not found.")
            return False
    except sqlite3.Error as e:
        print(f"Error updating account: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def delete_account(account_id):
    """
    Delete an account from the database.
    """
    conn = get_db_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Accounts WHERE account_id = ?", (account_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Account with ID {account_id} deleted successfully.")
            return True
        else:
            print(f"Account with ID {account_id} not found.")
            return False
    except sqlite3.Error as e:
        print(f"Error deleting account: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

# --- Contact Operations ---
def create_contact(first_name, last_name, email, phone, account_id):
    """
    Create a new contact in the database.
    """
    conn = get_db_connection()
    if conn is None:
        return None

    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Contacts (first_name, last_name, email, phone, account_id) VALUES (?, ?, ?, ?, ?)", (first_name, last_name, email, phone, account_id))
        conn.commit()
        contact_id = cursor.lastrowid
        print(f"Contact created with ID: {contact_id}")
        return contact_id
    except sqlite3.Error as e:
        print(f"Error creating contact: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_contact(contact_id):
    """
    Retrieve a contact from the database by its ID.
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
        print(f"Error getting contact: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def update_contact(contact_id, first_name, last_name, email, phone, account_id):
    """
    Update an existing contact in the database.
    """
    conn = get_db_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Contacts SET first_name = ?, last_name = ?, email = ?, phone = ?, account_id = ? WHERE contact_id = ?", (first_name, last_name, email, phone, account_id, contact_id))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Contact with ID {contact_id} updated successfully.")
            return True
        else:
            print(f"Contact with ID {contact_id} not found.")
            return False
    except sqlite3.Error as e:
        print(f"Error updating contact: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def delete_contact(contact_id):
    """
    Delete a contact from the database.
    """
    conn = get_db_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Contacts WHERE contact_id = ?", (contact_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Contact with ID {contact_id} deleted successfully.")
            return True
        else:
            print(f"Contact with ID {contact_id} not found.")
            return False
    except sqlite3.Error as e:
        print(f"Error deleting contact: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

# --- Opportunity Operations ---
def create_opportunity(name, description, amount, close_date, account_id, contact_id):
    """
    Create a new opportunity in the database.
    """
    conn = get_db_connection()
    if conn is None:
        return None

    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Opportunities (name, description, amount, close_date, account_id, contact_id) VALUES (?, ?, ?, ?, ?, ?)", (name, description, amount, close_date, account_id, contact_id))
        conn.commit()
        opportunity_id = cursor.lastrowid
        print(f"Opportunity created with ID: {opportunity_id}")
        return opportunity_id
    except sqlite3.Error as e:
        print(f"Error creating opportunity: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_opportunity(opportunity_id):
    """
    Retrieve an opportunity from the database by its ID.
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
        print(f"Error getting opportunity: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def update_opportunity(opportunity_id, name, description, amount, close_date, account_id, contact_id):
    """
    Update an existing opportunity in the database.
    """
    conn = get_db_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Opportunities SET name = ?, description = ?, amount = ?, close_date = ?, account_id = ?, contact_id = ? WHERE opportunity_id = ?", (name, description, amount, close_date, account_id, contact_id, opportunity_id))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Opportunity with ID {opportunity_id} updated successfully.")
            return True
        else:
            print(f"Opportunity with ID {opportunity_id} not found.")
            return False
    except sqlite3.Error as e:
        print(f"Error updating opportunity: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def delete_opportunity(opportunity_id):
    """
    Delete an opportunity from the database.
    """
    conn = get_db_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Opportunities WHERE opportunity_id = ?", (opportunity_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Opportunity with ID {opportunity_id} deleted successfully.")
            return True
        else:
            print(f"Opportunity with ID {opportunity_id} not found.")
            return False
    except sqlite3.Error as e:
        print(f"Error deleting opportunity: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
