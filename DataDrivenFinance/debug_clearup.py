from DataDrivenFinance import app
from DataDrivenFinance.databases import db, Performance, Rankings
from DataDrivenFinance.databases import TradingWeek, ActualRanks, ActualPrices


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
