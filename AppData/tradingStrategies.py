import dash
from app import app
from flask import render_template
import dash_bootstrap_components as dbc
import dash_html_components as html
import os
import numpy as np

import dash_core_components as dcc
from dash import callback_context as ctx
from dash.dependencies import Input, Output, State
# ctx = dash.callback_context
pageHeader = dbc.CardHeader("Trading Strategies")

path = "tradingStrategies/scripts/"
# get scripts name
scripts_name = [i.split('.')[0] for i in os.listdir(path)]

# border color from bootstrap
border_color = ["border-secondary","border-success","border-dark","border-warning","border-primary"]

popUp =  dbc.Modal(
            [
                dbc.ModalHeader("Header",id="modalHeader"),
                dbc.ModalBody(dcc.Markdown(id="markdownCode",highlight_config={'theme':'dark'},
                ) ,id="modalBody", className="overflow-auto"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close", className="ml-auto")
                ),
            ],
            id="modal",
        )

# dynamically generate the strategies code
pageBody = dbc.CardBody([dbc.Row([
    dbc.Col(dbc.Label(i)),
    dbc.Col(dbc.Button("Score",id=i,className="btn float-md-right ")),
    dbc.Col(dbc.Button("Show Code", id=i+"_code",className="ml-0 btn  float-md-right"),)
]
    ,justify="around",className="border mb-1 "+np.random.choice(border_color)) for i in scripts_name])

layout = dbc.Card([pageHeader,pageBody,popUp],outline=True)


    
@app.callback(
    [Output("modalHeader", "children"),
    Output("markdownCode", "children"),
    Output("modal", "is_open")],
    [Input("close", "n_clicks")]+
    [Input(i+"_code", "n_clicks") for i in scripts_name],
    State("modal", "is_open")
)
def toggle_modal(is_open,*args):
    # print("button clicked")
    changed = ctx.triggered[0]['prop_id'].split('.')[0]
    if 'close' in changed or changed == '':
        return '','',False
    name = changed.replace('_code','')
    code = "```python\n"+open(os.path.join(path,name+'.py')).read()+"\n```"

    return name,code,True


    # code = open(os.path.join(path,)

    # if n1 or n2:
    #     return not is_open
    # return is_open