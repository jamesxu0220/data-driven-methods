from flask_sqlalchemy import SQLAlchemy
from DataDrivenFinance import app


db = SQLAlchemy(app)


class Group(db.Model):
    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(15), nullable=False)
    member1_id = db.Column(db.String(15))
    member2_id = db.Column(db.String(15))
    member3_id = db.Column(db.String(15))
    member4_id = db.Column(db.String(15))
    member5_id = db.Column(db.String(15))


class Decision(db.Model):
    group_id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), primary_key=True)
    rank1 = db.Column(db.Float, nullable=False)
    rank2 = db.Column(db.Float, nullable=False)
    rank3 = db.Column(db.Float, nullable=False)
    rank4 = db.Column(db.Float, nullable=False)
    rank5 = db.Column(db.Float, nullable=False)
    decision = db.Column(db.Float, nullable=False)


class Performance(db.Model):
    submission_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, primary_key=True)
    rps = db.Column(db.Float)
    #ret = db.Column(db.Float)
    #sdp = db.Column(db.Float)
    #ir = db.Column(db.Float)
    #rps_rank = db.Column(db.Integer)
    #ir_rank = db.Column(db.Integer)
    #overall_ranking = db.Column(db.Integer)

# class AssetsHistory(db.Model):
