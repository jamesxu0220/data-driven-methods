from DataDrivenFinance import app
from DataDrivenFinance.databases import db, Decision, Performance
from flask import request, render_template
import numpy as np


def getRPS(gid: int, sid: int) -> float:
    portfolio = Decision.query.filter_by(
        group_id=gid, submission_id=sid).first()

    sample = Decision.query.filter_by(
        group_id=-999, submission_id=sid).first()


    f_array = np.array([[portfolio.rank1, portfolio.rank2,
                       portfolio.rank3, portfolio.rank4, portfolio.rank5]])
    f = np.cumsum(f_array, axis=1)
    q_array = np.array(
        [[sample.rank1, sample.rank2, sample.rank3, sample.rank4, sample.rank5]])
    q = np.cumsum(q_array, axis=1)
    return float(np.sum((q-f)**2, axis=1)/f.shape[1])


@app.route('/performance/', methods=['POST', 'GET'])
def performance():
    if request.method == 'POST':
        gid = request.form['group_id']
        sid = request.form['submission_id']
        if not Decision.query.filter_by(
                group_id=gid, submission_id=sid).all():
            return "Error: portfolio does not exist"
        elif not Decision.query.filter_by(
                group_id=-999, submission_id=sid).all():
            return "Error: Results not ready"
        perf = Performance.query.filter_by(
            group_id=gid, submission_id=sid).first()
        if perf is None:
            new_rps = getRPS(gid, sid)
            new_perf = Performance(
                group_id=gid, submission_id=sid, rps=new_rps)
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
