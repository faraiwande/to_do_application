from dotenv import load_dotenv, find_dotenv
import pytest, mongomock, os
from todo_app import app

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        # Create the new app
        test_app = app.create_app()

        # Use the app to create a test_client that can be used in our tests
        with test_app.test_client() as client:
            yield client

def test_index_page(client):
    pymongo_client = mongomock.MongoClient(os.getenv("MONGODB_CONNECTIONSTRING"))
    
    db = pymongo_client[os.getenv("MONGODB_COLLECTION_NAME")]
    collection = db[os.getenv("MONGODB_COLLECTION_NAME")]
    
    test_doc = {
        'title': 'T',
        'description': 'E',
        'status': 'S'
    }
    
    collection.insert_one(test_doc)
    
    response = client.get('/')  
    
    assert response.status_code == 200
