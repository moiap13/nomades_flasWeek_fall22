#!/Users/antoniopisanello/Desktop/tmp2/nomades_flaskWeek_fall22/flask_week/bin/python
from curses.ascii import US
import re
import string
from tokenize import String
from flask import Flask, render_template, url_for, session, request, redirect, flash
from pytz import utc
from datetime import datetime, timedelta

from flask_mail import Mail, Message

from DB_API import *
from FlaskNomadesBlog import ADMIN_MAIL, EMAIL_REGEX, is_logged_in, random_with_N_digits

from FlaskNomadesBlog.forms import ExampleForms, FormArticle, UserLogin, UserResetPwdCode

# blueprint imports
from FlaskNomadesBlog.blueprint.test_blueprint import test_bp
from FlaskNomadesBlog.blueprint.login import Mylogin
from FlaskNomadesBlog.blueprint.user import Myuser
from FlaskNomadesBlog.blueprint.posts import Myposts

#creation d'une instance flask
app = Flask(__name__)
app.secret_key = "secret"

app.register_blueprint(test_bp, url_prefix="/test_bp")
app.register_blueprint(Mylogin, url_prefix="/")
app.register_blueprint(Myuser, url_prefix="/")
app.register_blueprint(Myposts, url_prefix="/")

admin_mail = 'antonionomades@gmail.com'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = admin_mail
app.config['MAIL_PASSWORD'] = 'Your password'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

#creation d'une route pour index
@app.route("/")
def index():
    loggedText:String = "Accès interdit"
    if session.get("loggedin") and session["loggedin"]:
        loggedText = "Bienvenue"
    
    posts=getAllDocumentsDB(u'posts')

    return render_template("index.html", loggedText=loggedText, posts=posts)

@app.route("/secret/")
@is_logged_in
def secret():
    return "<h1>Bienvennue dans la partie interdite</h1>"

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
   msg = Message('Hello test class', sender = admin_mail, recipients = ['moiap13@gmail.com', 'antonio.pisanello.ap@gmail.com'])
   msg.body = "This is the email body"
   mail.send(msg)
   return "Sent"


@app.route("/reset/", methods=["GET", "POST"])
def reset_pwd():
    if 'loggedin' in session and session['loggedin']:
        return redirect(url_for("user.usermodification"))
    
    resetForm = UserLogin(request.form)

    if(request.method == "POST"):
        uid:string = resetForm.uid.data

        collection = u'users'
        if(re.match(EMAIL_REGEX, uid)):
            user_db = getDocumentsWhere(collection, u'email', u'==', uid)
        else:
            user_db = getDocumentsWhere(collection, u'uid', u'==', uid)

        if(user_db):
            user_db = user_db[next(iter(user_db))]
            code = random_with_N_digits(6)
            now_plus_10 = datetime.now() + timedelta(minutes=10)
            updateDB(collection, user_db["uid"], {u'code': code, u'code_expiration': now_plus_10})
            msg = Message('FlaskNomadesBlog - Reset password code', sender = ADMIN_MAIL, recipients = [user_db["email"]])
            msg.body = "<h1> Reset Code </h1> <p> Your reset code is: {} </p> <p> Please insert it in the page : {} </p>".format(code, url_for("reset_pwd_code", email=user_db["email"]))
            mail.send(msg)
            return redirect(url_for("reset_pwd_code", email=user_db["email"]))
        
        flash('User not found')
    return render_template("login/reset.html", form=resetForm)
 
@app.route("/reset_code/<email>", methods=["GET", "POST"])
def reset_pwd_code(email):
    if 'loggedin' in session and session['loggedin']:
        return redirect(url_for("user.usermodification"))
    
    resetForm = UserResetPwdCode(request.form)
    err = False

    if(request.method == "POST"):
        email:string = resetForm.email.data
        code:string = resetForm.code.data

        collection = u'users'
        user_db = getDocumentsWhere(collection, u'email', u'==', email)
        print(user_db)

        if(user_db):
            user_db = user_db[next(iter(user_db))]

            now = datetime.now().replace(tzinfo=utc)
            exp = user_db["code_expiration"].replace(tzinfo=utc)
            if(now > exp):
                flash('Code expired', 'danger')
                return redirect(url_for("reset_pwd"))

            if(code == str(user_db["code"])):
                flash('Code correct', 'success')
                session["loggedin"] = True
                session["uid"] = user_db["uid"]
                session["email"] = user_db["email"]
                return redirect(url_for("user.usermodification"))
            flash('Code not valid', 'danger')
            return redirect(url_for("reset_pwd_code", email=user_db["email"]))
        
        flash('User not found', 'danger')
    return render_template("login/reset_code.html", form=resetForm, email=email)

#running the APP
if __name__ =='__main__':
    app.run(debug=True, host="0.0.0.0", port=13225)