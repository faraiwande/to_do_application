from flask import Flask, request,render_template,  url_for 
from todo_app.flask_config import Config
from todo_app.data.session_items import get_items, add_item

app = Flask(__name__)
app.config.from_object(Config())


     

@app.route('/', methods=['GET','POST'] )
def index():
        items = get_items()
        return render_template ('index.html', my_items = items)
        

@app.route('/add_tasks', methods=['POST'])
def add_tasks():
        add_item(dict(request.form.items())['title'])
        items = get_items()
        return render_template ('index.html', my_items = items)
        
    


