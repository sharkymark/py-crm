import sys
import csv
import os
from datetime import datetime, timezone # Added timezone
# Update imports to use relative paths within the src directory
from .database import initialize_database

def truncate_text(text, max_length=30):
    """
    Truncates text to the specified maximum length and adds ellipsis if needed.
    
    Args:
        text (str): The text to truncate
        max_length (int): Maximum length before truncation (default: 30)
        
    Returns:
        str: Truncated text with ellipsis if needed
    """
    if not text or text == 'N/A':
        return 'N/A'
    
    text = str(text)  # Convert to string if not already
    if len(text) <= max_length:
        return text
    
    return text[:max_length-3] + '...'
from .crm_dal import (
    create_account, get_account, list_accounts, update_account, delete_account, search_accounts,
    create_contact, get_contact, list_contacts, update_contact, delete_contact, search_contacts,
    create_opportunity, get_opportunity, list_opportunities, update_opportunity, delete_opportunity, search_opportunities,
    get_contacts_by_account, get_opportunities_by_account
)

def truncate_text(text, max_length=30):
    """
    Truncate text to specified length and add ellipsis if needed.
    Also replaces newlines with spaces to ensure proper display in tables.
    
    Returns the original text if it's shorter than max_length, or truncated text with ellipsis.
    """
    if not text or text == 'N/A':
        return "N/A"
    
    # Replace newlines with spaces to make it work well in tabular views
    text_single_line = str(text).replace('\n', ' ')
    
    if len(text_single_line) <= max_length:
        return text_single_line
    else:
        # Return truncated text with ellipsis
        return text_single_line[:max_length-3] + "..."

