from flask import Flask, redirect, render_template, request, url_for 
from flask_sqlalchemy import SQLAlchemy
import datetime 
app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
db = SQLAlchemy(app) 

 
# create a database model 
class Todo(db.Model) : 
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(100)) 
    complete = db.Column(db.Boolean)  


@app.route("/") 
def index() : 
    todo_list= Todo.query.all() ; # returns list of all items 
    print(todo_list) 
    day = datetime.datetime.now() 
    date = datetime.datetime.now() 
    month = datetime.datetime.now() 
    return render_template("base.html", todo_list=todo_list, day = day.strftime("%A") , date = date.strftime("%d"), month = month.strftime("%b"))

@app.route("/add", methods=["POST"])
#add is a route that should not be displayed but we have to specify it as a route that can be mentioned as action in form tag 
def add() :
   #add a new item 
   title = request.form.get("title" ) 
   if not title  : 
       return redirect(url_for("index"))
   
   newTodo = Todo(title= title , complete = False) 
   db.session.add(newTodo) 
   db.session.commit()
   #will redirect the user to index page 
   return redirect(url_for("index"))

@app.route("/update/<int:todo_id>") 
def update(todo_id) : 
    todo = Todo.query.filter_by(id=todo_id).first() 
    todo.complete = not todo.complete 
    db.session.commit() 
    return redirect(url_for("index")) 

@app.route("/delete/<int:todo_id>")  
def delete(todo_id) : 
    todo = Todo.query.filter_by(id=todo_id).first() 
    db.session.delete(todo) 
    db.session.commit() 
    return redirect(url_for("index"))  

if __name__ == "__main__" :  
    with app.app_context():
        db.create_all()
        
   
    app.run(debug=True)  