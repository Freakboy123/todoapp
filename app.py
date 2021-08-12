# source env/bin/activate
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.datetime.now)
    high_priority = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.id} {self.content}>'

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['contentText']
        priority = bool(request.form.get('priority'))
        new_task = Todo(content=task_content, high_priority=priority)
        print(new_task)
        try:
            db.session.add(new_task) 
            db.session.commit()
            return redirect('/')
        except:
            return("THERE WAS AN ERROR")
    else:  
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task = Todo.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except:
        return 'ERROR DELETING TASK'    

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task_content = request.form['contentText']
        priority = bool(request.form.get('priority'))
        
        try:
            task.content = task_content
            db.session.commit()
            task.high_priority = priority
            db.session.commit()
            return redirect('/')
        except:
            return 'UPDATING TASK'  
    else:
        return render_template('update.html', task=task)  
if __name__=='__main__': 
    app.run(debug=True)