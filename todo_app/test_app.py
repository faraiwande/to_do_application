from dotenv import load_dotenv, find_dotenv
import pytest, requests, os
from todo_app import app

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    # Create the new app.
    test_app = app.create_app()

    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client


def test_index_page(monkeypatch, client):
    # This replaces any call to requests.get with our own function
    monkeypatch.setattr(requests, 'get', stub)


    response = client.get('/')

    assert response.status_code == 200
    assert 'Test card description' in response.data.decode()

class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data

    def raise_for_status(self):
        pass 

    def json(self):
        return self.fake_response_data

def stub(url, params=None):
    if params is None:
        params = {}

    test_board_id = os.getenv("TRELLO_BOARD_ID")
    if url.startswith(f'https://api.trello.com/1/boards/{test_board_id}/lists'):
        fake_response_data = [{
            'id': '123abc',
            'name': 'To Do',
        }]
        return StubResponse(fake_response_data)
    elif url.startswith(f'https://api.trello.com/1/boards/{test_board_id}/cards'):
        fake_response_data = [{
            'id': '123abc-card',
            'name': 'To Do 2',
            'idList': '123abc',
            'desc': 'Test card description'
        }]
        return StubResponse(fake_response_data)
