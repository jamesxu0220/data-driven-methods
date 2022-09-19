# FOR DEBUGGING ONLY
# FOR DEBUGGING ONLY
# FOR DEBUGGING ONLY

from DataDrivenFinance import app, get_yfinance
from DataDrivenFinance.databases import db, TradingWeek

@app.route('/test/get_ranks/')
def get_ranks_test():
    get_yfinance.calculateRanks(0)
    return "Success"


def set_new_week(sid, start_date, end_date):
    new_week = TradingWeek(
        submission_id=sid, start_day=start_date, end_day=end_date)
    db.session.add(new_week)
    db.session.commit()


@app.route('/test/set_week/')
def set_week_test():
    set_new_week(0, "2022-09-09", "2022-09-17")
    return "Success"