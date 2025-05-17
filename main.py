import sys
from database import create_tables
from crm_dal import (
    create_account, get_account, list_accounts, update_account, delete_account, search_accounts,
    create_contact, get_contact, list_contacts, update_contact, delete_contact, search_contacts,
    create_opportunity, get_opportunity, list_opportunities, update_opportunity, delete_opportunity, search_opportunities,
    get_contacts_by_account, get_opportunities_by_account # Import new DAL functions
)

def display_main_menu():
    """Displays the main menu options."""
    print("\n--- Simple CRM Main Menu ---")
    print("1. Manage Accounts")
    print("2. Manage Contacts")
    print("3. Manage Opportunities")
    print("4. Summary") # Added Summary Option
    print("5. Exit") # Renumbered Exit
    print("----------------------------")

def display_accounts_menu():
    """Displays the accounts management menu."""
    print("\n--- Manage Accounts ---")
    print("1. Create Account")
    print("2. List All Accounts")
    print("3. Get Account") # Removed "by ID"
    print("4. Update Account") # Removed "by ID"
    print("5. Delete Account") # Removed "by ID"
    print("6. Back to Main Menu") # Renumbered
    print("-----------------------")

def display_contacts_menu():
    """Displays the contacts management menu."""
    print("\n--- Manage Contacts ---")
    print("1. Create Contact")
    print("2. List All Contacts")
    print("3. Get Contact") # Removed "by ID"
    print("4. Update Contact") # Removed "by ID"
    print("5. Delete Contact") # Removed "by ID"
    print("6. Back to Main Menu") # Renumbered
    print("-----------------------")

def display_opportunities_menu():
    """Displays the opportunities management menu."""
    print("\n--- Manage Opportunities ---")
    print("1. Create Opportunity")
    print("2. List All Opportunities")
    print("3. Get Opportunity") # Removed "by ID"
    print("4. Update Opportunity") # Removed "by ID"
    print("5. Delete Opportunity") # Removed "by ID"
    print("6. Back to Main Menu") # Renumbered
    print("--------------------------")

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

def select_account_by_search(prompt="Enter Account Name or ID (or 'back'): "):
    """
    Prompts user to search for an account by name or enter an ID,
    handles search results, and returns the selected account ID or None/back.
    Returns None if user leaves search blank and it's optional.
    """
    while True:
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

def select_contact_by_search(prompt="Enter Contact Name, Email, or ID (or 'back'): "):
    """
    Prompts user to search for a contact by name/email or enter an ID,
    handles search results, and returns the selected contact ID or None/back.
    Returns None if user leaves search blank and it's optional.
    """
    while True:
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

def select_opportunity_by_search(prompt="Enter Opportunity Name, Description, or ID (or 'back'): "):
    """
    Prompts user to search for an opportunity by name/description or enter an ID,
    handles search results, and returns the selected opportunity ID or None/back.
    Returns None if user leaves search blank and it's optional.
    """
    while True:
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


