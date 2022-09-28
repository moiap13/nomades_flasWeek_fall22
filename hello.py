from curses import flash
from email.policy import default
from fileinput import filename
from tokenize import String
from xmlrpc.client import Boolean
from flask import Flask, render_template, url_for, session, request, redirect
from wtforms import Form, StringField, SubmitField, PasswordField, validators
import csv
import os
from passlib.hash import sha256_crypt
from functools import wraps
import firebase_admin
from firebase_admin import credentials, firestore

#creation d'une instance flask
app = Flask(__name__)
app.secret_key = "secret"


def is_logged_in(f):
    @wraps(f)
    def decorated_func(*args,**kwargs):
        if session.get("loggedin") and session["loggedin"]:
            return f(*args,**kwargs)
        else:
            return redirect(url_for("login"))
    return decorated_func



# creation d'une classe de formulaire pour le login
class UserLogin(Form):
    uName = StringField("Username", validators=[validators.InputRequired()])
    uPwd = PasswordField("Password", validators=[validators.InputRequired()])
    btnSubmit = SubmitField("Login")

#creation d'une route pour index
@app.route("/")
def index():
    loggedText:String = "Accès interdit"
    if session.get("loggedin") and session["loggedin"]:
        loggedText = "Bienvenue"

    return render_template("index.html", login=login, loggedText=loggedText)


@app.route("/user/<name>/<age>")
def user(name:String, age:int):
    #return "<h2>Bonjour {}</h2>".format(name.capitalize())
    ctx = {
        "name": name,
        "age": age
    }
    return render_template("user/user.html", ctx=ctx)

@app.route("/enregistrer/", methods=["GET", "POST"])
def enregistrer():
    if request.method == "POST":
        uname:String = request.form["uName"]
        upwd:String = request.form["uPwd"]
        epwd = sha256_crypt.encrypt(upwd)
        add:Boolean = True
        userFile = os.path.join(app.static_folder, 'user.csv')
        
        #TODO: ouvrir un fichier (/static/user.csv)
        with open(userFile, 'r+') as file:
            #TODO: Sinon l'ajouter au fichier
            reader = csv.reader(file, delimiter = ';')

            for row in reader:
                if row[0].lower() == uname.lower():
                    add = False
                    break
            if add:
                file.write("{};{}\n".format(uname, epwd))

    return render_template("enregistrer.html")

@app.route("/login/", methods=["GET", "POST"])
def login():
    loginForm = UserLogin(request.form)
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

    return render_template("loginwtf.html", form=loginForm)

@app.route("/logout/", methods=["GET"])
@is_logged_in
def logout():
    session.clear()
    return redirect("/")

@app.route("/secret/")
@is_logged_in
def secret():
    return "<h1>Bienvennue dans la partie interdite</h1>"

#running the APP
if __name__ =='__main__':
    app.run(debug=True, host="0.0.0.0", port=13225)