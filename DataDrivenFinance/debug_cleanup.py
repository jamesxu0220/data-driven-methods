from DataDrivenFinance import app
from DataDrivenFinance.databases import db, Performance, Rankings
from DataDrivenFinance.databases import TradingWeek, ActualRanks, ActualPrices
from flask import render_template


@app.route('/debug/cleanup')
def debug_cleanup():
    for a in Performance.query.all():
        db.session.delete(a)
    for a in Rankings.query.all():
        db.session.delete(a)
    for a in TradingWeek.query.all():
        db.session.delete(a)
    for a in ActualRanks.query.all():
        db.session.delete(a)
    for a in ActualPrices.query.all():
        db.session.delete(a)
    db.session.commit()

    return render_template('debug/debug_cleanup.html')


@app.route('/debug/test')
def debug_test():
    test = 1029
    return render_template('debug/debug_test.html', test=test)
