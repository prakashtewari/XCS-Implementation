"""
Name: XCS_GHEnvironment.py
Author: Ryan Urbanowicz - written at Dartmouth College, Hanover, NH, USA 
Note: Code primarily based on python XCS authored by Jose Antonio Martin H. <jamartin@dia.fi.upm.es> tranlated from a version by Martin V. Butz (in Java 1.0) 
Contact: ryan.j.urbanowicz@darmouth.edu
Created: 3/20/2009
Updated: 10/15/2013
Description: This class implements the Genetic Heterogeneity Classification Problem.  It loads an dataset containing strings with attribute and class 
values, determines if a classification was correct, and which payoff is provided. A hybrid of the Maze and MP environments.  Takes the file handling from 
the Maze environment and the reward and function fundamentals from the MPEnvironment



Methohds - 

1.INIT
2. MakeEnvironment
3. SWITCHTOTESTING
4. RESETDATACOUNT
5. RESETSTATE 
6. EXECE


---------------------------------------------------------------------------------------------------------------------------------------------------------
XCS Version 1.0: A Python implementation of the XCS learning classifier system algorithm implemented for SNP genetic data mining and classification tasks.
Copyright (C) 2013 Ryan Urbanowicz 
This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the 
Free Software Foundation; either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABLILITY 
or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, 
Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
---------------------------------------------------------------------------------------------------------------------------------------------------------
"""



#!/usr/bin/env python

#Import modules
from XCS_Environment import *
from XCS_Constants import *
import random
import sys

class GHEnvironment(Environment):
    #In the Multiplexer problem there are two classifications possible!
    nrActions=2
        
    def __init__(self, inFileString, testFileString, attLength, reward):
        """ Initialize environment objects. """

        self.headerList = []
        self.datasetList = []
        self.numAttributes = 0  # Saves the number of attributes in the input file.
        self.numSamples = 0
        self.classPosition = 0
        self.currentState = []
        self.currentClass = None
        self.dataCount = 0
        self.correct = False
        self.reset = False
        self.formatedDataset = []    
        self.attributeCombos = 3
        XCSConstants.setEConstants(self.attributeCombos)
        
        self.maxPayoff = reward
        self.attributeLength = attLength
        self.testFileString = testFileString  
        
        # Calls a method to open the training file and initialize the environment according to that data.
        self.makeEnvironment(inFileString)    
        #***********************************************************************
        
    
    def makeEnvironment(self,dataset):   
        """ Formats the input data into a data set nested list object. 
        PT updated - Removed shuffling 
        """
        
        SNP0 = []
        SNP1 = []
        SNP2 = []
        
        if self.attributeLength==3:
            SNP0 = ['0','0','1']
            SNP1 = ['0','1','0']
            SNP2 = ['1','0','0']
        elif self.attributeLength==2:
            SNP0 = ['0','0']
            SNP1 = ['0','1']
            SNP2 = ['1','0']  
        elif self.attributeLength==1:
            print "Use Direct Coding"
            SNP0 = ['0']
            SNP1 = ['1']
            SNP2 = ['2']  
        else:
            print "Coding Length out of bounds!"       

        #*******************Initial file handling**********************************************************
        try:       
            f = open(dataset, 'r')
            self.headerList = f.readline().rstrip('\n').split('\t')   #strip off first row
            for line in f:
                lineList = line.strip('\n').split('\t')
                self.datasetList.append(lineList)
            f.close()
            self.numAttributes = len(self.headerList) - 1 # subtract 1 to account for the class column
            self.classPosition = len(self.headerList) - 1    # Could be altered to look for "class" header
            self.numSamples = len(self.datasetList)
            #self.segmentSize = self.numSamples/self.divisions      
                  
        except IOError, (errno, strerror):
            print ("Could not Read File!")
            print ("I/O error(%s): %s" % (errno, strerror))
            raise
        except ValueError:
            print ("Could not convert data to an integer.")
            raise
        except:
            print ("Unexpected error:", sys.exc_info()[0])
            raise
        
        # Build empty matrix for formated data [sample][att]
        for i in range(self.numSamples):  # for each column - one for the attribute data and one for the class
            self.formatedDataset.append([])
        for i in range(self.numSamples):
            self.formatedDataset[i] = [' ', ' ']

        # Fill in the matrix built above with the binary attribute encoding and the binary class value    
        for line in range(len(self.datasetList)):
            codeList = []
            for att in range(self.numAttributes):
                if self.datasetList[line][att] == '0': #might need to be double checked /think thru
                    for j in range(self.attributeLength):
                        codeList.append(SNP0[j])

                if self.datasetList[line][att] == '1':
                    for j in range(self.attributeLength):
                        codeList.append(SNP1[j])

                if self.datasetList[line][att] == '2':
                    for j in range(self.attributeLength):
                        codeList.append(SNP2[j])
            self.formatedDataset[line][0] = codeList
            self.formatedDataset[line][1] = self.datasetList[line][self.classPosition]                         

        #from random import shuffle
        #shuffle(self.formatedDataset)
        
        print ('Data read and number of datapoints read: ' +str(self.getNrSamples()))
        
        self.currentState = self.formatedDataset[self.dataCount][0]
        self.currentClass = self.formatedDataset[self.dataCount][1]
        
        
    def switchToTesting(self):
        """ Makes the data set of focus the testing data, as opposed to the training data. """
        
        self.datasetList = []    
        self.dataCount = 0
        self.formatedDataset = []
        self.makeEnvironment(self.testFileString) 
        
    def switchToNewData(self, newData):
        """ Makes the data set of focus the new update data, as opposed to the training data. """
        self.runNewData = 1
        self.datasetList = []    
        self.dataCount = 0
        self.formatedDataset = []
        self.makeEnvironment(newData) 


    def resetDataCount(self):
        """ Resets the iteration count through the current data set. """
        self.dataCount = 0
        

    def resetState(self):
        """  Changes the state to the next sample input.  Once all of the data has been explored, the order is shuffled and it is explored again. 
        PT updated - Removed shuffling 
        """

        if self.dataCount < (self.numSamples):
            # get the next data point in self.formatedDatasets
            self.currentState = self.formatedDataset[self.dataCount][0]
            self.currentClass = self.formatedDataset[self.dataCount][1]
            self.dataCount += 1
        else:   # This is done so that the training order varies with each epoch.
            self.dataCount = 0
