from flask import Blueprint, request, render_template, redirect, url_for, flash
from markupsafe import escape
from .models import User
from . import db

from flask_login import login_user, login_required, logout_user, current_user

LANDING = 'views.home'
auth = Blueprint('auth',__name__)


@auth.route('/login', methods=['GET','POST'])
def login():

    if request.method =='POST':
        data = request.form.to_dict()
        
        if 'username' in data:
            handleLogin(escape(data['username']))

            # user = User.query.filter_by(username=data['username']).first()

            # if user:
            #     flash("Logged in.", category="success")
            #     login_user(user, remember=True)
            #     return redirect(url_for(LANDING))
            # else:
            #     flash("Username not found",category="error")

        # if user:
        #     if user.verify_password(escape(data['password'])):
        #         flash("Logged In",category="success")
        #         login_user(user, remember=True)
        #         return redirect(url_for('views.home'))
        #     else:
        #         flash("Username/password incorrect",category="error")
        # else:
        #     flash("Username/password incorrect",category="error")

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.",category="info")
    return redirect(url_for("auth.login"))

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():

    if request.method =='POST':
        data = request.form.to_dict()

        if 'username' in data:
            new_user = User(
                username=escape(data['username'])
            )

            db.session.add(new_user)
            db.session.commit()

            flash("New account created.")
            login_user(new_user, remember=True)
            return redirect(url_for(LANDING))

        # if data['password1'] == data['password2']:
        #     new_user = User(
        #         username=data['username'],
        #         password_hash=User.set_password(data['password1'])
        #     )
            
        #     # this should probably be in a try/except
        #     db.session.add(new_user)
        #     db.session.commit()
            
        #     flash("Account Created",category="success")
        #     login_user(new_user, remember=True)
        #     return redirect(url_for('views.home'))
        # else:
        #     flash("Error creating account",category="error")

    return render_template("sign_up.html", user=current_user)

def handleLogin(username):

    user = User.query.filter_by(username=username).first()

    if user:
        flash("Logged in.", category="success")
        login_user(user, remember=True)
        return True
    else:
        flash("Username not found",category="error")
        return False
