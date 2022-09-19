from DataDrivenFinance import app, get_yfinance, performance
from DataDrivenFinance.databases import db, Decision, Performance, TradingWeek, ActualRanks


@app.route('/test/set_week/<int:sid>/<string:start_date>/<string:end_date>')
def set_new_week(sid, start_date, end_date):
    start_date = "2022-" + start_date
    end_date = "2022-" + end_date
    # first week 0 - "2022-09-09" to "2022-09-17"
    # so link to update is /test/set_week/0/09-09/09-17

    new_week = TradingWeek(
        submission_id=sid, start_day=start_date, end_day=end_date)
    db.session.add(new_week)
    db.session.commit()

    #if not ActualRanks.query.filter_by(submission_id=sid).all():
    get_yfinance.calculateRanks(sid)

    gids = Decision.query.filter_by(submission_id=sid).with_entities(
        Decision.group_id).distinct().all()

    for gid in gids:
        gid = gid.group_id
        new_rps = performance.getRPS(gid, sid)
        new_ret, new_sdp, new_ir = performance.getIR(gid, sid)
        new_perf = Performance(
            group_id=gid, submission_id=sid, rps=new_rps, ret=new_ret, sdp=new_sdp, ir=new_ir)
        try:
            db.session.add(new_perf)
            db.session.commit()
        except:
            return "Error when adding new performance result to database for group " + str(gid)

    return "Success setting up results for week " + str(sid) + "; added performance results for " + \
        str(len(gids)) + " groups."
