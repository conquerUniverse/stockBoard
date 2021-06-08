import dash
from app import app
from dash.dependencies import Input, Output,State
from dash.exceptions import PreventUpdate
from dash import callback_context as ctx

import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
import importlib

from tradingStrategies.backtest import BackTest

scriptPath = "tradingStrategies/scripts"

def getScriptsName():
  names = [i[:-3] for i in os.listdir(scriptPath) if i[-3:] == '.py' and i != '__init__.py']
  return names


g = dcc.Graph(id='stockChart')

stockDataAvailable = [{'label':i.split('.')[0],'value':i.split('.')[0]} for i in 
os.listdir("./data/stockData/daily") if i.split('.')[1] == 'csv']

strategyAvailable = [{'label':i.split('.')[0],'value':i.split('.')[0]} for i in getScriptsName()]
# print(stockDataAvailable)

# global Variable
df = None 

strategyDropdown = dcc.Dropdown(id='strategy_id', options=strategyAvailable,
            value = None, style={ 'color': 'black',
                                      'background-color': 'white',
                                    } )

dp = dcc.Dropdown(id='dropdown', options=stockDataAvailable,
            value = 'RELIANCE', style=
                                    { 
                                      'color': 'black',
                                      'background-color': 'white',
                                    } )
sma_list = [5,10,20,46,50,100]
sma = dcc.Dropdown(multi=True,id="smaDropdown",
  options = [{'label':i,'value':i} for i in sma_list],className="w-100 ")

def create_figure(name,df,xCol,yCol,**kwargs):
    fig = go.Figure(data=[go.Candlestick(x=df[xCol],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                # title=f'{name} Chart'
                ) ])
    # fig = px.line( df,x=xCol, y=yCol,
    #  title=f'{name} Chart',**kwargs
                                    # )


    # fig  = go.Figure(data=[go.Line( x=df[xCol], y=df[[yCol]],
    #                                   # title=f'{name} Chart',**kwargs
    #                                 )])
    # if yCol is not None and len(yCol) > 0 :
    #   fig.add_trace(go.scatter.Line( x=df[xCol], y=df[yCol],
    #                                   # title=f'{name} Chart',**kwargs
    #                                 ))
    fig.update_layout(title =f'{name} Chart', margin=dict(l=0,r=0,b=0))
    fig.update_yaxes(fixedrange=False)
    fig.update_xaxes(rangeslider_visible=False,
    # rangebreaks=[
    #     dict(bounds=["sun", "mon"])],
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
        ))
    return fig


@app.callback(Output('stockChart', 'figure'), 
              [Input('dropdown', 'value'),
              Input('smaDropdown', 'value'),
              Input('start_date', 'value'),
              Input('end_date', 'value'),
              Input('strategy_trade', 'n_clicks')],
              State('strategy_id','value'))
def update_figure(selected_value,sma_value,start_date,end_date,strategyButton,strategyName):
    # print(sma_value)
    global df
    df = pd.read_csv(f"./data/stockData/daily/{selected_value}.csv")
    if start_date is not None:
      df = df[df.timestamp >= start_date]
    else:
      df = df[df.timestamp >= '2020-06-05']
    if end_date is not None:
      df = df[df.timestamp <= end_date]
    yCol = ['close']
    # yCol = []
    if sma_value is not None:
      for smaV in sma_value:
        df["sma-"+str(smaV)] = df["close"].rolling(window=smaV).mean()
        yCol.append('sma-'+str(smaV))

    # if trade strategy is selected
    changed = ctx.triggered[0]['prop_id'].split('.')[0]
    if 'strategy_trade' in changed:
      if strategyName == None:
        raise PreventUpdate # when user has not selected the Strategy name

      module = importlib.import_module('tradingStrategies.scripts.'+strategyName)
      scriptFunction = module.run
      df.reset_index(drop=True,inplace=True)
      df_otpt = pd.DataFrame(scriptFunction(df))
      df_temp = pd.merge(df,df_otpt,how='left',on='timestamp')
      # df_temp = pd.concat([df,df_otpt],axis=1)z
      
      fig = create_figure(selected_value,df_temp,'timestamp',yCol   )
      
      buyData = df_temp[df_temp['actions']=='buy']
      fig.add_trace(go.Scatter(name='buy',mode='markers',x=buyData['timestamp'],y=buyData['close'],
      marker={'size':10}, marker_color='blue'))

      sellData = df_temp[df_temp['actions']=='sell']
      
      fig.add_trace(go.Scatter(name='sell',mode='markers',x=sellData['timestamp'],y=sellData['close'],
      marker={'size':10}, marker_color='yellow'))
      return fig

    else:
      fig = create_figure(selected_value,df,'timestamp',yCol)

    return fig

@app.callback(
  Output("analysisResult","children"),
  Input("strategy_trade","n_clicks"),
  [State("strategy_id","value"),State('dropdown', 'value')]
)
def getAnalysisResult(_,strategyName,stockName):
  if  _ == None or strategyName == None or stockName == None:
    print("prevent updattes")
    raise PreventUpdate
  # get Analysis of Stock based on strategy

  global df # using the global df
  
  bt = BackTest("data/stockData/daily/")
  res = bt.backtest(strategyName,df)
  # print("backtesting the strategy",res)
  
  colNames = ['profitPercent','stockGrowth','totalNetWorth','totalInvestment','NumberOfTrades']
  vw = dbc.Row([
    dbc.Col([dbc.Row(i,className="col"),dbc.Row(round(res[i],3),className="col")] , 
    className="col-2 col-xs-6 overflow-auto") 
    for i in colNames 
  ],className="w-100 border border-success mt-1")
  
  # print(res)
  return vw

table_header = dbc.Col(
  [dbc.Row([html.Div(dp,className="col-2  p-0 mr-2"),
  html.Div(sma,className="col-2  p-0 mr-2"),
  dbc.Label("Start date",className="col  p-0"),
  dbc.Input(type="date",id="start_date",className="col  "),
  dbc.Label("End date",className="col "),
  dbc.Input(type="date",id="end_date",className="col ")
  ]),
  dbc.Row([
    html.Span("Strategy" ,className="col-2 h5 col-xs-2 w-auto"),
    html.Div(strategyDropdown,className="col-2 mt-1 col-xs-5 w-auto"),
  dbc.Button("trade",id="strategy_trade", className="btn-primary btn-sm col-1 mt-1 col-xs-5 w-auto"),
  
  ]),
  html.Div(id="analysisResult",className="row")
  
  ]
# ,className="col-12"
)

layout = dbc.Card([dbc.CardHeader(table_header,className="border border-danger"),dbc.CardBody(g)], outline=True)