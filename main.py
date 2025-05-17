import argparse
import sys
from database import create_tables
from crm_dal import (
    create_account, get_account, list_accounts, update_account, delete_account,
    create_contact, get_contact, list_contacts, update_contact, delete_contact,
    create_opportunity, get_opportunity, list_opportunities, update_opportunity, delete_opportunity
)

# --- Command Wrapper Functions ---

# Account Commands
def create_account_command(args):
    account_id = create_account(args.name, args.industry)
    if account_id:
        print(f"Account '{args.name}' created successfully with ID: {account_id}")
    else:
        print(f"Failed to create account '{args.name}'.")

def list_accounts_command(args):
    accounts = list_accounts()
    if accounts:
        print("\n--- Accounts ---")
        for account in accounts:
            print(f"ID: {account['account_id']}, Name: {account['name']}, Industry: {account['industry']}, Created: {account['created_at']}")
        print("----------------")
    else:
        print("No accounts found.")

def get_account_command(args):
    account = get_account(args.account_id)
    if account:
        print("\n--- Account Details ---")
        print(f"ID: {account['account_id']}")
        print(f"Name: {account['name']}")
        print(f"Industry: {account['industry']}")
        print(f"Created: {account['created_at']}")
        print("-----------------------")
    else:
        print(f"Account with ID {args.account_id} not found.")

def update_account_command(args):
    # Only pass arguments if they were provided on the command line
    update_params = {}
    if args.name is not None:
        update_params['name'] = args.name
    if args.industry is not None:
        update_params['industry'] = args.industry

    if not update_params:
        print("No update parameters provided.")
        return

    success = update_account(args.account_id, **update_params)
    if success:
        print(f"Account with ID {args.account_id} updated successfully.")
    else:
        print(f"Failed to update account with ID {args.account_id}. It might not exist or no changes were made.")

def delete_account_command(args):
    success = delete_account(args.account_id)
    if success:
        print(f"Account with ID {args.account_id} deleted successfully.")
    else:
        print(f"Failed to delete account with ID {args.account_id}. It might not exist.")

# Contact Commands
def create_contact_command(args):
    contact_id = create_contact(args.first_name, args.last_name, args.email, args.phone, args.account_id)
    if contact_id:
        print(f"Contact '{args.first_name} {args.last_name}' created successfully with ID: {contact_id}")
    else:
        print(f"Failed to create contact '{args.first_name} {args.last_name}'. Ensure the account ID is valid.")

def list_contacts_command(args):
    contacts = list_contacts()
    if contacts:
        print("\n--- Contacts ---")
        for contact in contacts:
            print(f"ID: {contact['contact_id']}, Name: {contact['first_name']} {contact['last_name']}, Email: {contact['email']}, Phone: {contact['phone']}, Account ID: {contact['account_id']}, Created: {contact['created_at']}")
        print("----------------")
    else:
        print("No contacts found.")

def get_contact_command(args):
    contact = get_contact(args.contact_id)
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
        print(f"Contact with ID {args.contact_id} not found.")

def update_contact_command(args):
    update_params = {}
    if args.first_name is not None:
        update_params['first_name'] = args.first_name
    if args.last_name is not None:
        update_params['last_name'] = args.last_name
    if args.email is not None:
        update_params['email'] = args.email
    if args.phone is not None:
        update_params['phone'] = args.phone
    if args.account_id is not None:
        update_params['account_id'] = args.account_id

    if not update_params:
        print("No update parameters provided.")
        return

    success = update_contact(args.contact_id, **update_params)
    if success:
        print(f"Contact with ID {args.contact_id} updated successfully.")
    else:
        print(f"Failed to update contact with ID {args.contact_id}. It might not exist or no changes were made.")

def delete_contact_command(args):
    success = delete_contact(args.contact_id)
    if success:
        print(f"Contact with ID {args.contact_id} deleted successfully.")
    else:
        print(f"Failed to delete contact with ID {args.contact_id}. It might not exist.")

# Opportunity Commands
def create_opportunity_command(args):
    opportunity_id = create_opportunity(args.name, args.description, args.amount, args.close_date, args.account_id, args.contact_id)
    if opportunity_id:
        print(f"Opportunity '{args.name}' created successfully with ID: {opportunity_id}")
    else:
        print(f"Failed to create opportunity '{args.name}'. Ensure account and contact IDs are valid.")

