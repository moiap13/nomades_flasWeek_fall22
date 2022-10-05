from flask import session, redirect, url_for
from functools import wraps
from random import randint

def is_logged_in(f):
    @wraps(f)
    def decorated_func(*args,**kwargs):
        if session.get("loggedin") and session["loggedin"]:
            return f(*args,**kwargs)
        else:
            return redirect(url_for("login.login"))
    return decorated_func   

EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
ADMIN_MAIL = "antonionomades@gmail.com"

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)