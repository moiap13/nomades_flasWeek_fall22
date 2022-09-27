from tokenize import String
from flask import Flask, render_template, url_for, session, request

#creation d'une instance flask
app = Flask(__name__)

app.secret_key = "secret"

#creation d'une route pour index
@app.route("/")
def index():
    return render_template("index.html")

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
        print(request.form["uName"])
        #TODO: ouvrir un fichier (/static/user.csv)
        #TODO: Verifier si l'utilisateur existe
        #TODO: Si l'utilisateur existe renvoyer a la page index
        #TODO: Sinon l'ajouter au fichier 
    
    return render_template("enregistrer.html")