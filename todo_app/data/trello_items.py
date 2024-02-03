import requests,os, json
key = os.getenv('TRELLO_API_KEY') 
token = os.getenv('TRELLO_API_TOKEN')



class Item:
    def __init__(self, id, name, status, desc):
        self.id = id
        self.name = name
        self.status = status
        self.desc = desc 

    @classmethod
    def from_trello_card(cls, card, lists):
        list_name = next((list['name'] for list in lists if list['id'] == card['idList']), None)
        return cls(card['id'], card['name'], list_name, card.get('desc', ''))

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
            url = f"https://api.trello.com/1/cards/{item.get('id')}?idList={list.get('id')}&key={key}&token={token}"
            requests.put(url)

 

def get_cards():
    board_id = get_board_id()
    url = 'https://api.trello.com/1/boards/{}/cards?&key={}&token={}'.format(board_id,key, token)
    response = requests.get(url)
    return response.json()