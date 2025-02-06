import json
from extensions.access import get_calendar_service
from extensions.colors import get_color_id
from extensions.upload_id import add_id_to_notion

# Obtain the authenticated Google Calendar service
service = get_calendar_service()

# Load the calendar ID from the credentials JSON file
with open('creds/credentials.json', 'r') as config_file:
    config = json.load(config_file)
    calendarId = config.get('email', '')

def create_event(event_data, service):
    """
    Creates an event in Google Calendar with the provided data.
    Args:
        event_data (dict): Dictionary with the event details.
        service (googleapiclient.discovery.Resource): Instance of the Google Calendar API service.
    """
    # Extract event data from the dictionary
    name = event_data.get('name')
    start_date = event_data.get('start_date')
    end_date = event_data.get('end_date')
    color = event_data.get('category')
    id = event_data.get('id')
    
    if start_date:
        # Determine the date format (date or dateTime)
        if 'T' in start_date:
            start = {'dateTime': start_date}
            end = {'dateTime': end_date} if end_date else {'dateTime': start_date}
        else:
            start = {'date': start_date}
            end = {'date': end_date} if end_date else {'date': start_date}
        
        # Create the event dictionary
        event = {
            'summary': name,
            'start': start,
            'end': end,
        }
        
        notion_id = id
        
        # Assign the color to the event if provided
        if color:
            color_id = get_color_id(color)
            if color_id:
                event['colorId'] = color_id
        else:
            event['colorId'] = 8  # Default color
        
        try:
            # Insert the event into Google Calendar
            event_creation = service.events().insert(calendarId=calendarId, body=event).execute()
            event_id = event_creation.get('id')
            print(f'Event created: {name}\n URL:{event_creation.get("htmlLink")}\n ID: {event_id}')
            # Add the event ID to Notion
            add_id_to_notion(notion_id, event_id)
        except Exception as e:
            print(f'Error creating event: {e}')
    else:
        print(f'Error: Event {name} has no start date.')

def update_event(event_data, service, event_id):
    """
    Updates an existing event in the calendar with the provided event data.
    Args:
        event_data (dict): A dictionary containing the event details. Expected keys are:
            - 'name' (str): The name of the event.
            - 'start_date' (str): The start date of the event in ISO format.
            - 'end_date' (str, optional): The end date of the event in ISO format.
            - 'category' (str, optional): The category of the event, used to determine the color.
        service (googleapiclient.discovery.Resource): The Google Calendar API service instance.
        event_id (str): The ID of the event to be updated.
    Returns:
        None
    Raises:
        Exception: If there is an error retrieving or updating the event.
    Notes:
        - If the start_date contains 'T', it is considered a date-time; otherwise, it is considered a date.
        - If the end_date is not provided, it defaults to the start_date.
        - If the category is provided, it is used to determine the colorId; otherwise, a default colorId of 8 is used.
    """
    # Extract event data from the dictionary
    name = event_data.get('name')
    start_date = event_data.get('start_date')
    end_date = event_data.get('end_date')
    color = event_data.get('category')
    
    try:
        # Retrieve the existing event from Google Calendar
        event = service.events().get(calendarId, eventId=event_id).execute()
    except Exception as e:
        print(f'Error retrieving event: {e}')
        return
    
    # Update the event's summary (name)
    event['summary'] = name

    if start_date:
        # Determine the date format (date or dateTime)
        if 'T' in start_date:
            event['start'] = {'dateTime': start_date}
            event['end'] = {'dateTime': end_date} if end_date else {'dateTime': start_date}
        else:
            event['start'] = {'date': start_date}
            event['end'] = {'date': end_date} if end_date else {'date': start_date}
        
        # Assign the color to the event if provided
        if color:
            color_id = get_color_id(color)
            if color_id:
                event['colorId'] = color_id
        else:
            event['colorId'] = 8  # Default color
        
        try:
            # Update the event in Google Calendar
            event_update = service.events().update(calendarId, eventId=event_id, body=event).execute()
            event_id = event_update.get('id')
            print(f'Event updated: {name}\n URL: {event_update.get("htmlLink")}\n ID: {event_id}.')
        except Exception as e:
            print(f'Error updating event: {e}')
    else:
        print(f'Error: Event {name} has no start date.')