import dash
from app import app
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash import callback_context as ctx

import dash_editor_components

import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
import importlib

from tradingStrategies.backtest import BackTest

# val = "apply filters"*100

template = open("assets/templateCode.py", "r").read()
fileName = dbc.Input(
    value="fileName.py",
    id="filename",
    style={"height": "5%", "marginBottom": "1%", "width": "20%"},
)
# print(template)
ide = dbc.Textarea(
    value=template,
    contentEditable="true",
    spellCheck="true",
    id="code",
    style={
        "height": "90%",
        "width": "100%",
        "fontFamliy": "monospace",
        "color": "crimson",
    },
    className="border border-success",
)

# ide = dash_editor_components.PythonEditor(children=template,id="code",className="row card card-body h-95",  )

# -------------- Filters -----------
stockDataAvailable = [
    {"label": i.split(".")[0], "value": i.split(".")[0]}
    for i in os.listdir("./data/stockData/daily")
    if i.split(".")[1] == "csv"
]

dp = dcc.Dropdown(
    id="stockdropdown",
    options=stockDataAvailable,
    value=None,
    placeholder="select stock",
    style={
        "color": "black",
        "background-color": "white",
    },
)
sma_list = [5, 10, 20, 46, 50, 100]
sma = dcc.Dropdown(
    multi=True,
    id="smaDropdown",
    placeholder="select filters",
    options=[{"label": i, "value": i} for i in sma_list],
    className="w-100 ",
)

filters = html.Div(
    [
        dbc.Row(
            [html.Div(dp, className="col-6 p-0"), html.Div(sma, className="col-6 p-0")],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label("Start date", className="col-3 p-0"),
                dbc.Input(type="date", id="start_date", className="col-3 p-0 "),
                dbc.Label("End date", className="col-3 "),
                dbc.Input(type="date", id="end_date", className="col-3 p-0"),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Checklist(
                    id="checkList",
                    options=[{"label": "execute Code ?", "value": True}],
                    className="col-3 mr-1",
                ),
                dbc.Button(
                    "Run",
                    id="run_code",
                    className=" btn btn-success float float-right mr-2 ",
                ),
                dbc.Button(
                    "Save file",
                    id="save_btn",
                    className=" btn btn-primary float float-right mr-0",
                ),
            ]
        ),
    ]
)

status = dbc.Alert(
    "status is working",
    color="success",
    id="status",
    className="row",
    dismissable=True,
    is_open=False,
)
results = html.Div(id="result", className="row")

options = dbc.Container(
    [status, filters, results],
    className="border border-primary col-5 ",
    style={"overflow": "auto", "height": "45vh", "padding": "2%"},
)


codeEditor = html.Div(
    [fileName, ide],
    className="border border-info m-0 pl-1 col-7",
    style={"height": "45vh", "overflow": "auto"},
)

# chart = html.Div("chart section",className="border border-danger row",style = {"height":'35vh'})

chart = dcc.Graph(
    id="stockChart_bot",
    figure={},
    className="border border-danger row",
    style={"height": "38vh"},
)


layout = html.Div(
    [
        dbc.Alert(
            id="save_status", dismissable=True, is_open=False, className="row info"
        ),
        html.Div([codeEditor, options], className="row h-60"),
        chart,
    ],
    className="col border border-success w-100 mt-0 mp-0",
    style={"height": "100%"},
)

# ------ important functions -----


def create_figure(name, df, xCol, yCol, **kwargs):
    fig = px.line(
        df,
        x=xCol,
        y=yCol,
        # title=f'{name} Chart',
        **kwargs,
    )
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="LightSteelBlue")
    return fig


def fileCheck(name):
    sp = name.split(".")
    if len(sp) != 2 or sp[1] != "py":
        return "invalid file naming should have <fileName>.py", True
    loc = "./tradingStrategies/scripts/"
    print("name check ", name)
    scriptsAvailable = [i.lower() for i in os.listdir(loc)]
    if name.lower() in scriptsAvailable:
        return "filename already exist ", True
    return "", False


