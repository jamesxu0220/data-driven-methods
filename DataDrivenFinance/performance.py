from DataDrivenFinance import app
from DataDrivenFinance.databases import Group, Decision, Rankings, ActualRanks, ActualPrices, Performance
from flask import render_template
import numpy as np


def getRPS(gid: int, sid: int) -> float:
    portfolio = np.array(Decision.query
                         .filter_by(group_id=gid, submission_id=sid).order_by(Decision.symbol)
                         .with_entities(Decision.rank1, Decision.rank2, Decision.rank3,
                                        Decision.rank4, Decision.rank5).all())
    actual = np.array(ActualRanks.query
                      .filter_by(submission_id=sid).order_by(ActualRanks.symbol)
                      .with_entities(ActualRanks.rank1, ActualRanks.rank2, ActualRanks.rank3,
                                     ActualRanks.rank4, ActualRanks.rank5).all())
    f = np.cumsum(portfolio, axis=1)
    q = np.cumsum(actual, axis=1)
    return float(np.mean(np.sum((q-f)**2, axis=1)/f.shape[1]))


def getIR(gid: int, sid: int) -> list[float]:
    weights = np.array(Decision.query
                       .filter_by(group_id=gid, submission_id=sid).order_by(Decision.symbol)
                       .with_entities(Decision.decision).all())

    prices = np.array(ActualPrices.query
                      .filter_by(submission_id=sid).order_by(ActualPrices.symbol)
                      .with_entities(ActualPrices.price_day1, ActualPrices.price_day2,
                                     ActualPrices.price_day3, ActualPrices.price_day4,
                                     ActualPrices.price_day5, ActualPrices.price_day6).all())

    RET = np.nansum(np.reshape(weights, (-1, 1)) *
                    (prices[:, 1:]/prices[:, :-1]-1), axis=0)
    ret = np.log(1 + RET)
    std = np.nanstd(ret, ddof=1)
    ret = np.nansum(ret)
    ir = (252/5)*ret/(np.sqrt(252)*std)
    return [float(ret), float(std), float(ir)]


@app.route('/performance/')
def performance():
    rankings = Rankings.query.order_by(
        Rankings.submission_id, Rankings.o_rank).all()
    performances = []
    for ranking in rankings:
        gname = Group.query.filter_by(
            group_id=ranking.group_id).first().group_name
        perf = Performance.query.filter_by(
            submission_id=ranking.submission_id, group_id=ranking.group_id).first()
        performances.append([perf, gname, ranking])
    return render_template('performance.html', performances=performances)
