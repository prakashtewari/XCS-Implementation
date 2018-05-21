# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 10:34:11 2018

@author: Prakash.Tiwari

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
from XCS_GHEnvironment import *
from XCS import *
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
                dcc.Input(id='input-2', type = 'text', value = 500),
                
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
                dcc.Upload(
                        id = 'upload-data',
                        children = html.Div([                      
                    'Drag and Drop or ',
                    html.A('Select a File')]),
                    style={
                        'width': '30%',
                        'height': '50px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center'
                        }),
                #dcc.Upload(html.Button('Upload File')),
                html.Div(id='output-data-upload'),
                html.Div(dt.DataTable(rows=[{}]),
                         style={'display': 'none'}),
                
               
                html.Br(),  
               
                
#                html.Label('upload-data', title = 'Enter first data'),
#                dcc.Input(id='filename', value = 'Data1.txt'),
                
                
                #Button for running on training data
                html.Button('Run XCS algo', id='button-1'),
                html.Div(id='run-xcs-button'),

#                html.Br(),
#                html.Label('upload-new-data', title = 'Enter new data'),
#                dcc.Input(id='newData', value = 'Data2.txt'),
                html.Br(),  
                
                #Loading Data for training the model
                dcc.Upload(
                        id = 'upload-data-new',
                        children = html.Div([                      
                    'Drag and Drop or ',
                    html.A('Select a File')]),
                    style={
                        'width': '30%',
                        'height': '50px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center'
                        }),

                #dcc.Upload(html.Button('Upload File')),
                html.Div(id='output-data-upload-new'),
                html.Div(dt.DataTable(rows=[{}]),
                         style={'display': 'none'}),
                
                html.Br(),
                html.Button('Update XCS algo', id='button-2'),
                html.Div(id='update-xcs-button'),
                html.Br(),
                
                #Export Files - Log, Rule Population, Iteration performances
                html.Button('Export files - Log/Rule Pop/Iteration Results', id='button-3'),
                html.Div(id='export-files-button'),
                html.Br()           
                     
                ]
            )


@app.callback(
    Output('export-files-button', 'children'),
    [Input('button-3', 'n_clicks')])
def XCS_Export(n_clicks):
    
    while n_clicks >0:
        pd.DataFrame(result, index = [0]).to_csv(u'Export\Results.csv')
        pd.read_csv()
        return html.Div('Accuracy file is exported.')
        
        
              
def parse_data(contents, filename):
    
    print filename
    
    try:
        if 'csv' or 'txt' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(filename, sep = '\t', nrows = 10)
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
              [Input('upload-data', 'contents'),
              Input('upload-data', 'filename')
              ])
def print_output(contents, filename):
    if contents is not None:
        # do something with contents
        children = [parse_data(contents, filename)]
        print filename
        print 'processed data from file ' + filename
        #print contents
        return children
    else:
        return 'no contents'
    
@app.callback(Output('output-data-upload-new', 'children'),
              [Input('upload-data-new', 'contents'),
              Input('upload-data-new', 'filename')
              ])
def print_output_new(contents, filename):
    if contents is not None:
        # do something with contents
        children = [parse_data(contents, filename)]
        print filename
        print 'processed data from file ' + filename
        #print contents
        return children
    else:
        return 'no contents'    


"""
XCS Results
"""
#
global result
result = {}

@app.callback(
    Output('run-xcs-button', 'children'),
    [Input('button-1', 'n_clicks'),
     Input('upload-data', 'filename')
     ],
    state=[State('input-1', 'value'),
           State('input-2', 'value'),
           State('input-3', 'value')
           #,State('filename', 'value')
           ]
           )
