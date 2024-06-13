from calendar_sync import create_event, update_event
from get_notion_pages import get_notion_pages
from extensions.access import get_calendar_service

def main():

    pages = get_notion_pages()
    service = get_calendar_service()
    print(f'{service}\n')
    
    for page in pages:
        calendar_id = page.get("calendar ID")  # Obtener el valor del campo 'calendar ID'
        
        if not calendar_id:
            create_event(page, service)
        else:
            update_event(page, service, calendar_id)
            
if __name__ == "__main__":
    main()