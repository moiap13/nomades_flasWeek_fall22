
import string
from flask import Blueprint, render_template, request, flash, session, redirect, url_for
import hashlib
import re
from flask_mail import Message

from DB_API import *
from FlaskNomadesBlog import ADMIN_MAIL, EMAIL_REGEX, is_logged_in, random_with_N_digits
import FlaskNomadesBlog
from FlaskNomadesBlog.forms import UserLogin, UserRegister, UserResetPwdCode
from FlaskNomadesBlog.schema import User

Mylogin = Blueprint('login', __name__, template_folder='templates', static_folder='static', static_url_path='assets')

@Mylogin.route("/register/", methods=["GET", "POST"])
def register():
    if 'loggedin' in session and session['loggedin']:
        return redirect(url_for("user.userinfo"))
    
    registerForm = UserRegister(request.form)
    
    if request.method == "POST":
        uid:string = registerForm.uid.data
        email:string = registerForm.email.data
        pwd:string = registerForm.pwd.data
        hpwd:string = hashlib.sha256(pwd.encode('utf-8')).hexdigest()
        
        collection = u'users'
        if getDocumentDB(collection, uid) == None:
            u = User(uid, email, hpwd)
            insertDb(collection, u.uid, u.toDict())
            session["uid"] = uid
            session["email"] = email
            session["loggedin"] = True
            return redirect(url_for("user.userinfo"))

    return render_template("login/register.html", form=registerForm)

@Mylogin.route("/login/", methods=["GET", "POST"])
def login():
    if 'loggedin' in session and session['loggedin']:
        return redirect(url_for("user.userinfo"))
    
    loginForm = UserLogin(request.form)
    err = False

    if(request.method == "POST"):
        uid:string = loginForm.uid.data
        pwd:string = loginForm.pwd.data
        hpwd:string = hashlib.sha256(pwd.encode('utf-8')).hexdigest()

        collection = u'users'
        if(re.match(EMAIL_REGEX, uid)):
            user_db = getDocumentsWhere(collection, u'email', u'==', uid)
        else:
            user_db = getDocumentsWhere(collection, u'uid', u'==', uid)


        if(user_db):
            user_db = user_db[next(iter(user_db))]
            print(user_db)
            if(user_db["pwd"] == hpwd):
                session["loggedin"] = True
                session["uid"] = user_db["uid"]
                session["email"] = user_db["email"]
                return redirect(url_for("user.userinfo"))
        
        flash('Login Failed', 'danger')
    return render_template("login/loginwtf.html", form=loginForm)

    """loginForm = UserLogin(request.form)
    if request.method == "POST":
        username:String = loginForm.uName.data
        password:String = loginForm.uPwd.data

        userFile = os.path.join(app.static_folder, 'user.csv')

        with open(userFile, "r") as file:
            reader = csv.reader(file, delimiter=";")
            for row in reader:
                if row[0] == username and row[1] == password:
                    session["uid"] = username
                    session["loggedin"] = True
                    return redirect(url_for('index'))

    return render_template("loginwtf.html", form=loginForm)"""

@Mylogin.route("/logout/", methods=["GET"])
@is_logged_in
def logout():
    session.clear()
    return redirect(url_for("index"))