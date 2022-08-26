from flask import Blueprint, request, render_template, redirect, url_for, flash
from .models import User
from . import db

auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET','POST'])
def login():

    if request.method =='POST':
        data = request.form.to_dict()
        
        user = User.query.filter_by(username=data['username']).first()

        if user:
            if user.verify_password(data['password']):
                flash("Logged In",category="success")
            else:
                flash("Username/password incorrect",category="error")
        else:
            flash("Username/password incorrect",category="error")



    return render_template("login.html")

@auth.route('/logout')
def logout():
    return render_template("logout.html")

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():

    if request.method =='POST':
        data = request.form.to_dict()

        # need to check a bunch of stuff:
        #   do passwords meet requirements?
        #   does username already exist?

        if data['password1'] == data['password2']:
            new_user = User(username=data['username'])
            new_user.set_password(data['password1'])
            db.session.add(new_user)
            db.session.commit()
            flash("Account Created",category="success")

            return redirect(url_for('views.home'))
        else:
            flash("Error creating account",category="error")

    return render_template("sign_up.html")