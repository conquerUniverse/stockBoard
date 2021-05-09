# dash design imports
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash.dependencies import Input, Output
from dash_extensions import Download
from dash_extensions.snippets import send_data_frame

# stockBorad lib imports
from scripts.StockBoard import StockBoard
from scripts.StockData import StockData

from app import app
# general imports
import os, hashlib,configparser

# noteToSelf = open(f"./profiles/{username}/noteToSelf.txt",'w+').read()


# global Variables
sd,username = None,'Fahim'

# loading password files
config = configparser.ConfigParser()
config.read('profiles/passwords.cfg')

content = dbc.Card(
    [dbc.CardHeader(   
        [   
        dbc.Tabs(
            [
                dbc.Tab(label="buy", tab_id="buy"),
                dbc.Tab(label="sell", tab_id="sell"),
                dbc.Tab(label="invest", tab_id="invest"),
                 ],
            id="tabs",
            active_tab="buy",
            className="col"
        ),
        dbc.Button("Download Data ",id="download_data",
        className="float-md-right btn col-2 btn-md ",outline=True)
     ],className="row" ),
        # dcc.ConfirmDialog( id='messageSave' ),
        dbc.CardBody(dbc.Container(id="tab-content", className="p-4")),
       Download(id="download"),
    ]
    , outline=True
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
            'width': '100px'},
            {'if': {'column_id': 'post'},
            'width': '200px'
            ,'height':'auto'},
        ],

    style_cell={
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'maxWidth': '1px',
            'textAlign':"center"
        }

    ,style_table={
    'maxHeight': '300px'
    ,'overflowY': 'auto'
    },
    )
    return dbc.Container(var)



def addStructuredData(category):
    nameAndDate = dbc.FormGroup(
            [   dbc.Row(
                [dbc.Label("Name", className="mr-2",width = 4),
                dbc.Input( placeholder="Enter Name",id="name")],                
            style = {"width":"50%"} ),
                dbc.Row(
                [dbc.Label("Date", className="mr-2",width = 4),
                dbc.Input( type="date",id="date")] ,
            style = {"width":"50%"} ,
            
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
                [dbc.Label("Price/Stock", className="mr-2",width = 4),
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
    

    password = dbc.Input(type="text", placeholder="PLs. enter Passwd",id="password")                 
    saveData = dbc.Button("Save Data", color="success",n_clicks = 0,id="saveData")
    
    buySellForm = html.Div(dbc.FormGroup([nameAndDate, numberAndPriceOfStock,totalCostAndExtraCharge]),id="buySellForm")
    investForm = html.Div(dbc.FormGroup([investForm,]),id="investForm",hidden=True)
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


def putData(category,*args):
    # print("displaying the data")
    # print(args)
    # print(args[:5])
    # print(args[6:])
    if not all(args[:5]) and not all(args[6:]):
        return False
    dataInvest = { 
                    "Amount":args[6],
                    "Date":args[7],
                    "Description":args[8],
                    }
    data = {"Name":args[0],
            "NumberOfStocks":args[1],
            "Date":args[3],
            "TotalCost":args[4],
            "ExtraCharges":args[5],
            }
    if category == "invest":
        sd.addData(category,**dataInvest)
        return True
    mapping = {"buy":"BuyingPrice","sell":"SellingPrice"}
    
    d = {**data,**{mapping[category]:args[2]}}
    sd.addData(category,**d)
    return True

def isPasswordMatching(pswd):
    if not pswd:
        return False
    hashed = config['passwords'][username]
    pswd = hashlib.md5(pswd.encode())

    if pswd.hexdigest() == hashed:
        return True
    return False

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
    Input("descInvest","value"), #9

    Input("password",'value'),
    Input("tabs","active_tab") # access as args[-1]
    ]
)
def updateForm(*args):
    defaultMessage = "This is a status Bar"
    if ischanged(args[0]):
        if isPasswordMatching(args[-2]): # submit button is pressed
            # print("Pressed save button")
            if putData(args[-1],*args[1:-2]):
                return (args[-1]+" Data is updated",formToggle(args[-1]),not formToggle(args[-1]))
            else:
                return ("Please fill all entries",formToggle(args[-1]),not formToggle(args[-1]))
        else:
            return ("The password is not matching",formToggle(args[-1]),not formToggle(args[-1]))
    else:
        return (defaultMessage,formToggle(args[-1]),not formToggle(args[-1]))



def formToggle(x):
    if x == "invest":
        return True
    return False



pastButton = 0
def ischanged(x):
    global pastButton
    if x != pastButton:
        pastButton = x
        return True
    else:
        return False



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
    if active_tab and data is not None:
        data  = sd.getData(active_tab)
        table =  tableView(data)
        message = dbc.Alert("All Fine",id="message",color = "info")


        form = dbc.Card([dbc.CardHeader("Update "+str(active_tab)+" Data",className="display-5"),
                    dbc.CardBody(addStructuredData(active_tab)),dbc.CardFooter(message)]
                    ,outline=True)

        return dbc.Container([table,html.Hr(),form])
    return html.H1("No tab selected")

# noteToSelf = dbc.InputGroup(
    
#             [
#                 dbc.Textarea(id = 'nts_text',spellCheck= True,value = noteToSelf,
#                 title = 'write note to self',style={'width':'90%'}),
#                 dbc.Button([html.H4("SAve files")],id="nts_save",n_clicks = 0,style={'width':'10%'} )
#             ],
#             className="mb-2",
#             id = 'nts'
#         )

# @app.callback(
#     Output("nts_save","children"),
#     [Input("nts_save", "n_clicks"),Input("nts_text", "value")],
# )
# def nts_save_to_file(n_clicks,value):
#     if n_clicks :
#         with open(f"./profiles/{username}/noteToSelf.txt",'w') as w:
#             w.write(value)
#         print("file saved")

@app.callback(
Output("download", "data"),
Input("download_data", "n_clicks"))
def download_data(n_clicks):
    if n_clicks is not None:
        return send_data_frame(sd.getData().to_csv, filename=sd.active_data+".csv")


def getLayout(user):
    global username,sd,content
    username = user # lets fix this here for now

    sd = StockData(username=username) # default value 

    sd.load() # load the data files

    return html.Div(
    children = [content]
    )
