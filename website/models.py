from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    combats = db.relationship("Combat")

    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))


class Combat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    combatants = db.relationship("Combatant")


class Combatant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    combat_id = db.Column(db.Integer, db.ForeignKey('combat.id'))

    combatantName = db.Column(db.String(150))
    initiativeBonus = db.Column(db.Integer)
    combatPosition = db.Column(db.Integer)