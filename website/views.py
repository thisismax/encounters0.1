from flask import Blueprint, render_template

views = Blueprint('views',__name__)

@views.route('/')
def home():
    return render_template("home.html", text="this is a variable")

@views.route('/addEncounter')
def addEncounter():
    return render_template("addEncounter.html")