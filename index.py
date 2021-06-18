# dash design imports
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash.dependencies import Input, Output, State

from app import app
from AppData import updateData,dashBoard,analysis,charts,tradingStrategies,tradeBot

# stockBorad lib imports
from scripts.StockBoard import StockBoard
from scripts.StockData import StockData

# general imports
import os
import importlib

def isUser(name):
    if name.lower() not in ("readme.md","passwords.cfg"):
        return True
    return False

usernames = [i for i in os.listdir("./profiles/") if isUser(i)]



# username = None
# sd = None # stock data dataframe


# dropdown = dbc.DropdownMenu(
#     children = [dbc.DropdownMenuItem(user,id=user) for user in usernames],        
#     # nav = True,
#     in_navbar = True,
#     id = 'login',
#     label = "Login",
#     color="Info"    
# )

dropdown = dcc.Dropdown(
    options = [{'label':user,'value':user} for user in usernames],        
    # nav = True,
    # in_navbar = True,
    id = 'login',
    style={'width':'8em'},
    value="alvin369",
    # label = "Login",
    # color="Info"    
)

# @app.callback(
#     Output('login', 'value'),
#     [Input('login', 'n_clicks')])
# def updateUserID(*args):
#     ctx = dash.callback_context
#     if not any(args):
#         return "Login"
#     # this gets the id of the button that triggered the callback
#     username = ctx.triggered[0]["prop_id"].split(".")[0]
#     # global username,sd
#     # username = button_id
#     print("clicked ",username)

#     sd = StockData(username=username) 
#     sd.load() # load the Data files
#     return button_id


            


navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("Cortex Bot", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
                
            ),
            
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Collapse(

                dbc.Row(       # right align dropdown menu with ml-auto className
            [
            dbc.NavLink("DashBoard", href="/"),
            dbc.NavLink("Charts", href="/charts"),
            dbc.NavLink("UpdateData", href="/updatedata"),
            dbc.NavLink("Analysis", href="/analysis"),
            dbc.NavLink("TradeBot", href="/tradeBot"),
            dbc.NavLink("Trading Strategies", href="/tradingstrategies"),
            dropdown
            ], className="ml-auto", 
            no_gutters=True,
            ),
                id="navbar-collapse",
                navbar=True,
            ),
        ]
        ,className="border border-info p-1 ",
        fluid= True # it will take the entire screen, else there is huge padding associated with containers
    ),
    color="dark",
    dark=True,
    className="mb-3",
    sticky = "top",
    style={"height":"5%"},
    
)


@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    dbc.Container(id='page-content',fluid=True,
    style={"overflow":"auto","height":"100%","marginBottom":"1%"}
    ),
    # footer
],
style={"height":"100%","width":"100%"})



@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')],
              State('login','value'))
def display_page(pathname,username):
    # global username
    if not username:
        return html.Div([html.H1('Please Select an userID and click the tab')])
    
    module = importlib.import_module('AppData.tradingStrategies')
    tradingStrategies = importlib.reload(module)
    linkToPage = {
            '/':dashBoard.getLayout(username),
            '/updatedata':updateData.getLayout(username),
            '/analysis':analysis.layout,
            '/charts':charts.layout,
            '/tradeBot':tradeBot.layout,
            '/tradingstrategies':tradingStrategies.layout
            }
    try: 
        # print("userename is ",username)
        return linkToPage[pathname]
    except:
        return html.Div([html.H1('Page Is Broken.. :( {}'.format(pathname)
        )])



app.run_server(debug=True,threaded=True)
# server = app.server
