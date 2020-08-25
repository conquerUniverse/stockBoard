import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG])


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Login", href="#")),
        # dbc.DropdownMenu(
        #     children=[
        #         dbc.DropdownMenuItem("More pages", header=True),
        #         dbc.DropdownMenuItem("Page 2", href="#"),
        #         dbc.DropdownMenuItem("Page 3", href="#"),
        #     ],
        #     nav=True,
        #     in_navbar=True,
        #     label="More",
        # ),
    ],
    brand="StockBoard",
    brand_href="#",
    color="dark",
    dark=True,
)
message = html.Div(style={'textAlign':'center','fontSize':'80px','width':'100%','height':'100%'},
children = "Hello Users")
app.layout = html.Div(
    style={'background':'Gray','width':'100%','height':'100%'},
    children = [navbar,message]
    )

if __name__ == '__main__':
    app.run_server(debug=True)