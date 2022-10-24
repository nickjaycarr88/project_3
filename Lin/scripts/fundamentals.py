import yfinance as yf
import pandas as pd
import scripts.plotlylayout as ply



def get_dividends(ticker):

    stock = yf.Ticker(ticker)

    ## Dividends

    dividends = stock.history(period='max')['Dividends']
    dividends = pd.DataFrame(dividends).reset_index()
    dividends = dividends.loc[dividends['Dividends']>0]
    dividends

    return ply.create_plotly_bar(dividends)


def get_cash(ticker):

    stock = yf.Ticker(ticker)

    ## Cash
    Cash = stock.get_balance_sheet()
    Cash = Cash.T
    Cash = Cash[['Cash']]
    Cash.index.name = 'date'
    Cash = Cash.reset_index()
   

    return ply.create_plotly_line(Cash)


def get_AL(ticker):

    stock = yf.Ticker(ticker)

    ## Asset/Liability
    AL = stock.get_balance_sheet()
    AL = AL.T
    AL = AL[['Total Assets','Total Current Assets','Total Liab','Total Current Liabilities']]
    AL.index.name = 'date'
    AL['Total Non-Current Assets']=AL[['Total Assets','Total Current Assets']].apply(lambda x:x['Total Assets']-x['Total Current Assets'],axis=1)
    AL['Total Non-Current Liabilities']=AL[['Total Liab','Total Current Liabilities']].apply(lambda x:x['Total Liab']-x['Total Current Liabilities'],axis=1)
    AL = AL.drop(['Total Assets','Total Liab'],axis=1)
   

    return ply.create_plotly_pie(AL)  ## Date is latest to past 

