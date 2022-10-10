from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Combat, Combatant
from . import db
from .auth import handleLogin
from markupsafe import escape

from flask_login import login_required, current_user

views = Blueprint('views',__name__)

@views.route('/', methods=['GET','POST'])
def home():

    if request.method =='POST':
        data = request.form.to_dict()
        
        if 'username' in data:
            handleLogin(escape(data['username']))
    
    return render_template("home.html", user=current_user)

@views.route('/combat', methods=['GET','POST'])
def combat_no_id():
    
    if request.method =='POST':
        data = request.form.to_dict()
        
        if 'username' in data:
            handleLogin(escape(data['username']))

    return render_template("combat.html", user=current_user, combat=None)

@views.route('/combat/<combat_arg>', methods=['GET','POST'])
def combat_id(combat_arg):

    combat = Combat.query.filter_by(combat_key=combat_arg).first()

    if not(combat):
        flash("Combat not found",category="error")
        return redirect(url_for("views.combat_no_id"))

    if request.method =='POST':
        data = request.form.to_dict()

        if 'username' in data:
            if handleLogin(escape(data['username'])):
                return render_template("combat.html", user=current_user, combat=combat)       

        postCombat(combat,data)
        db.session.commit()

    return render_template("combat.html", user=current_user, combat=combat)

@views.route('/manageCombats', methods=['GET','POST'])
@login_required
def manageCombats():

    if request.method =='POST':
        data = request.form.to_dict()
        
        new_combat = Combat(
            combatName=escape(data['combatName']),
            combat_key=Combat.set_combat_key(),
            user_id=current_user.id
        )
        
        # this should probably be in a try/except
        db.session.add(new_combat)
        db.session.commit()
        
        flash("Added new Combat",category="success")

    return render_template("manageCombat.html", user=current_user)



def postCombat(combat,data):
    
    if data['combatantForm'] == "addCombatant":
        
        if not data['initiative']:
            data['initiative'] = 0

        print(data)

        if data['initiativeType']=="radioBonus": # user has selected 'bonus' for initiative
            newCombatPosition = combat.newCombatantPosition()
            randomInitiative = True
        else: # user has selected 'total' for initiative
            newCombatPosition = data['initiative']
            randomInitiative = False

        new_combatant = Combatant(
            combatantName=escape(data['combatantName']),
            initiativeBonus=escape(data['initiative']),
            combat_id=combat.id,
            damage = 0,
            combatPosition = newCombatPosition,
            randomInitiative = randomInitiative,
            active = False
        )

        db.session.add(new_combatant)
    
        flash(f"Added new Combatant {new_combatant.combatPosition}",category="success")

    elif data['combatantForm'] == "editCombatant":
        
        print(data)
        
        combatant = Combatant.query.get(escape(data['combatantId']))

        # check for deletion
        if 'delete' in data:
            db.session.delete(combatant)

        # check position
        if 'changePosition' in data:
            # get all the combatants
            
            if data['changePosition'] == "Up" and combatant.combatPosition < combat.getFirstPosition().combatPosition:
                swap = True
                trader = combat.getPrevPosition(combatant.combatPosition)
            elif data['changePosition'] == "Down" and combatant.combatPosition > combat.getLastPosition().combatPosition:
                swap = True
                trader = combat.getNextPosition(combatant.combatPosition)
            else:
                swap = False
            
            if swap:
                if combatant.active:
                    combat.nextCombatant()
                combatant.combatPosition, trader.combatPosition = trader.combatPosition, combatant.combatPosition

        # modify damage
        if not data['addDamage']:
            data['addDamage'] = 0
        combatant.damage = max(combatant.damage + int(escape(data['addDamage'])),0)

        # commit changes
        db.session.commit()
        flash(f"Updated Combatant: {combatant}",category="success")

    elif data['combatantForm'] == "runCombat":
        if 'rollInitiative' in data:
            combat.rollInitiative()
        elif 'nextCombatant' in data:
            combat.nextCombatant()
            pass

    return None