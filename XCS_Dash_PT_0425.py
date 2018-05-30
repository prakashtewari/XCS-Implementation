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
                #input-reward --> input-reward
                html.Label('Reinforcement Reward', title = 'What is the reinforcement reward for each correct prediction?'),
                dcc.Input(id='input-reward', type = 'number', value = 1000),

                #input-rule-pop --> input-rule-pop
                html.Br(),
                html.Label('Rule Population', title = 'What is the maximum number of rules to be generated?'),
                dcc.Input(id='input-rule-pop', type = 'text', value = 200),
                
                #input-GA --> input-GA
                html.Br(),
                html.Label('Genetic Algoritm', title = 'Which genetic algorithm to use?'),
                dcc.Dropdown(id='input-GA',
                             options = [
                                     {'label': 'Roulette Wheel', 'value': 0},
                                     {'label': 'Tournament', 'value': 1}
                                     ],
                             value = 0),
                
                #input-learning-cycle --> input-learning-cycle           
                html.Br(),
                html.Label('Learning cycle', title = 'Enter learning cycles (separated by dot)'),
                dcc.Input(id='input-learning-cycle', type = 'text', value = '20000'),
                                
                html.Hr(),

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
                html.Div(dt.DataTable(rows=[{}])),
                         #style={'display': 'none'}),
                
               
                html.Br(),  
               
                
#                html.Label('upload-data', title = 'Enter first data'),
#                dcc.Input(id='filename', value = 'Data1.txt'),
                
                
                #Button for running on training data
                html.Button('Run XCS algo', id='button-run'),
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
                html.Div(dt.DataTable(rows=[{}])),
                         #style={'display': 'none'}),
                
                html.Br(),
                html.Button('Update XCS algo', id='button-update'),
                html.Div(id='update-xcs-button'),
                html.Br(),
                
                #Button for testing accuracy
                html.Button('Test Accuracy', id='button-test-accuracy'),
                html.Div(id='xcs-test-accuracy'),
                
                #Export Files - Log, Rule Population, Iteration performances
                html.Button('Export files - Log/Rule Pop/Iteration Results', id='button-export'),
                html.Div(id='export-files-button'),
                html.Br()           
                     
                ]
            )

   

                        
"""
XCS Results
"""

#
global result
result = {}
      
###################
## Callback functions        
###################

@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents'),
              Input('upload-data', 'filename')
              ])
def print_output(contents, filename):
    """
    Callback Function to print the output of the uploaded data. 
    Calls parse_data to return the output
    """
    return [parse_data(contents, filename)]

    
@app.callback(Output('output-data-upload-new', 'children'),
              [Input('upload-data-new', 'contents'),
              Input('upload-data-new', 'filename')
              ])
def print_output_new(contents, filename):
    """
    Callback Function to print the output of the uploaded data. 
    Calls parse_data to return the output
    """
    return [parse_data(contents, filename)]

@app.callback(
    Output('export-files-button', 'children'),
    [Input('button-export', 'n_clicks')],
    state=[State('input-learning-cycle', 'value')]
    )
def XCS_Export(n_clicks, value):
    """
    Callback Function to export the Result file and Rule population. 
    Executed from the button and takes input the iteration Input
    """
    
    while n_clicks >0:
        pd.DataFrame(result, index = [0]).to_csv(u'Export\Results.csv')
        print 'Accuracy file exported'
        #Figure out the iteration stops for evaluation, and the max iterations.
        iterList, lastIter = iterFunc(value)
    
        txtToExcel(textData = 'PopulationOutput.%d.txt'%lastIter , excelData = 'Export\PopulationOutput_%d_run.xlsx'%n_clicks , excelSheet = '%d_run'%n_clicks)
        print 'Rule population exported'
        return html.Div('Accuracy and rule population files are exported.') 

