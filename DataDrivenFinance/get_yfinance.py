from DataDrivenFinance import app
from DataDrivenFinance.databases import db, TradingWeek, ActualPrices, ActualRanks
import yfinance as yf
import pandas as pd
import numpy as np
from scipy.stats import rankdata


def calculateRanks(sid: int):
    symbols = ['ABBV', 'ACN', 'AEP', 'AIZ', 'ALLE', 'AMAT', 'AMP', 'AMZN', 'AVB', 'AVY', 'AXP',
                'BDX', 'BF-B', 'BMY', 'BR', 'CARR', 'CDW', 'CE', 'CHTR', 'CNC', 'CNP', 'COP', 'CTAS',
                'CZR', 'DG', 'DPZ', 'DRE', 'DXC', 'META', 'FTV', 'GOOG', 'GPC', 'HIG', 'HST', 'JPM',
                'KR', 'OGN', 'PG', 'PPL', 'PRU', 'PYPL', 'RE', 'ROL', 'ROST', 'UNH', 'URI', 'V', 'VRSK',
                'WRK', 'XOM', 'IVV', 'IWM', 'EWU', 'EWG', 'EWL', 'EWQ', 'IEUS', 'EWJ', 'EWT', 'MCHI',
                'INDA', 'EWY', 'EWA', 'EWH', 'EWZ', 'EWC', 'IEMG', 'LQD', 'HYG', 'SHY', 'IEF', 'TLT',
                'SEGA.L', 'IEAA.L', 'HIGH.L', 'JPEA.L', 'IAU', 'SLV', 'GSG', 'REET', 'ICLN', 'IXN',
                'IGF', 'IUVL.L', 'IUMO.L', 'SPMV.L', 'IEVL.L', 'IEFM.L', 'MVEU.L', 'XLK', 'XLF', 'XLV',
                'XLE', 'XLY', 'XLI', 'XLC', 'XLU', 'XLP', 'XLB', 'VXX', 'BTC-USD', 'ETH-USD', 'BNB-USD',
                'ADA-USD', 'XRP-USD', 'SOL-USD', 'DOGE-USD', 'DOT-USD', 'SHIB-USD', 'AVAX-USD']

    trading_week = TradingWeek.query.filter_by(submission_id=sid).all()
    if not trading_week:
        raise ValueError("Trading Week not defined")
    start_date = trading_week[0].start_day
    end_date = trading_week[0].end_day

    dfs = []
    for s in symbols:
        data = yf.download(s, start=start_date, end=end_date, progress=False)
        df = data.reset_index()[['Date', 'Adj Close']]
        df['Date'] = pd.to_datetime(df['Date'])
        df['symbol'] = s
        df = df.rename(columns={'Adj Close': 'price', 'Date': 'date'})
        df = df[['symbol', 'date', 'price']]
        dfs.append(df)

    assets_df = pd.concat(dfs)
    assets_df.reset_index(drop=True, inplace=True)
    assets_df = assets_df.pivot_table(
        values='price', index='symbol', columns='date')
    assets_df = assets_df.iloc[:, [0] +
                                list(range(3, min(len(assets_df.columns), 7)))]
    assets_df = assets_df.sort_index()

    prices = assets_df.to_numpy()
    ActualPricesList = []
    for i, row in enumerate(prices):
        ActualPricesList.append(ActualPrices(submission_id=sid, symbol=assets_df.index[i],
                                                price_day1=row[0], price_day2=row[1], price_day3=row[2],
                                                price_day4=row[3], price_day5=row[4]))

    for price in ActualPricesList:
        try:
            db.session.add(price)
            db.session.commit()
        except:
            return "Error when adding closing price to database"
            
    idx = (rankdata(prices[:, -1]/prices[:, 0], method='ordinal')-1)//(110//5)
    actual_ranks = np.zeros((110, 5))
    for i in range(110):
        actual_ranks[i, idx[i]] = 1

    ActualRanksList = []
    for i, row in enumerate(actual_ranks):
        ActualRanksList.append(ActualRanks(submission_id=sid, symbol=assets_df.index[i],
                                           rank1=row[0], rank2=row[1], rank3=row[2],
                                           rank4=row[3], rank5=row[4]))

    for rank in ActualRanksList:
        try:
            db.session.add(rank)
            db.session.commit()
        except:
            return "Error when adding ranks to database"
