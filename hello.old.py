import hashlib
from tokenize import String
from flask import Flask, render_template, url_for, session, request, redirect
from wtforms import Form, StringField, SubmitField, PasswordField, validators
from functools import wraps
import firebase_admin
from firebase_admin import credentials, firestore
from flask_mail import Mail, Message

from templates.forms.forms import ExampleForms
from test_blueprint import test_bp

#creation d'une instance flask
app = Flask(__name__)
app.secret_key = "secret"

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'moiap13@gmail.com'
app.config['MAIL_PASSWORD'] = 'xyxozyszwnkaysbn'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

app.register_blueprint(test_bp, url_prefix="/test_bp")

mail = Mail(app)

def insertDb(collection, id, value):
    if type(value) is dict:
        db.collection(collection).document(id).set(value) # value doit etre un dictionnaire 

def getDocumentDB(collection, id):
    doc = db.collection(collection).document(id).get()
    return doc.to_dict() if doc.exists else None

def getAllDucmentsDB(collection):
    stream = db.collection(collection).stream()
    ret = {}
    for doc in stream:
        ret[doc.id] = doc.to_dict()
    return ret

def updateDB(collection, id, value):
    if type(value) is dict:
        db.collection(collection).document(id).update(value) # value doit etre un dictionnaire


def deleteDB(collection, id):
    db.collection(collection).document(id).delete()

key = {
  "type": "service_account",
  "project_id": "nomadesflaskweekfall2022",
  "private_key_id": "7a589f62413d6b421364667223c2c664eb0ac59f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQCuEjMuHHqXl+L/\nGvBhfQ1wfBcCdjgCdXYr8sMpyO30IVCurvt9n/TT+utYhhy4eJktUVi7ZO9Qhc19\nriJV/VU1IYG1owG8q0p7qxbRRLTWOOOhZ8DC9Fx6lVuwgfaG4w2BMIzHtn3JcG6a\n++l6kRCbtaN/uHFkNL3QtcPsEtcrPKseKi8St8BCmCGW5+Om+Sbmw5NtwXqKiW7K\nPJSqYmtGl77Hm55i/89uVpPtEe5aB8PQhS62QwFVW+fc/95JTAbekeKTP/RdfnXP\nbxl5AueYgRnwooiQn8YtcgPduujfzw+2K72lw+4T+95/8JSVFkIDxtuMu3HIlybz\nQbJQtabLAgMBAAECggEAFvc6vmYufGqjHcIpncsYZ1NP29jKCfUCWskEG7KxRkjQ\n8sMOViQw8njD7SGAj4wFtZdqbArkkgydMGw1hn/OapyZluPDOmelA4zujTyR2UOX\nMLfWFEKWIuwqtS5oXqJ9KSLFKCI5FUcaqKL8yllyRgDgadzlRPG6a1tX1oEj10XJ\nILgqMN76e51AGWgwaJ4rHhztX2hYgjkwYSJLvk3T/R5WuX7vdoBEZ2nXfHlfFHiN\nfEbAwWs8slB4JsbFuz418zMlitsAvMbsnZm+L+NBv+Ru6MlQIwhSR8sjgwAejVlg\noI5u13lG/9BI5bUuXsxs1iO5yKQ/uW/NLz2VERjpFQKBgQDxPyPVIpbuKWbojdU9\nafNFc+boUwdpte9p8RRJ8XF5oUFsAwqcbYhx3aFsHp/Uv0TjUz3iglb9/jenS3DG\nYXI+PBBBwzmBmamju/FL51Kp6aAqwoUuAH6uPBsE4rL0HvDoVPRqad35gOWujA6h\nONZtTNKsvIf4zruk41XMsV7uLQKBgQC4t2L+0f9pwmQzSXXW513aGQRjFuLd/hr0\nt65bjR7Ed3Nulr6LhDnjfSFBQmg5b+aR4wv2rUheqarNydR6XU4IAxFhKB7bWDvA\n9lyp8pSGPw+hh0F952m51RT9/9prHBcTHY/AIfGi4pqGpKpzByJeGw3xi3d0fCid\n6BtCdzx71wKBgQCpNyGaMU3utemx+zJ0hmmV8MspcHvFoVDSXcBecVWn+/0YlzWN\nLaNEQzIj1YNExfi6/ztsMwJz3CoLVXZAID/y+Uxp5Fbk2fTMnVqOZC5ucinfdFvY\nPY6eBhjpn13or/9I57YdIi8KAGiauzDT0ztMpVMsyH0Tf2bNLIyVLGCq7QKBgQCG\nDzKd1jMUwqyOPGZ1zf1jaHyync2RZ/aQXS8B6u3FkRwJywYHo7OP0yTrhBK4fOpO\nPwZTxXecnG8GY9D97fHQBsn6RW//qY3UgfjGrvP0apghl1SE2Ar3gBp4LdSLoBtv\nGClYPEpu+R9FUQUT7r2WpvP7tkjAFcw0rlv6ZSdUiQKBgQCmdHntsL6R8+HH7WOR\nMfBzHL2Yd1+zAq0FJBT7/yzYNjuZE3oazckokgiv6pquxTEfPVNqsM9xp31ZtDOo\nFyU9vKnp+jynCyXSax10J/jBrfdvnkSs35qRPr2MWXIrVW6/QHFiXRIjeNIc76xx\nFnppjzTvGAWFRFP33O4LMMghDA==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-93e2x@nomadesflaskweekfall2022.iam.gserviceaccount.com",
  "client_id": "100255854051119303065",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-93e2x%40nomadesflaskweekfall2022.iam.gserviceaccount.com"
}