# --- Summary Handler ---
def handle_summary_menu():
    """Handles the summary menu option."""
    print("\n--- CRM Summary ---")
    search_term = input("Enter search term for Accounts, Contacts, or Opportunities (or 'back'): ").strip()
    if search_term.lower() == 'back':
        return
    if not search_term:
        print("Search term cannot be empty.")
        return

    matching_accounts = search_accounts(search_term)
    matching_contacts = search_contacts(search_term)
    matching_opportunities = search_opportunities(search_term)

    displayed_contact_ids = set()
    displayed_opportunity_ids = set()

    print("\n--- Accounts ---")
    if matching_accounts:
        for account in matching_accounts:
            print(f"Account ID: {account['account_id']}, Name: {account['name']}, Industry: {account['industry']}")

            # Display Contacts linked to this Account
            contacts_for_account = get_contacts_by_account(account['account_id'])
            if contacts_for_account:
                print("  Contacts:")
                for contact in contacts_for_account:
                    print(f"    ID: {contact['contact_id']}, Name: {contact['first_name']} {contact['last_name']}, Email: {contact['email']}")
                    displayed_contact_ids.add(contact['contact_id'])

            # Display Opportunities linked to this Account
            opportunities_for_account = get_opportunities_by_account(account['account_id'])
            if opportunities_for_account:
                print("  Opportunities:")
                for opp in opportunities_for_account:
                    print(f"    ID: {opp['opportunity_id']}, Name: {opp['name']}, Amount: {opp['amount']}, Close Date: {opp['close_date']}")
                    displayed_opportunity_ids.add(opp['opportunity_id'])

                    # Display Contact linked to this Opportunity (if any)
                    if opp['contact_id']:
                        contact_for_opp = get_contact(opp['contact_id'])
                        if contact_for_opp:
                            print(f"      Contact: ID: {contact_for_opp['contact_id']}, Name: {contact_for_opp['first_name']} {contact_for_opp['last_name']}")
                            displayed_contact_ids.add(contact_for_opp['contact_id'])
    else:
        print("No matching accounts found.")

    print("\n--- Standalone Contacts ---")
    standalone_contacts_found = False
    if matching_contacts:
        for contact in matching_contacts:
            if contact['contact_id'] not in displayed_contact_ids:
                print(f"Contact ID: {contact['contact_id']}, Name: {contact['first_name']} {contact['last_name']}, Email: {contact['email']}, Account ID: {contact['account_id']}")
                standalone_contacts_found = True
                displayed_contact_ids.add(contact['contact_id']) # Add just in case

    if not standalone_contacts_found:
         print("No standalone matching contacts found.")


    print("\n--- Standalone Opportunities ---")
    standalone_opportunities_found = False
    if matching_opportunities:
        for opp in matching_opportunities:
            if opp['opportunity_id'] not in displayed_opportunity_ids:
                print(f"Opportunity ID: {opp['opportunity_id']}, Name: {opp['name']}, Amount: {opp['amount']}, Close Date: {opp['close_date']}, Account ID: {opp['account_id']}")
                standalone_opportunities_found = True
                displayed_opportunity_ids.add(opp['opportunity_id']) # Add just in case

                # Display Contact linked to this Standalone Opportunity (if any)
                if opp['contact_id']:
                    contact_for_opp = get_contact(opp['contact_id'])
                    if contact_for_opp:
                        print(f"  Contact: ID: {contact_for_opp['contact_id']}, Name: {contact_for_opp['first_name']} {contact_for_opp['last_name']}")
                        displayed_contact_ids.add(contact_for_opp['contact_id']) # Add just in case

    if not standalone_opportunities_found:
        print("No standalone matching opportunities found.")

    print("\n--- End Summary ---")


# --- Menu Handlers ---
def handle_accounts_menu():
    """Handles the accounts management menu loop."""
    while True:
        display_accounts_menu()
        choice = input("Enter your choice: ").strip()

        if choice == '1': # Create Account
            name = input("Enter account name (required): ").strip()
            if not name:
                print("Account name is required.")
                continue
            industry = input("Enter account industry (optional): ").strip() or None
            account_id = create_account(name, industry)
            if account_id:
                print(f"Account '{name}' created successfully with ID: {account_id}")
            else:
                print(f"Failed to create account '{name}'.")

        elif choice == '2': # List Accounts
            accounts = list_accounts()
            if accounts:
                print("\n--- Accounts ---")
                for account in accounts:
                    print(f"ID: {account['account_id']}, Name: {account['name']}, Industry: {account['industry']}, Created: {account['created_at']}")
                print("----------------")
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
                print(f"ID: {account['account_id']}")
                print(f"Name: {account['name']}")
                print(f"Industry: {account['industry']}")
                print(f"Created: {account['created_at']}")
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

            print(f"Current Account Details: ID: {account['account_id']}, Name: {account['name']}, Industry: {account['industry']}")
            new_name = input(f"Enter new name (leave blank to keep '{account['name']}'): ").strip() or None
            new_industry = input(f"Enter new industry (leave blank to keep '{account['industry']}'): ").strip() or None

            update_params = {}
            if new_name is not None:
                update_params['name'] = new_name
            if new_industry is not None:
                update_params['industry'] = new_industry

            if not update_params:
                print("No update parameters provided.")
                continue

            success = update_account(account_id, **update_params)
            if success:
                print(f"Account with ID {account_id} updated successfully.")
            else:
                print(f"Failed to update account with ID {account_id}.") # DAL prints specific error

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
                print(f"Account with ID {account_id} deleted successfully.")
            else:
                print(f"Failed to delete account with ID {account_id}. It might not exist.")

        elif choice == '6': # Back
            break

        else:
            print("Invalid choice. Please try again.")

