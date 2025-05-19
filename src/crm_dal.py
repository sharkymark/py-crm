# This file will contain the Data Access Layer (DAL) functions for performing CRUD operations on the CRM data (Accounts, Contacts, Opportunities).

import sqlite3
# Update import to use relative path
from .database import get_db_connection

# --- Account Operations ---
def create_account(name, industry_id=None, description=None, website=None, street=None, city=None, state=None, zip=None, country=None):
    """
    Create a new account in the database.
    
    Args:
        name (str): The account name (required)
        industry_id (int): The industry picklist ID (optional)
        description, website, street, city, state, zip, country: Optional account details
    
    Returns the account_id on success, None on failure.
    """
    conn = get_db_connection()
    if conn is None:
        return None

    cursor = conn.cursor()
    try:
        cursor.execute(
            """INSERT INTO Accounts 
               (name, industry_id, description, website, street, city, state, zip, country) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
            (name, industry_id, description, website, street, city, state, zip, country)
        )
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

def search_accounts(query):
    """
    Search for accounts by name (case-insensitive, partial match).
    Returns a list of matching account rows.
    """
    conn = get_db_connection()
    if conn is None:
        return []

    cursor = conn.cursor()
    try:
        # Use LIKE for partial, case-insensitive search
        search_term = '%' + query + '%'
        cursor.execute("SELECT * FROM Accounts WHERE name LIKE ?", (search_term,))
        accounts = cursor.fetchall()
        return accounts
    except sqlite3.Error as e:
        print(f"Database error searching accounts: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def update_account(account_id, name=None, industry_id=None, description=None, website=None, 
                street=None, city=None, state=None, zip=None, country=None):
    """
    Update an existing account in the database.
    
    The industry_id parameter should be an integer with the picklist_value_id
    
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
    if industry_id is not None:
        updates.append("industry_id = ?")
        params.append(industry_id)
    if description is not None:
        updates.append("description = ?")
        params.append(description)
    if website is not None:
        updates.append("website = ?")
        params.append(website)
    if street is not None:
        updates.append("street = ?")
        params.append(street)
    if city is not None:
        updates.append("city = ?")
        params.append(city)
    if state is not None:
        updates.append("state = ?")
        params.append(state)
    if zip is not None:
        updates.append("zip = ?")
        params.append(zip)
    if country is not None:
        updates.append("country = ?")
        params.append(country)

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
def create_contact(first_name, last_name, email, phone, account_id, title=None, description=None, 
                website=None, street=None, city=None, state=None, zip=None, country=None):
    """
    Create a new contact in the database.
    Returns the contact_id on success, None on failure.
    """
    conn = get_db_connection()
    if conn is None:
        return None

    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Contacts 
            (first_name, last_name, email, phone, account_id, title, description, 
            website, street, city, state, zip, country) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (first_name, last_name, email, phone, account_id, title, description, 
              website, street, city, state, zip, country))
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

