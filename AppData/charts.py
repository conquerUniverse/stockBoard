import dash
from app import app
from dash.dependencies import Input, Output,State

from dash import callback_context as ctx

import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
import importlib

scriptPath = "tradingStrategies/scripts"

def getScriptsName():
  names = [i[:-3] for i in os.listdir(scriptPath) if i[-3:] == '.py' and i != '__init__.py']
  return names


g = dcc.Graph(id='stockChart')

stockDataAvailable = [{'label':i.split('.')[0],'value':i.split('.')[0]} for i in 
os.listdir("./data/stockData/daily") if i.split('.')[1] == 'csv']

strategyAvailable = [{'label':i.split('.')[0],'value':i.split('.')[0]} for i in getScriptsName()]
# print(stockDataAvailable)
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
  options = [{'label':i,'value':i} for i in sma_list])

def create_figure(name,df,xCol,yCol,**kwargs):
    fig = px.line(  df,x=xCol, y=yCol,
                                    title=f'{name} Chart',**kwargs
                                  )
    return fig


@app.callback(Output('stockChart', 'figure'), 
              [Input('dropdown', 'value'),
              Input('smaDropdown', 'value'),
              Input('start_date', 'value'),
              Input('end_date', 'value'),
              Input('strategy_trade', 'n_clicks')],
              State('strategy_id','value'))
def update_figure(selected_value,sma_value,start_date,end_date,strategyButton,strategyName):
    print(sma_value)
    df = pd.read_csv(f"./data/stockData/daily/{selected_value}.csv")
    if start_date is not None:
      df = df[df.timestamp >= start_date]
    if end_date is not None:
      df = df[df.timestamp <= end_date]
    yCol = ['close']
    if sma_value is not None:
      for smaV in sma_value:
        df["sma-"+str(smaV)] = df["close"].rolling(window=smaV).mean()
        yCol.append('sma-'+str(smaV))

    # if trade strategy is selected
    changed = ctx.triggered[0]['prop_id'].split('.')[0]
    if 'strategy_trade' in changed:
      print('trading with ',strategyName)
      module = importlib.import_module('tradingStrategies.scripts.'+strategyName)
      scriptFunction = module.run
      # print("func loadede")
      df_otpt = pd.DataFrame(scriptFunction(df))
      df = pd.concat([df,df_otpt],axis=1)
      fig = create_figure(selected_value,df,'timestamp',yCol   )
      print("fig ready")
      buyData = df[df['actions']=='buy']
      fig.add_trace(go.Scatter(name='buy',mode='markers',x=buyData['timestamp'],y=buyData['close'],
      marker={'size':10}))

      sellData = df[df['actions']=='sell']
      fig.add_trace(go.Scatter(name='sell',mode='markers',x=sellData['timestamp'],y=sellData['close'],
      marker={'size':10}))
      # fig = go.Figure(data = fig.data+fig2.data)

    else:
      fig = create_figure(selected_value,df,'timestamp',yCol)

    return fig

table_header = dbc.Col(
  [dbc.Row([html.Div(dp,className="col-2"),
  html.Div(sma,className="col-2"),
  dbc.Label("Start date",className="col"),
  dbc.Input(type="date",id="start_date",className="col"),
  dbc.Label("End date",className="col "),
  dbc.Input(type="date",id="end_date",className="col")
  ]),
  dbc.Row([
    html.Span("Strategy" ,className="col-2 h5 "),
    html.Div(strategyDropdown,className="col-2 mt-1"),
  dbc.Button("trade",id="strategy_trade", className="btn-primary btn-sm col-1 mt-1")])
  ]
,className="col-12"
)

layout = dbc.Card([dbc.CardHeader(table_header),dbc.CardBody(g)], outline=True)