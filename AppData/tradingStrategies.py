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
from dash_table import DataTable
import pandas as pd
from dash.exceptions import PreventUpdate

from tradingStrategies.backtestFast import BackTest

path = "tradingStrategies/scripts/"
path_results = "tradingStrategies/results/"

# get scripts name
scripts_name = [
    i[:-3] for i in os.listdir(path) if i[-3:] == ".py" and i != "__init__.py"
]
# scripts_name = [i.split('.')[0] for i in os.listdir(path)]

# border color from bootstrap
border_color = [
    "border-secondary",
    "border-success",
    "border-dark",
    "border-warning",
    "border-primary",
]

popUp = dbc.Modal(
    [
        dbc.ModalHeader("Header", id="modalHeader"),
        dbc.ModalBody(
            dcc.Markdown(
                id="markdownCode",
                highlight_config={"theme": "dark"},
            ),
            id="modalBody",
            className="overflow-auto",
        ),
        dbc.ModalFooter(dbc.Button("Close", id="close", className="ml-auto")),
    ],
    id="modal",
    style={"minWidth": "80%"},
)

popUpResult = dbc.Modal(
    [
        dbc.ModalHeader("Header", id="modalHeaderResult"),
        dbc.ModalBody(id="modalBodyResult", className="overflow-auto"),
        dbc.ModalFooter(dbc.Button("Close", id="closeResult", className="ml-auto")),
    ],
    id="modalResult",
    style={"minWidth": "90%"},
)


@app.callback(
    [
        Output("modalHeader", "children"),
        Output("markdownCode", "children"),
        Output("modal", "is_open"),
    ],
    [Input("close", "n_clicks"), Input("show_code", "n_clicks")],
    [State("strategy", "value"), State("modal", "is_open")],
)
def toggle_modal(is_open, show_code, strategy, *args):
    changed = ctx.triggered[0]["prop_id"].split(".")[0]
    if "close" in changed or changed == "" or strategy is None:
        return "", "", False

    # code display button
    # name = changed.replace('_code','')
    code = "```python\n" + open(os.path.join(path, strategy + ".py")).read() + "\n```"
    return strategy, code, True


@app.callback(
    [
        Output("modalHeaderResult", "children"),
        Output("modalBodyResult", "children"),
        Output("modalResult", "is_open"),
    ],
    [Input("closeResult", "n_clicks"), Input("backtestData", "n_clicks")],
    [State("strategy", "value"), State("modalResult", "is_open")],
)
def toggle_modal_result(is_open, backtestData, strategy, *args):
    # print("button clicked")
    changed = ctx.triggered[0]["prop_id"].split(".")[0]
    if "close" in changed or changed == "" or strategy is None:
        return "", "", False

    try:
        df = pd.read_csv(os.path.join(path_results, strategy + ".csv"))
        df.sort_values("profitPercent", ascending=False, inplace=True)
        df.dropna()
        df = df[
            [
                "name",
                "profitPercent",
                "totalInvestment",
                "totalNetWorth",
                "NumberOfTrades",
                "totalBuy",
                "totalSell",
                "currentStocksInHandValue",
            ]
        ]

        cols = [
            {
                "name": i,
                "id": i,
            }
            for i in df.columns
        ]
        data = df.to_dict("records")

        performance = dbc.Container(
            DataTable(
                columns=cols,
                data=data,
                page_size=30,
                sort_action="native",
                filter_action="native",
                style_header={"backgroundColor": "black"},
                style_cell={"backgroundColor": "black"},
            )
        )
        return strategy + " - " + str(len(df)), performance, True
    except:
        return strategy, dbc.Label("Backtest data not available", className="h6"), True


# dynamically generate the strategies code
pageBody = dbc.CardBody(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Label(i),
                    className=" col-md-6 col-lg-8 col-sm-6 col-xs-12 p-0 m-0",
                )
            ],
            no_gutters=True,
            justify="around",
            className="border mb-1 row-fluid " + np.random.choice(border_color),
        )
        for i in scripts_name
    ]
)

dropDownStrategies = dcc.Dropdown(
    id="strategy",
    options=[{"label": i, "value": i} for i in scripts_name],
    value=None,
    style={"color": "black", "background-color": "white", "width": "20em"},
    # className="col"
)

pageHeader = dbc.CardHeader(
    [
        dbc.Label("Trading Strategies", className="mr-2 mr-auto"),
        dropDownStrategies,
        dbc.Col(
            dbc.Button("Details", id="backtestData", className="btn btn-block "),
            className="h6 col-md-1 col-lg-1 col-sm-3 col-xs-6 p-0 m-0  m-xs-0",
        ),
        dbc.Col(
            dbc.Button("Show Code", id="show_code", className="btn btn-block"),
            className="h6 col-md-1 col-lg-1 col-sm-3 col-xs-6 p-0 m-0  m-xs-0",
        ),
        dbc.Col(
            dbc.Button("Run Backtest", id="runBackTest", className="btn btn-block"),
            className="h6 col-md-2 col-lg-2 col-sm-3 col-xs-6 p-0 m-0  m-xs-0",
        ),
    ],
    className="row",
)

alertView = dbc.Alert(
    id="alert", className="row", color="success", is_open=False, dismissable=True
)


@app.callback(
    [Output("alert", "is_open"), Output("alert", "children")],
    Input("runBackTest", "n_clicks"),
    State("strategy", "value"),
)
def runBackTest(click, strategy):
    if click is None:
        raise PreventUpdate
    bt = BackTest("data/stockData/daily/")
    bt.runMultiprocessing(strategy, True)
    return True, "backtest Completed"


layout = dbc.Container(
    [
        dbc.Card(
            [pageHeader, alertView, pageBody], outline=True, className="w-100 p-0 m-0"
        ),
        popUp,
        popUpResult,
    ],
    fluid=True,
    className="w-100 p-0 m-0",
)