def handle_contacts_menu():
    """Handles the contacts management menu loop."""
    while True:
        display_contacts_menu()
        choice = input("Enter your choice: ").strip()

        if choice == '1': # Create Contact
            first_name = input("Enter contact first name (required): ").strip()
            last_name = input("Enter contact last name (required): ").strip()
            email = input("Enter contact email (required, must be unique): ").strip()
            phone = input("Enter contact phone (optional): ").strip() or None

            if not first_name or not last_name or not email:
                 print("First name, last name, and email are required.")
                 continue

            # Use the new select_account_by_search helper
            print("\n--- Link Contact to Account ---")
            # select_account_by_search returns None if user leaves blank, which is okay for optional account_id
            account_id = select_account_by_search("Enter associated Account Name or ID (optional, leave blank for none, or 'back'): ")
            if account_id == 'back': continue # Go back if user entered 'back' during account selection

            contact_id = create_contact(first_name, last_name, email, phone, account_id)
            if contact_id:
                print(f"Contact '{first_name} {last_name}' created successfully with ID: {contact_id}")
            else:
                print(f"Failed to create contact '{first_name} {last_name}'. Ensure email is unique and account ID is valid.")

        elif choice == '2': # List Contacts
            contacts = list_contacts()
            if contacts:
                print("\n--- Contacts ---")
                for contact in contacts:
                    print(f"ID: {contact['contact_id']}, Name: {contact['first_name']} {contact['last_name']}, Email: {contact['email']}, Phone: {contact['phone']}, Account ID: {contact['account_id']}, Created: {contact['created_at']}")
                print("----------------")
            else:
                print("No contacts found.")

        elif choice == '3': # Get Contact (by search/ID)
            print("\n--- Get Contact ---")
            contact_id_selection = select_contact_by_search("Enter Contact Name, Email, or ID to get (or 'back'): ")
            if contact_id_selection == 'back': continue
            if contact_id_selection is None: # User left blank, but Get requires selection
                 print("Contact selection is required to get details.")
                 continue

            contact = get_contact(contact_id_selection)
            if contact:
                print("\n--- Contact Details ---")
                print(f"ID: {contact['contact_id']}")
                print(f"Name: {contact['first_name']} {contact['last_name']}")
                print(f"Email: {contact['email']}")
                print(f"Phone: {contact['phone']}")
                print(f"Account ID: {contact['account_id']}")
                print(f"Created: {contact['created_at']}")
                print("-----------------------")
            else:
                 # This case should ideally not be reached if select_contact_by_search returns a valid ID
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

            print(f"Current Contact Details: ID: {contact['contact_id']}, Name: {contact['first_name']} {contact['last_name']}, Email: {contact['email']}, Phone: {contact['phone']}, Account ID: {contact['account_id']}")
            new_first_name = input(f"Enter new first name (leave blank to keep '{contact['first_name']}'): ").strip() or None
            new_last_name = input(f"Enter new last name (leave blank to keep '{contact['last_name']}'): ").strip() or None
            new_email = input(f"Enter new email (leave blank to keep '{contact['email']}'): ").strip() or None
            new_phone = input(f"Enter new phone (leave blank to keep '{contact['phone']}'): ").strip() or None

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
            if new_email is not None:
                update_params['email'] = new_email
            if new_phone is not None:
                update_params['phone'] = new_phone

            # Only update account_id if the user provided input during the selection process
            # (i.e., new_account_id_selection was not None and not 'back')
            if new_account_id_selection is not None and new_account_id_selection != 'back':
                 update_params['account_id'] = new_account_id


            if not update_params:
                print("No update parameters provided.")
                continue

            success = update_contact(contact_id, **update_params)
            if success:
                print(f"Contact with ID {contact_id} updated successfully.")
            else:
                print(f"Failed to update contact with ID {contact_id}. Ensure email is unique and account ID is valid.") # DAL prints specific error

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
                print(f"Contact with ID {contact_id} deleted successfully.")
            else:
                print(f"Failed to delete contact with ID {contact_id}. It might not exist.")

        elif choice == '6': # Back
            break

        else:
            print("Invalid choice. Please try again.")

