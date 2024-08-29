from flask import Flask, request,render_template, redirect
from todo_app.flask_config import Config
from todo_app.data.mongo_items import add_item, save_item, get_item, Item, get_items
from todo_app.data.view_model import ViewModel


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
  
    @app.route('/', methods=['GET', 'POST'])
    def index():
         items = get_items()
         view_model = ViewModel(items)
         return render_template('index.html', view_model=view_model)

    @app.route('/add_tasks', methods=['POST'])
    def add_tasks():
        add_item(
                request.form['title'],
                request.form['description'],
                request.form['status']
        )
        return redirect('/')

    @app.route('/update_task_status', methods=['POST'])
    def update_task():
        item = get_item(request.form['id'])
        item.status = request.form['status']
        save_item(item)
        return redirect('/')

    
    return app