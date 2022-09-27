from email.policy import default
from fileinput import filename
from tokenize import String
from xmlrpc.client import Boolean
from flask import Flask, render_template, url_for, session, request, redirect
from wtforms import Form, StringField, SubmitField, PasswordField, validators
import csv
import os


#creation d'une instance flask
app = Flask(__name__)
app.secret_key = "secret"

# creation d'une classe de formulaire pour le login
class UserLogin(Form):
    uName = StringField("Username", validators=[validators.InputRequired()])
    uPwd = PasswordField("Password", validators=[validators.InputRequired()])
    btnSubmit = SubmitField("Login")

#creation d'une route pour index
@app.route("/")
def index():
    login = "uid" in session

    return render_template("index.html", login=login)

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
                file.write("{};{}\n".format(uname, upwd))

    return render_template("enregistrer.html")

@app.route("/login/", methods=["GET", "POST"])
def login():
    loginForm = UserLogin(request.form)

    if(request.method == "POST"):
        print(loginForm.uName.data)
    return render_template("loginwtf.html", form=loginForm)

@app.route("/logout/", methods=["GET"])
def logout():
    session.pop("uid", default=None)
    return redirect("/")

@app.route("/secret/")
def secret():
    if not "uid" in session:
        return "Vous n'avez pas acces !"
    else:
        return "Bienvennue dans la aprtie protégée du site :)"