import hashlib
import string
from flask import Blueprint, render_template, request, session, redirect, url_for
from DB_API import *

from FlaskNomadesBlog import is_logged_in
from FlaskNomadesBlog.forms import UserLogin, UserModification, UserRegister
from FlaskNomadesBlog.schema import User

Myuser = Blueprint('user', __name__, template_folder='templates', static_folder='static', static_url_path='assets')

@Myuser.route("/user/<name>/<age>")
def user(name:string, age:int):
    ctx = {
        "name": name,
        "age": age
    }
    return render_template("user/user.html", ctx=ctx)

@Myuser.route("/userinfo/")
@is_logged_in
def userinfo():
    ctx = {
        "uid": session["uid"],
        "email": session["email"]
    }
    return render_template("user/user.html", ctx=ctx)

@Myuser.route("/user/modification/", methods=["GET", "POST"])
@is_logged_in
def usermodification():
    modificationForm = UserModification(request.form)
    user_db = getDocumentDB(u'users', session["uid"])
    pwd = user_db["pwd"]

    if(request.method == "POST"):
        uid = modificationForm.uid.data
        email = modificationForm.email.data
        pwd = modificationForm.pwd.data
        hpwd = hashlib.sha256(pwd.encode('utf8')).hexdigest()
        u = User(uid, email, hpwd)

        updateDB(u'users', uid, u.toDict() if pwd != '' else {u'uid': uid, u'email': email})

        session["uid"] = uid
        session["email"] = email

    ctx = {
        "uid": session["uid"],
        "email": session["email"],
        "pwd": pwd,
        "form": modificationForm
    }

    return render_template("user/usermodification.html", ctx=ctx)

@Myuser.route("/user/delete/")
@is_logged_in
def userdelete():
    deleteDB(u'users', session["uid"])
    return redirect(url_for("login.logout"))

@Myuser.route("/user/add/<string:uid>/<string:pwd>/<int:age>")
def useradd(uid, pwd, age):
    user = User(uid, pwd, age)
    
    insertDb(u"test", uid, user.toDict())
    return "Utilisateur ajouter avec succès"

@Myuser.route("/user/get/<string:collection>/<string:uid>/")
def userget(collection, uid):
    return getDocumentDB(collection, uid)

@Myuser.route("/user/all/<string:collection>/")
def collectionget(collection):
    return getAllDocumentsDB(collection)