def list_opportunities_command(args):
    opportunities = list_opportunities()
    if opportunities:
        print("\n--- Opportunities ---")
        for opp in opportunities:
            print(f"ID: {opp['opportunity_id']}, Name: {opp['name']}, Amount: {opp['amount']}, Close Date: {opp['close_date']}, Account ID: {opp['account_id']}, Contact ID: {opp['contact_id']}, Created: {opp['created_at']}")
        print("---------------------")
    else:
        print("No opportunities found.")

def get_opportunity_command(args):
    opportunity = get_opportunity(args.opportunity_id)
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
        print(f"Opportunity with ID {args.opportunity_id} not found.")

def update_opportunity_command(args):
    update_params = {}
    if args.name is not None:
        update_params['name'] = args.name
    if args.description is not None:
        update_params['description'] = args.description
    if args.amount is not None:
        update_params['amount'] = args.amount
    if args.close_date is not None:
        update_params['close_date'] = args.close_date
    if args.account_id is not None:
        update_params['account_id'] = args.account_id
    if args.contact_id is not None:
        update_params['contact_id'] = args.contact_id

    if not update_params:
        print("No update parameters provided.")
        return

    success = update_opportunity(args.opportunity_id, **update_params)
    if success:
        print(f"Opportunity with ID {args.opportunity_id} updated successfully.")
    else:
        print(f"Failed to update opportunity with ID {args.opportunity_id}. It might not exist or no changes were made.")

def delete_opportunity_command(args):
    success = delete_opportunity(args.opportunity_id)
    if success:
        print(f"Opportunity with ID {args.opportunity_id} deleted successfully.")
    else:
        print(f"Failed to delete opportunity with ID {args.opportunity_id}. It might not exist.")


