from todo_app.data.view_model import ViewModel
from todo_app.data.view_model import Item

def test_demo_test():
    # Arrange
    items = [ 
        Item(1,'Build Unit Tests','Done','done items needs doing'),
        Item(2,'Build Unit Tests','Doing','doing items unit test'),
        Item(3,'Build Unit Tests','To Do','doing items unit test')]
     
    view_model = ViewModel(items)



    # Act  
    returned_items = view_model._items


    # Assert 
    assert len(returned_items) == 1
    returned_item = returned_items[0]
    assert returned_item.status =='Done'