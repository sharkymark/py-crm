import sys
from database import create_tables
from crm_dal import (
    create_account, get_account, list_accounts, update_account, delete_account,
    create_contact, get_contact, list_contacts, update_contact, delete_contact,
    create_opportunity, get_opportunity, list_opportunities, update_opportunity, delete_opportunity
)

def display_main_menu():
    """Displays the main menu options."""
    print("\n--- Simple CRM Main Menu ---")
    print("1. Manage Accounts")
    print("2. Manage Contacts")
    print("3. Manage Opportunities")
    print("4. Exit")
    print("----------------------------")

def display_accounts_menu():
    """Displays the accounts management menu."""
    print("\n--- Manage Accounts ---")
    print("1. Create Account")
    print("2. List Accounts")
    print("3. Get Account by ID")
    print("4. Update Account by ID")
    print("5. Delete Account by ID")
    print("6. Back to Main Menu")
    print("-----------------------")

def display_contacts_menu():
    """Displays the contacts management menu."""
    print("\n--- Manage Contacts ---")
    print("1. Create Contact")
    print("2. List Contacts")
    print("3. Get Contact by ID")
    print("4. Update Contact by ID")
    print("5. Delete Contact by ID")
    print("6. Back to Main Menu")
    print("-----------------------")

def display_opportunities_menu():
    """Displays the opportunities management menu."""
    print("\n--- Manage Opportunities ---")
    print("1. Create Opportunity")
    print("2. List Opportunities")
    print("3. Get Opportunity by ID")
    print("4. Update Opportunity by ID")
    print("5. Delete Opportunity by ID")
    print("6. Back to Main Menu")
    print("--------------------------")

