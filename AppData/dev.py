import dash
from app import app
from flask import render_template
import dash_bootstrap_components as dbc
import dash_html_components as html


layout = dbc.Jumbotron(
    [html.H1(" Development.. Testing"),
    html.Div("firebase deployment not possible.")]
    
    )
