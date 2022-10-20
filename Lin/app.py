
from flask import Flask, render_template,request
from bs4 import BeautifulSoup as bs
import requests as req
import yfinance as yf
import pandas as pd
import datetime as dt
import plotly
import json
import scripts.fundamentals as funds ## fundamentals.py
import scripts.plotlylayout as ply ## plotlylayout.py

app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def index():
 
    url = "https://www.businesstoday.in/latest/economy"
    
    webpage = req.get(url)  # YOU CAN EVEN DIRECTLY PASTE THE URL IN THIS
    # HERE HTML PARSER IS ACTUALLY THE WHOLE HTML PAGE
    soup = bs(webpage.content, "lxml")
    results = soup.find_all('a',href=True)
    
    posts=[]
    
    for result in results:
      if(str(type(result.string)) == "<class 'bs4.element.NavigableString'>"
      and len(result.string) > 35):
  
        if len(posts)<10:
            posts.append(result)

    
    return render_template('index.html', posts = posts)



@app.route('/dashboard')
def dashboard():
    
    stockcode1=request.args['stockcode']

    adjustName = f'{stockcode1.upper()}.AX'

    # dividend plot
    dividend = funds.get_dividends(adjustName)   ## This gets the data and create a plot

    plotlyplot_dividend = json.dumps(dividend, cls=plotly.utils.PlotlyJSONEncoder)## To display the plot as html we have to put into a json            ## format.

    #cash plot
    cash = funds.get_cash(adjustName)   ## This gets the data and create a plot

    plotlyplot_cash = json.dumps(cash, cls=plotly.utils.PlotlyJSONEncoder)## To display the plot as html we have to put into a json            ## format.

    # Asset/Liabilities plot
    AL = funds.get_AL(adjustName)   ## This gets the data and create a plot

    plotlyplot_AL = json.dumps(AL, cls=plotly.utils.PlotlyJSONEncoder)## To display the plot as html we have to put into a json  
    
   
    # Historic Price plot
    histPrice = ply.create_plotly_hp(adjustName)   ## This gets the data and create a plot

    plotlyplot_histPrice = json.dumps(histPrice, cls=plotly.utils.PlotlyJSONEncoder)## To display the plot as html we have to put into a json  
    
    
    # Stock Infomation
    stockInfo = yf.Ticker(adjustName).info['longBusinessSummary']

    #Today stock price
    price =yf.Ticker(adjustName).history(period='2d')['Close'][0]
    yesterdayPrice =yf.Ticker(adjustName).history(period='2d')['Close'][1]
    rate = round(((price-yesterdayPrice)/yesterdayPrice*100),2)
    
    price = f'${round(price,2)}'  #ADD dollar sign
    

    return render_template('dashboard.html',adjustName = adjustName,
                                            plotlyplot_dividend = plotlyplot_dividend, 
                                            plotlyplot_cash = plotlyplot_cash, 
                                            plotlyplot_AL = plotlyplot_AL,
                                            stockInfo = stockInfo,
                                            plotlyplot_histPrice = plotlyplot_histPrice,
                                            price = price,
                                            rate = rate)


if __name__ == '__main__':
    app.run(debug=True)