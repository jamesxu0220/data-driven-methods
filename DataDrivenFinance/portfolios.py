from DataDrivenFinance import app
from DataDrivenFinance.databases import Decision, Group
from flask import request, render_template


@app.route('/portfolios/', methods=['POST', 'GET'])
def portfolios():
    if request.method == 'POST':
        gid = request.form['group_id']
        sid = request.form['submission_id']
        return view(gid, sid)
    else:
        return render_template('portfolio/portfolio_inquiry.html')


@app.route('/portfolio/g<int:gid>/s<int:sid>')
def view(gid, sid):
    portfolios = Decision.query.filter_by(
        group_id=gid, submission_id=sid).all()
    gname = Group.query.filter_by(group_id=gid).with_entities(
            Group.group_name).first().group_name
    if len(portfolios) == 0:
        return """
        <!doctype html>
        <title>Error</title>
        <h3>Error: Found no matching portfolio - try checking inputs</h3>
        <a href=".">Try Again</a>
        """
    return render_template('portfolio/portfolios.html', portfolios=portfolios, gname=gname)


@app.route('/portfolios_summary/')
def portfolios_summary():
    sid_gid_pairs = Decision.query.with_entities(Decision.group_id, Decision.submission_id).order_by(
        Decision.group_id, Decision.submission_id).distinct().all()
    submissions = []
    for pair in sid_gid_pairs:
        sid = pair.submission_id
        gid = pair.group_id
        gname = Group.query.filter_by(group_id=gid).with_entities(
            Group.group_name).first().group_name
        submissions.append((gid, gname, sid))
    return render_template('portfolio/portfolios_summary.html', submissions=submissions)
