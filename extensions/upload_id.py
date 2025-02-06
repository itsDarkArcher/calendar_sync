import json
import requests 

def add_id_to_notion(page_id, event_id):
    # Load token from the JSON file
    with open('creds/access.json', 'r') as config_file:
        config = json.load(config_file)
        token = config.get('token', '')
    # Extraer la ID de la pagina de la url
    page_id = page_id.replace("-","")
    
    url = f"https://api.notion.com/v1/pages/{page_id}"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
        }
    
    data ={
        "properties": {
            "Calendar ID":{
                "rich_text":[
                    {
                        "text":{
                            "content": event_id
                            }
                        }
                    ]
                }
            }
        }
    response = requests.patch(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print(f"Succesfully updated Notion page with CalendarID: {event_id}\n")
    else:
        print(f"Failed to update Notion page. Status code: {response.status_code}\n Response: {response.text}")
