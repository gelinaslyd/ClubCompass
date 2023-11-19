from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id 

@app.route('/', methods=['POST','GET'])
def index():
    error_message=None

    if request.method == 'POST':
        task_content = request.form['content']

        if not task_content.strip():
            error_message = 'Task content cannot be blank'
            return render_template('error.html', error_message=error_message)
        else:
            new_task = Todo(content=task_content)

        try: 
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except: 
            error_message = 'There was an issue adding your posting'
            return render_template('error.html', error_message=error_message)

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        new_content = request.form['content'].strip()

        if not new_content:
            return render_template('error.html')


        task.content = new_content


        try:
            db.session.commit()
            return redirect('/')
        except: 
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)

@app.route('/description/<int:id>')
def description(id):
    return render_template('description.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__== "__main__":
    app.run(debug=True)