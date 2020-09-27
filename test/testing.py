import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash

external_stylesheets = [dbc.themes.SUPERHERO]

app = dash.Dash(__name__, 
external_stylesheets=external_stylesheets,
suppress_callback_exceptions=True)

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"


navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                    dbc.Col(dbc.NavbarBrand("Navbar", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
                
            ),
            href="https://plot.ly",
            style={"marginRight":"10%"}
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse([
            dbc.Row(

            [
            dbc.NavLink("DashBoard", href="/"),
            dbc.NavLink("UpdateData", href="/updatedata"),
            dbc.NavLink("Analysis", href="/analysis")
            ],
            # no_gutters=True,
            justify="end",
                
            ),
            ], id="navbar-collapse", navbar=True,
            style = {"marginRight":"auto"}
            
            ),
    ],
    
    color="dark",
    dark=True,
)


# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


app.layout = dbc.Container(navbar)
app.run_server(debug=True)