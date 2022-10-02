from wtforms import StringField,Form,validators,PasswordField,TextAreaField, SelectField, BooleanField, DateTimeField, EmailField, HiddenField, IntegerRangeField, RadioField, SubmitField
import email_validator

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

class FormArticle(Form):
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