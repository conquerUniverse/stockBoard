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
    nav = True,
    in_navbar = True,
    id = 'login',
    label = "Login"
)

@app.callback(
    [Output('login', 'label'),
    Output('investmentVal','children')],
              [Input(user, 'n_clicks') for user in usernames])
def updateUserID(*args):
    if not any(args):
        return "Login",0
        # print("one click atleast")

    ctx = dash.callback_context

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
            dbc.NavbarBrand("StockBoard", className="ml-2"),
            dbc.NavItem(dbc.NavLink("DashBoard", href="/")),
            dbc.NavItem(dbc.NavLink("UpdateData", href="/updatedata")),
            dbc.NavItem(dbc.NavLink("Analysis", href="/analysis")),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(



                dbc.Nav(
                    # right align dropdown menu with ml-auto className
                    [dropdown], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="mb-4",
)

def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
)(toggle_navbar_collapse)










footer = dbc.Container(html.Footer(
    [ html.H4(["Total Investment ",
    html.Span("0",
     style={"color":"green"}    
    ,
    id = "investmentVal"
    )
    
    ])]))
   

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content'),
    footer
])



@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    global username
    if not username:
        dbc.Alert("Select An ID..",color = "danger")

    linkToPAge = {'/':dashBoard.layout,
            '/updatedata':updateData.layout,
            # '/analysis':analysis.app.layout
            }
    try: 
        return linkToPAge[pathname]
    except:
        return html.Div([html.H1('Page Dosen\'t exist {}'.format(pathname))   ])



#app.run_server()
server = app.server
