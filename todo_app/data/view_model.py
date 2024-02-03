from todo_app.data.trello_items import Item

class ViewModel:
    def __init__(self, items : list[Item]):
        self._items = items

        @property
        def items(self):
            return  self._items
        