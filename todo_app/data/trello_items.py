import requests,os, json
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

key = os.getenv('TRELLO_API_KEY') 
token = os.getenv('TRELLO_API_TOKEN')


def get_board_id():
    fields = 'fields=name'
    url = 'https://api.trello.com/1/members/me/boards?{}&key={}&token={}'.format(fields,key,token)
    reponse = requests.get(url)
    boards_json = reponse.json()

    for board in boards_json:
        if board.get('name') =='DevOps Engineering':
            board_id = board.get('id')
    return board_id

def get_lists():
    fields = 'fields=name'
    url = 'https://api.trello.com/1/boards/{}/lists?{}&key={}&token={}'.format(get_board_id(),fields,key,token)
    reponse = requests.get(url)
    lists_json = reponse.json()
    return lists_json


def get_items():
    items = []
    fields = 'fields=name,idList,desc,labels'
    url = 'https://api.trello.com/1/boards/{}/cards?{}&key={}&token={}'.format(get_board_id(),fields,key,token)
    reponse = requests.get(url)
    cards_json = reponse.json()

    for card in cards_json:
        for list in get_lists():
            if card.get('idList') == list.get('id'):
                card.update({'idList':list.get('name')})
                id = card.get('id')
                status = card.get('idList')
                title = card.get('name')
                description = card.get('desc')
                     
                items.append({'id': id, 'status': status, 'title' : title, 'description':description})
    return items
                
def get_item(id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()
    return next((item for item in items if item['id'] == id), None)
    

def add_item(title,description,status):
    for list in get_lists():
        if list.get('name') == status:
            url = 'https://api.trello.com/1/cards/?idList={}&key={}&token={}'.format(list.get('id'),key,token)
            payload = {'name':title ,'desc' :description}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            requests.post(url, data = json.dumps(payload), headers=headers)
            

        
def save_item(item):
    for list in get_lists():
        if list.get('name') == item.get('status'):
            url = 'https://api.trello.com/1/cards/{}?idList={}&key={}&token={}'.format(item.get('id'),list.get('id'),key,token)
            requests.put(url)


def delete_item (item):
    url = 'https://api.trello.com/1/cards/?{}&key={}&token={}'.format(item.get('id'),key,token)
    requests.delete(url) 