def convert_utc_to_local_display(utc_dt_str):
    """Converts a UTC datetime string to a local datetime string for display."""
    if not utc_dt_str:
        return "N/A"
    try:
        # Try parsing with microseconds
        dt_utc = datetime.strptime(utc_dt_str, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        try:
            # Try parsing without microseconds
            dt_utc = datetime.strptime(utc_dt_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            # If parsing fails, return the original string
            return utc_dt_str

    dt_utc = dt_utc.replace(tzinfo=timezone.utc)
    dt_local = dt_utc.astimezone() # Converts to local timezone
    return dt_local.strftime("%Y-%m-%d %H:%M:%S")

def display_main_menu():
    """Displays the main menu options."""
    print("\n--- Simple CRM Main Menu ---")
    print("1. Manage Accounts")
    print("2. Manage Contacts")
    print("3. Manage Opportunities")
    print("4. Summary")
    print("5. Export")
    print("6. Exit")
    print("----------------------------")

def display_accounts_menu():
    """Displays the accounts management menu."""
    print("\n--- Manage Accounts ---")
    print("1. Create Account")
    print("2. List All Accounts")
    print("3. Get Account")
    print("4. Update Account")
    print("5. Delete Account")
    print("6. Back to Main Menu")
    print("-----------------------")

def display_contacts_menu():
    """Displays the contacts management menu."""
    print("\n--- Manage Contacts ---")
    print("1. Create Contact")
    print("2. List All Contacts")
    print("3. Get Contact")
    print("4. Update Contact")
    print("5. Delete Contact")
    print("6. Back to Main Menu")
    print("-----------------------")

def display_opportunities_menu():
    """Displays the opportunities management menu."""
    print("\n--- Manage Opportunities ---")
    print("1. Create Opportunity")
    print("2. List All Opportunities")
    print("3. Get Opportunity")
    print("4. Update Opportunity")
    print("5. Delete Opportunity")
    print("6. Back to Main Menu")
    print("--------------------------")

def display_export_menu():
    """Displays the export menu options."""
    print("\n--- Export Options ---")
    print("1. Export Contacts")
    print("2. Export Opportunities")
    print("3. Back to Main Menu")
    print("--------------------")

def graceful_exit():
    """Prints the exit message and exits the program."""
    print("\nExiting application. Goodbye!")
    sys.exit(0)

def get_integer_input(prompt):
    """Gets integer input from the user with validation."""
    while True:
        try:
            value = input(prompt)
            if value.lower() == 'back': # Allow 'back' to exit input loop
                return 'back'
            return int(value)
        except ValueError:
            print("Invalid input. Please enter an integer or 'back'.")
        except (KeyboardInterrupt, EOFError):
            graceful_exit()


def get_float_input(prompt):
    """Gets float input from the user with validation."""
    while True:
        try:
            value = input(prompt)
            if value.lower() == 'back': # Allow 'back' to exit input loop
                return 'back'
            if not value: # Allow empty input for optional fields
                return None
            return float(value)
        except ValueError:
            print("Invalid input. Please enter a number or 'back'.")
        except (KeyboardInterrupt, EOFError):
            graceful_exit()


def get_multiline_input(prompt):
    """
    Gets multi-line input from the user.
    User can enter text with newlines and end input by typing 'DONE' on a new line.
    
    Args:
        prompt (str): The prompt to display to the user
        
    Returns:
        str or None: The multi-line input or None if user left it empty
        'back': If the user entered 'back' to go back
    """
    print(f"{prompt} (Type 'DONE' on a new line when finished, or 'BACK' to go back)")
    lines = []
    
    while True:
        try:
            line = input()
            # Check for end or back commands
            if line.strip().upper() == 'DONE':
                break
            if line.strip().upper() == 'BACK':
                return 'back'
            
            # Add the line to our collection
            lines.append(line)
        except (KeyboardInterrupt, EOFError):
            graceful_exit()
    
    # Join the lines with newlines
    result = '\n'.join(lines)
    
    # If the result is empty, return None
    if not result.strip():
        return None
    
    return result


def select_account_by_search(prompt="Enter Account Name or ID (or 'back'): "):
    """
    Prompts user to search for an account by name or enter an ID,
    handles search results, and returns the selected account ID or None/back.
    Returns None if user leaves search blank and it's optional.
    """
    while True:
        try:
            query = input(prompt).strip()
            if query.lower() == 'back':
                return 'back'
            if not query:
                # If query is empty, return None. This is useful for optional fields.
                # The caller needs to handle whether None is acceptable.
                return None

            try:
                # Try interpreting input as an ID
                account_id = int(query)
                account = get_account(account_id)
                if account:
                    print(f"Selected Account: ID: {account['account_id']}, Name: {account['name']}")
                    return account_id
                else:
                    print(f"No account found with ID: {account_id}")
                    continue # Ask again
            except ValueError:
                # Input is not an integer, perform search
                accounts = search_accounts(query)
                if not accounts:
                    print(f"No accounts found matching '{query}'.")
                    continue # Ask again
                elif len(accounts) == 1:
                    account = accounts[0]
                    print(f"Found 1 matching account: ID: {account['account_id']}, Name: {account['name']}")
                    confirm = input("Use this account? (yes/no or 'back'): ").strip().lower()
                    if confirm == 'yes' or confirm == 'y':
                        return account['account_id']
                    elif confirm == 'back':
                        return 'back'
                    else:
                        continue # Ask again
                else:
                    print(f"Found {len(accounts)} matching accounts:")
                    for acc in accounts:
                        print(f"  ID: {acc['account_id']}, Name: {acc['name']}, Industry: {acc['industry']}")
                    select_id_input = get_integer_input("Enter the ID of the account to select (or 'back'): ")
                    if select_id_input == 'back':
                        return 'back'
                    selected_account = get_account(select_id_input)
                    if selected_account:
                        return selected_account['account_id']
                    else:
                        print("Invalid ID selected.")
                        continue # Ask again
        except (KeyboardInterrupt, EOFError):
            graceful_exit()


def select_contact_by_search(prompt="Enter Contact Name, Email, or ID (or 'back'): "):
    """
    Prompts user to search for a contact by name/email or enter an ID,
    handles search results, and returns the selected contact ID or None/back.
    Returns None if user leaves search blank and it's optional.
    """
    while True:
        try:
            query = input(prompt).strip()
            if query.lower() == 'back':
                return 'back'
            if not query:
                # If query is empty, return None. This is useful for optional fields.
                # The caller needs to handle whether None is acceptable.
                return None

            try:
                # Try interpreting input as an ID
                contact_id = int(query)
                contact = get_contact(contact_id)
                if contact:
                    print(f"Selected Contact: ID: {contact['contact_id']}, Name: {contact['first_name']} {contact['last_name']}, Email: {contact['email']}")
                    return contact_id
                else:
                    print(f"No contact found with ID: {contact_id}")
                    continue # Ask again
            except ValueError:
                # Input is not an integer, perform search
                contacts = search_contacts(query)
                if not contacts:
                    print(f"No contacts found matching '{query}'.")
                    continue # Ask again
                elif len(contacts) == 1:
                    contact = contacts[0]
                    print(f"Found 1 matching contact: ID: {contact['contact_id']}, Name: {contact['first_name']} {contact['last_name']}, Email: {contact['email']}")
                    confirm = input("Use this contact? (yes/no or 'back'): ").strip().lower()
                    if confirm == 'yes' or confirm == 'y':
                        return contact['contact_id']
                    elif confirm == 'back':
                        return 'back'
                    else:
                        continue # Ask again
                else:
                    print(f"Found {len(contacts)} matching contacts:")
                    for con in contacts:
                        print(f"  ID: {con['contact_id']}, Name: {con['first_name']} {con['last_name']}, Email: {con['email']}")
                    select_id_input = get_integer_input("Enter the ID of the contact to select (or 'back'): ")
                    if select_id_input == 'back':
                        return 'back'
                    selected_contact = get_contact(select_id_input)
                    if selected_contact:
                        return selected_contact['contact_id']
                    else:
                        print("Invalid ID selected.")
                        continue # Ask again
        except (KeyboardInterrupt, EOFError):
            graceful_exit()


def select_opportunity_by_search(prompt="Enter Opportunity Name, Description, or ID (or 'back'): "):
    """
    Prompts user to search for an opportunity by name/description or enter an ID,
    handles search results, and returns the selected opportunity ID or None/back.
    Returns None if user leaves search blank and it's optional.
    """
    while True:
        try:
            query = input(prompt).strip()
            if query.lower() == 'back':
                return 'back'
            if not query:
                # If query is empty, return None. This is useful for optional fields.
                # The caller needs to handle whether None is acceptable.
                return None

            try:
                # Try interpreting input as an ID
                opportunity_id = int(query)
                opportunity = get_opportunity(opportunity_id)
                if opportunity:
                    print(f"Selected Opportunity: ID: {opportunity['opportunity_id']}, Name: {opportunity['name']}")
                    return opportunity_id
                else:
                    print(f"No opportunity found with ID: {opportunity_id}")
                    continue # Ask again
            except ValueError:
                # Input is not an integer, perform search
                opportunities = search_opportunities(query)
                if not opportunities:
                    print(f"No opportunities found matching '{query}'.")
                    continue # Ask again
                elif len(opportunities) == 1:
                    opportunity = opportunities[0]
                    print(f"Found 1 matching opportunity: ID: {opportunity['opportunity_id']}, Name: {opportunity['name']}, Amount: {opportunity['amount']}")
                    confirm = input("Use this opportunity? (yes/no or 'back'): ").strip().lower()
                    if confirm == 'yes' or confirm == 'y':
                        return opportunity['opportunity_id']
                    elif confirm == 'back':
                        return 'back'
                    else:
                        continue # Ask again
                else:
                    print(f"Found {len(opportunities)} matching opportunities:")
                    for opp in opportunities:
                        print(f"  ID: {opp['opportunity_id']}, Name: {opp['name']}, Amount: {opp['amount']}")
                    select_id_input = get_integer_input("Enter the ID of the opportunity to select (or 'back'): ")
                    if select_id_input == 'back':
                        return 'back'
                    selected_opportunity = get_opportunity(select_id_input)
                    if selected_opportunity:
                        return selected_opportunity['opportunity_id']
                    else:
                        print("Invalid ID selected.")
                        continue # Ask again
        except (KeyboardInterrupt, EOFError):
            graceful_exit()


# --- Summary Handler ---
def handle_summary_menu():
    """Handles the summary menu option."""
    print("\n--- CRM Summary ---")
    try:
        search_term = input("Enter search term for Accounts, Contacts, or Opportunities (leave blank for all, or 'back'): ").strip()
        if search_term.lower() == 'back':
            return

        if not search_term:
            print("Displaying all entries.")
            matching_accounts = list_accounts()
            matching_contacts = list_contacts()
            matching_opportunities = list_opportunities()
        else:
            print(f"Searching for: '{search_term}'")
            matching_accounts = search_accounts(search_term)
            matching_contacts = search_contacts(search_term)
            matching_opportunities = search_opportunities(search_term)

        displayed_contact_ids = set()
        displayed_opportunity_ids = set()
        summary_width = 80  # Define a width for separators
        item_separator = "  " + "-" * (summary_width - 2)

        print("\n--- Accounts Summary ---")
        if matching_accounts:
            for acc in matching_accounts:
                print(f"  Account: {acc['name']} (ID: {acc['account_id']}) - Industry: {acc['industry'] or 'N/A'}")
                
                contacts_for_account = get_contacts_by_account(acc['account_id'])
                if contacts_for_account:
                    print("    Linked Contacts:")
                    for contact in contacts_for_account:
                        print(f"      - {contact['first_name']} {contact['last_name']} (ID: {contact['contact_id']}) - Email: {contact['email']}")
                        displayed_contact_ids.add(contact['contact_id'])
                
                opportunities_for_account = get_opportunities_by_account(acc['account_id'])
                if opportunities_for_account:
                    print("    Linked Opportunities:")
                    for opp in opportunities_for_account:
                        print(f"      - {opp['name']} (ID: {opp['opportunity_id']}) - Amount: {opp['amount'] or 'N/A'}, Close Date: {opp['close_date'] or 'N/A'}")
                        displayed_opportunity_ids.add(opp['opportunity_id'])
                print(item_separator)
        else:
            print("  No matching accounts found." if search_term else "  No accounts found.")

        print("\n--- Standalone Contacts Summary ---")
        standalone_contacts_found_in_summary = False
        if matching_contacts:
            for contact in matching_contacts:
                if contact['contact_id'] not in displayed_contact_ids:
                    if not standalone_contacts_found_in_summary:
                        standalone_contacts_found_in_summary = True
                    print(f"  Contact: {contact['first_name']} {contact['last_name']} (ID: {contact['contact_id']})")
                    print(f"    Email: {contact['email']}, Phone: {contact['phone'] or 'N/A'}")
                    account_info = "N/A"
                    if contact['account_id']:
                        acc = get_account(contact['account_id'])
                        account_info = f"{acc['name']} (ID: {contact['account_id']})" if acc else f"ID: {contact['account_id']} (Account not found)"
                    print(f"    Linked to Account: {account_info}")
                    # No direct display of opportunities linked only to contact in this summary view to keep it cleaner
                    # User can get contact details for that.
                    print(item_separator)

        if not standalone_contacts_found_in_summary:
             print("  No additional standalone contacts found." if search_term else "  No standalone contacts found.")

        print("\n--- Standalone Opportunities Summary ---")
        standalone_opportunities_found_in_summary = False
        if matching_opportunities:
            for opp in matching_opportunities:
                if opp['opportunity_id'] not in displayed_opportunity_ids:
                    if not standalone_opportunities_found_in_summary:
                        standalone_opportunities_found_in_summary = True
                    print(f"  Opportunity: {opp['name']} (ID: {opp['opportunity_id']})")
                    print(f"    Description: {opp['description'] or 'N/A'}")
                    print(f"    Amount: {opp['amount'] or 'N/A'}, Close Date: {opp['close_date'] or 'N/A'}")
                    
                    account_info = "N/A"
                    if opp['account_id']:
                        acc = get_account(opp['account_id'])
                        account_info = f"{acc['name']} (ID: {opp['account_id']})" if acc else f"ID: {opp['account_id']} (Account not found)"
                    print(f"    Linked to Account: {account_info}")

                    contact_info = "N/A"
                    if opp['contact_id']:
                        contact = get_contact(opp['contact_id'])
                        contact_info = f"{contact['first_name']} {contact['last_name']} (ID: {opp['contact_id']})" if contact else f"ID: {opp['contact_id']} (Contact not found)"
                    print(f"    Linked to Contact: {contact_info}")
                    print(item_separator)

        if not standalone_opportunities_found_in_summary:
            print("  No additional standalone opportunities found." if search_term else "  No standalone opportunities found.")

        print("\n--- End Summary ---")
        print("=" * summary_width)

    except (KeyboardInterrupt, EOFError):
        graceful_exit()
    except Exception as e:
        print(f"An unexpected error occurred during summary generation: {e}")
        # Consider logging e to a file or more detailed error handling
        # graceful_exit() # Or allow returning to menu


# --- Menu Handlers ---
def handle_accounts_menu():
    """Handles the accounts management menu loop."""
    while True:
        try:
            display_accounts_menu()
            choice = input("Enter your choice: ").strip()

            if choice == '1': # Create Account
                name = input("Enter account name (required): ").strip()
                if not name:
                    print("Account name is required.")
                    continue
                industry = input("Enter account industry (optional): ").strip() or None
                description = get_multiline_input("Enter account description (optional):")
                if description == 'back':
                    continue
                website = input("Enter account website (optional): ").strip() or None
                street = input("Enter street address (optional): ").strip() or None
                city = input("Enter city (optional): ").strip() or None
                state = input("Enter state/province (optional): ").strip() or None
                zip_code = input("Enter zip/postal code (optional): ").strip() or None
                country = input("Enter country (optional): ").strip() or None
                
                account_id = create_account(name, industry, description, website, street, city, state, zip_code, country)
                if account_id:
                    print(f"SUCCESS: Account '{name}' created with ID: {account_id}")
                else:
                    print(f"FAILED: Could not create account '{name}'.")

            elif choice == '2': # List Accounts
                accounts = list_accounts()
                if accounts:
                    print("\n--- All Accounts ---")
                    padding = 2
                    # Determine dynamic column widths
                    min_id_width = len("ID") + padding
                    min_name_width = len("Name") + padding
                    min_industry_width = len("Industry") + padding
                    min_description_width = len("Description") + padding
                    min_website_width = len("Website") + padding
                    min_location_width = len("Location") + padding
                    min_created_at_width = len("Created At") + padding

                    max_id_len = min_id_width
                    max_name_len = min_name_width
                    max_industry_len = min_industry_width
                    max_description_len = min_description_width
                    max_website_len = min_website_width
                    max_location_len = min_location_width
                    # Created At is fixed width for now, can be dynamic if needed
                    # max_created_at_len = min_created_at_width

                    for account in accounts:
                        max_id_len = max(max_id_len, len(str(account['account_id'])) + padding)
                        max_name_len = max(max_name_len, len(account['name']) + padding)
                        max_industry_len = max(max_industry_len, len(account['industry'] or 'N/A') + padding)
                        
                        # Truncate description for display
                        description = truncate_text(account['description'] or 'N/A')
                        max_description_len = max(max_description_len, len(description) + padding)
                        
                        max_website_len = max(max_website_len, len(account['website'] or 'N/A') + padding)
                        
                        # Format location as city, state, country
                        location_parts = []
                        if account['city']:
                            location_parts.append(account['city'])
                        if account['state']:
                            location_parts.append(account['state'])
                        if account['country']:
                            location_parts.append(account['country'])
                        location = ", ".join(location_parts) if location_parts else "N/A"
                        max_location_len = max(max_location_len, len(location) + padding)
                        # max_created_at_len = max(max_created_at_len, len(account['created_at']) + padding)

                    id_col_width = max_id_len
                    name_col_width = max_name_len
                    industry_col_width = max_industry_len
                    description_col_width = max_description_len
                    website_col_width = max_website_len
                    location_col_width = max_location_len
                    created_at_col_width = 20 # Keep fixed or use max_created_at_len

                    header = f"{'ID':<{id_col_width}} | {'Name':<{name_col_width}} | {'Industry':<{industry_col_width}} | {'Description':<{description_col_width}} | {'Website':<{website_col_width}} | {'Location':<{location_col_width}} | {'Created At':<{created_at_col_width}}"
                    print(header)
                    print("-" * len(header))
                    for account in accounts:
                        industry_display = account['industry'] or 'N/A'
                        description_display = truncate_text(account['description'] or 'N/A')
                        website_display = account['website'] or 'N/A'
                        
                        # Format location as city, state, country
                        location_parts = []
                        if account['city']:
                            location_parts.append(account['city'])
                        if account['state']:
                            location_parts.append(account['state'])
                        if account['country']:
                            location_parts.append(account['country'])
                        location_display = ", ".join(location_parts) if location_parts else "N/A"
                        
                        created_at_display = convert_utc_to_local_display(account['created_at'])
                        print(f"{str(account['account_id']):<{id_col_width}} | {account['name']:<{name_col_width}} | {industry_display:<{industry_col_width}} | {description_display:<{description_col_width}} | {website_display:<{website_col_width}} | {location_display:<{location_col_width}} | {created_at_display:<{created_at_col_width}}")
                    print("-" * len(header))
                else:
                    print("No accounts found.")

            elif choice == '3': # Get Account (by search/ID)
                print("\n--- Get Account ---")
                account_id_selection = select_account_by_search("Enter Account Name or ID to get (or 'back'): ")
                if account_id_selection == 'back': continue
                if account_id_selection is None: # User left blank, but Get requires selection
                     print("Account selection is required to get details.")
                     continue

                account = get_account(account_id_selection)
                if account:
                    print("\n--- Account Details ---")
                    print(f"  ID         : {account['account_id']}")
                    print(f"  Name       : {account['name']}")
                    print(f"  Industry   : {account['industry'] or 'N/A'}")
                    print(f"  Description: {account['description'] or 'N/A'}")
                    print(f"  Website    : {account['website'] or 'N/A'}")
                    print(f"  Address    : {account['street'] or 'N/A'}")
                    print(f"  City       : {account['city'] or 'N/A'}")
                    print(f"  State      : {account['state'] or 'N/A'}")
                    print(f"  Zip        : {account['zip'] or 'N/A'}")
                    print(f"  Country    : {account['country'] or 'N/A'}")
                    print(f"  Created At : {convert_utc_to_local_display(account['created_at'])}")
                    
                    # Display linked contacts
                    contacts = get_contacts_by_account(account['account_id'])
                    if contacts:
                        print("  Linked Contacts:")
                        for contact in contacts:
                            print(f"    - ID: {contact['contact_id']}, Name: {contact['first_name']} {contact['last_name']}, Email: {contact['email']}")
                    else:
                        print("  Linked Contacts: None")
                    # Display linked opportunities
                    opportunities = get_opportunities_by_account(account['account_id'])
                    if opportunities:
                        print("  Linked Opportunities:")
                        for opp in opportunities:
                            print(f"    - ID: {opp['opportunity_id']}, Name: {opp['name']}, Amount: {opp['amount'] or 'N/A'}")
                    else:
                        print("  Linked Opportunities: None")
                    print("-----------------------")
                else:
                    # This case should ideally not be reached if select_account_by_search returns a valid ID
                    print(f"Account with ID {account_id_selection} not found.")

            elif choice == '4': # Update Account (by search/ID)
                print("\n--- Update Account ---")
                account_id_selection = select_account_by_search("Enter Account Name or ID to update (or 'back'): ")
                if account_id_selection == 'back': continue
                if account_id_selection is None: # User left blank, but Update requires selection
                     print("Account selection is required to update.")
                     continue
                account_id = account_id_selection # Use the selected ID

                account = get_account(account_id) # Re-fetch to show current details
                if not account:
                    print(f"Account with ID {account_id} not found.")
                    continue

                print(f"\nCurrent Account Details:")
                print(f"  ID: {account['account_id']}")
                print(f"  Name: {account['name']}")
                print(f"  Industry: {account['industry'] or 'N/A'}")
                print(f"  Description: {account['description'] or 'N/A'}")
                print(f"  Website: {account['website'] or 'N/A'}")
                print(f"  Street: {account['street'] or 'N/A'}")
                print(f"  City: {account['city'] or 'N/A'}")
                print(f"  State: {account['state'] or 'N/A'}")
                print(f"  Zip: {account['zip'] or 'N/A'}")
                print(f"  Country: {account['country'] or 'N/A'}")
                
                new_name = input(f"Enter new name (leave blank to keep '{account['name']}'): ").strip() or None
                new_industry = input(f"Enter new industry (leave blank to keep '{account['industry'] or 'N/A'}'): ").strip() or None
                
                # Handle multi-line description
                print(f"Current description: {account['description'] or 'N/A'}")
                new_description = get_multiline_input(f"Enter new description (leave blank to keep current)")
                if new_description == 'back':
                    continue
                
                new_website = input(f"Enter new website (leave blank to keep '{account['website'] or 'N/A'}'): ").strip() or None
                new_street = input(f"Enter new street (leave blank to keep '{account['street'] or 'N/A'}'): ").strip() or None
                new_city = input(f"Enter new city (leave blank to keep '{account['city'] or 'N/A'}'): ").strip() or None
                new_state = input(f"Enter new state (leave blank to keep '{account['state'] or 'N/A'}'): ").strip() or None
                new_zip = input(f"Enter new zip (leave blank to keep '{account['zip'] or 'N/A'}'): ").strip() or None
                new_country = input(f"Enter new country (leave blank to keep '{account['country'] or 'N/A'}'): ").strip() or None

                update_params = {}
                if new_name is not None:
                    update_params['name'] = new_name
                if new_industry is not None:
                    update_params['industry'] = new_industry
                if new_description is not None:
                    update_params['description'] = new_description
                if new_website is not None:
                    update_params['website'] = new_website
                if new_street is not None:
                    update_params['street'] = new_street
                if new_city is not None:
                    update_params['city'] = new_city
                if new_state is not None:
                    update_params['state'] = new_state
                if new_zip is not None:
                    update_params['zip'] = new_zip
                if new_country is not None:
                    update_params['country'] = new_country

                if not update_params:
                    print("No update parameters provided.")
                    continue

                success = update_account(account_id, **update_params)
                if success:
                    print(f"SUCCESS: Account with ID {account_id} updated.")
                else:
                    print(f"FAILED: Could not update account with ID {account_id}.") # DAL prints specific error

            elif choice == '5': # Delete Account (by search/ID)
                print("\n--- Delete Account ---")
                account_id_selection = select_account_by_search("Enter Account Name or ID to delete (or 'back'): ")
                if account_id_selection == 'back': continue
                if account_id_selection is None: # User left blank, but Delete requires selection
                     print("Account selection is required to delete.")
                     continue
                account_id = account_id_selection # Use the selected ID

                success = delete_account(account_id)
                if success:
                    print(f"SUCCESS: Account with ID {account_id} deleted.")
                else:
                    print(f"FAILED: Could not delete account with ID {account_id}. It might not exist or have linked records.")

            elif choice == '6': # Back
                break

            else:
                print("Invalid choice. Please try again.")
        except (KeyboardInterrupt, EOFError):
            graceful_exit()


def handle_contacts_menu():
    """Handles the contacts management menu loop."""
    while True:
        try:
            display_contacts_menu()
            choice = input("Enter your choice: ").strip()

            if choice == '1': # Create Contact
                first_name = input("Enter contact first name (required): ").strip()
                last_name = input("Enter contact last name (required): ").strip()
                title = input("Enter contact title (optional): ").strip() or None
                email = input("Enter contact email (required, must be unique): ").strip()
                phone = input("Enter contact phone (optional): ").strip() or None
                description = get_multiline_input("Enter contact description (optional):")
                if description == 'back':
                    continue
                website = input("Enter contact website (optional): ").strip() or None
                
                # Address information
                street = input("Enter street address (optional): ").strip() or None
                city = input("Enter city (optional): ").strip() or None
                state = input("Enter state/province (optional): ").strip() or None
                zip_code = input("Enter zip/postal code (optional): ").strip() or None
                country = input("Enter country (optional): ").strip() or None

                if not first_name or not last_name or not email:
                     print("First name, last name, and email are required.")
                     continue

                # Use the new select_account_by_search helper
                print("\n--- Link Contact to Account ---")
                # select_account_by_search returns None if user leaves blank, which is okay for optional account_id
                account_id = select_account_by_search("Enter associated Account Name or ID (optional, leave blank for none, or 'back'): ")
                if account_id == 'back': continue # Go back if user entered 'back' during account selection

                contact_id = create_contact(first_name, last_name, email, phone, account_id, title, description, 
                                          website, street, city, state, zip_code, country)
                if contact_id:
                    print(f"SUCCESS: Contact '{first_name} {last_name}' created with ID: {contact_id}")
                else:
                    print(f"FAILED: Could not create contact '{first_name} {last_name}'. Ensure email is unique and account ID is valid.")

            elif choice == '2': # List Contacts
                contacts = list_contacts()
                if contacts:
                    print("\n--- All Contacts ---")
                    padding = 2
                    # Determine dynamic column widths
                    min_name_width = len("Name (ID)")
                    min_title_width = len("Title")
                    min_description_width = len("Description")
                    min_account_width = len("Account Name (ID)")
                    min_email_width = len("Email")
                    min_phone_width = len("Phone")
                    min_location_width = len("Location")
                    min_created_at_width = len("Created At")

                    max_name_len = min_name_width
                    max_title_len = min_title_width
                    max_description_len = min_description_width
                    max_account_len = min_account_width
                    max_email_len = min_email_width
                    max_phone_len = min_phone_width
                    max_location_len = min_location_width
                    # Created At is often fixed, but we can calculate it too for consistency
                    max_created_at_len = min_created_at_width


                    contact_display_data = []
                    for contact_item in contacts:
                        name_with_id = f"{contact_item['first_name']} {contact_item['last_name']} ({contact_item['contact_id']})"
                        max_name_len = max(max_name_len, len(name_with_id))

                        email_display = contact_item['email'] or 'N/A'
                        max_email_len = max(max_email_len, len(email_display))

                        phone_display = contact_item['phone'] or 'N/A'
                        max_phone_len = max(max_phone_len, len(phone_display))
                        
                        # Truncate description for display
                        description_display = truncate_text(contact_item['description'] or 'N/A')
                        max_description_len = max(max_description_len, len(description_display))

                        account_display = "N/A"
                        if contact_item['account_id']:
                            acc = get_account(contact_item['account_id'])
                            if acc:
                                account_display = f"{acc['name']} ({contact_item['account_id']})"
                            else:
                                account_display = f"Unknown Account ({contact_item['account_id']})"
                        max_account_len = max(max_account_len, len(account_display))
                        
                        created_at_display = convert_utc_to_local_display(contact_item['created_at'])
                        max_created_at_len = max(max_created_at_len, len(str(created_at_display)))

                        # Format title
                        title_display = contact_item['title'] or 'N/A'
                        max_title_len = max(max_title_len, len(title_display))
                        
                        # Format location as city, state, country
                        location_parts = []
                        if contact_item['city']:
                            location_parts.append(contact_item['city'])
                        if contact_item['state']:
                            location_parts.append(contact_item['state'])
                        if contact_item['country']:
                            location_parts.append(contact_item['country'])
                        location_display = ", ".join(location_parts) if location_parts else "N/A"
                        max_location_len = max(max_location_len, len(location_display))
                        
                        contact_display_data.append({
                            'name_with_id': name_with_id,
                            'title': title_display,
                            'description': description_display,
                            'email': email_display,
                            'phone': phone_display,
                            'account': account_display,
                            'location': location_display,
                            'created_at': created_at_display
                        })

                    name_col_width = max_name_len + padding
                    title_col_width = max_title_len + padding
                    description_col_width = max_description_len + padding
                    account_col_width = max_account_len + padding
                    email_col_width = max(min_email_width, max_email_len) + padding
                    phone_col_width = max(min_phone_width, max_phone_len) + padding
                    location_col_width = max_location_len + padding
                    created_at_col_width = max(min_created_at_width, max_created_at_len) + padding

                    header_parts = [
                        f"{'Name (ID)':<{name_col_width}}",
                        f"{'Title':<{title_col_width}}",
                        f"{'Description':<{description_col_width}}",
                        f"{'Email':<{email_col_width}}",
                        f"{'Phone':<{phone_col_width}}",
                        f"{'Account Name (ID)':<{account_col_width}}",
                        f"{'Location':<{location_col_width}}",
                        f"{'Created At':<{created_at_col_width}}"
                    ]
                    header = " | ".join(header_parts)
                    print(header)
                    print("-" * len(header))

                    for data in contact_display_data:
                        row_parts = [
                            f"{data['name_with_id']:<{name_col_width}}",
                            f"{data['title']:<{title_col_width}}",
                            f"{data['description']:<{description_col_width}}",
                            f"{data['email']:<{email_col_width}}",
                            f"{data['phone']:<{phone_col_width}}",
                            f"{data['account']:<{account_col_width}}",
                            f"{data['location']:<{location_col_width}}",
                            f"{data['created_at']:<{created_at_col_width}}"
                        ]
                        print(" | ".join(row_parts))
                    print("-" * len(header))
                else:
                    print("No contacts found.")

            elif choice == '3': # Get Contact (by search/ID)
                print("\n--- Get Contact ---")
                contact_id_selection = select_contact_by_search("Enter Contact Name, Email, or ID to get (or 'back'): ")
                if contact_id_selection == 'back': continue
                if contact_id_selection is None: # User left blank, but Get requires selection
                     print("Contact selection is required to get details.")
                     continue

                contact_details = get_contact(contact_id_selection) # Renamed to avoid conflict
                if contact_details:
                    print("\n--- Contact Details ---")
                    print(f"  ID           : {contact_details['contact_id']}")
                    print(f"  First Name   : {contact_details['first_name']}")
                    print(f"  Last Name    : {contact_details['last_name']}")
                    print(f"  Title        : {contact_details['title'] or 'N/A'}")
                    print(f"  Email        : {contact_details['email']}")
                    print(f"  Phone        : {contact_details['phone'] or 'N/A'}")
                    print(f"  Description  : {contact_details['description'] or 'N/A'}")
                    print(f"  Website      : {contact_details['website'] or 'N/A'}")
                    print(f"  Street       : {contact_details['street'] or 'N/A'}")
                    print(f"  City         : {contact_details['city'] or 'N/A'}")
                    print(f"  State        : {contact_details['state'] or 'N/A'}")
                    print(f"  Zip          : {contact_details['zip'] or 'N/A'}")
                    print(f"  Country      : {contact_details['country'] or 'N/A'}")
                    
                    account_display_details = "N/A"
                    if contact_details['account_id']:
                        acc = get_account(contact_details['account_id'])
                        if acc:
                            account_display_details = f"{acc['name']} (ID: {acc['account_id']})"
                        else:
                            account_display_details = f"Unknown Account (ID: {contact_details['account_id']})"
                    print(f"  Account      : {account_display_details}")
                    print(f"  Created At   : {convert_utc_to_local_display(contact_details['created_at'])}")
                    print("-----------------------")
                else:
                    print(f"Contact with ID {contact_id_selection} not found.")

            elif choice == '4': # Update Contact (by search/ID)
                print("\n--- Update Contact ---")
                contact_id_selection = select_contact_by_search("Enter Contact Name, Email, or ID to update (or 'back'): ")
                if contact_id_selection == 'back': continue
                if contact_id_selection is None: # User left blank, but Update requires selection
                     print("Contact selection is required to update.")
                     continue
                contact_id = contact_id_selection # Use the selected ID

                contact = get_contact(contact_id) # Re-fetch to show current details
                if not contact:
                    print(f"Contact with ID {contact_id} not found.")
                    continue

                print(f"\nCurrent Contact Details:")
                print(f"  ID: {contact['contact_id']}")
                print(f"  First Name: {contact['first_name']}")
                print(f"  Last Name: {contact['last_name']}")
                print(f"  Title: {contact['title'] or 'N/A'}")
                print(f"  Email: {contact['email']}")
                print(f"  Phone: {contact['phone'] or 'N/A'}")
                print(f"  Description: {contact['description'] or 'N/A'}")
                print(f"  Website: {contact['website'] or 'N/A'}")
                print(f"  Street: {contact['street'] or 'N/A'}")
                print(f"  City: {contact['city'] or 'N/A'}")
                print(f"  State: {contact['state'] or 'N/A'}")
                print(f"  Zip: {contact['zip'] or 'N/A'}")
                print(f"  Country: {contact['country'] or 'N/A'}")
                print(f"  Account ID: {contact['account_id'] or 'None'}")
                
                new_first_name = input(f"Enter new first name (leave blank to keep '{contact['first_name']}'): ").strip() or None
                new_last_name = input(f"Enter new last name (leave blank to keep '{contact['last_name']}'): ").strip() or None
                new_title = input(f"Enter new title (leave blank to keep '{contact['title'] or 'N/A'}'): ").strip() or None
                new_email = input(f"Enter new email (leave blank to keep '{contact['email']}'): ").strip() or None
                new_phone = input(f"Enter new phone (leave blank to keep '{contact['phone'] or 'N/A'}'): ").strip() or None
                
                # Handle multi-line description
                print(f"Current description: {contact['description'] or 'N/A'}")
                new_description = get_multiline_input(f"Enter new description (leave blank to keep current)")
                if new_description == 'back':
                    continue
                    
                new_website = input(f"Enter new website (leave blank to keep '{contact['website'] or 'N/A'}'): ").strip() or None
                new_street = input(f"Enter new street (leave blank to keep '{contact['street'] or 'N/A'}'): ").strip() or None
                new_city = input(f"Enter new city (leave blank to keep '{contact['city'] or 'N/A'}'): ").strip() or None
                new_state = input(f"Enter new state (leave blank to keep '{contact['state'] or 'N/A'}'): ").strip() or None
                new_zip = input(f"Enter new zip (leave blank to keep '{contact['zip'] or 'N/A'}'): ").strip() or None
                new_country = input(f"Enter new country (leave blank to keep '{contact['country'] or 'N/A'}'): ").strip() or None

                # Use the new select_account_by_search helper for updating account link
                print("\n--- Update Account Link ---")
                # Pass the current account ID to the prompt for clarity
                current_account_display = contact['account_id'] if contact['account_id'] is not None else 'None'
                # select_account_by_search returns None if user leaves blank, which means keep the old value.
                # It returns an int ID if user selects one, or 'back'.
                new_account_id_selection = select_account_by_search(f"Enter new associated Account Name or ID (leave blank to keep '{current_account_display}', enter 0 for none, or 'back'): ")

                if new_account_id_selection == 'back': continue # Go back if user entered 'back' during account selection

                # Determine the new account_id value based on user input
                new_account_id = None # Default: keep old value (don't add to update_params)
                if isinstance(new_account_id_selection, int):
                     # User entered a valid ID or 0
                     new_account_id = new_account_id_selection if new_account_id_selection > 0 else None
                     # Add to update_params below
                elif new_account_id_selection is None:
                     # User left the search blank. This means keep the old value.
                     # We don't add account_id to update_params in this case.
                     pass # new_account_id remains None, and we won't add it to update_params
                # Note: select_account_by_search handles invalid input and loops internally.


                update_params = {}
                if new_first_name is not None:
                    update_params['first_name'] = new_first_name
                if new_last_name is not None:
                    update_params['last_name'] = new_last_name
                if new_title is not None:
                    update_params['title'] = new_title
                if new_email is not None:
                    update_params['email'] = new_email
                if new_phone is not None:
                    update_params['phone'] = new_phone
                if new_description is not None:
                    update_params['description'] = new_description
                if new_website is not None:
                    update_params['website'] = new_website
                if new_street is not None:
                    update_params['street'] = new_street
                if new_city is not None:
                    update_params['city'] = new_city
                if new_state is not None:
                    update_params['state'] = new_state
                if new_zip is not None:
                    update_params['zip'] = new_zip
                if new_country is not None:
                    update_params['country'] = new_country

                # Only update account_id if the user provided input during the selection process
                # (i.e., new_account_id_selection was not None and not 'back')
                if new_account_id_selection is not None and new_account_id_selection != 'back':
                     update_params['account_id'] = new_account_id


                if not update_params:
                    print("No update parameters provided.")
                    continue

                success = update_contact(contact_id, **update_params)
                if success:
                    print(f"SUCCESS: Contact with ID {contact_id} updated.")
                else:
                    print(f"FAILED: Could not update contact with ID {contact_id}. Ensure email is unique and account ID is valid.") # DAL prints specific error

            elif choice == '5': # Delete Contact (by search/ID)
                print("\n--- Delete Contact ---")
                contact_id_selection = select_contact_by_search("Enter Contact Name, Email, or ID to delete (or 'back'): ")
                if contact_id_selection == 'back': continue
                if contact_id_selection is None: # User left blank, but Delete requires selection
                     print("Contact selection is required to delete.")
                     continue
                contact_id = contact_id_selection # Use the selected ID

                success = delete_contact(contact_id)
                if success:
                    print(f"SUCCESS: Contact with ID {contact_id} deleted.")
                else:
                    print(f"FAILED: Could not delete contact with ID {contact_id}. It might not exist.")

            elif choice == '6': # Back
                break

            else:
                print("Invalid choice. Please try again.")
        except (KeyboardInterrupt, EOFError):
            graceful_exit()


def handle_opportunities_menu():
    """Handles the opportunities management menu loop."""
    while True:
        try:
            display_opportunities_menu()
            choice = input("Enter your choice: ").strip()

            if choice == '1': # Create Opportunity
                name = input("Enter opportunity name (required): ").strip()
                description = get_multiline_input("Enter description (optional):")
                if description == 'back':
                    continue

                amount_input = get_float_input("Enter amount (optional, leave blank for none, or 'back'): ")
                if amount_input == 'back': continue
                amount = amount_input

                close_date = input("Enter expected close date (YYYY-MM-DD, optional, or 'back'): ").strip()
                if close_date.lower() == 'back': continue
                close_date = close_date or None # Set to None if empty after stripping

                if not name:
                    print("Name is required.")
                    continue

                # Use the new select_account_by_search helper for required account
                print("\n--- Link Opportunity to Account ---")
                account_id = select_account_by_search("Enter associated Account Name or ID (required, or 'back'): ")
                if account_id == 'back': continue
                if account_id is None: # select_account_by_search returns None if search yields no results and user didn't enter ID
                     print("Account selection failed or no account found. Account is required.")
                     continue # Stay in opportunity menu

                # Use the new select_contact_by_search helper for optional contact
                print("\n--- Link Opportunity to Contact ---")
                # select_contact_by_search returns None if user leaves blank, which is okay for optional contact_id
                contact_id = select_contact_by_search("Enter associated Contact Name, Email, or ID (optional, leave blank for none, or 'back'): ")
                if contact_id == 'back': continue # Go back if user entered 'back' during contact selection


                opportunity_id = create_opportunity(name, description, amount, close_date, account_id, contact_id)
                if opportunity_id:
                    print(f"SUCCESS: Opportunity '{name}' created with ID: {opportunity_id}")
                else:
                    print(f"FAILED: Could not create opportunity '{name}'. Ensure account ID is valid.") # DAL prints specific error

            elif choice == '2': # List Opportunities
                opportunities = list_opportunities()
                if opportunities:
                    # Debug: Print first opportunity raw data
                    print("\nDEBUG - Raw opportunity data:")
                    first_opp = opportunities[0]
                    print(f"Type: {type(first_opp)}")
                    print(f"Keys: {list(first_opp.keys()) if hasattr(first_opp, 'keys') else 'No keys method'}")
                    print(f"Dict representation: {dict(first_opp) if hasattr(first_opp, '__iter__') else 'Cannot convert to dict'}")
                    
                    # Additional logging for each field access
                    print("\nDEBUG - Key checks:")
                    for key in ['opportunity_id', 'name', 'account_id', 'contact_id', 'stage', 'status', 'amount', 'created_at']:
                        try:
                            print(f"Key '{key}' exists: {key in first_opp}, Value: {first_opp[key] if key in first_opp else 'N/A'}")
                        except Exception as e:
                            print(f"Error accessing key '{key}': {str(e)}")
                    
                    print("End DEBUG\n")
                    
                    print("\n--- All Opportunities ---")
                    padding = 2

                    # Headers
                    id_header = "ID"
                    name_header = "Name"
                    description_header = "Description"
                    account_header = "Account"
                    contact_header = "Contact"
                    value_header = "Value"
                    created_at_header = "Created At" # New header

                    # Initialize max lengths with header lengths
                    max_id_len = len(id_header)
                    max_name_len = len(name_header)
                    max_description_len = len(description_header)
                    max_account_len = len(account_header)
                    max_contact_len = len(contact_header)
                    max_value_len = len(value_header)
                    max_created_at_len = len(created_at_header) # New max length

                    processed_opportunities = []
                    for opp in opportunities: # opp is an sqlite3.Row object
                        try:
                            # Direct access without checking 'in' since sqlite3.Row doesn't support it
                            opp_id_str = str(opp['opportunity_id'])
                            opp_name_str = opp['name'] if opp['name'] is not None else "N/A"
                            
                            # Truncate description for display
                            description_display = truncate_text(opp['description'] or 'N/A')
                            
                            account_display = "N/A"
                            if opp['account_id'] is not None:
                                acc = get_account(opp['account_id'])
                                if acc:
                                    account_display = f"{acc['name']} (ID: {opp['account_id']})"
                                else:
                                    account_display = f"(ID: {opp['account_id']}) (Not Found)"
                            
                            contact_display = "N/A"
                            if opp['contact_id'] is not None:
                                con = get_contact(opp['contact_id'])
                                if con:
                                    contact_display = f"{con['first_name']} {con['last_name']} (ID: {opp['contact_id']})"
                                else:
                                    contact_display = f"(ID: {opp['contact_id']}) (Not Found)"
                            
                            # Use amount field for value display
                            value_str = str(opp['amount']) if opp['amount'] is not None else "N/A"
                            
                            # Convert 'created_at' to local timezone display
                            created_at_display = convert_utc_to_local_display(opp['created_at']) if opp['created_at'] else "N/A"
                        except Exception as e:
                            print(f"ERROR processing opportunity: {str(e)}")
                            continue

                        processed_opportunities.append({
                            'id': opp_id_str,
                            'name': opp_name_str,
                            'description': description_display,
                            'account': account_display,
                            'contact': contact_display,
                            'value': value_str,
                            'created_at': created_at_display # Add to processed data
                        })

                        # Update max lengths based on data
                        max_id_len = max(max_id_len, len(opp_id_str))
                        max_name_len = max(max_name_len, len(opp_name_str))
                        max_description_len = max(max_description_len, len(description_display))
                        max_account_len = max(max_account_len, len(account_display))
                        max_contact_len = max(max_contact_len, len(contact_display))
                        max_value_len = max(max_value_len, len(value_str))
                        max_created_at_len = max(max_created_at_len, len(created_at_display)) # Update for new column

                    # Add padding to max lengths to get column widths
                    id_col_width = max_id_len + padding
                    name_col_width = max_name_len + padding
                    description_col_width = max_description_len + padding
                    account_col_width = max_account_len + padding
                    contact_col_width = max_contact_len + padding
                    value_col_width = max_value_len + padding
                    created_at_col_width = max_created_at_len + padding # New column width

                    # Construct header string and print
                    header_format = f"{{:<{id_col_width}}} | {{:<{name_col_width}}} | {{:<{description_col_width}}} | {{:<{account_col_width}}} | {{:<{contact_col_width}}} | {{:<{value_col_width}}} | {{:<{created_at_col_width}}}"
                    header_line = header_format.format(id_header, name_header, description_header, account_header, contact_header, value_header, created_at_header)
                    print(header_line)
                    print("-" * len(header_line))

                    # Print data rows
                    for popp in processed_opportunities:
                        print(header_format.format(popp['id'], popp['name'], popp['description'], popp['account'], popp['contact'], popp['value'], popp['created_at']))
                    print("-" * len(header_line))
                else:
                    print("No opportunities found.")
            elif choice == '3': # Get Opportunity
                print("\n--- Get Opportunity ---")
                opportunity_id_selection = select_opportunity_by_search("Enter Opportunity Name, Description, or ID to get (or 'back'): ")
                if opportunity_id_selection == 'back': continue
                if opportunity_id_selection is None: # User left blank, but Get requires selection
                     print("Opportunity selection is required to get details.")
                     continue

                opportunity_details = get_opportunity(opportunity_id_selection) # Renamed to avoid conflict
                if opportunity_details:
                    print("\n--- Opportunity Details ---")
                    print(f"  ID           : {opportunity_details['opportunity_id']}")
                    print(f"  Name         : {opportunity_details['name']}")
                    print(f"  Description  : {opportunity_details['description'] or 'N/A'}")
                    print(f"  Amount       : {opportunity_details['amount'] or 'N/A'}")
                    print(f"  Close Date   : {opportunity_details['close_date'] or 'N/A'}")
                    
                    account_display_details = "N/A"
                    if opportunity_details['account_id']:
                        acc = get_account(opportunity_details['account_id'])
                        if acc:
                            account_display_details = f"{acc['name']} (ID: {acc['account_id']})"
                        else:
                            account_display_details = f"Unknown Account (ID: {opportunity_details['account_id']})"
                    print(f"  Account      : {account_display_details}")

                    contact_display_details = "N/A"
                    if opportunity_details['contact_id']:
                        contact_obj = get_contact(opportunity_details['contact_id'])
                        if contact_obj:
                            contact_display_details = f"{contact_obj['first_name']} {contact_obj['last_name']} (ID: {contact_obj['contact_id']})"
                        else:
                            contact_display_details = f"Unknown Contact (ID: {opportunity_details['contact_id']})"
                    print(f"  Contact      : {contact_display_details}")
                    print(f"  Created At   : {convert_utc_to_local_display(opportunity_details['created_at'])}")
                    print("-------------------------")
                else:
                    print(f"Opportunity with ID {opportunity_id_selection} not found.")

            elif choice == '4': # Update Opportunity (by search/ID)
                print("\n--- Update Opportunity ---")
                opportunity_id_selection = select_opportunity_by_search("Enter Opportunity Name, Description, or ID to update (or 'back'): ")
                if opportunity_id_selection == 'back': continue
                if opportunity_id_selection is None: # User left blank, but Update requires selection
                     print("Opportunity selection is required to update.")
                     continue
                opportunity_id = opportunity_id_selection # Use the selected ID

                opportunity = get_opportunity(opportunity_id) # Re-fetch to show current details
                if not opportunity:
                    print(f"Opportunity with ID {opportunity_id} not found.")
                    continue

                print(f"Current Opportunity Details: ID: {opportunity['opportunity_id']}, Name: {opportunity['name']}, Amount: {opportunity['amount']}, Close Date: {opportunity['close_date']}, Account ID: {opportunity['account_id']}, Contact ID: {opportunity['contact_id']}")

                new_name = input(f"Enter new name (leave blank to keep '{opportunity['name']}'): ").strip() or None
                
                # Handle multi-line description
                print(f"Current description: {opportunity['description'] or 'N/A'}")
                new_description = get_multiline_input(f"Enter new description (leave blank to keep current)")
                if new_description == 'back':
                    continue

                new_amount_input_str = input("Enter new amount (leave blank to keep '{}', or 'back'): ".format(opportunity['amount'] or 'None')).strip()
                if new_amount_input_str.lower() == 'back': continue
                new_amount = None
                if new_amount_input_str:
                    try:
                        new_amount = float(new_amount_input_str)
                    except ValueError:
                        print("Invalid amount entered. Keeping old value.")
                        new_amount = opportunity['amount'] # Revert to old value on invalid input
                else:
                    new_amount = opportunity['amount'] # Keep old value if blank


                new_close_date_input = input("Enter new close date (YYYY-MM-DD, leave blank to keep '{}', or 'back'): ".format(opportunity['close_date'] or 'None')).strip()
                if new_close_date_input.lower() == 'back': continue
                new_close_date = new_close_date_input or None # Set to None if empty after stripping


                # Use the new select_account_by_search helper for updating account link
                print("\n--- Update Account Link ---")
                current_account_display = opportunity['account_id'] if opportunity['account_id'] is not None else 'None'
                # select_account_by_search returns None if user leaves blank, which means keep the old value.
                # It returns an int ID if user selects one, or 'back'.
                new_account_id_selection = select_account_by_search(f"Enter new associated Account Name or ID (leave blank to keep '{current_account_display}', or 'back'): ")

                if new_account_id_selection == 'back': continue # Go back if user entered 'back' during account selection

                # Determine the new account_id value based on user input
                new_account_id = None # Default: keep old value (don't add to update_params)
                if isinstance(new_account_id_selection, int):
                     # User entered a valid ID
                     new_account_id = new_account_id_selection
                     # Add to update_params below
                elif new_account_id_selection is None:
                     # User left the search blank. This means keep the old value.
                     # We don't add account_id to update_params in this case.
                     pass # new_account_id remains None, and we won't add it to update_params


                # Use the new select_contact_by_search helper for updating contact link
                print("\n--- Update Contact Link ---")
                current_contact_display = opportunity['contact_id'] if opportunity['contact_id'] is not None else 'None'
                # select_contact_by_search returns None if user leaves blank, which means keep the old value.
                # It returns an int ID if user selects one, or 'back'.
                new_contact_id_selection = select_contact_by_search(f"Enter new associated Contact Name, Email, or ID (leave blank to keep '{current_contact_display}', enter 0 for none, or 'back'): ")

                if new_contact_id_selection == 'back': continue # Go back if user entered 'back' during contact selection

                # Determine the new contact_id value based on user input
                new_contact_id = None # Default: keep old value (don't add to update_params)
                if isinstance(new_contact_id_selection, int):
                     # User entered a valid ID or 0
                     new_contact_id = new_contact_id_selection if new_contact_id_selection > 0 else None
                     # Add to update_params below
                elif new_contact_id_selection is None:
                     # User left the search blank. This means keep the old value.
                     # We don't add contact_id to update_params in this case.
                     pass # new_contact_id remains None, and we won't add it to update_params


                update_params = {}
                if new_name is not None:
                    update_params['name'] = new_name
                if new_description is not None:
                    update_params['description'] = new_description
                # Only update amount if the user provided a non-empty input string (handled by get_float_input returning float or None)
                # Check if new_amount is not None (user entered a number) OR if the original input string was empty (user cleared it)
                # Corrected logic: Check if the user provided *any* input for amount (new_amount_input_str is not empty)
                if new_amount_input_str:
                     update_params['amount'] = new_amount
                if new_close_date is not None:
                    update_params['close_date'] = new_close_date

                # Only update account_id if the user provided input during the selection process
                if new_account_id_selection is not None and new_account_id_selection != 'back':
                     update_params['account_id'] = new_account_id

                # Only update contact_id if the user provided input during the selection process
                if new_contact_id_selection is not None and new_contact_id_selection != 'back':
                     update_params['contact_id'] = new_contact_id


                if not update_params:
                    print("No update parameters provided.")
                    continue

                success = update_opportunity(opportunity_id, **update_params)
                if success:
                    print(f"SUCCESS: Opportunity with ID {opportunity_id} updated.")
                else:
                    print(f"FAILED: Could not update opportunity with ID {opportunity_id}. Ensure account/contact IDs are valid.") # DAL prints specific error


            elif choice == '5': # Delete Opportunity (by search/ID)
                print("\n--- Delete Opportunity ---")
                opportunity_id_selection = select_opportunity_by_search("Enter Opportunity Name, Description, or ID to delete (or 'back'): ")
                if opportunity_id_selection == 'back': continue
                if opportunity_id_selection is None: # User left blank, but Delete requires selection
                     print("Opportunity selection is required to delete.")
                     continue
                opportunity_id = opportunity_id_selection # Use the selected ID

                success = delete_opportunity(opportunity_id)
                if success:
                    print(f"SUCCESS: Opportunity with ID {opportunity_id} deleted.")
                else:
                    print(f"FAILED: Could not delete opportunity with ID {opportunity_id}. It might not exist.")

            elif choice == '6': # Back
                break

            else:
                print("Invalid choice. Please try again.")
        except (KeyboardInterrupt, EOFError):
            graceful_exit()


def export_contacts_to_csv():
    """Export contacts with account names to a CSV file."""
    contacts = list_contacts()
    
    if not contacts:
        print("No contacts to export.")
        return
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/contacts_export_{timestamp}.csv"
    
    try:
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['ID', 'First Name', 'Last Name', 'Title', 'Email', 'Phone', 
                      'Description', 'Website', 'Street', 'City', 'State', 'Zip', 'Country', 'Account Name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for contact in contacts:
                # Get account name if account_id is available
                account_name = "N/A"
                if contact['account_id']:
                    account = get_account(contact['account_id'])
                    if account:
                        account_name = account['name']
                
                writer.writerow({
                    'ID': contact['contact_id'],
                    'First Name': contact['first_name'],
                    'Last Name': contact['last_name'],
                    'Title': contact['title'] or 'N/A',
                    'Email': contact['email'] or 'N/A',
                    'Phone': contact['phone'] or 'N/A',
                    'Description': contact['description'] or 'N/A',
                    'Website': contact['website'] or 'N/A',
                    'Street': contact['street'] or 'N/A',
                    'City': contact['city'] or 'N/A',
                    'State': contact['state'] or 'N/A',
                    'Zip': contact['zip'] or 'N/A',
                    'Country': contact['country'] or 'N/A',
                    'Account Name': account_name
                })
        
        print(f"SUCCESS: Contacts exported to {filename}")
    except Exception as e:
        print(f"ERROR: Failed to export contacts: {e}")

def export_opportunities_to_csv():
    """Export opportunities with account names and contact details to a CSV file."""
    opportunities = list_opportunities()
    
    if not opportunities:
        print("No opportunities to export.")
        return
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/opportunities_export_{timestamp}.csv"
    
    try:
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['ID', 'Name', 'Description', 'Amount', 'Close Date', 'Account Name', 'Contact Name', 'Contact Email', 'Created At']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for opp in opportunities:
                # Get account name if account_id is available
                account_name = "N/A"
                if opp['account_id']:
                    account = get_account(opp['account_id'])
                    if account:
                        account_name = account['name']
                
                # Get contact details if contact_id is available
                contact_name = "N/A"
                contact_email = "N/A"
                if opp['contact_id']:
                    contact = get_contact(opp['contact_id'])
                    if contact:
                        contact_name = f"{contact['first_name']} {contact['last_name']}"
                        contact_email = contact['email'] or "N/A"
                
                writer.writerow({
                    'ID': opp['opportunity_id'],
                    'Name': opp['name'],
                    'Description': opp['description'] or 'N/A',
                    'Amount': opp['amount'] or 'N/A',
                    'Close Date': opp['close_date'] or 'N/A',
                    'Account Name': account_name,
                    'Contact Name': contact_name,
                    'Contact Email': contact_email,
                    'Created At': convert_utc_to_local_display(opp['created_at'])
                })
        
        print(f"SUCCESS: Opportunities exported to {filename}")
    except Exception as e:
        print(f"ERROR: Failed to export opportunities: {e}")

def handle_export_menu():
    """Handles the export menu options."""
    while True:
        try:
            display_export_menu()
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':  # Export Contacts
                export_contacts_to_csv()
            elif choice == '2':  # Export Opportunities
                export_opportunities_to_csv()
            elif choice == '3':  # Back to Main Menu
                break
            else:
                print("Invalid choice. Please try again.")
        except (KeyboardInterrupt, EOFError):
            graceful_exit()


def main():
    """
    Main function for the CRM CLI application.
    Displays menus and handles user interaction.
    """
    # Ensure database tables exist and are properly migrated
    initialize_database()

    print("Welcome to the Simple CRM CLI Application!")

    while True:
        try:
            display_main_menu()
            choice = input("Enter your choice: ").strip()

            if choice == '1':
                handle_accounts_menu()
            elif choice == '2':
                handle_contacts_menu()
            elif choice == '3':
                handle_opportunities_menu()
            elif choice == '4': # Handle Summary
                handle_summary_menu()
            elif choice == '5': # Handle Export
                handle_export_menu()
            elif choice == '6': # Handle Exit
                graceful_exit()
            else:
                print("Invalid choice. Please try again.")
        except (KeyboardInterrupt, EOFError):
            graceful_exit()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

