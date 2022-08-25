from flask import Blueprint, render_template, request, flash

views = Blueprint('views',__name__)

@views.route('/', methods=['GET','POST'])
def home():
    if request.method =='POST':
        #data = request.form.to_dict()
        flash("Sweet!",category="info")

    return render_template("home.html")

#@views.route('/addEncounter')
#def addEncounter():
#    return render_template("addEncounter.html")