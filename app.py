# dash design imports
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash.dependencies import Input, Output

# stockBorad lib imports
from scripts.StockBoard import StockBoard
from scripts.StockData import StockData

username = 'alvin369'

sd = StockData(username=username) # default value 
# sc = StockBoard()
sd.load() # load the data files

noteToSelf = open(f"./profiles/{username}/noteToSelf.txt",'r').read()
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(external_stylesheets=[dbc.themes.SUPERHERO])
# bootstrap themes are the best way to style the websites




navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Login", href="#")),
        
    ],
    brand="StockBoard",
    brand_href="#",
    color="dark",
    dark=True
)


content = dbc.Container(
    [
               
        html.Hr(),
        
        dbc.Tabs(
            [
                dbc.Tab(label="buy", tab_id="buy"),
                dbc.Tab(label="sell", tab_id="sell"),
                dbc.Tab(label="invest", tab_id="invest"),
            ],
            id="tabs",
            active_tab="buy",
        ),
        html.Div(id="tab-content", className="p-4"),
    ]
)


@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab")],
)
def render_tab_content(active_tab, data=1):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    print(active_tab,data )
    if active_tab and data is not None:
        # print("enter")
        data = buyData = sd.getData(active_tab)
        table =  dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),

            style_header = {
                'backgroundColor': 'rgb(40, 20, 100)',
                'color': 'white'
            }
            ,
            style_data_conditional=[{
                'if': {'column_id': ['Name','TotalCost','Amount']
                },
                'backgroundColor': 'rgb(10, 100, 30)',
                'color': 'white'
            }],

            style_data = {
                'backgroundColor': 'rgb(60, 50, 40)',
                'color': 'white'
            },

            style_cell_conditional=[
                    {'if': {'column_id': 'title'},
                    'width': '200px'},
                    {'if': {'column_id': 'post'},
                    'width': '670px'
                    ,'height':'auto'},
                ],

            style_cell={
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'maxWidth': '50px'
                }
            # ,style_table={
            # 'maxHeight': '700px'
            # ,'overflowY': 'scroll'
            # },
        )

        return table
    return "No tab selected"

noteToSelf = dbc.InputGroup(
    
            [
                dbc.Textarea(id = 'nts_text',spellCheck= True,value = noteToSelf,
                title = 'write note to self',style={'width':'90%'}),
                dbc.Button([html.H4("SAve files")],id="nts_save",n_clicks = 0,style={'width':'10%'} )
            ],
            className="mb-2",
            id = 'nts'
        )

footer = dbc.Container( html.Footer(
    
    [noteToSelf,html.H4([f"Total Investment ",html.Span(sum(sd.getData('invest').Amount),style={"color":"green"})]), 
    ]
    ))


@app.callback(
    Output("nts_save","children"),
    [Input("nts_save", "n_clicks"),Input("nts_text", "value")],
)
def nts_save_to_file(n_clicks,value):
    if n_clicks :
        with open(f"./profiles/{username}/noteToSelf.txt",'w') as w:
            w.write(value)
        print("file saved")
    



app.layout = html.Div(
    children = [navbar,content,footer]
    )

if __name__ == '__main__':
    app.run_server(debug = True)