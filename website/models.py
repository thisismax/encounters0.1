from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    combats = db.relationship("Combat")

    username = db.Column(db.String(150), unique=True)
    password_hash = db.Column(db.String(150))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


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