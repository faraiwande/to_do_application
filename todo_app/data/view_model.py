from todo_app.data.trello_items import Item

class ViewModel:
    def __init__(self, items : list[Item]):
        self._items = items

        @property
        def items(self):
            return  self._items
        
        @property
        def todo_items(self):
            return []

        @property
        def doing_items(self):
            return []

        @property
        def done_items(self):
            return []    