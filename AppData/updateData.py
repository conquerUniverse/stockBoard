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

from app import app
# general imports
import os


username = 'alvin369' # lets fix this here for now

sd = StockData(username=username) # default value 

sd.load() # load the data files

noteToSelf = open(f"./profiles/{username}/noteToSelf.txt",'r').read()



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
        dbc.Container(id="tab-content", className="p-4"),
    ]
)



def tableView(data):

    var = dash_table.DataTable(
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

    ,style_table={
    'maxHeight': '50%'
    ,'overflowY': 'auto'
    },
    )
    return var



def addStructuredData(category):
    print(category)
    nameAndDate = dbc.FormGroup(
            [   dbc.Row(
                [dbc.Label("Name", className="mr-2",width = 4),
                dbc.Input( placeholder="Enter Name",)],                
            style = {"width":"50%"} ),
                dbc.Row(
                [dbc.Label("Date", className="mr-2"),
                dbc.Input( type="date")] ,
            style = {"width":"50%"} 
                )
                
            ],
            className="mr-3",
            row = True,
            style = {"width":"100%"}
            )


    numberAndPriceOfStock = dbc.FormGroup(
            [   dbc.Row(
                [dbc.Label("NumberOfStocks", className="mr-2",width = 4),
                dbc.Input(type="number", placeholder="No. of stock")],
                
            style = {"width":"50%"} ),

                dbc.Row(
                [dbc.Label("Price/Stock", className="mr-2"),
                dbc.Input(type='number')] ,

            style = {"width":"50%"} 
                )
                
            ],
            className="mr-3",
            row = True,
            style = {"width":"100%"}
            )

    totalCostAndExtraCharge = dbc.FormGroup(
            [   dbc.Row(
                [dbc.Label("TotalCost", className="mr-2",width = 4),
                dbc.Input(type="number", placeholder="No. of stock")],
                
            style = {"width":"50%"} ),

                dbc.Row(
                [dbc.Label("ExtraCharge", className="mr-2",width = 4),
                dbc.Input(type='number')] ,

            style = {"width":"50%"} 
                )
                
            ],
            className="mr-3",
            row = True,
            style = {"width":"100%"}
            )

    submitButton = dbc.Row([dbc.Button("Submit", color="primary"),
                        dbc.Input(type="text", placeholder="enter Passwd")],justify="center")

    investForm = dbc.FormGroup(
            [   dbc.Row(
                [dbc.Label("Amount", className="mr-2",width = 4),
                dbc.Input(type="number", placeholder="No. of stock")],
                
            style = {"width":"50%"} ),

                dbc.Row(
                [dbc.Label("Date", className="mr-2",width = 4),
                dbc.Input(type='date')] ,

            style = {"width":"50%"} 
                ),
                dbc.Row(
                [dbc.Label("Description", className="mr-2",width = 4),
                dbc.Input(type='text',value="add")] ,

            style = {"width":"50%"} 
                )
                
            ],
            className="mr-3",
            row = True,
            style = {"width":"100%"}
            )
    if category == "invest" :
        return dbc.Form( [investForm,submitButton],inline=True )
    else:
        return  dbc.Form( [nameAndDate, numberAndPriceOfStock,totalCostAndExtraCharge,submitButton] ,inline=True)


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
    # print(active_tab,data )
    if active_tab and data is not None:
        # print("enter")
        data  = sd.getData(active_tab)
        table =  tableView(data)
        form = addStructuredData(active_tab)
        # return form
        return dbc.Container([table,html.Hr(),html.H3("Update "+str(active_tab)+" Data"),form])
    return html.H1("No tab selected")

noteToSelf = dbc.InputGroup(
    
            [
                dbc.Textarea(id = 'nts_text',spellCheck= True,value = noteToSelf,
                title = 'write note to self',style={'width':'90%'}),
                dbc.Button([html.H4("SAve files")],id="nts_save",n_clicks = 0,style={'width':'10%'} )
            ],
            className="mb-2",
            id = 'nts'
        )




@app.callback(
    Output("nts_save","children"),
    [Input("nts_save", "n_clicks"),Input("nts_text", "value")],
)
def nts_save_to_file(n_clicks,value):
    if n_clicks :
        with open(f"./profiles/{username}/noteToSelf.txt",'w') as w:
            w.write(value)
        print("file saved")
    



layout = html.Div(
    children = [content]
    )
