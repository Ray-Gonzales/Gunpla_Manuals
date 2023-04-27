from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user_model import Users
from flask_app.models.manual_model import Manuals
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 


@app.route("/register")
def registration():
    return render_template("register.html")

@app.route('/register', methods=["POST"])
def create_user():
    if not Users.validate_user(request.form):
        return redirect('/register')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    print(request.form)
    id = Users.create(data)
    session['user_id'] = id
    return redirect('/')

@app.route("/login")
def sign_in():
    return render_template("login.html")

@app.route('/login',methods=['POST'])
def login_user():
    data = {"email": request.form['email']}
    user = Users.get_one_email(data)
    if not user:
        flash("Invalid Email" , 'login')
        return redirect('/login')
    if not bcrypt.check_password_hash(user.password , request.form['password']):
        flash("Invalid Password" , 'login')
        return redirect('/login')
    session['user_id'] = user.id
    print(request.form)
    return redirect('/')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