@app.callback(
    Output('run-xcs-button', 'children'),
    [Input('button-run', 'n_clicks'),
     Input('upload-data', 'filename')
     ],
    state=[State('input-reward', 'value'),
           State('input-rule-pop', 'value'),
           State('input-GA', 'value'),
           State('input-learning-cycle', 'value')
           #,State('filename', 'value')
           ]
           )
def XCS_Run(n_clicks, filename, input1, input2 , input3, input4 ):
    """
    Callback Function to run the xcs algorithm for the first time
    XCS is a global object which will be executed upon clicking of the 'Run XCS algo' button in the UI
    Returns a dictionary containing accuracy on the testing data
    """  
    while n_clicks> 0:
        
        print 'n_clicks = '+str(n_clicks) +'\n'
        
        outProg, outNew, outPop, bitLength, CVpartitions, graphPerformance, iterList, lastIter, sub, testData, trackCycles = XCS_parameters(filename, input1, input2, input3, input4)
        
        #Sets up up algorithm to be run.
        e = GHEnvironment(inFileString = filename ,  testFileString= testData, attLength = bitLength, reward = input1)
        sampleSize = e.getNrSamples()
        
        global xcs    
        xcs = XCS(e, outProg, outNew, outPop, bitLength, CVpartitions, graphPerformance)
    
        #Set some XCS parameters.
        if trackCycles == 'Default':
            xcs.setTrackingIterations(sampleSize)
        else:
            xcs.setTrackingIterations(trackCycles)
        xcs.setNumberOfTrials(lastIter,iterList)
        xcs.setPopulationSize(popsize = input2)
        xcs.setSubsumption(subsumption = sub)
        xcs.setSelection(selection = input3)      
    
        print '\n Running XCS implementation for n_clicks = {}'.format(n_clicks)+ ' \n'

        xcs.runXCS() 
        print  xcs.test_output

        global result
        result['{}'.format(filename)] = xcs.test_output[0][1]*100
        
        print 'Result {}'.format(result)
    
        return html.Div('XCS algorithm trained for the first time. \n Click the below button to test accuracy')
    
               
@app.callback(
    Output('xcs-test-accuracy', 'children'),
    [Input('button-test-accuracy', 'n_clicks')
     ]
    )
def XCS_test_accuracy(n_clicks):
    """
    Callback Function to test the accuracy of XCS algorithm
    Results is a global object - updated everytime the algorithm is run or updated. 
    Returns a graph containing accuracy.
    """  
    global result

    print 'Result {}'.format(result)

    trace = go.Bar(
            x = list(result.keys()),
            y = list(result.values())
            )
    
    layout = go.Layout(
            width = 800, 
            height = 400,
            title = 'XCS implementation',
            titlefont = dict(family = 'Courier New, monospace', size = 20, color = '#7f7f7f'),
            margin = dict( l = 100, r = 100),
            xaxis = dict( title ='Data Used'), 
            yaxis = dict( title ='Accuracy on test data in %'))
    fig = go.Figure(data = [trace], layout = layout)
    
    return dcc.Graph(
                    id = 'run-xcs',
                    figure = fig)
    
    
@app.callback(
    Output('update-xcs-button', 'children'),
    [Input('button-update', 'n_clicks'),
     Input('upload-data-new', 'filename')
     ],
    state=[State('input-reward', 'value'),
           State('input-rule-pop', 'value'),
           State('input-GA', 'value'),
           State('input-learning-cycle', 'value')
           #,State('newData', 'value')
           ]
           )
def XCS_Update(n_clicks, filename, input1, input2 , input3, input4 ):
    """
    Callback Function to update the xcs algorithm. 
    XCS is a global object which will be updated upon clicking of the 'Update XCS algo' button in the UI
    Returns a dictionary containing accuracy on the testing data
    """
    
    while n_clicks >0:           
        
        outProg, outNew, outPop, bitLength, CVpartitions, graphPerformance, iterList, lastIter, sub, testData, trackCycles = XCS_parameters(filename, input1, input2, input3, input4)
        
        print '\n Running New XCS implementation for n_clicks = {}'.format(n_clicks)+ ' \n'
        
        global xcs
        xcs.updateXCS(filename)
        print 'XCS Test Output from n_clicks = {}'.format(n_clicks) + ' is {}'.format(xcs.test_output)
        
        global result
        result['{}_{}'.format(filename, n_clicks)] = xcs.test_output[n_clicks][1]*100
        
        print 'Result {}'.format(result)
        print '\n accuracy = {}'.format(result['{}_{}'.format(filename, n_clicks)])
        
        return html.Div('XCS algorithm updated. \n Click the below button to test accuracy')


