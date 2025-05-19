#!/usr/bin/env python3
# filepath: /Users/markmilligan/Documents/src/py-crm/src/picklist.py
"""
Picklist Management for CRM Application

This module provides functions to manage picklists in the CRM application.
Picklists are predefined lists of values that users can select from.
"""

import sqlite3
import csv
import os
from .database import get_db_connection

def create_picklist_tables():
    """
    Create picklist tables in the database if they don't exist.
    """
    conn = get_db_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        # Create PicklistType table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS PicklistType (
                picklist_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                entity_type TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create PicklistValue table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS PicklistValue (
                picklist_value_id INTEGER PRIMARY KEY AUTOINCREMENT,
                picklist_type_id INTEGER NOT NULL,
                value TEXT NOT NULL,
                display_order INTEGER DEFAULT 0,
                is_default BOOLEAN DEFAULT 0,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (picklist_type_id) REFERENCES PicklistType(picklist_type_id),
                UNIQUE (picklist_type_id, value)
            )
        """)

        conn.commit()
        print("Picklist tables created successfully.")
        return True
    except sqlite3.Error as e:
        print(f"Error creating picklist tables: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def create_picklist_type(name, entity_type, description=None):
    """
    Create a new picklist type.
    
    Args:
        name (str): The name of the picklist (e.g., 'industry', 'stage')
        entity_type (str): The entity this picklist belongs to (e.g., 'account', 'opportunity')
        description (str, optional): Description of the picklist
        
    Returns:
        int: The ID of the new picklist type, or None on failure
    """
    conn = get_db_connection()
    if conn is None:
        return None

    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO PicklistType (name, description, entity_type) VALUES (?, ?, ?)",
            (name, description, entity_type)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        # Check if it already exists
        cursor.execute("SELECT picklist_type_id FROM PicklistType WHERE name = ?", (name,))
        result = cursor.fetchone()
        return result['picklist_type_id'] if result else None
    except sqlite3.Error as e:
        print(f"Error creating picklist type: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def add_picklist_value(picklist_type_id, value, display_order=0, is_default=False):
    """
    Add a value to a picklist type.
    
    Args:
        picklist_type_id (int): The ID of the picklist type
        value (str): The value to add
        display_order (int, optional): Order to display in lists (default: 0)
        is_default (bool, optional): Whether this is the default value (default: False)
        
    Returns:
        int: The ID of the new value, or None on failure
    """
    conn = get_db_connection()
    if conn is None:
        return None

    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO PicklistValue (picklist_type_id, value, display_order, is_default) VALUES (?, ?, ?, ?)",
            (picklist_type_id, value, display_order, is_default)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        # Check if it already exists
        cursor.execute(
            "SELECT picklist_value_id FROM PicklistValue WHERE picklist_type_id = ? AND value = ?", 
            (picklist_type_id, value)
        )
        result = cursor.fetchone()
        return result['picklist_value_id'] if result else None
    except sqlite3.Error as e:
        print(f"Error adding picklist value: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_picklist_values(picklist_name):
    """
    Get all active values for a picklist by name.
    
    Args:
        picklist_name (str): The name of the picklist type
        
    Returns:
        list: A list of dictionaries containing picklist value information
    """
    conn = get_db_connection()
    if conn is None:
        return []

    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT pv.picklist_value_id, pv.value, pv.display_order, pv.is_default
            FROM PicklistValue pv
            JOIN PicklistType pt ON pv.picklist_type_id = pt.picklist_type_id
            WHERE pt.name = ? AND pv.is_active = 1
            ORDER BY pv.display_order, pv.value
        """, (picklist_name,))
        
        return [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Error fetching picklist values: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_picklist_value_by_id(picklist_value_id):
    """
    Get a picklist value by its ID.
    
    Args:
        picklist_value_id (int): The ID of the picklist value
        
    Returns:
        str: The value, or None if not found
    """
    if picklist_value_id is None:
        return None
        
    conn = get_db_connection()
    if conn is None:
        return None

    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT value FROM PicklistValue WHERE picklist_value_id = ?", 
            (picklist_value_id,)
        )
        result = cursor.fetchone()
        return result['value'] if result else None
    except sqlite3.Error as e:
        print(f"Error fetching picklist value: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_picklist_id_by_value(picklist_name, value):
    """
    Get a picklist value ID by its text value.
    
    Args:
        picklist_name (str): The name of the picklist type
        value (str): The text value to look up
        
    Returns:
        int: The picklist_value_id, or None if not found
    """
    if not value:
        return None
        
    conn = get_db_connection()
    if conn is None:
        return None

    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT pv.picklist_value_id
            FROM PicklistValue pv
            JOIN PicklistType pt ON pv.picklist_type_id = pt.picklist_type_id
            WHERE pt.name = ? AND pv.value = ? AND pv.is_active = 1
        """, (picklist_name, value))
        result = cursor.fetchone()
        return result['picklist_value_id'] if result else None
    except sqlite3.Error as e:
        print(f"Error fetching picklist ID: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def display_picklist_menu(picklist_name):
    """
    Display a numbered menu of picklist values for user selection.
    
    Args:
        picklist_name (str): The name of the picklist to display
        
    Returns:
        list: A list of picklist values with their IDs
    """
    values = get_picklist_values(picklist_name)
    
    if not values:
        print(f"No values found for picklist '{picklist_name}'")
        return []
    
    print(f"\nSelect {picklist_name}:")
    for i, value in enumerate(values, 1):
        default_marker = " (default)" if value['is_default'] else ""
        print(f"{i}. {value['value']}{default_marker}")
    
    return values

def get_picklist_selection(picklist_name, prompt="Enter selection number or leave blank for default"):
    """
    Get a user selection from a picklist.
    
    Args:
        picklist_name (str): The name of the picklist
        prompt (str, optional): Prompt to display to the user
        
    Returns:
        tuple: (picklist_value_id, value_text) or (None, None) if cancelled
    """
    values = display_picklist_menu(picklist_name)
    
    if not values:
        return None, None
    
    # Find default value
    default_value = next((v for v in values if v['is_default']), values[0] if values else None)
    default_index = values.index(default_value) + 1 if default_value else 1
    
    while True:
        try:
            user_input = input(f"{prompt} (1-{len(values)}) [default: {default_index}]: ").strip()
            
            # Handle empty input (use default)
            if not user_input:
                return default_value['picklist_value_id'], default_value['value']
            
            # Handle back command
            if user_input.lower() == 'back':
                return None, None
            
            # Handle numeric selection
            selection = int(user_input)
            if 1 <= selection <= len(values):
                selected = values[selection - 1]
                return selected['picklist_value_id'], selected['value']
            else:
                print(f"Please enter a number between 1 and {len(values)}")
        except ValueError:
            print("Please enter a valid number")

def import_picklists_from_csv(filepath):
    """
    Import picklist definitions and values from a CSV file.
    
    CSV format:
    picklist_name,entity_type,description,value,display_order,is_default,is_active
    
    Args:
        filepath (str): Path to the CSV file
        
    Returns:
        bool: True on success, False on failure
    """
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return False
    
    # Define valid entity types and their corresponding valid picklist columns
    valid_entity_columns = {
        'account': ['industry'],
        'contact': [],  # Currently no picklist columns for contacts
        'opportunity': ['stage']
    }
    
    try:
        with open(filepath, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # Validate the CSV structure
            required_fields = ['picklist_name', 'entity_type', 'value']
            header_fields = reader.fieldnames
            
            if not header_fields:
                print(f"Error: Empty or invalid CSV file: {filepath}")
                return False
                
            missing_fields = [field for field in required_fields if field not in header_fields]
            if missing_fields:
                print(f"Error: CSV file is missing required columns: {', '.join(missing_fields)}")
                print(f"Required columns: {', '.join(required_fields)}")
                print(f"Found columns: {', '.join(header_fields)}")
                return False
            
            picklist_types = {}  # Cache for picklist_type_id
            row_count = 0
            success_count = 0
            error_count = 0
            
            for row in reader:
                row_count += 1
                # Get or create the picklist type
                picklist_name = row.get('picklist_name', '').strip()
                entity_type = row.get('entity_type', '').strip()
                description = row.get('description', '').strip()
                
                if not picklist_name or not entity_type:
                    print(f"Skipping row {row_count} - missing required fields: {row}")
                    error_count += 1
                    continue
                
                # Validate entity_type
                if entity_type not in valid_entity_columns:
                    print(f"Skipping row {row_count} - invalid entity type: '{entity_type}'. Valid types: {list(valid_entity_columns.keys())}")
                    error_count += 1
                    continue
                
                # Validate picklist_name against valid columns for the entity
                if picklist_name not in valid_entity_columns[entity_type]:
                    print(f"Skipping row {row_count} - '{picklist_name}' is not a valid picklist column for {entity_type}")
                    print(f"  Valid picklists for {entity_type}: {valid_entity_columns[entity_type] or 'None'}")
                    error_count += 1
                    continue
                
                if picklist_name not in picklist_types:
                    picklist_type_id = create_picklist_type(picklist_name, entity_type, description)
                    if not picklist_type_id:
                        print(f"Failed to create picklist type: {picklist_name}")
                        error_count += 1
                        continue
                    picklist_types[picklist_name] = picklist_type_id
                
                # Add the picklist value
                value = row.get('value', '').strip()
                
                try:
                    display_order = int(row.get('display_order', 0))
                except (ValueError, TypeError):
                    print(f"Warning in row {row_count}: Invalid display_order value, using 0.")
                    display_order = 0
                
                is_default = row.get('is_default', '').lower() in ('true', '1', 'yes', 'y')
                
                if not value:
                    print(f"Skipping row {row_count} - empty value for {picklist_name}")
                    error_count += 1
                    continue
                
                picklist_value_id = add_picklist_value(
                    picklist_types[picklist_name], 
                    value,
                    display_order,
                    is_default
                )
                
                if picklist_value_id:
                    success_count += 1
                else:
                    error_count += 1
                    print(f"Failed to add value '{value}' for picklist '{picklist_name}'")
            
            # Print summary information
            print(f"\nImport summary for {filepath}:")
            print(f"  Total rows processed: {row_count}")
            print(f"  Successfully imported: {success_count}")
            print(f"  Errors/skipped rows: {error_count}")
            print(f"  Picklist types created/used: {len(picklist_types)}")
            
            if success_count > 0:
                print(f"Successfully imported picklists from {filepath}")
                return True
            else:
                print(f"No valid picklist entries found in {filepath}")
                return False
    except (IOError, csv.Error) as e:
        print(f"Error importing picklists from CSV: {e}")
        return False

def initialize_default_picklists():
    """
    Initialize default picklists - deprecated function, kept for compatibility.
    Now only creates the necessary tables, but doesn't add any default values.
    Picklists are now managed through the admin interface.
    
    Returns:
        bool: True on success, False on failure
    """
    print("NOTE: Default picklists initialization skipped - use Admin menu to manage picklists")
    return create_picklist_tables()

def migrate_existing_data():
    """
    Migrate existing data to use picklists for industry field and stage field.
    
    Returns:
        bool: True on success, False on failure
    """
    conn = get_db_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        # --- Migrate account industry values ---
        print("Migrating account industry values to picklists...")
        
        # Get all distinct industry values from Accounts table
        cursor.execute("SELECT DISTINCT industry FROM Accounts WHERE industry IS NOT NULL AND industry != ''")
        industries = [row['industry'] for row in cursor.fetchall()]
        
        # Add each industry to the picklist if it doesn't already exist
        industry_mappings = {}  # Store mappings of industry text to picklist IDs
        for industry in industries:
            industry_id = get_picklist_id_by_value('industry', industry)
            if not industry_id:
                # Get the picklist type ID for 'industry'
                cursor.execute("SELECT picklist_type_id FROM PicklistType WHERE name = 'industry'")
                picklist_type = cursor.fetchone()
                if not picklist_type:
                    print("Industry picklist type not found")
                    continue
                
                # Add the industry value
                industry_id = add_picklist_value(picklist_type['picklist_type_id'], industry)
            
            if industry_id:
                industry_mappings[industry] = industry_id
        
        # Update the industry_id field in the Accounts table
        for industry_text, industry_id in industry_mappings.items():
            print(f"Updating accounts with industry '{industry_text}' to use picklist ID {industry_id}")
            cursor.execute(
                "UPDATE Accounts SET industry_id = ? WHERE industry = ?", 
                (industry_id, industry_text)
            )
        
        # --- Migrate opportunity stage values ---
        # Check if the Opportunities table has stage text field (older schema)
        cursor.execute("PRAGMA table_info(Opportunities)")
        opp_columns = [row[1] for row in cursor.fetchall()]
        
        if "stage" in opp_columns and "stage_id" in opp_columns:
            print("Migrating opportunity stage values to picklists...")
            
            # Get all distinct stage values
            cursor.execute("SELECT DISTINCT stage FROM Opportunities WHERE stage IS NOT NULL AND stage != ''")
            stages = [row['stage'] for row in cursor.fetchall()]
            
            # Map each stage to a picklist ID
            stage_mappings = {}
            for stage in stages:
                stage_id = get_picklist_id_by_value('stage', stage)
                if not stage_id:
                    # Check if there's a similar stage name in the picklist
                    cursor.execute("""
                        SELECT pv.picklist_value_id, pv.value 
                        FROM PicklistValue pv
                        JOIN PicklistType pt ON pv.picklist_type_id = pt.picklist_type_id
                        WHERE pt.name = 'stage'
                    """)
                    picklist_stages = {row['value'].lower(): row['picklist_value_id'] for row in cursor.fetchall()}
                    
                    # Try to find a case-insensitive match
                    stage_lower = stage.lower()
                    if stage_lower in picklist_stages:
                        stage_id = picklist_stages[stage_lower]
                    else:
                        # Get the picklist type ID for 'stage'
                        cursor.execute("SELECT picklist_type_id FROM PicklistType WHERE name = 'stage'")
                        picklist_type = cursor.fetchone()
                        if not picklist_type:
                            print("Stage picklist type not found")
                            continue
                        
                        # Add the stage value
                        stage_id = add_picklist_value(picklist_type['picklist_type_id'], stage)
                
                if stage_id:
                    stage_mappings[stage] = stage_id
            
            # Update the stage_id field in the Opportunities table
            for stage_text, stage_id in stage_mappings.items():
                print(f"Updating opportunities with stage '{stage_text}' to use picklist ID {stage_id}")
                cursor.execute(
                    "UPDATE Opportunities SET stage_id = ? WHERE stage = ?", 
                    (stage_id, stage_text)
                )
        
        conn.commit()
        print("Data migration to picklists completed successfully")
        return True
    except sqlite3.Error as e:
        print(f"Error migrating existing data: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    create_picklist_tables()  # Only create tables, don't initialize default picklists
