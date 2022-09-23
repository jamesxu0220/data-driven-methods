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
    rps = db.Column(db.Float, nullable=False)
    ret = db.Column(db.Float, nullable=False)
    sdp = db.Column(db.Float, nullable=False)
    ir = db.Column(db.Float, nullable=False)


class Rankings(db.Model):
    submission_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, primary_key=True)
    f_rank = db.Column(db.Integer, nullable=False)
    d_rank = db.Column(db.Integer, nullable=False)
    o_rank = db.Column(db.Integer, nullable=False)


class TradingWeek(db.Model):
    submission_id = db.Column(db.Integer, primary_key=True)
    start_day = db.Column(db.String(10), nullable=False)
    end_day = db.Column(db.String(10), nullable=False)


class ActualRanks(db.Model):
    submission_id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), primary_key=True)
    rank1 = db.Column(db.Float, nullable=False)
    rank2 = db.Column(db.Float)
    rank3 = db.Column(db.Float)
    rank4 = db.Column(db.Float)
    rank5 = db.Column(db.Float)


class ActualPrices(db.Model):
    submission_id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), primary_key=True)
    price_day1 = db.Column(db.Float, nullable=False)
    price_day2 = db.Column(db.Float)
    price_day3 = db.Column(db.Float)
    price_day4 = db.Column(db.Float)
    price_day5 = db.Column(db.Float)
