import dash
from app import app
from dash.dependencies import Input, Output,State
from dash.exceptions import PreventUpdate
from dash import callback_context as ctx

import dash_editor_components

import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
import importlib

from tradingStrategies.backtest import BackTest
# val = "apply filters"*100

template = open("assets/templateCode.py",'r').read()
fileName = html.Div("fileName.py",id="filename",contentEditable="true",style={'height':'5%','marginBottom':'1%'})
# print(template)
ide = dbc.Textarea(value=template,contentEditable="true",spellCheck="true",id="code",
          style={'height':'90%',"width":'100%','fontFamliy':"monospace",'color':'crimson'},
              className="border border-success")

# ide = dash_editor_components.PythonEditor(children=template,id="code",className="row card card-body h-95",  )

# -------------- Filters -----------
stockDataAvailable = [{'label':i.split('.')[0],'value':i.split('.')[0]} for i in 
os.listdir("./data/stockData/daily") if i.split('.')[1] == 'csv']

dp = dcc.Dropdown(id='stockdropdown', options=stockDataAvailable,
            value = None,placeholder="select stock", style={  'color': 'black',
                                      'background-color': 'white',} )
sma_list = [5,10,20,46,50,100]
sma = dcc.Dropdown(multi=True,id="smaDropdown",placeholder="select filters",
  options = [{'label':i,'value':i} for i in sma_list],className="w-100 ")

filters = html.Div([dbc.Row(
    [html.Div(dp,className="col-6 p-0"),
    html.Div(sma,className="col-6 p-0")],className="mb-1"
  ),
  dbc.Row([
    dbc.Label("Start date",className="col-3 p-0"),
    dbc.Input(type="date",id="start_date",className="col-3 p-0 "),
    dbc.Label("End date",className="col-3 "),
    dbc.Input(type="date",id="end_date",className="col-3 p-0")],className="mb-1"
  ),

  dbc.Row([dbc.Checklist(id="checkList",options=[{"label":"execute Code ?","value":True}],className="col-3 mr-1"),
    dbc.Button("Run",id="run_code",className=" btn btn-success float float-right ")])

])

status = dbc.Alert("status is working",color="success",id="status",className="row",
                  dismissable=True)

options = dbc.Container([status,filters],className="border border-primary col-5 ",
          style={"overflow": 'auto',"height":'45vh','padding':'2%'})


codeEditor = html.Div([fileName,ide], className = "border border-info m-0 pl-1 col-7", 
          style = {"height":'45vh',"overflow": 'auto'})

# chart = html.Div("chart section",className="border border-danger row",style = {"height":'35vh'})

chart = dcc.Graph(id='stockChart_bot',figure={},className="border border-danger row",style = {"height":'35vh'})






layout = html.Div([ html.Div([codeEditor,options],className="row h-60"),
        chart],className="col border border-success w-100 mt-0 mp-0 h-100")

# ------ important functions -----

def create_figure(name,df,xCol,yCol,**kwargs):
    fig = px.line(  df,x=xCol, y=yCol,
                                    # title=f'{name} Chart',
                                    **kwargs
                                  )
    fig.update_layout(margin=dict(l=0,r=0,t=0,b=0),paper_bgcolor="LightSteelBlue")
    return fig

#----- callbacks ---------

@app.callback([
  Output("status",'children'),
  Output('status','is_open'),
  Output('stockChart_bot','figure')],
  [Input("run_code","n_clicks")],
  [State("stockdropdown",'value'),
  State("smaDropdown","value"),
  State("start_date",'value'),
  State("end_date",'value'),
  State("checkList",'value'),
  State("code",'value'),
  State("filename","children")])
def updateChart(btn,stock,sma_value,start_date,end_date,check,code,filename):
  if btn == None:
    print("update chart prevent update")
    raise PreventUpdate
  else:
    
    if stock == None:
      return "Please select a stock name",True,{}

    df = pd.read_csv(f"./data/stockData/daily/{stock}.csv")
    if start_date is not None:
      df = df[df.timestamp >= start_date]
    if end_date is not None:
      df = df[df.timestamp <= end_date]
    yCol = ['close']
    if sma_value is not None:
      for smaV in sma_value:
        df["sma-"+str(smaV)] = df["close"].rolling(window=smaV).mean()
        yCol.append('sma-'+str(smaV))
    
    # print(check)
    
    if check!=None and len(check) > 0:
      loc = "./tradingStrategies/tempScripts/"
      F = open(loc+filename,'w')
      # print("code is ",code)
      F.write(code)
      F.close()
      print("code successfully saved @ ",loc)

      try:
        module = importlib.import_module('tradingStrategies.tempScripts.'+filename.split('.')[0])
        module = importlib.reload(module)
        scriptFunction = module.run
        df.reset_index(drop=True,inplace=True)
        df_otpt = pd.DataFrame(scriptFunction(df))
        df_temp = pd.concat([df,df_otpt],axis=1)
        # print(df_temp)
        fig = create_figure(stock,df_temp,'timestamp',yCol   )
        
        buyData = df_temp[df_temp['actions']=='buy']
        fig.add_trace(go.Scatter(name='buy',mode='markers',x=buyData['timestamp'],y=buyData['close'],
        marker={'size':10}))

        sellData = df_temp[df_temp['actions']=='sell']
        
        fig.add_trace(go.Scatter(name='sell',mode='markers',x=sellData['timestamp'],y=sellData['close'],
        marker={'size':10}))
        return "",False,fig
      except Exception as e:
        return str(e),True,{}
    else:
      fig = create_figure(stock,df,'timestamp',yCol)
      return "",False,fig
