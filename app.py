from flask import Flask,render_template,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import request
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# the above is telling where our database is located,3 slashes is a relative path
# 4 forward slashes is an absolute path;test.db is where our database is going to be
# everything is gonna be stored in th etest.db file
db=SQLAlchemy(app)
# the above line initialises the database

class Todo(db.Model):
  # creates a model
  # next we are gonna form a column an id column
  id=db.Column(db.Integer, primary_key=True)
  # it is actually a unique identifier since the content can be the same
  content=db.Column(db.String(200), nullable=False)
  # above creates a text column,ie what holds each task
  # 'nullable=False' means that we dont want this to be blank ie content of task shouldnt be empty
  completed=db.Column(db.Integer, default=0)
  # Nnever really used but ok
  date_created=db.Column(db.DateTime,default=datetime.utcnow)
  # something the user needs access to and will be set automatically since we are making use of modules

  def __repr__(self):
  # return a string everytime we create a new element and we shall tell what to retrun here
    return '<Task %r>' %self.id
  # returns the task and the id of that
@app.route('/',methods=['POST','GET'])
def index():
  if request.method=='POST':
      task_content=request.form['content']#contents of the inputs here
      new_task=Todo(content=task_content)

      try:
        db.session.add(new_task)
        db.session.commit()
        return redirect('/')
      except:
         return 'There was an issue adding your task'
  else:
      tasks=Todo.query.order_by(Todo.date_created).all()
      # the above will going to look at all of the database content in the order of their creation ie the date in which they are added
      # all() ie we are gonna grab them all,we can also do first() the most recent one
      return render_template('index.html',tasks=tasks)

  # the above is how we are going to grab our task in and put it in our database otherwise we are pretty much looking at the page
  

@app.route('/delete/<int:id>')
def delete(id):
   task_to_delete = Todo.query.get_or_404(id)

   try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
   except:
         return 'There was an issue deleting that task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
   task=Todo.query.get_or_404(id)

   if request.method=='POST':
      task.content=request.form['content']
  #  the above is the update logic
      try:
            db.session.commit()
            return redirect('/')
      except:
         return 'There was an issue updating your task'
       
   else:
      return render_template('update.html',task=task)
   
if __name__=="__main__" :
  with app.app_context():
    db.create_all()
    app.run(debug=True)
