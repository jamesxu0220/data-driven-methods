from DataDrivenFinance import app
from DataDrivenFinance.databases import Decision
from flask import request, render_template


@app.route('/portfolios/', methods=['POST', 'GET'])
def portfolios():
    if request.method == 'POST':
        gid = request.form['group_id']
        sid = request.form['submission_id']
        portfolios = Decision.query.filter_by(
            group_id=gid).filter_by(submission_id=sid).all()
        if len(portfolios) == 0:
            return """
            <!doctype html>
            <title>Error</title>
            <h3>Error: Found no matching portfolio - try checking inputs</h3>
            <a href=".">Try Again</a>
            """
        return render_template('portfolio/portfolios.html', portfolios=portfolios)
    else:
        return render_template('portfolio/portfolio_inquiry.html')
