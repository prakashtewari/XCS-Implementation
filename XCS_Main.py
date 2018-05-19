# -*- coding: utf-8 -*-
"""
Created on Wed May 02 22:23:01 2018

@author: Prakash.Tiwari
"""
#Import modules
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

def XCS_Start(n_clicks, input1, input2 , input3 , filename):
    
    while n_clicks > 0:
        print 'n_clicks = '+str(n_clicks) +'\n'
        print 'filename = '+ str(filename) +'\n'
        print 'input1/reward = '+str(input1) +'\n'
        print 'input2/Pop size= '+str(input2) +'\n'
        print 'input3/GA algo = '+str(input3) +'\n'
        
        #input1, input2, input3, input4 = 1000, 200, 0, 0
        graphPerformance = False
        trainData =filename
        #trainData = 'Data1.txt'#"2_1000_0_1600_0_0_CV_0_Train.txt" #"Data1.txt"
        testData = "2_1000_0_1600_0_0_CV_0_Test.txt"
        outProg = "FirstDataTrack"
        outPop = "PopulationOutput"
        outNew = "NewDataTrack"
        bitLength = 1    
        reward = input1
        CVpartitions = 2
        iterInput = '500'
        #trackCycles = 'Default' # set tracking cycles to number of data samples - trackCycles = 100 
        trackCycles = '100'#100
        pop = input2 #200
        sub = 0
        select = input3
        
        #Figure out the iteration stops for evaluation, and the max iterations.
        iterList = iterInput.split('.')
        for i in range(len(iterList)):
            iterList[i] = int(iterList[i])
        lastIter = iterList[len(iterList)-1]
        
        #Sets up up algorithm to be run.
        e = GHEnvironment(trainData,testData,bitLength,reward)
        sampleSize = e.getNrSamples()
        
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

    
        if n_clicks == 1:
            print '\n Running XCS implementation for n_clicks = {}'.format(n_clicks)+ ' \n'
    
            xcs.runXCS() 
            print  xcs.test_output
            accuracy = [xcs.test_output[0][1]]
    
            return dcc.Graph(
                            id='XCS-run',
                            figure={
                                    'data': [
                                            go.Bar(
                                                    x=[0],
                                                    y=accuracy
                                                    )
                                            ],
                                    'layout': 
                                        go.Layout(
                                            title = 'Implementation of XCS',
                                            xaxis = dict(title = 'Implementation Number',
                                                         range= [0,n_clicks+1],
                                                         zeroline=True,
                                                         zerolinecolor='#969696',
                                                         zerolinewidth=4,
                                                         autorange = False),
                                            yaxis = dict(title = 'Accuracy on testing data',
                                                         tickformat= ',.1%',
                                                         range = [0,1],
                                                         zeroline=True,
                                                         zerolinecolor='#969696',
                                                         zerolinewidth=4
                                                         ),
                                           margin = dict(l = 100, b= 40, t= 0, r= 40)
                                                )
                                    }
                            )
            
        #elif n_clicks >1:
            #xcs.runXCS() 
    #        accuracy = [xcs.test_output[0][1]]
        if n_clicks > 1:
            print '\n Running XCS implementation for n_clicks = {}'.format(n_clicks)+ ' \n'
                        
            newData= filename
            print 'newData' + str(newData) +'is uploaded \n'                     
            
            xcs.runXCS() 
            accuracy = [xcs.test_output[0][1]]
    
            print 'XCS Test Output from first run {}'.format(xcs.test_output) +'\n'
    
            for i in range(n_clicks-1):
                xcs.updateXCS(newData)
                print 'XCS Test Output from n_clicks = {}'.format(n_clicks) + 'is {}'.format(xcs.test_output)
                updated_accuracy = [xcs.test_output[i+1][1]]
                accuracy.extend(updated_accuracy)
            
            print '\n For Graph \n'
            
            print '\n n_clicks = {}'.format(n_clicks)
            print '\n accuracy = {}'.format(accuracy)
            
            
            #return (html.H4(str(XCS_func(1,1))))
            return dcc.Graph(
                            id='XCS-run',
                            figure={
                                    'data': [
                                            go.Bar(
                                                    x=range(n_clicks+1),
                                                    y=accuracy 
                                                    )
                                            ],
                                     'layout':
                                         go.Layout(
                                            title = 'Implementation of XCS',
                                            xaxis = dict(title = 'Implementation Number',
                                                         range= [0,n_clicks+1],
                                                         zeroline=True,
                                                         zerolinecolor='#969696',
                                                         zerolinewidth=4
                                                         ),
                                            yaxis = dict(title = 'Accuracy on testing data',
                                                         tickformat= ',.1%',
                                                         range = [0,1],
                                                         zeroline=True,
                                                         zerolinecolor='#969696',
                                                         zerolinewidth=4),
                                            margin = dict(l = 100, b= 40, t= 0, r= 40)
                                                )
                                    }
                            )
