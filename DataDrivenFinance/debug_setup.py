from DataDrivenFinance import app, get_yfinance, performance
from DataDrivenFinance.databases import db, Decision, Performance, TradingWeek, Rankings
from flask import render_template
import pandas as pd
import numpy as np
from scipy.stats import rankdata


@app.route('/debug/setup/<int:sid>/<string:start_date>/<string:end_date>')
def debug_setup(sid, start_date, end_date):
    start_date = "2022-" + start_date
    end_date = "2022-" + end_date
    # initial week 0 - "2022-09-09" to "2022-09-17"
    # so link to update is /debug/setup/0/09-09/09-17
    
    # first week 1 - "2022-09-16" to "2022-09-24"
    # so link to update is /debug/setup/1/09-16/09-24

    trading_week = TradingWeek.query.filter_by(submission_id=sid).all()
    if not trading_week:
        try:
            new_week = TradingWeek(
                submission_id=sid, start_day=start_date, end_day=end_date)
            db.session.add(new_week)
            db.session.commit()
        except:
            return "Error setting up trading week"

    try:
        # if not ActualRanks.query.filter_by(submission_id=sid).all():
        get_yfinance.calculateRanks(sid)
    except:
        return "Error downloading results from yahoo finance"

    gids = Decision.query.filter_by(submission_id=sid).with_entities(
        Decision.group_id).distinct().all()

    stats = pd.DataFrame(
        columns=['gid', 'forecast_performance', 'decision_performance'])

    for i, gid in enumerate(gids):
        gid = gid.group_id
        new_rps = performance.getRPS(gid, sid)
        new_ret, new_sdp, new_ir = performance.getIR(gid, sid)
        new_perf = Performance(
            group_id=gid, submission_id=sid, rps=new_rps, ret=new_ret, sdp=new_sdp, ir=new_ir)
        stats.loc[i, :] = gid, new_rps, new_ir
        try:
            db.session.add(new_perf)
            db.session.commit()
        except:
            return "Error when adding new performance result to database for group " + str(gid)
    fp = pd.Series(stats['forecast_performance']).rank(ascending=True)
    fp[fp.isna()] = np.nanmax(fp) + 1
    dp = pd.Series(stats['decision_performance']).rank(ascending=False)
    dp[dp.isna()] = np.nanmax(dp) + 1
    stats['forecast_rank'] = fp
    stats['decision_rank'] = dp
    stats['overall_rank'] = (fp+dp)/2

    for index, row in stats.iterrows():
        new_rank = Rankings(submission_id=sid, group_id=row['gid'], f_rank=row['forecast_rank'],
                            d_rank=row['decision_rank'], o_rank=row['overall_rank'])
        try:
            db.session.add(new_rank)
            db.session.commit()
        except:
            return "Error when adding new ranking result to database for group " + str(gid)

    return render_template('debug/debug_setup.html', sid=str(sid), gid=str(len(gids)))
