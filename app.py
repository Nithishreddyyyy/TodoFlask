from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'todo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer , primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500),nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)
    
    
    def __repr__(self) ->str:
        return f"{self.sno} - {self.title}"
    
    

@app.route('/',methods = ['GET','POST'])
def hello_world():
    if request.method == 'POST':
        title = (request.form['title'])
        desc = (request.form['desc'])
        todo = Todo(title=title , desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    print(allTodo)
    return render_template('index.html',allTodo=allTodo)

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo.title = title
        todo.desc = desc
        db.session.commit()
        return redirect('/')
    
    allTodo = Todo.query.all()  # So the table can be rendered in the same view
    return render_template('update.html', todo=todo, allTodo=allTodo)

    
@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/show')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'This is products page!'

if __name__ == '__main__':
    app.run(debug=False,port =8000)