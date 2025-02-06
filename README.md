# Calendar Sync

**Description:**  
This project synchronizes all your tasks from Notion to your Google Calendar.

## Features
- Sync tasks from Notion to Google Calendar
- Automatically update calendar events when tasks are modified
- Supports recurring tasks

## Usage

1. **Set up your Notion and Google API keys:**  # Setup Guide for Calendar Sync

This guide will help you set up the Calendar Sync project to synchronize your tasks from Notion to Google Calendar.

## Prerequisites

- Python 3.x installed
- A Google account
- A Notion account

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/itsDarkArcher/calendar_sync.git
    ```

2. **Navigate to the project directory:**
    ```sh
    cd calendar_sync
    ```

3. **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

## Configuration

### Google API Setup

1. **Create a project in the Google Cloud Console:**
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Click on the project drop-down and select "New Project".
   - Enter a name for your project and click "Create".

2. **Enable the Google Calendar API:**
   - In the Google Cloud Console, go to the "APIs & Services" > "Library".
   - Search for "Google Calendar API" and click on it.
   - Click "Enable".

3. **Create credentials for the API:**
   - Go to "APIs & Services" > "Credentials".
   - Click on "Create Credentials" and select "OAuth 2.0 Client IDs".
   - Set the application type to "Desktop app" and click "Create".
   - Download the JSON file with your credentials and save it as `credentials.json` in the project directory.

### Notion API Setup

1. **Create an integration in Notion:**
   - Go to [Notion Integrations](https://www.notion.so/my-integrations).
   - Click "New Integration".
   - Enter a name for your integration and select your workspace.
   - Copy the "Internal Integration Token" and save it for later use.

2. **Share your Notion database with the integration:**
   - Go to the Notion page or database you want to sync.
   - Click "Share" and invite your integration by selecting its name.

## Running the Synchronization Script

1. **Ensure your credentials file is correctly set up:**
   - Your `credentials.json` file should contain your Google API credentials.
   - Create a `notiondb.json` file with the following content:
   ```json
   {
     "token": "<Your Notion Integration Token>",
     "database_id": "<Your Notion Database ID>"
   }
   ```
     ```

2. **Run the synchronization script:**
    ```sh
    python main.py
    ```

## Troubleshooting
- Ensure that your Google and Notion credentials are correctly configured.
- Check the console output for any error messages and follow the instructions to resolve them.

## Contributing
Feel free to submit issues, fork the repository, and send pull requests. We appreciate all contributions.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
