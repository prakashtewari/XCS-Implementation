# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 10:34:11 2018

@author: Prakash.Tiwari
Steps  -
a. Run code from line top till 100 to get first version of the model
b. To update the model run next two lines 
c. To update the model again run next two lines 
d. Visualisation Part - Updated

"""
#!/usr/bin/env python
import pandas as pd
import os
from random import randint
import pandas as pd
import functools
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import datetime
os.chdir(r'C:\Work\Daily Tasks\Machine Learning Udemy\iAgent\Urbanwicz_XCS_PT')

#Import modules
from XCS_Main import XCS_Start

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
from dash.dependencies import Input, Output, Event, State
import plotly
import numpy as np
from random import randint
import plotly.graph_objs as go
import base64

"""
GUI Part
"""
app = dash.Dash()

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions']=True

image_filename = 'iAgentImage.jpg' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app.layout = html.Div([
        
                html.H1('iAgent @Work'),
                
                html.Img(src='data:image/jpg;base64,{}'.format(encoded_image), width = 100, title = 'iAgent'),
                html.Br(),
                
                html.Hr(), 
                               
                html.H3('Select iAgent parameters'),
                
                html.Label('Reinforcement Reward', title = 'What is the reinforcement reward for each correct prediction?'),
                dcc.Input(id='input-1', type = 'number', value = 1000),

                html.Br(),
                html.Label('Rule Population', title = 'What is the maximum number of rules to be generated?'),
                dcc.Input(id='input-2', type = 'text', value = 200),
                
                html.Br(),
                html.Label('Genetic Algoritm', title = 'Which genetic algorithm to use?'),
                dcc.Dropdown(id='input-3',
                             options = [
                                     {'label': 'Roulette Wheel', 'value': 0},
                                     {'label': 'Tournament', 'value': 1}
                                     ],
                             value = 0),
                
                html.Br(),
                
                #Loading Data for training the model
#                html.Label('Upload Data'),    
#                dcc.Upload(
#                    id='upload-data-1',
#                    children=html.Div([
#                        html.A('Select Files')
#                    ]),
#                style={
#                    'width': '10%',
#                    'height': '80px',
#                    'lineHeight': '60px',
#                    'borderWidth': '1px',
#                    'borderStyle': 'dashed',
#                    'borderRadius': '5px',
#                    'textAlign': 'center',
#                    'margin': '10px'
#                        },
#                # Allow multiple files to be uploaded
#                    multiple=False
#                ),
#                html.Div(id='output-data-upload'),
#                html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'}),
                
               
                html.Br(),
                html.Label('Upload data'),
                dcc.Input(id='filename', type = 'text'),
                
                html.Br(),
                #Button for running on training data
                html.Button('Run XCS algo', id='button-1'),
                html.Div(id='run-xcs-button'),
                
                html.Br(),
                
                html.Br(),
                html.Button('Updated XCS algo', id='button-2'),
                html.Div(id='update-xcs-button'),
                html.Br(),
                
                #Export Files - Log, Rule Population, Iteration performances
                html.Button('Export files - Log/Rule Pop/Iteration Results', id='button-3'),
                html.Div(id='export-files-button'),
                html.Br()           
                     
                ]
            )
              
def parse_data(filename):
    
    print filename
    
    try:
        if 'csv' or 'txt' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(filename, sep = '\t')
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(filename)
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        
        # Use the DataTable prototype component:
        # github.com/plotly/dash-table-experiments
        dt.DataTable(rows=df.to_dict('records')),

        #dt.VirtualizedTable(df),
        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:10] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])
                        


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data-1', 'filename')])
def print_output(filename):
    if filename is not None:
        children = [
            parse_data(filename) ]
        return children

#@app.callback(Output('output-data-upload2', 'children'),
#              [Input('upload-data-2', 'filename')])
#def upload_data(filename):
#    if filename is not None:
#        return str(filename                   
    
@app.callback(
    Output('run-xcs-button', 'children'),
    [Input('button-1', 'n_clicks')
     ],
    state=[State('input-1', 'value'),
           State('input-2', 'value'),
           State('input-3', 'value'),
           State('filename', 'value')
           ]
           )
def XCS_Start1(n_clicks, input1, input2 , input3 , filename):

    return XCS_Start(n_clicks, input1, input2 , input3 , filename)

if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)