def search_contacts(query):
    """
    Search for contacts by first name, last name, or email (case-insensitive, partial match).
    Returns a list of matching contact rows.
    """
    conn = get_db_connection()
    if conn is None:
        return []

    cursor = conn.cursor()
    try:
        # Use LIKE for partial, case-insensitive search across multiple fields
        search_term = '%' + query + '%'
        cursor.execute("""
            SELECT * FROM Contacts
            WHERE first_name LIKE ? OR last_name LIKE ? OR email LIKE ?
        """, (search_term, search_term, search_term))
        contacts = cursor.fetchall()
        return contacts
    except sqlite3.Error as e:
        print(f"Database error searching contacts: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_contacts_by_account(account_id):
    """
    Retrieve all contacts linked to a specific account.
    Returns a list of contact rows.
    """
    conn = get_db_connection()
    if conn is None:
        return []

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Contacts WHERE account_id = ?", (account_id,))
        contacts = cursor.fetchall()
        return contacts
    except sqlite3.Error as e:
        print(f"Database error getting contacts by account: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def update_contact(contact_id, first_name=None, last_name=None, email=None, phone=None, account_id=None,
                title=None, description=None, website=None, street=None, city=None, state=None, zip=None, country=None):
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
    if title is not None:
        updates.append("title = ?")
        params.append(title)
    if description is not None:
        updates.append("description = ?")
        params.append(description)
    if website is not None:
        updates.append("website = ?")
        params.append(website)
    if street is not None:
        updates.append("street = ?")
        params.append(street)
    if city is not None:
        updates.append("city = ?")
        params.append(city)
    if state is not None:
        updates.append("state = ?")
        params.append(state)
    if zip is not None:
        updates.append("zip = ?")
        params.append(zip)
    if country is not None:
        updates.append("country = ?")
        params.append(country)

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
def create_opportunity(name, description, amount, close_date, account_id, contact_id, stage=None):
    """
    Create a new opportunity in the database.
    
    The stage parameter can be either:
    - A picklist value ID (integer) already looked up
    - A string value, in which case we'll look up the ID or use the default stage
    - None, in which case we'll use the default stage
    
    Returns the opportunity_id on success, None on failure.
    """
    from .picklist import get_picklist_id_by_value, get_picklist_values
    
    conn = get_db_connection()
    if conn is None:
        return None

    cursor = conn.cursor()
    try:
        # Handle stage as picklist
        stage_id = None
        if stage:
            if isinstance(stage, int):
                stage_id = stage
            else:
                stage_id = get_picklist_id_by_value('stage', stage)
        else:
            # Use default stage if none provided
            stages = get_picklist_values('stage')
            if stages:
                default_stage = next((s for s in stages if s['is_default']), stages[0] if stages else None)
                if default_stage:
                    stage_id = default_stage['picklist_value_id']

        cursor.execute(
            "INSERT INTO Opportunities (name, description, amount, close_date, account_id, contact_id, stage_id) VALUES (?, ?, ?, ?, ?, ?, ?)", 
            (name, description, amount, close_date, account_id, contact_id, stage_id)
        )
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

def search_opportunities(query):
    """
    Search for opportunities by name or description (case-insensitive, partial match).
    Returns a list of matching opportunity rows.
    """
    conn = get_db_connection()
    if conn is None:
        return []

    cursor = conn.cursor()
    try:
        # Use LIKE for partial, case-insensitive search across multiple fields
        search_term = '%' + query + '%'
        cursor.execute("""
            SELECT * FROM Opportunities
            WHERE name LIKE ? OR description LIKE ?
        """, (search_term, search_term))
        opportunities = cursor.fetchall()
        return opportunities
    except sqlite3.Error as e:
        print(f"Database error searching opportunities: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_opportunities_by_account(account_id):
    """
    Retrieve all opportunities linked to a specific account.
    Returns a list of opportunity rows.
    """
    conn = get_db_connection()
    if conn is None:
        return []

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Opportunities WHERE account_id = ?", (account_id,))
        opportunities = cursor.fetchall()
        return opportunities
    except sqlite3.Error as e:
        print(f"Database error getting opportunities by account: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def update_opportunity(opportunity_id, name=None, description=None, amount=None, close_date=None, account_id=None, contact_id=None, stage=None):
    """
    Update an existing opportunity in the database.
    
    The stage parameter can be either:
    - A picklist value ID (integer) already looked up
    - A string value, in which case we'll look up the ID
    - None, in which case we won't update the stage
    
    Returns True if updated, False otherwise.
    """
    from .picklist import get_picklist_id_by_value
    
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
    if stage is not None:
        # Handle stage as picklist
        stage_id = None
        if isinstance(stage, int):
            stage_id = stage
        else:
            stage_id = get_picklist_id_by_value('stage', stage)
            
        if stage_id:
            updates.append("stage_id = ?")
            params.append(stage_id)

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
