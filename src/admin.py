#!/usr/bin/env python3
# filepath: /Users/markmilligan/Documents/src/py-crm/src/admin.py
"""
Admin functionality for the CRM application.
This module contains functions for administrative tasks.
"""

import os
from .picklist import import_picklists_from_csv

def display_admin_menu():
    """Displays the admin menu options."""
    print("\n--- Admin Menu ---")
    print("1. Import Picklists from CSV")
    print("2. Back to Main Menu")
    print("------------------")

def handle_picklist_import():
    """Handles the import of picklists from a CSV file."""
    print("\n--- Import Picklists from CSV ---")
    print("CSV file should contain these required columns: picklist_name, entity_type, value")
    print("Optional columns: description, display_order, is_default, is_active")
    print("\nCurrently supported picklists:")
    print("  - picklist_name 'industry' for entity_type 'account'")
    print("  - picklist_name 'stage' for entity_type 'opportunity'")
    print("\nExample CSV files are available in the 'data' directory:")
    print("  - ./data/picklist_industry.csv")
    print("  - ./data/picklist_stage.csv")
    
    filepath = input("Enter the path to the CSV file (or 'back'): ").strip()
    
    if filepath.lower() == 'back':
        return
    
    if not os.path.exists(filepath):
        print(f"Error: File not found at {filepath}")
        return
    
    print(f"Importing picklists from {filepath}...")
    success = import_picklists_from_csv(filepath)
    
    if success:
        print("\nImport completed. Picklists have been added to the system.")
        print("You can now use these picklists in the relevant parts of the application.")
    else:
        print("\nImport failed or no valid entries found. Please check the following:")
        print("1. The CSV file has the required column headers")
        print("2. The picklist_name is valid for the specified entity_type")
        print("3. The data in the file is correctly formatted")
        print("\nExample CSV content:")
        print("picklist_name,entity_type,description,value,display_order,is_default")
        print("industry,account,Industry categories,Technology,1,true")
        print("stage,opportunity,Stage categories,Discovery,1,true")
        print("\nTry using one of the sample files:")
        print("  - ./data/picklist_industry.csv")
        print("  - ./data/picklist_stage.csv")

def handle_admin_menu():
    """Handles the admin menu loop."""
    while True:
        try:
            display_admin_menu()
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':  # Import Picklists from CSV
                handle_picklist_import()
            elif choice == '2':  # Back to Main Menu
                break
            else:
                print("Invalid choice. Please try again.")
        except (KeyboardInterrupt, EOFError):
            # Just break out to the main menu instead of trying to import graceful_exit
            # This avoids circular imports
            print("\nReturning to main menu...")
            break
