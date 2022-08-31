from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Combat
from . import db

from flask_login import login_required, current_user

views = Blueprint('views',__name__)

@views.route('/')
def home():
    return render_template("home.html", user=current_user)

@views.route('/combat')
def combat():
    return render_template("combat.html", user=current_user)

@views.route('/manageCombats', methods=['GET','POST'])
@login_required
def manageCombats():

    if request.method =='POST':
        data = request.form.to_dict()
        
        new_combat = Combat(
            combatName=data['combatName'],
            user_id=current_user.id
        )
        
        # this should probably be in a try/except
        db.session.add(new_combat)
        db.session.commit()
        
        flash("Added new Combat",category="success")

    return render_template("manageCombat.html", user=current_user)