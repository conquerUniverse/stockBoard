import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash.dependencies import Input, Output, State

# from app.app_init import app
from scripts.StockBoard import StockBoard
from scripts.StockData import StockData

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


def getLayout(user):
    sd = StockData(username=user) # default value 
    sd.load()
    stock = StockBoard(sd)
    layout = dbc.Card([
        dbc.CardHeader("Current Holdings"),
        dbc.CardBody(tableView(stock.getCurrHoldings()))
    ],
    outline = True
        )

    return layout