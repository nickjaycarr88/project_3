import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf


def create_plotly_bar(data):

    fig_dividend = px.bar(data,
                  x="Date",
                  y="Dividends",
                  title="Dividends",
                  barmode='group'
                  )
   
    fig_dividend.update_layout(title_font=dict(color='navy',family = 'Arial Bold',size=26),yaxis_tickprefix='$')
    return fig_dividend

def create_plotly_line(data):

    fig_cash = px.line(data,
                  x="date",
                  y="Cash",
                  title="Cash"
                    )
    
    fig_cash.update_layout(title_font=dict(color='navy',family = 'Arial Bold',size=26),yaxis_tickprefix='$')

    return fig_cash


def create_plotly_pie(data):

    #  Date is latest to past, so we reverse
    AL1=data.iloc[3,:] #Return series
    AL2=data.iloc[2,:]
    AL3=data.iloc[1,:]
    AL4=data.iloc[0,:]

    AL1 = AL1.tolist()
    AL2 = AL2.tolist()
    AL3 = AL3.tolist()
    AL4 = AL4.tolist()
 

    labels = ['Total Current Assets','Total Current Liabilities','Total Non-Current Assets','Total Non-Current Liabilities']
    specs = [[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}, {'type':'domain'}]]
    # Create a 1*4 subplots for comparing the past four years of companies' performances.
    fig_AL = make_subplots(rows=1, cols=4, specs=specs,subplot_titles = data.index.strftime("%Y/%m/%d"))

    fig_AL.add_trace(go.Pie(labels=labels, values= AL1, scalegroup='one'), 1, 1)
    fig_AL.add_trace(go.Pie(labels=labels, values= AL2, scalegroup='one'), 1, 2)
    fig_AL.add_trace(go.Pie(labels=labels, values= AL3, scalegroup='one'), 1, 3)
    fig_AL.add_trace(go.Pie(labels=labels, values= AL4, scalegroup='one'), 1, 4)

    fig_AL.update_layout(title_text='Asset/Liabilities(Based On Amount)' ,title_font=dict(color='navy',family = 'Arial Bold',size=26 ))

    return fig_AL



def create_plotly_hp(ticker):


    stock = yf.Ticker(ticker)
    
    hist3M = stock.history(period='3mo')
    hist3M= hist3M[['Close']].reset_index() 

    hist6M = stock.history(period='6mo')
    hist6M= hist6M[['Close']].reset_index() 
    
    hist1Y = stock.history(period='1y')
    hist1Y= hist1Y[['Close']].reset_index() 
    
    hist3Y= stock.history(period='3y')
    hist3Y= hist3Y[['Close']].reset_index() 

    hist5Y = stock.history(period='5y')
    hist5Y= hist5Y[['Close']].reset_index() 
    


    # Initialize figure
    fig_histPrice = go.Figure()

    # Add Traces

    fig_histPrice.add_trace(
        go.Scatter(x=list(hist3M['Date']),
                y=list(hist3M['Close']),
                name="3 Months"))

    fig_histPrice.add_trace(
        go.Scatter(x=list(hist6M['Date']),
                y=list(hist6M['Close']),
                visible=False,
                name="6 Months"))

    fig_histPrice.add_trace(
        go.Scatter(x=list(hist1Y['Date']),
                y=list(hist3M['Close']),
                visible=False,
                name="1 Year"))

    fig_histPrice.add_trace(
        go.Scatter(x=list(hist3Y['Date']),
                y=list(hist3Y['Close']),
                visible=False,
                name="3 Years"))  

    fig_histPrice.add_trace(
        go.Scatter(x=list(hist5Y['Date']),
                y=list(hist5Y['Close']),
                visible=False,
                name="5 Years"))  

    # Create a drop down menu to let users to choose different time durations
    fig_histPrice.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=list([
                    dict(label="3 Months",
                        method="update",
                        args=[{"visible": [True, False, False, False, False]}]),
                    dict(label="6 Months",
                        method="update",
                        args=[{"visible": [False, True, False, False, False]}]),
                    dict(label="1 Year",
                        method="update",
                        args=[{"visible": [False, False, True, False, False]}]),
                    dict(label="3 Year",
                        method="update",
                        args=[{"visible": [False, False, False, True, False]}]),
                    dict(label="5 Year",
                        method="update",
                        args=[{"visible": [False, False, False, False, True]}])
                ])
            )
        ])

    fig_histPrice.update_layout(title_text="Historic Price", title_font=dict(color='navy',family = 'Arial Bold',size=26), yaxis_tickprefix='$' )

    return fig_histPrice
