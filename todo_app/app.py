from flask import Flask, request,render_template
from todo_app.flask_config import Config
from todo_app.data.session_items import get_items, add_item, get_item, save_item, delete_item



app = Flask(__name__)
app.config.from_object(Config())
  

@app.route('/', methods=['GET','POST'] )
def index():
        items = get_items()
        return render_template ('index.html', my_items = items)
        

@app.route('/add_tasks', methods=['POST'])
def add_tasks():
        add_item(dict(request.form.items())['title'],dict(request.form.items())['priority'], dict(request.form.items())['status'])
        items = get_items()
        return render_template ('index.html', my_items = items)
        
    
@app.route('/update_task_status', methods=['POST'])
def update_task():
        item = get_item(dict(request.form.items())['id'])
        item.update({'status': dict(request.form.items())['status']})
        save_item(item)
        items = get_items()
        return render_template ('index.html', my_items = items)


@app.route('/delete_task', methods=['POST'])
def delete_task():
        item = get_item(dict(request.form.items())['id'])
        delete_item(item)
        items = get_items()
        return render_template ('index.html', my_items = items)