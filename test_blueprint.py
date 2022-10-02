from flask import Blueprint, render_template

test_bp = Blueprint('test_bp', __name__, template_folder='templates', static_folder='static', static_url_path='assets')

@test_bp.route("/")
def testindex():
    return "test bp"

@test_bp.route("/test")
def testtest():
    return "test"

@test_bp.route("/bp")
def testbp():
    return "bp"