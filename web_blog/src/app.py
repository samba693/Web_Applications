from flask import Flask, render_template, request, session, redirect, url_for
from models.user import User
from models.database import Database

__author__ = 'Sambasiva Rao Gangineni'

app = Flask(__name__)
app.secret_key = "samba"

@app.route('/')
def home_template():
    try:
        cookie = session['email']
    except:
        cookie = None
    return render_template('home.html',message="Welcome to the Web development Blog",condition=True if cookie is None else False)

@app.route('/login') #www.examplesite.com/api/
def login_template():
    return render_template('login.html')

@app.route('/login/<x>') #www.examplesite.com/api/
def login_templates(x):
    return render_template('login.html',message=x)

@app.route('/register')
def register_templates(x="Join Us!"):
    return render_template('register.html', message=x)

@app.route('/register/<x>')
def register_template(x):
    return render_template('register.html', message=x)

@app.before_first_request
def intialize_database():
    Database.initialize()

@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email,password):
        User.login(email)
    elif User.get_by_email(email) is None:
        session['email']=None
        register_template(x="Account does not exists. Please Create an account.")
        return redirect(url_for('register_template',x="Account does not exists. Please Create an account."))
    else:
        session['email']=None
        login_templates(x="Authentication failed! Please try again")
        return redirect(url_for('login_templates',x="Authentication failed! Please try again"))
    
    return render_template("profile.html", email=session['email'].split('@')[0] if session['email'] is not None and '@' in session['email'] else session['email'])

@app.route('/auth/register',methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']
    User.register(email,password)
    if session['email'] is not None:
        return render_template("profile.html", email=session['email'].split('@')[0] if '@' in session['email'] else session['email'])
    else:
        register_template(x="Email already exists! Login or try with other email ")
        return redirect(url_for("register_template",x="Email already exsists! Login or try with other email"))    
     

@app.route('/logout')
def logout_template():
    session['email']=None
    return render_template("logout.html", message="Successfully Logged Out")

if __name__ == "__main__":
    app.run()
