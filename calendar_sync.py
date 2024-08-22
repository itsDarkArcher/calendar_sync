from extensions.access import get_calendar_service
from extensions.colors import get_color_id
from extensions.upload_id import add_id_to_notion

service = get_calendar_service()

def create_event(event_data, service):  
    name = event_data.get('name')
    start_date = event_data.get('start_date')
    end_date = event_data.get('end_date')
    color = event_data.get('category')
    id = event_data.get('id')
    
    if start_date:
        # Determinar el formato de la fecha
        if 'T' in start_date:
            start = {'dateTime': start_date}
            end = {'dateTime': end_date} if end_date else {'dateTime': start_date}
        else:
            start = {'date': start_date}
            end = {'date': end_date} if end_date else {'date': start_date}
        
        event ={
            'summary': name,
            'start': start,
            'end': end,
            }
        notion_id = id
        if color:
            color_id = get_color_id(color)
            if color_id:
                event['colorId'] = color_id
        else:
            event['colorId'] = 8
        
        try:
            event_creation = service.events().insert(calendarId='mauri.duarte.24@gmail.com', body=event).execute()
            event_id = event_creation.get('id')
            print(f'Event created: {name}\n URL:{event_creation.get('htmlLink')}\n ID: {event_id}')
            add_id_to_notion(notion_id, event_id)
        except Exception as e:
            print(f'Error creating event: {e}')
    else:
        print(f'Error: Evento {name} no tiene fecha.')

def update_event(event_data, service, event_id):
    name = event_data.get('name')
    start_date = event_data.get('start_date')
    end_date = event_data.get('end_date')
    color = event_data.get('category')
    try:
        event = service.events().get(calendarId='mauri.duarte.24@gmail.com', eventId=event_id).execute()
    except Exception as e:
        print(f'Error retrieving event')
        return
    
    event['summary'] = name

    if start_date:
        # Determinar el formato de la fecha
        if 'T' in start_date:
            event['start'] = {'dateTime': start_date}
            event['end'] = {'dateTime': end_date} if end_date else {'dateTime': start_date}
        else:
            event['start'] = {'date': start_date}
            event['end'] = {'date': end_date} if end_date else {'date': start_date}
        
        
        if color:
            color_id = get_color_id(color)
            if color_id:
                event['colorId'] = color_id
        else:
            event['colorId'] = 8
        
        try:
            event_update = service.events().update(calendarId='mauri.duarte.24@gmail.com', eventId=event_id, body=event).execute()
            event_id = event_update.get('id')
            print(f'Event updated: {name}\n URL: {event_update.get('htmlLink')}\n ID: {event_id}.\n')
        except Exception as e:
            print(f'Error updating event: {e}')
    else:
        print(f'Error: {name} no contiene fecha')