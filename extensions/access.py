import os
import json
import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from googleapiclient.discovery import build

# Load token from the JSON file
with open('creds/access.json', 'r') as config_file:
    config = json.load(config_file)
    NOTION_TOKEN = config.get('token', '')
NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Configuración de Google Calendar API
SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = 'creds/credentials.json'
def get_calendar_service():
    """
    Autentica y devuelve el servicio de Google Calendar.
    """
    creds = None
    token_path = 'creds/token.json'
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError:
                # Delete the token file and re-authenticate
                os.remove(token_path)
                flow = InstalledAppFlow.from_client_secrets_file(SERVICE_ACCOUNT_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
                with open(token_path, 'w') as token:
                    token.write(creds.to_json())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(SERVICE_ACCOUNT_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service

def get_notion_db(database_id):
    """
    Recupera las páginas de una base de datos específica de Notion.

    Args:
        database_id (str): El ID de la base de datos de Notion.

    Returns:
        list: Una lista de páginas en la base de datos de Notion.
    """
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    response = requests.post(url, headers=NOTION_HEADERS)
    if response.status_code == 200:
        return response.json().get("results")
    else:
        print(f"Error fetching database: {response.status_code} {response.text}")
        return []