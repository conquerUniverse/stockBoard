import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash.dependencies import Input, Output, State

# from app.app_init import app
from scripts.StockBoard import StockBoard
from scripts.StockData import StockData

import plotly.express as px
import plotly.graph_objects as go

import pandas as pd

# username = "alvin369"

def tableView(data):

    var = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in data.columns],
    data=data.to_dict('records'),

    style_header = {
        'backgroundColor': 'rgb(40, 20, 100)',
        'color': 'white'
    }
    ,
    style_data_conditional=[{
        'if': {'column_id': ['Name','TotalCost','Amount']
        },
        'backgroundColor': 'rgb(10, 100, 30)',
        'color': 'white'
    }],

    style_data = {
        'backgroundColor': 'rgb(60, 50, 40)',
        'color': 'white'
    },

    style_cell_conditional=[
            {'if': {'column_id': 'title'},
            'width': '100px'},
            {'if': {'column_id': 'post'},
            'width': '200px'
            ,'height':'auto'},
        ],

    style_cell={
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'maxWidth': '1px',
            'textAlign':"center"
        }

    ,style_table={
    'maxHeight': '300px'
    ,'overflowY': 'auto'
    },
    )
    return dbc.Container(var)

def getOverviewData(sb):
    name_list = ["total Brokerage","total value invested","Demat Account Balance"]
    tb = round(sb.getTotalBrokerage(),3)
    iv = round(sb.getInvestedValue(),3)
    cb = sb.getCurrBalance()
    value_list = [tb,iv-cb,cb]
    li = []
    for i,j in zip(name_list,value_list):
        d = {}; d["name"] = i; d["value"] = j
        li.append(d)
    return pd.DataFrame(li),'name','value'

def getPieChart(df,name,value,**kwargs):
    data = [go.Pie(labels = df[name],values=df[value],hole=.5)]
    layout = go.Layout(title="Overview",paper_bgcolor = 'rgba(0,0,0,0)',
            plot_bgcolor = 'rgba(0,0,0,0)',font ={'color':'white'})
    fig = go.Figure(data = data,layout=layout,)
    # fig = px.pie(df,values=xCol,names=yCol,**kwargs)
    return fig

def getLayout(user):
    sd = StockData(username=user) # default value 
    sd.load()
    stock = StockBoard(sd)
    df_,name_,value_ = getOverviewData(stock)
    fig = getPieChart(df_,name_,value_)
    layout = dbc.Card([
        dbc.CardHeader("Current Holdings"),
        dbc.CardBody(
            dbc.Col([
            dbc.Row(tableView(stock.getCurrHoldings())),
            dbc.Container(dcc.Graph(id="overview_chart",figure=fig),className="row m-2 p-1")
            ]))
    ],
    outline = True
        )


    return layout