###################
## Static functions        
###################

def iterFunc(iterInput):
    """
    Function to iterate over learning cycles and save it in a list    
    """
    
    iterList = iterInput.split('.')
    for i in range(len(iterList)):
        iterList[i] = int(iterList[i])
    lastIter = iterList[len(iterList)-1]
    
    return iterList, lastIter


#text to excel converter
def txtToExcel(textData, excelData, excelSheet):     
    """
    Function to export text output in an excel format
    """
       
    datasetList = []
    try:
        f = open(textData, 'r')
        headerList = f.readline().split('\t')   #strip off first row
        for line in f:
            lineList = line.strip('\n').split('\t')
            datasetList.append(lineList)
        f.close()
    
    except:
        print ("Unexpected error:", sys.exc_info()[0])
        raise
    
    df = pd.DataFrame(datasetList)
        
    try:      
        # open existing workbook
        book = load_workbook(excelData)
        writer = pd.ExcelWriter(excelData, engine='openpyxl')
        writer.book = book
        df.to_excel(writer, excelSheet)
        writer.save()
    except:
        df.to_excel(excelData, excelSheet)        
  
#parsing text data            
def parse_data(contents, filename):
    """
    Function to parse the content of a text file and return in a DataTable format
    """
    if contents is not None:
        
        print filename
        print 'processed data from file ' + filename
    
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
            dt.DataTable(rows=df.to_dict('records'),
                         # optional - sets the order of columns
                         columns=list(df.columns)),
    
            #dt.VirtualizedTable(df),
            html.Hr(),  # horizontal line
    
            # For debugging, display the raw contents provided by the web browser
            html.Div('Raw Content of the file'),
            html.Pre(contents[0:10] + '...', style={
                'whiteSpace': 'pre-wrap',
                'wordBreak': 'break-all'
            })
        ])
    else:
        return 'no contents'

def XCS_parameters(filename, input1, input2, input3, input4):
    """
    Function to pass the XCS parameters. 
        Can be passed in a better way
    """     
    print 'input1/reward = '+str(input1) +'\n'
    print 'input2/Pop size= '+str(input2) +'\n'
    print 'input3/GA algo = '+str(input3) +'\n'
    print 'input4/Learning cycles = '+str(input4) +'\n'
    print 'NewData {}'.format(filename)
    
        #trainData = 'Data1.txt'#"2_1000_0_1600_0_0_CV_0_Train.txt" 
    #trainData = "Data1.txt"
        
    #input1, input2, input3, input4 = 1000, 200, 0, 0
    graphPerformance = False
    testData = "2_1000_0_1600_0_0_CV_0_Test.txt"
    outProg = "FirstDataTrack"
    outNew = "NewDataTrack"
    outPop = "PopulationOutput"
    bitLength = 1    
    reward = input1 
    #reward = 1000
    CVpartitions = 2
    iterInput = input4
    #iterInput = '5000'
    #trackCycles = 'Default' # set tracking cycles to number of data samples - trackCycles = 100 
    trackCycles = '1000'#100
    pop = input2 
    #pop = 200
    sub = 0
    select = input3
    #select = 0
    
    #Figure out the iteration stops for evaluation, and the max iterations.
    iterList, lastIter = iterFunc(iterInput)
    
    return outProg, outNew, outPop, bitLength, CVpartitions, graphPerformance, iterList, lastIter, sub, testData, trackCycles
    
    
if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)
