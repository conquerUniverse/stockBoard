# dash design imports
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash.dependencies import Input, Output, State

from app import app
from AppData import updateData,dashBoard,analysis
#from app import server


# stockBorad lib imports
from scripts.StockBoard import StockBoard
from scripts.StockData import StockData

# general imports
import os

def isUser(name):
    if name.lower() != "readme.md":
        return True
    return False

usernames = [i for i in os.listdir("./profiles/") if isUser(i)]



username = None

if username :
    sd = StockData(username='alvin369') # default value 
    # sc = StockBoard()
    sd.load() # load the data files
    investmentValue = html.Span(sum(sd.getData('invest').Amount))
else:
    investmentValue = html.Span("0")

dropdown = dbc.DropdownMenu(
    children = [dbc.DropdownMenuItem(user,id=user) for user in usernames],        
    # nav = True,
    in_navbar = True,
    id = 'login',
    label = "Login",
    color="Info"
    
)

@app.callback(
    [Output('login', 'label'),
    Output('investmentVal','children')],
              [Input(user, 'n_clicks') for user in usernames])
def updateUserID(*args):
    ctx = dash.callback_context
    if not any(args):
        return "Login",0
    # this gets the id of the button that triggered the callback
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    global username

    username = button_id
    val = 0
    if username:
        try:
            sd = StockData(username=username) 
            sd.load() # load the data files
            val = sum(sd.getData('invest').Amount)
        except:
            dbc.Alert("No Data Found")
            return "Login",0
            
        

    return button_id,val


            


navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("StockBoard", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
                
            ),
            
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Collapse(

                dbc.Row(       # right align dropdown menu with ml-auto className
            [
            dbc.NavLink("DashBoard", href="/"),
            dbc.NavLink("UpdateData", href="/updatedata"),
            dbc.NavLink("Analysis", href="/analysis"),
            dropdown
            ], className="ml-auto", 
            no_gutters=True,
            ),
                id="navbar-collapse",
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="mb-4",
    sticky = "top",
    style={"height":"5%"}
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


footer = dbc.Navbar(
    dbc.Row(
    [ dbc.Col(html.H5(["Total Investment ",
    html.Span("0" ,style={"textShadow":"0px 0px 50px white"},
    id = "investmentVal"
    )]),style={"width":"50%"}),
    
    dbc.Col(html.H5("A Fun Project"),style={"width":"50%"})
    ],
    justify="center"
    
    ,style={"width":"100%"}
    ),

    color="dark",
    dark = True,
    style = {"bottom":"0%","position":"fixed","width":"100%","height":"5%"}
    )
   


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    dbc.Container(id='page-content',
    style={"overflow":"auto","height":"100%","marginBottom":"2%","width":"95%"}
    ),
    footer
],
style={"height":"100%"})



@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    global username
    if not username:
        dbc.Alert("Select An ID..",color = "danger")

    linkToPAge = {
            '/':dashBoard.layout,
            '/updatedata':updateData.layout,
            '/analysis':analysis.layout
            }
    try: 
        return linkToPAge[pathname]
    except:
        return html.Div([html.H1('Page Is Broken.. :( {}'.format(pathname)
        )])



#app.run_server()
server = app.server
