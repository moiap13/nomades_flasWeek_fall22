from flask import Flask, render_template

#creation d'une instance flask
app = Flask(__name__)

#creation d'une route pour index
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user/<name>/")
def user(name):
    #return "<h2>Bonjour {}</h2>".format(name.capitalize())
    age = 23
    ctx = {
        "name": name,
        "age": 23
    }
    return render_template("user/user.html", ctx=ctx)

@app.route("/pizza/")
def pizza():
    pizza_pref = ["margarita", "calzone", "diavola", 23]
    return render_template("pizza.html", pizza=pizza_pref)