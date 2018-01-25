from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:Mares eat oats@localhost:8889/blogz'

app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'HeyEveryoneThisIsMySecretKey'

db = SQLAlchemy(app)

#global variables

usernameGlb = ""


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, username, password):
        self.username = username
        self.password = password
       
class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    body = db.Column(db.String(150))
    username = db.Column(db.String(120))

    def __init__(self, title, body, username):
        self.title = title
        self.body = body
        self.username = username


# @app.before_request
# def require_login():
#     login_required_routes = ['newpost']
#     if request.endpoint in login_required_routes and 'username' not in session:
#         return redirect('/login')


@app.route('/', methods=['POST', 'GET'])
def index():

    User_all = User.query.all()
    
    return render_template('home.html', title="Blog Users", users=User_all)



@app.route('/newpost', methods=['GET','POST'])
def newpost():
    if not ( 'username' in list (session.keys() ) ):   
        return redirect('/login')
    
    errorTitle = ""
    errorBody = ""
    title=""
    body=""
    username=""

    if request.method == 'POST':
        title = request.form['title'] 
        body = request.form['body']
        username = session.get('username')
        
    
        if (title and body):
 
            new_Blog = Blog(title, body, username)
            db.session.add(new_Blog)
            db.session.commit()
            
            blog_id = int(new_Blog.id)
           
            title = "New Blog"    
            blogs = Blog.query.filter_by(id=int(blog_id)).all() 
            
            return render_template('blogs.html', blogs=blogs, title=title)

        elif not title:
            errorTitle='Missing Title' 
        elif not body:
            errorBody='Missing Blog'   
         
    return render_template('newpost.html', errorTitle=errorTitle, errorBody=errorBody, 
        title=title, body=body)            


@app.route('/singleBlog/<string:a_blog_id>', methods=['GET', 'POST'])
def singleBlog(a_blog_id):  
    # print('singleBlog-a')       
    # print(a_blog_id)

    title = "Clicked on Blog"    
    blogs = Blog.query.filter_by(id=int(a_blog_id)).all() 
            
    return render_template('blogs.html', blogs=blogs, title=title)




@app.route('/userBlogs/<string:a_username>/', methods=['GET', 'POST'])
def userBlogs(a_username):
    # print('userBlogs-a')
    # print(a_username)

    
    username = a_username  

    
    title = "User Blogs"    
    blogs = Blog.query.filter_by(username=username).all()   
    return render_template('blogs.html', blogs=blogs, title=title)


@app.route('/allPosts', methods=['GET', 'POST'])
def allPosts():
    title = "All Blogs"    
    blogs = Blog.query.all()   
    return render_template('blogs.html', blogs=blogs, title=title)



@app.route('/signup', methods=['GET','POST'])
def signup():
    username     = ""
    password     = ""
    v_password   = ""
    username_error = ""
    password_error = ""
    v_password_error = ""
    existing_User = ""

    if request.method == 'GET':
        pass
    else:    
        username = request.form['username'] 
        username_error = editUsername(username)
        
        if username_error:
            pass 
        else:
            existing_User = User.query.filter_by(username=username).first()   
                               
            if existing_User: 
                username_error = "User Name already on file: Please click 'Login'"
               
        if username_error:
            pass 
        else:    
            password = request.form['password']
            v_password = request.form['v_password']
            password_error = editPassword(password)

            if password_error:
                pass
            elif v_password == "":
                v_password_error = "Please validate Password"    
            elif password == v_password:
                pass
            else:
                password_error = "Password and Validate Password don't match"

        if (username_error) or (password_error) or (v_password_error):
            password = ""
            v_password = ""
            
        else:
            
                       
            new_User = User(username, password)
            db.session.add(new_User)
            db.session.commit()

            session['username'] = new_User.username
            return redirect('/newpost')


    return render_template( "signup.html", username=username, password=password,
        v_password=v_password, username_error=username_error, password_error=password_error,
        v_password_error=v_password_error )



@app.route('/login', methods=['GET','POST'])
def login():
    username     = ""
    password     = ""
    username_error = ""
    password_error = ""
    existing_User = ""

    if request.method == 'GET':
        pass

    else:    
        username = request.form['username'] 
        username_error = editUsername(username)
        
        if username_error:
            pass 
        else:
            existing_User = User.query.filter_by(username=username).first()   
                               
            if existing_User: 
               pass
            else:    
               username_error = "User Name not on file: Please click 'Create One!'"
               

        if username_error:
            pass
        else:    
            password = request.form['password']
            password_error = editPassword(password)

            if password_error:
                pass
            elif password == existing_User.password:
                pass
            else:
                password_error = "Incorrect Password"


        if (username_error) or (password_error):
            password = ""
         
        else:
            session['username'] = existing_User.username         
            return redirect('/newpost')
 

    return render_template( "login.html", username=username, password=password,
                username_error = username_error, password_error = password_error )


def editUsername(username):
 
    if not username:
        return "Please enter User Name"
    elif (len(username) < 3):
        return "User Name can't be less than 3 characters"
    elif ' ' in username:    
        return "User Name must not contain spaces"

    return ""


def editPassword(password):
 
    if not password:
        return "Please enter Password"
    elif (len(password) < 3):
        return "Password can't be less than 3 characters"

    return ""
 

@app.route('/logout', methods=['GET','POST'])
def logout():
    if ( 'username' in list( session.keys() ) ):  
        del session['username']

    return render_template( "logout.html" )
      

if __name__ == '__main__':
    app.run()