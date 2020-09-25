import dash
import dash_bootstrap_components as dbc

# bootstrap theme
# https://bootswatch.com/lux/

# bootstrap themes are the best way to style the websites

external_stylesheets = [dbc.themes.SUPERHERO]

app = dash.Dash(__name__, 
external_stylesheets=external_stylesheets,
suppress_callback_exceptions=True)

server = app.server