# ----- callbacks ---------
@app.callback(
    [Output("save_status", "children"), Output("save_status", "is_open")],
    Input("save_btn", "n_clicks"),
    [State("code", "value"), State("filename", "value")],
)
def saveFile(save_btn, code, filename):
    if save_btn == None:
        raise PreventUpdate

    msg, flag = fileCheck(filename)
    if flag:
        return msg, flag  # give error msg
    try:
        exec(code)
    except Exception as e:
        return str(e), True

    # save to file
    loc = "./tradingStrategies/scripts/"
    F = open(loc + filename, "w")
    F.write(code)
    F.close()
    return "File Saved", True


@app.callback(
    [
        Output("status", "children"),
        Output("status", "is_open"),
        Output("stockChart_bot", "figure"),
        Output("result", "children"),
    ],
    [Input("run_code", "n_clicks")],
    [
        State("stockdropdown", "value"),
        State("smaDropdown", "value"),
        State("start_date", "value"),
        State("end_date", "value"),
        State("checkList", "value"),
        State("code", "value"),
        State("filename", "value"),
    ],
)
def updateChart(btn, stock, sma_value, start_date, end_date, check, code, filename):
    if btn == None:
        print("update chart prevent update")
        raise PreventUpdate
    else:

        if stock == None:
            return "Please select a stock name", True, {}, ""

        df = pd.read_csv(f"./data/stockData/daily/{stock}.csv")
        if start_date is not None:
            df = df[df.timestamp >= start_date]
        if end_date is not None:
            df = df[df.timestamp <= end_date]
        yCol = ["close"]
        if sma_value is not None:
            for smaV in sma_value:
                df["sma-" + str(smaV)] = df["close"].rolling(window=smaV).mean()
                yCol.append("sma-" + str(smaV))

        # print(check)

        if check != None and len(check) > 0:
            loc = "./tradingStrategies/tempScripts/"
            try:
                exec(code)
            except Exception as e:
                return str(e), True, {}, ""
            print("filename is ", filename)
            F = open(loc + filename, "w")
            # print("code is ",code)
            F.write(code)
            F.close()
            print("code successfully saved @ ", loc)

            try:
                module = importlib.import_module(
                    "tradingStrategies.tempScripts." + filename.split(".")[0]
                )
                module = importlib.reload(module)
                scriptFunction = module.run
                df.reset_index(drop=True, inplace=True)
                bt = BackTest("data/stockData/daily/")
                res = bt.backtest(scriptFunction, df)

                colNames = [
                    "profitPercent",
                    "stockGrowth",
                    "totalNetWorth",
                    "totalInvestment",
                    "NumberOfTrades",
                ]
                result_view = dbc.Row(
                    [
                        dbc.Col(
                            [dbc.Row(i), dbc.Row(round(res[i], 3))],
                            className="col col-xs-6 overflow-auto",
                        )
                        for i in colNames
                    ],
                    className="m-1 border border-success",
                    style={"width": "100%"},
                )

                print("result is ", res)
                df_otpt = pd.DataFrame(scriptFunction(df))
                df_temp = pd.merge(df, df_otpt, on="timestamp", how="left")
                # print(df_temp)
                fig = create_figure(stock, df_temp, "timestamp", yCol)

                buyData = df_temp[df_temp["actions"] == "buy"]
                fig.add_trace(
                    go.Scatter(
                        name="buy",
                        mode="markers",
                        x=buyData["timestamp"],
                        y=buyData["close"],
                        marker={"size": 10},
                    )
                )

                sellData = df_temp[df_temp["actions"] == "sell"]

                fig.add_trace(
                    go.Scatter(
                        name="sell",
                        mode="markers",
                        x=sellData["timestamp"],
                        y=sellData["close"],
                        marker={"size": 10},
                    )
                )
                return "", False, fig, result_view
            except Exception as e:
                return str(e), True, {}, ""
        else:
            fig = create_figure(stock, df, "timestamp", yCol)
            return "", False, fig, ""
