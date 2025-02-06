import json
from extensions.access import get_notion_db

def get_notion_pages():
    # Load the database ID from the JSON file
    with open('creds/notiondb.json', 'r') as config_file:
        config = json.load(config_file)
        database_id = config.get('database_id', '')
    # Obteining the pages from the database to filter
    database = get_notion_db(database_id)        
    pages = []
    
    # Iterating over each page of the database
    for page in database:
        if ('properties' in page and
            'Name' in page['properties'] and 
            'title' in page['properties']['Name'] and # Checking name is present
            'State' in page['properties'] and
            'status' in page['properties']['State']): # Checking status is present
        
            # Defining state filters
            state = page['properties']['State']['status']['name'] 
            if state.lower() not in ['cancelado', 'listo']: # If name of state is not finished 
                name = page['properties']['Name']['title'][0]['plain_text'] 
                # setting default dates and color
                start_date = None
                end_date = None
                color = None
                calendar_id = None
                
                # if there are start and finished dates
                if 'Deadline' in page['properties']and page['properties']['Deadline']['date']:
                    start_date = page['properties']['Deadline']['date'].get('start')
                    end_date = page['properties']['Deadline']['date'].get('end')               
                if 'Calendar ID' in page['properties'] and 'rich_text' in page['properties']['Calendar ID']:
                    rich_text = page["properties"]["Calendar ID"]["rich_text"]
                    if rich_text:
                        calendar_id = page["properties"]["Calendar ID"]["rich_text"][0]["plain_text"]
                if 'Category' in page['properties'] and 'select' in page['properties']['Category']:
                    select = page["properties"]["Category"]["select"]
                    if select:
                        color = page['properties']['Category']['select'].get('color')
                
                # Get page id
                page_id = page.get('id')
                
                page = {
                    'name': name,
                    'start_date': start_date,
                    'end_date': end_date,
                    'category': color,
                    'id': page_id,
                    'calendar ID': calendar_id,
                }      
                
                pages.append(page)
                
    return pages

