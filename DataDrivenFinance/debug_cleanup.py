from DataDrivenFinance import app
from DataDrivenFinance.databases import db, Performance, Rankings
from DataDrivenFinance.databases import TradingWeek, ActualRanks, ActualPrices
from DataDrivenFinance.databases import Group, Decision
from flask import render_template


@app.route('/debug/test')
def debug_test():
    test = 1029
    return render_template('debug/debug_test.html', test=test)


@app.route('/debug/cleanup/evaluations')
def debug_cleanup_evaluations():
    for a in Performance.query.all():
        db.session.delete(a)
    for a in Rankings.query.all():
        db.session.delete(a)
    for a in ActualRanks.query.all():
        db.session.delete(a)
    for a in ActualPrices.query.all():
        db.session.delete(a)
    db.session.commit()
    return render_template('debug/debug_cleanup.html')


@app.route('/debug/cleanup/tradingweeks')
def debug_cleanup_tradingweeks():
    for a in TradingWeek.query.all():
        db.session.delete(a)
    db.session.commit()
    return render_template('debug/debug_cleanup.html')


@app.route('/debug/cleanup/portfolios')
def debug_cleanup_portfolios():
    for a in Decision.query.all():
        db.session.delete(a)
    db.session.commit()
    return render_template('debug/debug_cleanup.html')


@app.route('/debug/cleanup/groups')
def debug_cleanup_groups():
    for a in Group.query.all():
        db.session.delete(a)
    db.session.commit()
    return render_template('debug/debug_cleanup.html')


@app.route('/debug/cleanup/everything')
def debug_cleanup_everything():
    db.drop_all()
    db.create_all()
    db.session.commit()
    return render_template('debug/debug_cleanup.html')