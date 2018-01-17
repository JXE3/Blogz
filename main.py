from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Mares eat oats@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)



class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    body = db.Column(db.String(150))
    
    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/', methods=['POST', 'GET'])
def index():
    
    blogs = Blog.query.all()

    return render_template('blog.html', blogs=blogs)


@app.route('/newpost', methods=['GET','POST'])
def newpost():
    

    errorTitle = ""
    errorBody = ""
    title=""
    body=""

    if request.method == 'POST':
        title = request.form['title'] 
        body = request.form['body']
        
        if title and body:
            new_Blog = Blog(title, body)
            db.session.add(new_Blog)
            db.session.commit()
            print("newpost-a")
            return render_template('thisBlog.html', title=title, body=body)
           
        elif not title:
            errorTitle='Missing Title' 
        elif not body:
            errorBody='Missing Blog'   
         
    return render_template('newpost.html', errorTitle=errorTitle, errorBody=errorBody, 
        title=title, body=body)            
        
           

@app.route('/thisBlog', methods=['GET'])
def thisBlog():
    blog_id = int(request.args.get('id'))
    
    thisBlog = Blog.query.get(blog_id)
    
    title = thisBlog.title
    body = thisBlog.body

    return render_template('thisBlog.html', title=title, body=body)

if __name__ == '__main__':
    app.run()