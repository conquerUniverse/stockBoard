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

options = html.Div("Apply filters",className="bg-blue m-1 col-4")
codeEditor = html.Div("this is code editor", className = "bg-yellow m-1 col-8")
chart = html.Div("chart section",className="bg-green row")

layout = html.Div([ html.Div([codeEditor,options],className="row"),
        chart],className="col")
