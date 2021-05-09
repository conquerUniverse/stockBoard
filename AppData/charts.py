import dash
from app import app
from dash.dependencies import Input, Output

import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import pandas as pd
import os

g = dcc.Graph(id='stockChart')

stockDataAvailable = [{'label':i.split('.')[0],'value':i.split('.')[0]} for i in 
os.listdir("./data/stockData/daily") if i.split('.')[1] == 'csv']
# print(stockDataAvailable)

dp = dcc.Dropdown(id='dropdown', options=stockDataAvailable,
            value = 'RELIANCE', style=
                                    { 
                                      'color': 'black',
                                      'background-color': 'white',
                                    } )



def create_figure(name,df):
    data = go.Scatter(          x=df['timestamp'],
                                      y=df['close'],
                                      mode='lines'
                                  )
    layout = go.Layout(         title=f'{name} Chart',
                                      xaxis={'title':'Time-line'},
                                      yaxis={'title':'Value'},margin={'l':2,'r':5,'b':5}
                                    #   hovermode='closest'
                                   )
    fig = go.Figure(data=data, layout=layout)
    return fig

@app.callback(Output('stockChart', 'figure'), 
              [Input('dropdown', 'value'),
              Input('start_date', 'value'),
              Input('end_date', 'value')])
def update_figure(selected_value,start_date,end_date):
    print(start_date,end_date)
    df = pd.read_csv(f"./data/stockData/daily/{selected_value}.csv")
    if start_date is not None:
      df = df[df.timestamp >= start_date]
    if end_date is not None:
      df = df[df.timestamp <= end_date]
    fig = create_figure(selected_value,df)

    return fig

table_header = dbc.Row([html.Div(dp,className="col-4"),
  dbc.Label("Start date",className="col"),
  dbc.Input(type="date",id="start_date",className="col"),
  dbc.Label("End date",className="col w-1"),
  dbc.Input(type="date",id="end_date",className="col")
  ])

layout = dbc.Card([dbc.CardHeader(table_header),dbc.CardBody(g)], outline=True)