def handle_opportunities_menu():
    """Handles the opportunities management menu loop."""
    while True:
        display_opportunities_menu()
        choice = input("Enter your choice: ").strip()

        if choice == '1': # Create Opportunity
            name = input("Enter opportunity name (required): ").strip()
            description = input("Enter description (optional): ").strip() or None

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
                print(f"Opportunity '{name}' created successfully with ID: {opportunity_id}")
            else:
                print(f"Failed to create opportunity '{name}'. Ensure account ID is valid.") # DAL prints specific error

        elif choice == '2': # List Opportunities
            opportunities = list_opportunities()
            if opportunities:
                print("\n--- Opportunities ---")
                for opp in opportunities:
                    print(f"ID: {opp['opportunity_id']}, Name: {opp['name']}, Amount: {opp['amount']}, Close Date: {opp['close_date']}, Account ID: {opp['account_id']}, Contact ID: {opp['contact_id']}, Created: {opp['created_at']}")
                print("---------------------")
            else:
                print("No opportunities found.")

        elif choice == '3': # Get Opportunity (by search/ID)
            print("\n--- Get Opportunity ---")
            opportunity_id_selection = select_opportunity_by_search("Enter Opportunity Name, Description, or ID to get (or 'back'): ")
            if opportunity_id_selection == 'back': continue
            if opportunity_id_selection is None: # User left blank, but Get requires selection
                 print("Opportunity selection is required to get details.")
                 continue

            opportunity = get_opportunity(opportunity_id_selection)
            if opportunity:
                print("\n--- Opportunity Details ---")
                print(f"ID: {opportunity['opportunity_id']}")
                print(f"Name: {opportunity['name']}")
                print(f"Description: {opportunity['description']}")
                print(f"Amount: {opportunity['amount']}")
                print(f"Close Date: {opportunity['close_date']}")
                print(f"Account ID: {opportunity['account_id']}")
                print(f"Contact ID: {opportunity['contact_id']}")
                print(f"Created: {opportunity['created_at']}")
                print("-------------------------")
            else:
                 # This case should ideally not be reached if select_opportunity_by_search returns a valid ID
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
            new_description = input(f"Enter new description (leave blank to keep '{opportunity['description']}'): ").strip() or None

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
                print(f"Opportunity with ID {opportunity_id} updated successfully.")
            else:
                print(f"Failed to update opportunity with ID {opportunity_id}. Ensure account/contact IDs are valid.") # DAL prints specific error


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
                print(f"Opportunity with ID {opportunity_id} deleted successfully.")
            else:
                print(f"Failed to delete opportunity with ID {opportunity_id}. It might not exist.")

        elif choice == '6': # Back
            break

        else:
            print("Invalid choice. Please try again.")


def main():
    """
    Main function for the CRM CLI application.
    Displays menus and handles user interaction.
    """
    # Ensure database tables exist
    create_tables()

    print("Welcome to the Simple CRM CLI Application!")

    while True:
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
        elif choice == '5': # Handle Exit
            print("Exiting application. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

