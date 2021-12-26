from datetime import datetime
import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    sn = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(280),  nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sn}-{self.title}"


@app.route('/', methods=["POST", "GET"])
def Hello_world():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    all_todo = Todo.query.all()
    return render_template("index.html", all_todo=all_todo)


# @app.route('/show')
# def Print_all_todo():
#     all_todo = Todo.query.all()
#     print(all_todo)
#     return f"{len(all_todo)}"


@app.route('/update/<int:sn>', methods=["POST", "GET"])
def update(sn):
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sn=sn).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    todo = Todo.query.filter_by(sn=sn).first()
    return render_template("update.html", todo=todo)


@app.route('/delete/<int:sn>')
def delete(sn):
    todo = Todo.query.filter_by(sn=sn).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