def main():
    """
    Main function for the CRM CLI application.
    Handles command-line arguments and dispatches to appropriate CRM functions.
    """
    # Ensure database tables exist
    create_tables()

    parser = argparse.ArgumentParser(description="Simple CRM CLI Application")

    # Add subparsers for different CRM objects (accounts, contacts, opportunities)
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # --- Account Commands ---
    account_parser = subparsers.add_parser('accounts', help='Manage accounts')
    account_subparsers = account_parser.add_subparsers(dest='account_command', help='Account commands')

    # accounts create
    create_account_parser = account_subparsers.add_parser('create', help='Create a new account')
    create_account_parser.add_argument('--name', required=True, help='Name of the account')
    create_account_parser.add_argument('--industry', help='Industry of the account')
    create_account_parser.set_defaults(func=create_account_command) # Link to function

    # accounts list
    list_accounts_parser = account_subparsers.add_parser('list', help='List all accounts')
    list_accounts_parser.set_defaults(func=list_accounts_command) # Link to function

    # accounts get <id>
    get_account_parser = account_subparsers.add_parser('get', help='Get account details by ID')
    get_account_parser.add_argument('account_id', type=int, help='ID of the account')
    get_account_parser.set_defaults(func=get_account_command) # Link to function

    # accounts update <id>
    update_account_parser = account_subparsers.add_parser('update', help='Update an account by ID')
    update_account_parser.add_argument('account_id', type=int, help='ID of the account')
    update_account_parser.add_argument('--name', help='New name for the account')
    update_account_parser.add_argument('--industry', help='New industry for the account')
    update_account_parser.set_defaults(func=update_account_command) # Link to function

    # accounts delete <id>
    delete_account_parser = account_subparsers.add_parser('delete', help='Delete an account by ID')
    delete_account_parser.add_argument('account_id', type=int, help='ID of the account')
    delete_account_parser.set_defaults(func=delete_account_command) # Link to function


    # --- Contact Commands ---
    contact_parser = subparsers.add_parser('contacts', help='Manage contacts')
    contact_subparsers = contact_parser.add_subparsers(dest='contact_command', help='Contact commands')

    # contacts create
    create_contact_parser = contact_subparsers.add_parser('create', help='Create a new contact')
    create_contact_parser.add_argument('--first-name', required=True, help='First name of the contact')
    create_contact_parser.add_argument('--last-name', required=True, help='Last name of the contact')
    create_contact_parser.add_argument('--email', required=True, help='Email of the contact (must be unique)')
    create_contact_parser.add_argument('--phone', help='Phone number of the contact')
    create_contact_parser.add_argument('--account-id', type=int, help='ID of the associated account')
    create_contact_parser.set_defaults(func=create_contact_command) # Link to function

    # contacts list
    list_contacts_parser = contact_subparsers.add_parser('list', help='List all contacts')
    list_contacts_parser.set_defaults(func=list_contacts_command) # Link to function

    # contacts get <id>
    get_contact_parser = contact_subparsers.add_parser('get', help='Get contact details by ID')
    get_contact_parser.add_argument('contact_id', type=int, help='ID of the contact')
    get_contact_parser.set_defaults(func=get_contact_command) # Link to function

    # contacts update <id>
    update_contact_parser = contact_subparsers.add_parser('update', help='Update a contact by ID')
    update_contact_parser.add_argument('contact_id', type=int, help='ID of the contact')
    update_contact_parser.add_argument('--first-name', help='New first name')
    update_contact_parser.add_argument('--last-name', help='New last name')
    update_contact_parser.add_argument('--email', help='New email')
    update_contact_parser.add_argument('--phone', help='New phone number')
    update_contact_parser.add_argument('--account-id', type=int, help='New associated account ID')
    update_contact_parser.set_defaults(func=update_contact_command) # Link to function

    # contacts delete <id>
    delete_contact_parser = contact_subparsers.add_parser('delete', help='Delete a contact by ID')
    delete_contact_parser.add_argument('contact_id', type=int, help='ID of the contact')
    delete_contact_parser.set_defaults(func=delete_contact_command) # Link to function


    # --- Opportunity Commands ---
    opportunity_parser = subparsers.add_parser('opportunities', help='Manage opportunities')
    opportunity_subparsers = opportunity_parser.add_subparsers(dest='opportunity_command', help='Opportunity commands')

    # opportunities create
    create_opportunity_parser = opportunity_subparsers.add_parser('create', help='Create a new opportunity')
    create_opportunity_parser.add_argument('--name', required=True, help='Name of the opportunity')
    create_opportunity_parser.add_argument('--description', help='Description of the opportunity')
    create_opportunity_parser.add_argument('--amount', type=float, help='Amount of the opportunity')
    create_opportunity_parser.add_argument('--close-date', help='Expected close date (YYYY-MM-DD)') # TODO: Add date validation
    create_opportunity_parser.add_argument('--account-id', type=int, required=True, help='ID of the associated account')
    create_opportunity_parser.add_argument('--contact-id', type=int, help='ID of the associated contact') # TODO: Validate contact belongs to account?
    create_opportunity_parser.set_defaults(func=create_opportunity_command) # Link to function

    # opportunities list
    list_opportunities_parser = opportunity_subparsers.add_parser('list', help='List all opportunities')
    list_opportunities_parser.set_defaults(func=list_opportunities_command) # Link to function

    # opportunities get <id>
    get_opportunity_parser = opportunity_subparsers.add_parser('get', help='Get opportunity details by ID')
    get_opportunity_parser.add_argument('opportunity_id', type=int, help='ID of the opportunity')
    get_opportunity_parser.set_defaults(func=get_opportunity_command) # Link to function

    # opportunities update <id>
    update_opportunity_parser = opportunity_subparsers.add_parser('update', help='Update an opportunity by ID')
    update_opportunity_parser.add_argument('opportunity_id', type=int, help='ID of the opportunity')
    update_opportunity_parser.add_argument('--name', help='New name')
    update_opportunity_parser.add_argument('--description', help='New description')
    update_opportunity_parser.add_argument('--amount', type=float, help='New amount')
    update_opportunity_parser.add_argument('--close-date', help='New close date (YYYY-MM-DD)') # TODO: Add date validation
    update_opportunity_parser.add_argument('--account-id', type=int, help='New associated account ID')
    update_opportunity_parser.add_argument('--contact-id', type=int, help='New associated contact ID') # TODO: Validate contact belongs to account?
    update_opportunity_parser.set_defaults(func=update_opportunity_command) # Link to function

    # opportunities delete <id>
    delete_opportunity_parser = opportunity_subparsers.add_parser('delete', help='Delete an opportunity by ID')
    delete_opportunity_parser.add_argument('opportunity_id', type=int, help='ID of the opportunity')
    delete_opportunity_parser.set_defaults(func=delete_opportunity_command) # Link to function


    # If no arguments are provided, print help message
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    # Dispatch commands based on args.func
    if hasattr(args, 'func'):
        args.func(args)
    else:
        # This case should ideally not be reached if subparsers are used correctly
        parser.print_help(sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

