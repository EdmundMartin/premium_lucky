from gino import Gino


db = Gino()


class WinningBond(db.Model):
    __tablename__ = 'winning_bonds'

    id = db.Column(db.Integer(), primary_key=True)
    bond = db.Column(db.String())
    date = db.Column(db.Date())
    prize = db.Column(db.Integer())