import dash
from app import app
from dash.dependencies import Input, Output

import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
# import plotly.graph_ as go
import pandas as pd
import os

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

def create_figure(name,df,xCol,yCol):
    fig = px.line(  df,          x=xCol, y=yCol,
                                    title=f'{name} Chart',
                                  )
    return fig


@app.callback(Output('stockChart', 'figure'), 
              [Input('dropdown', 'value'),
              Input('smaDropdown', 'value'),
              Input('start_date', 'value'),
              Input('end_date', 'value')])
def update_figure(selected_value,sma_value,start_date,end_date):
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
    fig = create_figure(selected_value,df,'timestamp',yCol)

    return fig

table_header = dbc.Row(
  [dbc.Row([html.Div(dp,className="col-3"),
  html.Div(sma,className="col"),
  dbc.Label("Start date",className="col"),
  dbc.Input(type="date",id="start_date",className="col"),
  dbc.Label("End date",className="col "),
  dbc.Input(type="date",id="end_date",className="col")
  ]),
  dbc.Row([strategyDropdown,
  dbc.Button("trade",id="strategy_trade", className="btn-primary btn-sm")])
  ]

)

layout = dbc.Card([dbc.CardHeader(table_header),dbc.CardBody(g)], outline=True)