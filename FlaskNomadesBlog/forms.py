import email
from wtforms import StringField,Form,validators,PasswordField,TextAreaField, SelectField, BooleanField, DateTimeField, HiddenField, RadioField, SubmitField
from wtforms.fields.html5 import EmailField, IntegerRangeField
import email_validator

# creation d'une classe de formulaire pour le login
class UserLogin(Form):
    uid = StringField("Username or E-mail", validators=[validators.InputRequired()])
    pwd = PasswordField("Password", validators=[validators.InputRequired()])#, widget=PasswordInput(hide_value=False))
    btnSubmit = SubmitField("Login")

class UserRegister(Form):
    uid = StringField("Username", validators=[validators.InputRequired()])
    email = EmailField("E-mail", validators=[validators.InputRequired(), validators.Email()])
    pwd = PasswordField("Password", validators=[validators.InputRequired()])#, widget=PasswordInput(hide_value=False))
    btnSubmit = SubmitField("Register")

class UserResetPwdCode(Form):
    email = EmailField("E-mail", validators=[validators.InputRequired(), validators.Email()])
    code = StringField("Code", validators=[validators.InputRequired()])
    btnSubmit = SubmitField("Reset")


class UserModification(Form):
    uid = StringField("Username", validators=[validators.InputRequired()])
    email = EmailField("E-mail", validators=[validators.InputRequired(), validators.Email()])
    pwd = PasswordField("Password", validators=[validators.Optional()])#, widget=PasswordInput(hide_value=False))
    btnSubmit = SubmitField("Modify")

class FormArticle(Form):
    titre=StringField('Titre',[validators.length(min=2,max=200)])
    corps=TextAreaField('Message',[validators.length(min=2,max=200)])

class ExampleForms(Form):
    uNom = StringField("Nom", validators=[validators.InputRequired(), validators.Length(min=3)])
    uSexe = SelectField("Sexe", validators=[validators.Optional()], choices=[('H', "Homme"), ('F', "Femme"), ('A', "Autre")])
    uAPropos = TextAreaField("A propos de vous", validators=[validators.Optional()])
    uMdp = PasswordField("Password", validators=[validators.InputRequired(), validators.equal_to('uMdpConfirmation', message='PASSWORDS DONT MATCH')])
    uMdpConfirmation = PasswordField("Confirmer", validators=[validators.InputRequired()])
    uConnecter = BooleanField("Rester connecter ?", default=True)
    uAnniversaire = DateTimeField("Date d'anniversaire", validators=[validators.Optional()], format='%m-%d-%Y')
    uEmail = EmailField("Email", validators=[validators.InputRequired(), validators.Email(), ])
    uHidden = HiddenField("ceci est un input cache")
    uIntegerRange = IntegerRangeField("Input range", [validators.NumberRange(min=0, max=100)])
    uRadio = RadioField('Sexe', choices=[(1,'Homme'), (2,'Femme'), (3,'Autre')])
    btnSubmit = SubmitField("Login")
    btnSubmit = SubmitField("Poster")