from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from random import choice, randint

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

    def getLastPosition(self):
        lastCombatant = (Combatant
            .query
            .filter_by(combat_id=self.id)
            .order_by(Combatant.combatPosition.desc())
            .first()
        )

        if lastCombatant:
            return lastCombatant.combatPosition
        else:
            return 0

    # getNextPosition and getPrevPosition could probably be combined if I were cleverer
    def getNextPosition(self,currentPosition):
        nextCombatant = (Combatant.query.filter(
                Combatant.combat_id==self.id,
                Combatant.combatPosition>currentPosition
            )
            .order_by(Combatant.combatPosition)
            .first()
        )

        if nextCombatant:
            return nextCombatant
        else:
            return None
    
    def getPrevPosition(self,currentPosition):
        nextCombatant = (Combatant.query.filter(
                Combatant.combat_id==self.id,
                Combatant.combatPosition<currentPosition
            )
            .order_by(Combatant.combatPosition.desc())
            .first()
        )

        if nextCombatant:
            return nextCombatant
        else:
            return None

    def fixCombatPositions(self,targetPosition):
        targets = Combatant.query.filter(
            Combatant.combat_id==self.id,
            Combatant.combatPosition>targetPosition
        ).all()
        if targets:
            for target in targets:
                target.combatPosition -= 1
        return None

    def rollInitiative(self):
        pass

class Combatant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    combat_id = db.Column(db.Integer, db.ForeignKey('combat.id'))

    combatantName = db.Column(db.String(150))
    initiativeBonus = db.Column(db.Integer)
    initiative = db.Column(db.Integer)
    damage = db.Column(db.Integer)
    disabled = db.Column(db.Boolean)
    combatPosition = db.Column(db.Float)

    def rollInitiative(self):
        self.combatPosition = randint(1,20)+self.initiativeBonus
        return self.combatPosition