
from flask import Flask, render_template, request, url_for, redirect
from bs4 import BeautifulSoup as bs
import requests as req
import yfinance as yf
import plotly
import json
import scripts.fundamentals as funds ## fundamentals.py
import scripts.plotlylayout as ply ## plotlylayout.py
import os
import numpy as np
from pytrends.request import TrendReq
from wordcloud import WordCloud
from PIL import Image
import matplotlib.pyplot as plt
import datetime as dt
import pymongo 
from bson.objectid import ObjectId





app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def index():
 
    # # url for scraping data from businesstodays news
    newsurl = "https://www.businesstoday.in/latest/economy"
    
    webpage = req.get(newsurl)  # parse a request for scraping the url
    soup = bs(webpage.content, "lxml")
    results = soup.find_all('a',href=True)
    
    posts=[] # Wiill be parsed to index.html
    
    for result in results:
      if(str(type(result.string)) == "<class 'bs4.element.NavigableString'>"
      and len(result.string) > 35):
  
        if len(posts)<10:
            posts.append(result) 

    
    # Generate wordclooud

    pytrend = TrendReq(hl='en-US', tz=-480)  # initialise TrendReq

    kw_list = ["asx"]

    pytrend.build_payload(kw_list, cat=0, timeframe='now 7-d', geo='AU', gprop='')

    trends = pytrend.related_queries() # Build pytrends payload and query

    kwTop = trends[kw_list[0]]["top"] # kwTop to store the results of top trends similar to the keyword.

    textList = []

    textList = (' '.join(kwTop["query"].to_list())) # textList to store kwTop lists as a string relating to key keyword.

    bg_mask = np.array(Image.open(os.path.join(os.getcwd(), "Resources/wordCloudBase.png"))) # Create mask for wordCloud 

    wc = WordCloud(      # Create wordCloud container storing parameters
        width = 600, 
        height = 1000,    
        background_color = 'white',
        mask = bg_mask,
        max_words = 100,
        max_font_size = 150,
        min_font_size = 15,
        contour_width = 2, 
        contour_color = 'gold'
    )
    nowDate = dt.datetime.now().date()
    wc.generate_from_text(textList)
    plt.switch_backend('Agg') #To run in the backend and output png
    plt.figure()
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(f'static/images/{nowDate}.png',bbox_inches='tight',pad_inches=0.0)
 
    # Using render_template method to target the webpage with given data
    return render_template('index.html', posts = posts, url = f'static/images/{nowDate}.png')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/dashboard')
def dashboard():
    try:
        stockcode1=request.args['stockcode'] # 'stockcode' is posted from index.html when users key in stock code and click "SUMMIT"

        adjustedName = f'{stockcode1.upper()}.AX' #Standarize stock code to match yfinance requirement

        # dividend plot
        dividend = funds.get_dividends(adjustedName)   # Parsing 'adjustedName' to fundamentals.py, then plotlylayout.py, then return back
        plotlyplot_dividend = json.dumps(dividend, cls=plotly.utils.PlotlyJSONEncoder) # To display the plot as html we have to put into a json format.

        #cash plot
        cash = funds.get_cash(adjustedName)  # Parsing 'adjustedName' to fundamentals.py, then plotlylayout.py, then return back

        plotlyplot_cash = json.dumps(cash, cls=plotly.utils.PlotlyJSONEncoder) # To display the plot as html we have to put into a json format.

        # Asset/Liabilities plot
        AL = funds.get_AL(adjustedName)   # Parsing 'adjustedName' to fundamentals.py, then plotlylayout.py, then return back

        plotlyplot_AL = json.dumps(AL, cls=plotly.utils.PlotlyJSONEncoder) # To display the plot as html we have to put into a json format.
        
    
        # Historic Price plot
        histPrice = ply.create_plotly_hp(adjustedName)   # Parsing 'adjustedName' to fundamentals.py, then plotlylayout.py, then return back

        plotlyplot_histPrice = json.dumps(histPrice, cls=plotly.utils.PlotlyJSONEncoder) # To display the plot as html we have to put into a json format.
        
        
        # Stock Infomation
        stockInfo = yf.Ticker(adjustedName).info['longBusinessSummary']

        #Today stock price/profit or lose

        lastRecentPrice = yf.Ticker(adjustedName).history()['Close'][-1]

        perivousPrice = yf.Ticker(adjustedName).history()['Close'][-2]

        lastRecentPrice =round(lastRecentPrice,2)

        perivousPrice  =round(perivousPrice ,2)

        rate = round(((lastRecentPrice-perivousPrice)/perivousPrice*100),2)

        # Using render_template method to target the webpage with given data
        return render_template('dashboard.html',adjustedName = adjustedName,
                                                plotlyplot_dividend = plotlyplot_dividend, 
                                                plotlyplot_cash = plotlyplot_cash, 
                                                plotlyplot_AL = plotlyplot_AL,
                                                stockInfo = stockInfo,
                                                plotlyplot_histPrice = plotlyplot_histPrice,
                                                lastRecentPrice = lastRecentPrice,
                                                rate = rate)
    except:
        # The dashboard has 5 parts of historic data
        # If one of them of the stock which a user would like to search cannot be called from yfinance
        # It will direct to error page and request the user to search another stock
        return render_template('error.html')

