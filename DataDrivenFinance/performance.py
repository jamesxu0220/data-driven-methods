from DataDrivenFinance import app, get_yfinance
from DataDrivenFinance.databases import db, Decision, Performance, TradingWeek, ActualRanks, ActualPrices
from flask import request, render_template
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


@app.route('/performance/', methods=['POST', 'GET'])
def performance():
    if request.method == 'POST':
        gid = request.form['group_id']
        sid = request.form['submission_id']

        if not Decision.query.filter_by(
                group_id=gid, submission_id=sid).all():
            return "Error: portfolio does not exist"

        elif not TradingWeek.query.filter_by(submission_id=sid).all():
            return "Error: Results not ready for week " + str(sid)

        elif not ActualRanks.query.filter_by(submission_id=sid).all():
            # Maybe add a progress bar here???
            # Grabs new info from yahoo finance and calculates the actual prices/ranks
            get_yfinance.calculateRanks(sid)

        performance = Performance.query.filter_by(
            group_id=gid, submission_id=sid).first()

        if performance is None:
            new_rps = getRPS(gid, sid)
            new_ret, new_sdp, new_ir = getIR(gid, sid)
            new_perf = Performance(
                group_id=gid, submission_id=sid, rps=new_rps, ret=new_ret, sdp=new_sdp, ir=new_ir)
            try:
                db.session.add(new_perf)
                db.session.commit()
            except:
                return "Error when adding new performance result to database"
            performance = Performance.query.filter_by(
                group_id=gid, submission_id=sid).first()
        return render_template('performance/performance.html', performance=performance)
    else:
        return render_template('performance/performance_inquiry.html')