def XCS_Run(n_clicks, filename, input1, input2 , input3 ):
    
    while n_clicks> 0:

        print 'n_clicks = '+str(n_clicks) +'\n'
        print 'filename = '+ str(filename) +'\n'
        print 'input1/reward = '+str(input1) +'\n'
        print 'input2/Pop size= '+str(input2) +'\n'
        print 'input3/GA algo = '+str(input3) +'\n'
        
        #trainData = 'Data1.txt'#"2_1000_0_1600_0_0_CV_0_Train.txt" 
        #trainData = "Data1.txt"
        trainData =filename   
        #input1, input2, input3, input4 = 1000, 200, 0, 0
        graphPerformance = False
        testData = "2_1000_0_1600_0_0_CV_0_Test.txt"
        outProg = "FirstDataTrack"
        outPop = "PopulationOutput"
        outNew = "NewDataTrack"
        bitLength = 1    
        reward = input1 
        #reward = 1000
        CVpartitions = 2
        iterInput = '5000'
        #trackCycles = 'Default' # set tracking cycles to number of data samples - trackCycles = 100 
        trackCycles = '100'#100
        pop = input2 
        #pop = 200
        sub = 0
        select = input3
        #select = 0
        
        #Figure out the iteration stops for evaluation, and the max iterations.
        iterList = iterInput.split('.')
        for i in range(len(iterList)):
            iterList[i] = int(iterList[i])
        lastIter = iterList[len(iterList)-1]
        
        #Sets up up algorithm to be run.
        e = GHEnvironment(trainData,testData,bitLength,reward)
        sampleSize = e.getNrSamples()
        
        global xcs    
        xcs = XCS(e, outProg, outNew, outPop, bitLength, CVpartitions, graphPerformance)
    
        #Set some XCS parameters.
        if trackCycles == 'Default':
            xcs.setTrackingIterations(sampleSize)
        else:
            xcs.setTrackingIterations(trackCycles)
        xcs.setNumberOfTrials(lastIter,iterList)
        xcs.setPopulationSize(pop)
        xcs.setSubsumption(sub)
        xcs.setSelection(select)      
    
        print '\n Running XCS implementation for n_clicks = {}'.format(n_clicks)+ ' \n'
        print 'trainData '.format(trainData)

        xcs.runXCS() 
        print  xcs.test_output
        global result
        result['{}'.format(trainData)] = xcs.test_output[0][1]
        
        print 'Result {}'.format(result)
    
        trace = go.Bar(
        x = list(result.keys()),
        y = list(result.values())
            )
        
        layout = go.Layout(
                width = 800, 
                height = 400,
                title = 'XCS implementation',
                xaxis = dict( title ='Data Used'), 
                yaxis = dict( title ='Accuracy on test data in %'))
        fig = go.Figure(data = [trace], layout = layout)
        #accuracy = [xcs.test_output[0][1]]
        
        return dcc.Graph(
                id = 'run-xcs',
                figure = fig)
         

@app.callback(
    Output('update-xcs-button', 'children'),
    [Input('button-2', 'n_clicks'),
     Input('upload-data-new', 'filename')
     ],
    state=[State('input-1', 'value'),
           State('input-2', 'value'),
           State('input-3', 'value')
           #,State('newData', 'value')
           ]
           )
def XCS_Update(n_clicks, filename, input1, input2 , input3 ):
    
    while n_clicks >0:      

        print 'n_clicks = '+str(n_clicks) +'\n'
        print 'input1/reward = '+str(input1) +'\n'
        print 'input2/Pop size= '+str(input2) +'\n'
        print 'input3/GA algo = '+str(input3) +'\n'
        print 'NewData {}'.format(filename)
        
        #trainData = 'Data1.txt'#"2_1000_0_1600_0_0_CV_0_Train.txt" 
        #trainData = "Data1.txt"
        trainData = filename
        
        #input1, input2, input3, input4 = 1000, 200, 0, 0
        graphPerformance = False
        testData = "2_1000_0_1600_0_0_CV_0_Test.txt"
        outProg = "FirstDataTrack"
        outPop = "PopulationOutput"
        outNew = "NewDataTrack"
        bitLength = 1    
        reward = input1 
        #reward = 1000
        CVpartitions = 2
        iterInput = '5000'
        #trackCycles = 'Default' # set tracking cycles to number of data samples - trackCycles = 100 
        trackCycles = '500'#100
        pop = input2 
        #pop = 200
        sub = 0
        select = input3
        #select = 0
        
        #Figure out the iteration stops for evaluation, and the max iterations.
        iterList = iterInput.split('.')
        for i in range(len(iterList)):
            iterList[i] = int(iterList[i])
        lastIter = iterList[len(iterList)-1]
        
    
        print '\n Running New XCS implementation for n_clicks = {}'.format(n_clicks)+ ' \n'
        
        #print 'XCS Test Output from first run {}'.result['filename %c'%trainData] +'\n'
    
        global xcs
        xcs.updateXCS(trainData)
        print 'XCS Test Output from n_clicks = {}'.format(n_clicks) + ' is {}'.format(xcs.test_output)
        
        global result
        result['{}'.format(trainData)] = xcs.test_output[i+1][1]
        
        print 'Result {}'.format(result)
        print '\n For Graph \n'
        
        print '\n n_clicks = {}'.format(n_clicks)
        print '\n accuracy = {}'.format(result['{}'.format(trainData)])
        
        trace = go.Bar(
                x = list(result.keys()),
                y = list(result.values())
                )
        layout = go.Layout(
                width = 800, 
                height = 400,
                title = 'XCS implementation',
                xaxis = dict( title ='Data Used'), 
                yaxis = dict( title ='Accuracy on test data in %'))
        
        fig = go.Figure(data = [trace],
                        layout = layout)
        #return (html.H4(str(XCS_func(1,1))))
        
        return dcc.Graph(
                        id = 'run-xcs',
                        figure= fig
                        )
       





if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)