#            from random import shuffle
#            shuffle(self.formatedDataset)

    	self.reset=False
    	return self.currentState

     
    def executeAction(self,action):
        """ Check to see if action prediction is a correct classification.  Use some new self.currentAction to hold on to present environmental action
        Executes the action and determines the reward.
        @param action Specifies the classification. """
        
        reward = 0
        if action == int(self.currentClass):
            reward = self.maxPayoff
            self.correct = True
        else:
            reward = 0
            self.correct = False
            
        self.reset = True
        return reward
  
#-------------------------------------------------------------------------------Methods which might be fine for any type of environment.
    
    def wasCorrect(self):
        """ Returns true if the last executed action was a correct classification."""
        return self.correct
    
     
    def doReset(self):
        """ Returns true after the current problem was classified."""
        return self.reset

        
    def getMaxPayoff(self):
        """ Returns the maximal payoff possible in the current multiplexer problem.
        The maximal payoff is determined out of the payoff type. If the payoff type 1000/0 is selected
        this function will return 1000, otherwise the maximal value depends on the problem size. """
        return self.maxPayoff

        
    def getNrActions(self):
        """ Returns the number of possible actions.
        in the Multiplexer problem there are two classifications possible. """
        return self.nrActions


    def getNrSamples(self):
        """ Returns the number of samples in the dataset being examined. """        
        return self.numSamples
    
    
    def getCurrentState(self):
        """ Returns -a copy- of the current problem state. """
        return self.currentState[:]
    
    
    def getHeaderList(self):
        """ Returns the file header text as a list of elements. """
        return self.headerList
    
    
    def getAttributeLength(self):
        """ Returns the number of possible attribute encodings.  Very specific to this type of environment. """
        return self.attributeLength
