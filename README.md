# Simple CRM CLI Application

A Python command-line application for managing Accounts, Contacts, and Opportunities.

## Features

- **CRUD Operations**: Create, Read, Update, and Delete functionality for Accounts, Contacts, and Opportunities.
- **Data Storage**: Uses SQLite3 for persistent storage in a local file.
- **Menu-Driven Interface**: Interact with the application through simple menus.
- **Export to CSV**: Export data to CSV files for easy sharing and reporting.
- **Search Functionality**: Search for Accounts, Contacts, and Opportunities by name or ID.
- **Schema Migration**: Automatically migrate the database schema to the latest version on startup.
- **Picklists**: Use predefined dropdown-style lists for standard fields like Industry and Opportunity Stage.

## Requirements

- Python 3.11+
- Required packages (see requirements.txt)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/sharkymark/repo.git
   cd repo
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application as a module using the `-m` flag:

```bash
python3 -m src.main
```

The application will present a main menu, and you can navigate through sub-menus for Accounts, Contacts, and Opportunities to perform CRUD operations.

## Database

The application uses a SQLite3 database file named `crm.db` located in the `data/` directory within the project root.

You can use database tools like [DBeaver](https://dbeaver.io/) or the `sqlite3` command-line tool to inspect or manage the `data/crm.db` file directly if needed.

## Picklists

Picklists provide standardized values for certain fields in the CRM system, such as industry types for accounts and stages for opportunities. They can be managed through the Admin menu.

### Supported Picklists

- `industry` - for Account records
- `stage` - for Opportunity records

### CSV Import Format

Picklists can be imported using CSV files with the following format:

```csv
picklist_name,entity_type,description,value,display_order,is_default,is_active
stage,opportunity,Stage,Discovery,1,false,true
stage,opportunity,Stage,Qualification,2,false,true
stage,opportunity,Stage,Negotiation,3,false,true
stage,opportunity,Stage,Closed Won,4,false,true
stage,opportunity,Stage,Closed Lost,5,false,true
```

Sample picklist CSV files are available in the `data/` directory:
- `data/picklist_industry.csv` - Industry types for accounts
- `data/picklist_stage.csv` - Stage values for opportunities

To import picklists, navigate to the Admin menu (option 6) in the main menu, then select "Import Picklists from CSV" and provide the path to your CSV file.

## Environment Variables

See `devcontainer.json` for gitenvironment variables.

## AI Agents

[GitHub Copilot](https://docs.github.com/en/copilot)

[Copilot Agent Mode](https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode)

[Aider commands](https://aider.chat/docs/usage/commands.html)

[Aider tips](https://aider.chat/docs/usage/tips.html)

[Goose CLI commands](https://block.github.io/goose/docs/guides/goose-cli-commands)

[Goose tips](https://block.github.io/goose/docs/guides/tips/)

## License

MIT License
