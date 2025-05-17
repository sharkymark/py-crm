# Simple CRM CLI Application

A Python command-line application for managing Accounts, Contacts, and Opportunities.

## Features

- **CRUD Operations**: Create, Read, Update, and Delete functionality for Accounts, Contacts, and Opportunities.
- **Data Storage**: Uses SQLite3 for persistent storage in a local file.
- **Menu-Driven Interface**: Interact with the application through simple menus.

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

## Environment Variables

See `devcontainer.json` for environment variables required.

## AI Agents

[Aider commands](https://aider.chat/docs/usage/commands.html)

[Aider tips](https://aider.chat/docs/usage/tips.html)

[Goose CLI commands](https://block.github.io/goose/docs/guides/goose-cli-commands)

[Goose tips](https://block.github.io/goose/docs/guides/tips/)

## License

MIT License