@app.post('/<id>/addToList/')  
def addToList(id):
    
    # Create a database in MongoDB
    conn = 'mongodb://localhost:27017'

    client = pymongo.MongoClient(conn) #Connect to MongoDB
   
    db = client.flask_db #Connect to flask_db

    stocks = db.stocks 

    # Calling data from yfianace about what we want to store in MongoDB
    lastRecentPrice = yf.Ticker(id).history()['Close'][-1]

    lastRecentPrice =round(lastRecentPrice,2) #round the price

    stockPirce = yf.Ticker(id).history(period="1y")['Close'] #Get the past 1 year stock price

    max52 =round(max(stockPirce),2)
    
    min52 =round(min(stockPirce),2)

    nowDate = dt.datetime.now().strftime("%d/%m/%Y") # Parse time data type to string type to mark search day

    stocks.insert_one({'StockCode': id, 'Price': lastRecentPrice, 'Weeks52High':max52, 'Weeks52Low':min52, 'LastSearchedDate': nowDate})

    client.close()

    # Stay at the same web page
    return redirect(url_for('mylist'))


@app.route('/mylist')

def mylist():

    conn = 'mongodb://localhost:27017'

    client = pymongo.MongoClient(conn)
   
    db = client.flask_db

    stocks = db.stocks

    all_stocks= stocks.find()

    client.close()

    # Using render_template method to target the webpage with given data
    return render_template('mylist.html', stocks=all_stocks)



@app.post('/<id>/delete/') # Delect stock user not interested
def delete(id):
    
    conn = 'mongodb://localhost:27017'

    client = pymongo.MongoClient(conn)
   
    db = client.flask_db

    stocks = db.stocks

    stocks.delete_one({"_id": ObjectId(id)})
    # stay at the same page
    return redirect(url_for('mylist'))



@app.post('/<checkstock>/search/')# Create search function let user follow listed stock's recently performance
def search(checkstock):

    adjustedName =checkstock #'checkstock' is parsed from 'have a look' event in mylist.html

    # dividend plot
    dividend = funds.get_dividends(adjustedName)  # Parsing 'adjustedName' to fundamentals.py, then plotlylayout.py, then return back

    plotlyplot_dividend = json.dumps(dividend, cls=plotly.utils.PlotlyJSONEncoder) # To display the plot as html we have to put into a json format.

    #cash plot
    cash = funds.get_cash(adjustedName)  # Parsing 'adjustedName' to fundamentals.py, then plotlylayout.py, then return back

    plotlyplot_cash = json.dumps(cash, cls=plotly.utils.PlotlyJSONEncoder) # To display the plot as html we have to put into a json format.

    # Asset/Liabilities plot
    AL = funds.get_AL(adjustedName) # Parsing 'adjustedName' to fundamentals.py, then plotlylayout.py, then return back

    plotlyplot_AL = json.dumps(AL, cls=plotly.utils.PlotlyJSONEncoder)## To display the plot as html we have to put into a json format.
    
   
    # Historic Price plot
    histPrice = ply.create_plotly_hp(adjustedName) # Parsing 'adjustedName' to fundamentals.py, then plotlylayout.py, then return back

    plotlyplot_histPrice = json.dumps(histPrice, cls=plotly.utils.PlotlyJSONEncoder) # To display the plot as html we have to put into a json format.
    
    
    # Stock Infomation
    stockInfo = yf.Ticker(adjustedName).info['longBusinessSummary']

   
    #Today stock price/profit or lose

    lastRecentPrice = yf.Ticker(adjustedName).history()['Close'][-1]

    perivousPrice = yf.Ticker(adjustedName).history()['Close'][-2]

    lastRecentPrice =round(lastRecentPrice,2)

    perivousPrice  =round(perivousPrice ,2)

    rate = round(((lastRecentPrice-perivousPrice)/perivousPrice*100),2)
    # Using render_template method to target the webpage with given data    
    return render_template('stockholder.html',adjustedName = adjustedName,
                                            plotlyplot_dividend = plotlyplot_dividend, 
                                            plotlyplot_cash = plotlyplot_cash, 
                                            plotlyplot_AL = plotlyplot_AL,
                                            stockInfo = stockInfo,
                                            plotlyplot_histPrice = plotlyplot_histPrice,
                                            lastRecentPrice = lastRecentPrice,
                                            rate = rate)
    
    
if __name__ == '__main__':
    app.run(debug=True)