def get_integer_input(prompt):
    """Gets integer input from the user with validation."""
    while True:
        try:
            value = input(prompt)
            return int(value)
        except ValueError:
            print("Invalid input. Please enter an integer.")

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

        elif choice == '3': # Get Account by ID
            account_id = get_integer_input("Enter account ID to get: ")
            account = get_account(account_id)
            if account:
                print("\n--- Account Details ---")
                print(f"ID: {account['account_id']}")
                print(f"Name: {account['name']}")
                print(f"Industry: {account['industry']}")
                print(f"Created: {account['created_at']}")
                print("-----------------------")
            else:
                print(f"Account with ID {account_id} not found.")

        elif choice == '4': # Update Account by ID
            account_id = get_integer_input("Enter account ID to update: ")
            account = get_account(account_id)
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

        elif choice == '5': # Delete Account by ID
            account_id = get_integer_input("Enter account ID to delete: ")
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
            account_id = get_integer_input("Enter associated account ID (optional, 0 for none): ")
            account_id = account_id if account_id > 0 else None # Allow 0 or blank for no account

            if not first_name or not last_name or not email:
                 print("First name, last name, and email are required.")
                 continue

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

        elif choice == '3': # Get Contact by ID
            contact_id = get_integer_input("Enter contact ID to get: ")
            contact = get_contact(contact_id)
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
                print(f"Contact with ID {contact_id} not found.")

        elif choice == '4': # Update Contact by ID
            contact_id = get_integer_input("Enter contact ID to update: ")
            contact = get_contact(contact_id)
            if not contact:
                print(f"Contact with ID {contact_id} not found.")
                continue

            print(f"Current Contact Details: ID: {contact['contact_id']}, Name: {contact['first_name']} {contact['last_name']}, Email: {contact['email']}, Phone: {contact['phone']}, Account ID: {contact['account_id']}")
            new_first_name = input(f"Enter new first name (leave blank to keep '{contact['first_name']}'): ").strip() or None
            new_last_name = input(f"Enter new last name (leave blank to keep '{contact['last_name']}'): ").strip() or None
            new_email = input(f"Enter new email (leave blank to keep '{contact['email']}'): ").strip() or None
            new_phone = input(f"Enter new phone (leave blank to keep '{contact['phone']}'): ").strip() or None
            new_account_id_str = input(f"Enter new account ID (leave blank to keep '{contact['account_id'] or 'None'}', enter 0 for none): ").strip()

            new_account_id = None
            if new_account_id_str == '0':
                 new_account_id = None # Explicitly set to None if user enters 0
            elif new_account_id_str:
                 try:
                     new_account_id = int(new_account_id_str)
                 except ValueError:
                     print("Invalid account ID entered. Keeping old value.")
                     new_account_id = contact['account_id'] # Revert to old value on invalid input
            else:
                 new_account_id = contact['account_id'] # Keep old value if blank

            update_params = {}
            if new_first_name is not None:
                update_params['first_name'] = new_first_name
            if new_last_name is not None:
                update_params['last_name'] = new_last_name
            if new_email is not None:
                update_params['email'] = new_email
            if new_phone is not None:
                update_params['phone'] = new_phone
            # Only update account_id if the user provided a valid input (either a number or 0)
            if new_account_id_str or new_account_id_str == '0':
                 update_params['account_id'] = new_account_id


            if not update_params:
                print("No update parameters provided.")
                continue

            success = update_contact(contact_id, **update_params)
            if success:
                print(f"Contact with ID {contact_id} updated successfully.")
            else:
                print(f"Failed to update contact with ID {contact_id}. Ensure email is unique and account ID is valid.") # DAL prints specific error

        elif choice == '5': # Delete Contact by ID
            contact_id = get_integer_input("Enter contact ID to delete: ")
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
            amount_str = input("Enter amount (optional, leave blank for none): ").strip()
            amount = float(amount_str) if amount_str else None
            close_date = input("Enter expected close date (YYYY-MM-DD, optional): ").strip() or None # TODO: Add date validation
            account_id = get_integer_input("Enter associated account ID (required): ")
            contact_id = get_integer_input("Enter associated contact ID (optional, 0 for none): ")
            contact_id = contact_id if contact_id > 0 else None # Allow 0 or blank for no contact

            if not name or not account_id:
                print("Name and Account ID are required.")
                continue

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

        elif choice == '3': # Get Opportunity by ID
            opportunity_id = get_integer_input("Enter opportunity ID to get: ")
            opportunity = get_opportunity(opportunity_id)
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
                print(f"Opportunity with ID {opportunity_id} not found.")

        elif choice == '4': # Update Opportunity by ID
            opportunity_id = get_integer_input("Enter opportunity ID to update: ")
            opportunity = get_opportunity(opportunity_id)
            if not opportunity:
                print(f"Opportunity with ID {opportunity_id} not found.")
                continue

            print(f"Current Opportunity Details: ID: {opportunity['opportunity_id']}, Name: {opportunity['name']}, Amount: {opportunity['amount']}, Close Date: {opportunity['close_date']}, Account ID: {opportunity['account_id']}, Contact ID: {opportunity['contact_id']}")

            new_name = input(f"Enter new name (leave blank to keep '{opportunity['name']}'): ").strip() or None
            new_description = input(f"Enter new description (leave blank to keep '{opportunity['description']}'): ").strip() or None
            new_amount_str = input(f"Enter new amount (leave blank to keep '{opportunity['amount'] or 'None'}'): ").strip()
            new_close_date = input(f"Enter new close date (YYYY-MM-DD, leave blank to keep '{opportunity['close_date'] or 'None'}'): ").strip() or None # TODO: Add date validation
            new_account_id_str = input(f"Enter new account ID (leave blank to keep '{opportunity['account_id'] or 'None'}'): ").strip()
            new_contact_id_str = input(f"Enter new contact ID (leave blank to keep '{opportunity['contact_id'] or 'None']}', enter 0 for none): ").strip()

            new_amount = None
            if new_amount_str:
                try:
                    new_amount = float(new_amount_str)
                except ValueError:
                    print("Invalid amount entered. Keeping old value.")
                    new_amount = opportunity['amount'] # Revert to old value on invalid input
            else:
                new_amount = opportunity['amount'] # Keep old value if blank

            new_account_id = None
            if new_account_id_str:
                 try:
                     new_account_id = int(new_account_id_str)
                 except ValueError:
                     print("Invalid account ID entered. Keeping old value.")
                     new_account_id = opportunity['account_id'] # Revert to old value on invalid input
            else:
                 new_account_id = opportunity['account_id'] # Keep old value if blank

            new_contact_id = None
            if new_contact_id_str == '0':
                 new_contact_id = None # Explicitly set to None if user enters 0
            elif new_contact_id_str:
                 try:
                     new_contact_id = int(new_contact_id_str)
                 except ValueError:
                     print("Invalid contact ID entered. Keeping old value.")
                     new_contact_id = opportunity['contact_id'] # Revert to old value on invalid input
            else:
                 new_contact_id = opportunity['contact_id'] # Keep old value if blank


            update_params = {}
            if new_name is not None:
                update_params['name'] = new_name
            if new_description is not None:
                update_params['description'] = new_description
            # Only update amount if the user provided a valid input
            if new_amount_str:
                 update_params['amount'] = new_amount
            if new_close_date is not None:
                update_params['close_date'] = new_close_date
            # Only update account_id if the user provided a valid input
            if new_account_id_str:
                 update_params['account_id'] = new_account_id
            # Only update contact_id if the user provided a valid input (number or 0)
            if new_contact_id_str or new_contact_id_str == '0':
                 update_params['contact_id'] = new_contact_id


            if not update_params:
                print("No update parameters provided.")
                continue

            success = update_opportunity(opportunity_id, **update_params)
            if success:
                print(f"Opportunity with ID {opportunity_id} updated successfully.")
            else:
                print(f"Failed to update opportunity with ID {opportunity_id}. Ensure account/contact IDs are valid.") # DAL prints specific error


        elif choice == '5': # Delete Opportunity by ID
            opportunity_id = get_integer_input("Enter opportunity ID to delete: ")
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
        elif choice == '4':
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

