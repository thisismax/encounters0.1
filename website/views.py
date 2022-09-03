from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Combat, Combatant
from . import db

from flask_login import login_required, current_user

views = Blueprint('views',__name__)

@views.route('/')
def home():
    return render_template("home.html", user=current_user)

@views.route('/combat')
def combat_no_id():
    return render_template("combat.html", user=current_user, combat=None)

@views.route('/combat/<combat_arg>', methods=['GET','POST'])
def combat_id(combat_arg):

    combat = Combat.query.filter_by(combat_key=combat_arg).first()

    if not(combat):
        return redirect(url_for("views.combat_no_id"))

    if request.method =='POST':
        data = request.form.to_dict()
        
        new_combat = Combatant(
            combatantName=data['combatantName'],
            initiativeBonus=data['initiativeBonus']
        )
        
        # this should probably be in a try/except
        db.session.add(new_combatant)
        db.session.commit()
        
        flash("Added new Combat",category="success")

    return render_template("combat.html", user=current_user, combat=combat)

@views.route('/manageCombats', methods=['GET','POST'])
@login_required
def manageCombats():

    if request.method =='POST':
        data = request.form.to_dict()
        
        new_combat = Combat(
            combatName=data['combatName'],
            combat_key=Combat.set_combat_key(),
            user_id=current_user.id
        )
        
        # this should probably be in a try/except
        db.session.add(new_combat)
        db.session.commit()
        
        flash("Added new Combat",category="success")

    return render_template("manageCombat.html", user=current_user)