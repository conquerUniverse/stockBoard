
# 
import dash_bootstrap_components as dbc
# bootstrap theme
# https://bootswatch.com/lux/

# bootstrap themes are the best way to style the websites


external_stylesheets = [dbc.themes.CYBORG]
run_jupyterDash = False
if run_jupyterDash:
    from jupyter_dash import JupyterDash
    app = JupyterDash(__name__,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
    meta_tags=[{'name':"viewport","content":"width=device-width,initial-scale=1"}])

else:
    import dash
    app = dash.Dash(__name__, 
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
    meta_tags=[{'name':"viewport","content":"width=device-width,initial-scale=1"}])

server = app.server