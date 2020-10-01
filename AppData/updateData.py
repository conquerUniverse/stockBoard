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


username = 'fahim' # lets fix this here for now

sd = StockData(username=username) # default value 

sd.load() # load the data files

noteToSelf = open(f"./profiles/{username}/noteToSelf.txt",'w+').read()



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
        dcc.ConfirmDialog(
        id='messageSave' ),
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
    # print(category)
    nameAndDate = dbc.FormGroup(
            [   dbc.Row(
                [dbc.Label("Name", className="mr-2",width = 4),
                dbc.Input( placeholder="Enter Name",id="name")],                
            style = {"width":"50%"} ),
                dbc.Row(
                [dbc.Label("Date", className="mr-2"),
                dbc.Input( type="date",id="date")] ,
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
                dbc.Input(type="number", placeholder="No. of stock",\
                    id = "numberofstocks")],
                
            style = {"width":"50%"} ),

                dbc.Row(
                [dbc.Label("Price/Stock", className="mr-2"),
                dbc.Input(type='number',id="price")] ,

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
                dbc.Input(type="number", placeholder="Cost of transaction",\
                    id="totalcost")],
                
            style = {"width":"50%"} ),

                dbc.Row(
                [dbc.Label("ExtraCharge", className="mr-2",width = 4),
                dbc.Input(type='number',id= "extracharges")] ,

            style = {"width":"50%"} 
                )
                
            ],
            className="mr-3",
            row = True,
            style = {"width":"100%"}
            )

   
    investForm = dbc.FormGroup(
            [   dbc.Row(
                [dbc.Label("Amount", className="mr-2",width = 4),
                dbc.Input(type="number", placeholder="amount added ",id="amountInvest")],
                
            style = {"width":"50%"} ),

                dbc.Row(
                [dbc.Label("Date", className="mr-2",width = 4),
                dbc.Input(type='date',id="dateInvest")] ,

            style = {"width":"50%"} 
                ),
                dbc.Row(
                [dbc.Label("Description", className="mr-2",width = 4),
                dbc.Input(type='text',value="add",id="descInvest")] ,

            style = {"width":"50%"} 
                )
                
            ],
            className="mr-3",
            row = True,
            style = {"width":"100%"}
            )


    submitButton = dbc.Row([dbc.Button(f"{category.capitalize()} Stock", \
        color="primary",n_clicks = 0,id="submit") ],justify="end")
    

    password = dbc.Input(type="text", placeholder="enter Passwd")                 
    saveData = dbc.Button("Save Data", color="success",n_clicks = 0,id="saveData")
    
    buySellForm = html.Div(dbc.FormGroup([nameAndDate, numberAndPriceOfStock,totalCostAndExtraCharge]),id="buySellForm")
    investForm = html.Div(dbc.FormGroup([investForm,]),id="investForm")
    return  dbc.Form( [buySellForm,investForm,
                dbc.FormGroup([password,submitButton]),html.Hr(),saveData
            ] ,inline=True)

# save Data
@app.callback(
    [Output("messageSave","message"),Output("messageSave","displayed")],
    [Input("saveData","n_clicks"),
    Input("tabs","active_tab")
    ]
)
def saveDataCallBack(_,category):
    if not  _:
        return "all Fine",False
    else:
        sd.updateData(category=category)
        return category+" Values updated Successfully",True

# update data BuySell
@app.callback(
    [Output("message","children"),
    Output("buySellForm","hidden"),
    Output("investForm","hidden")
    ],

    [
    Input("submit","n_clicks"),#0

    Input("name","value"),
    Input("numberofstocks","value"),
    Input("price","value"),
    Input("date","value"),
    Input("totalcost","value"),
    Input("extracharges","value"), #6

    Input("amountInvest","value"),
    Input("dateInvest","value"),
    Input("descInvest","value"),


    Input("tabs","active_tab")
    ]
)
def updateForm(*args):
    defaultMessage = "This is a status Bar"
    if args[-1] == "buy":
        if ischanged(args[0]):
            return (defaultMessage,False,True)
        if all(args[:7]):
            data = {"Name":args[1],
                    "NumberOfStocks":args[2],
                    "BuyingPrice":args[3],
                    "Date":args[4],
                    "TotalCost":args[5],
                    "ExtraCharges":args[6],
                    }
            sd.addData(args[-1],**data)
            return ("Buy Data updates",False,True)
        else:
            return ("Please fill all entries",False,True)

    elif args[-1] == "sell":
        if ischanged(args[0]):
            return (defaultMessage,False,True)
        if all(args[:7]):
            data = {"Name":args[1],
                    "NumberOfStocks":args[2],
                    "SellingPrice":args[3],
                    "Date":args[4],
                    "TotalCost":args[5],
                    "ExtraCharges":args[6],
                    }
            sd.addData(args[-1],**data)
            return ("Sell Data updates",False,True)
        else:
            return ("Please fill all entries",False,True)
    
    else:
        if ischanged(args[0]):
            return (defaultMessage,True,False)
        if all(args[7:-1]):
            data = {  "Amount":args[7],
                    "Date":args[8],
                    "Description":args[9],
                    }
            sd.addData(args[-1],**data)
            return ("Invest Data updates",True,False)
        else:
            return ("Please fill all entries",True,False)

pastButton = 0
def ischanged(x):
    global pastButton
    print(pastButton,x)
    if x != pastButton:
        pastButton = x
        return False
    else:
        return True



# Tab select view
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
        message = dbc.Alert("All Fine",id="message",color = "info")


        form = dbc.Jumbotron([html.H2("Update "+str(active_tab)+" Data",className="display-5"),
                                    html.Br(),addStructuredData(active_tab),message])

        return dbc.Container([table,html.Hr(),form])
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
