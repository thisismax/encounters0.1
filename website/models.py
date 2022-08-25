from . import db

class Combat(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    combatantName = db.Column(db.String(150))
    initiativeBonus = db.Column(db.Integer)
    combatPosition = db.Column(db.Integer)