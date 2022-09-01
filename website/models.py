from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from random import choice

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    combats = db.relationship("Combat")

    username = db.Column(db.String(150), unique=True)
    password_hash = db.Column(db.String(150))

    @staticmethod
    def set_password(password):
         return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Combat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    combat_key = db.Column(db.String(8), unique=True)
    combatName = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    combatants = db.relationship("Combatant")

    @staticmethod
    def set_combat_key():
        letters = ['1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
        key = ""
        for i in range(8):
            key += choice(letters)
        return key


class Combatant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    combat_id = db.Column(db.Integer, db.ForeignKey('combat.id'))

    combatantName = db.Column(db.String(150))
    initiativeBonus = db.Column(db.Integer)
    combatPosition = db.Column(db.Integer)