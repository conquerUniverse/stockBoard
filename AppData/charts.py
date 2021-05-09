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



def create_figure(name):
    df = pd.read_csv(f"./data/stockData/daily/{name}.csv")

    data = go.Scatter(          x=df['timestamp'],
                                      y=df['close'],
                                      mode='lines'
                                  )
    layout = go.Layout(         title=f'{name} Chart',
                                      xaxis={'title':'Time-line'},
                                      yaxis={'title':'Value'},
                                    #   hovermode='closest'
                                   )
    fig = go.Figure(data=data, layout=layout)
    return fig

@app.callback(Output('stockChart', 'figure'), 
              [Input('dropdown', 'value')])
def update_figure(selected_value):

    fig = create_figure(selected_value)
    return fig

layout = dbc.Card([dbc.CardHeader(dp),dbc.CardBody(g)], outline=True)