cred = credentials.Certificate(key)
firebase_admin.initialize_app(cred)
db = firestore.client()

test_collection = db.collection(u"test")

class User(object):
    def __init__(self, uid, pwd, age) -> None:
        self.uid = uid
        self.pwd = pwd
        self.age = age
    def toDict(self):
        return self.__dict__


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
    """tdict = {}
    t_temp = test_collection.document("docIdTest").get()
    print(t_temp.to_dict()["testPrenom"])
    if t_temp.exists:
        #tdict[t_temp.id] = t_temp.to_dict()
        tdict = t_temp.to_dict()["testPrenom"]
    else:
        tdict = "No documents found with id"
    
    return tdict"""

    
    """data={}
    docs = db.collection(u'test').where(u"uid", u"==", "antoage").get()
    for doc in docs:
        data[doc.id] =doc.to_dict()
    return data"""

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
        uid:String = request.form["uName"]
        pwd:String = request.form["uPwd"]
        age:int = request.form["age"]
        hpwd = hashlib.sha256(pwd.encode('utf-8')).hexdigest()
        
        collection = u'users'
        if getDocumentDB(collection, uid) == None:
            u = User(uid, hpwd, age)
            insertDb(collection, uid, u.toDict())
            session["uid"] = uid
            session["loggedin"] = True
            return redirect(url_for("index"))

    return render_template("enregistrer.html")

@app.route("/login/", methods=["GET", "POST"])
def login():
    loginForm = UserLogin(request.form)
    err = False

    if(request.method == "POST"):
        uid = loginForm.uName.data
        pwd = loginForm.uPwd.data
        hpwd = hashlib.sha256(pwd.encode('utf-8')).hexdigest()
        err=True

        user_db = getDocumentDB(u'users', uid)
        if(user_db):
            if(user_db["pwd"] == hpwd):
                session["loggedin"] = True
                session["uid"] = uid
                return redirect(url_for("userinfo"))
    
    return render_template("loginwtf.html", form=loginForm, error=err)

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

@app.route("/logout/", methods=["GET"])
@is_logged_in
def logout():
    session.clear()
    return redirect("/")

@app.route("/secret/")
@is_logged_in
def secret():
    return "<h1>Bienvennue dans la partie interdite</h1>"


@app.route("/users")
def users():
    test_stream = test_collection.stream()
    printdict = {}
    for doc in test_stream:
        printdict[doc.id] = doc.to_dict()

    return printdict


@app.route("/user/add/<string:uid>/<string:pwd>/<int:age>")
def useradd(uid, pwd, age):
    user = User(uid, pwd, age)
    
    insertDb(u"test", uid, user.toDict())
    return "Utilisateur ajouter avec succès"

@app.route("/user/get/<string:collection>/<string:uid>/")
def userget(collection, uid):
    return getDocumentDB(collection, uid)

@app.route("/user/all/<string:collection>/")
def collectionget(collection):
    return getAllDucmentsDB(collection)

@app.route("/userinfo/")
@is_logged_in
def userinfo():
    ctx = {
        "uid": session["uid"]
    }
    return render_template("user/user.html", ctx=ctx)

@app.route("/user/modification/", methods=["GET", "POST"])
@is_logged_in
def usermodification():
    loginForm = UserLogin(request.form)
    user_db = getDocumentDB(u'users', session["uid"])
    pwd = user_db["pwd"]
    print(pwd)

    if(request.method == "POST"):
        uid = loginForm.uName.data
        pwd = loginForm.uPwd.data

        updateDB(uid, pwd)

        session["uid"] = uid

    ctx = {
        "uid": session["uid"],
        "pwd": pwd,
        "form": loginForm
    }

    return render_template("user/usermodification.html", ctx=ctx)

@app.route("/user/delete/")
@is_logged_in
def userdelete():
    #deleteDB(session["uid"])
    return redirect(url_for("logout"))

@app.route("/form/example", methods=["GET", "POST"])
def formexample():
    form = ExampleForms(request.form)
    if request.method=="POST":
        if not form.uNom.data[0].isalpha():
            form.uNom.errors.append("Le nom doit forcement commencer par une lettre")
        
        print(form.uNom.data)
    return render_template("forms/forms.html", form=form)

@app.route("/sendmail")
def sendmail():
   msg = Message('Hello', sender = 'moiap13@gmail.com', recipients = ['antonio.pisanello.ap@gmail.com'])
   msg.body = "This is the email body"
   mail.send(msg)
   return "Sent"


#running the APP
if __name__ =='__main__':
    app.run(debug=True, host="0.0.0.0", port=13225)