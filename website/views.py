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
        flash("Combat not found",category="error")
        return redirect(url_for("views.combat_no_id"))

    if request.method =='POST':
        data = request.form.to_dict()
        
        # note to self - put these in their own class/functions
        if data['combatantForm'] == "addCombatant":
            
            if not data['initiativeBonus']:
                data['initiativeBonus'] = 0

            new_combatant = Combatant(
                combatantName=data['combatantName'],
                initiativeBonus=data['initiativeBonus'],
                combat_id=combat.id,
                damage = 0,
                disabled = False,
                combatPosition = Combatant.query.filter_by(combat_id=combat.id).count()+1
            )

            db.session.add(new_combatant)
            db.session.commit()
        
            flash(f"Added new Combatant {new_combatant.combatPosition}",category="success")

        elif data['combatantForm'] == "editCombatant":
            
            print(data)
            
            combatant = Combatant.query.get(data['combatantId'])

            # check for deletion
            if 'delete' in data:
                db.session.delete(combatant)

            # check if character has been disabled/enabled
            # should I change this to skip? act / skip? or something.
            if 'disable' in data:
                if data['disable'] == 'Enable':
                    combatant.disabled = False
                else:
                    combatant.disabled = True

            # check position
            if 'changePosition' in data:
                # get all the combatants
                combatants_query = (Combatant
                    .query
                    .filter_by(combat_id=combat.id)
                    .order_by('combatPosition')
                    .all()
                )
                combatants_list = [combatant.id for combatant in combatants_query]
                
                if data['changePosition'] == "Up":
                    # need to stop people from overrunning the array here
                    current_Position = combatants_list.index(combatant.id)
                    combatants_list.pop(current_Position)
                    combatants_list.insert(current_Position-1,combatant.id)

                print(combatants_list)
                
                # Fack. And then I have to go in and update everything.
                # I need to figure out an elegant way to store, retrieve and modify the combat position.

            # modify damage
            if not data['addDamage']:
                data['addDamage'] = 0
            combatant.damage = max(combatant.damage + int(data['addDamage']),0)

            # commit changes
            db.session.commit()
            flash(f"Updated Combatant: {combatant}",category="success")



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