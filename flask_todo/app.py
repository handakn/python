from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  title = db.Column(db.Text)
  description = db.Column(db.Text)
  done = db.Column(db.Integer)

@app.route('/')
def index():
  todos = Todo.query.all()
  return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
  title = request.form['title']
  description = request.form['description']
  todo = Todo(title=title, description=description)
  db.session.add(todo)
  db.session.commit()
  return redirect(url_for('index'))

@app.route('/done/<int:id>')
def done(id):
  todo = Todo.query.get_or_404(id)
  todo.done = 1
  db.session.commit()
  return redirect(url_for('index'))

@app.route('/undone/<int:id>')
def undone(id):
  todo = Todo.query.get_or_404(id)
  todo.done = 0
  db.session.commit()
  return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
  todo = Todo.query.get_or_404(id)
  db.session.delete(todo)
  db.session.commit()
  return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

