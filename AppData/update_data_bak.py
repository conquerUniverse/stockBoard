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



class UpdateDataPage:
    def __init__(self,username = 'fahim'):
        self.username = username # lets fix this here for now
        self.sd = StockData(username=username) # default value 

        self.sd.load() # load the data files
        self.pastButton = 0

        # noteToSelf = open(f"./profiles/{username}/noteToSelf.txt",'w+').read()

    def run(self):
        self.getContent()


    def getContent(self,):
        content = dbc.Container(
            [ html.Hr(),
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
        



    def tableView(self,data):

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



    def addStructuredData(self,category):
        # print(category)
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


    def putData(self,category,*args):
        print("displaying the data")
        print(args)
        print(args[:5])
        print(args[6:])
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


        Input("tabs","active_tab") # access as args[-1]
        ]
    )
    def updateForm(*args):
        defaultMessage = "This is a status Bar"
        if ischanged(args[0]): # submit button is pressed
            # print(args[-1])
            print("Pressed save button")
            if putData(args[-1],*args[1:-1]):
                return (args[-1]+" Data is updated",formToggle(args[-1]),not formToggle(args[-1]))
            else:
                return ("Please fill all entries",formToggle(args[-1]),not formToggle(args[-1]))
        else:
            return (defaultMessage,formToggle(args[-1]),not formToggle(args[-1]))



    def formToggle(self,x):
        if x == "invest":
            return True
        return False



    
    def ischanged(self,x):
        # global pastButton
        print(self.pastButton,x)
        if x != self.pastButton:
            self.pastButton = x
            return True
        else:
            return False



    # Tab select view
    @app.callback(
        Output("tab-content", "children"),
        [Input("tabs", "active_tab")],
    )
    def render_tab_content(self,active_tab, data=1):
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


def getLayout(user):
    global username
    username = user

    return html.Div(content)