"""
Name: XCS_PredictionArray.py
Author: Ryan Urbanowicz - written at Dartmouth College, Hanover, NH, USA 
Note: Code primarily based on python XCS authored by Jose Antonio Martin H. <jamartin@dia.fi.upm.es> tranlated from a version by Martin V. Butz (in Java 1.0) 
Contact: ryan.j.urbanowicz@darmouth.edu
Created: 3/20/2009
Updated: 10/15/2013
Description: This class generates a prediction array of the provided set. The prediction array is generated according to Wilson's Classifier Fitness 
Based on Accuracy (Evolutionary Computation Journal, 1995).  Moreover, this class provides all methods to handle selection in the prediction array, 
essentially, to select the best action, a present random action or an action by roulette wheel selection.
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
from XCS_Constants import *
from XCS_ClassifierSet import *
import sys
import random

class XCSPredictionArray:
    def __init__(self, set, size):
        """ Constructs the prediction array according to the current set and the possible number of actions. 
        @param set The classifier set out of which a prediction array is formed (normally the match set).
        @param size The number of entries in the prediction array (should be set to the number of possible actions in the problem) """
    	self.pa = [0.0 for i in range(size)] #The prediction array.
    	self.nr = [0.0 for i in range(size)] #The sum of the fitness of classifiers that represent each entry in the prediction array.

        for cl in set.clSet: # check each classifier in the set (different actions)
    	    self.pa[cl.getAction()] += (cl.getPrediction()*cl.getFitness())   # Fitness weighted average of predictions 1/20/09 Made slight change to coding
    	    self.nr[cl.getAction()] += cl.getFitness()

    	for i in range(size):
    	    if self.nr[i]!=0:
    		  self.pa[i] = self.pa[i]/self.nr[i]
    	    else:
    		  self.pa[i]=0.0  # if an action is not represented than it's prediction is set to zero.

        
    def getBestValue(self):
        """ Returns the highest value in the prediction array. """
        return max(self.pa)
    
        
    def getValue(self, i):
        """ Returns the value of the specified entry in the prediction array. """
    	if i>=0 and i<len(self.pa):
    	    return self.pa[i]
    	return -1.0


    ##*************** Action selection functions ****************
    def randomActionWinner(self):
        """ Selects an action randomly. The function assures that the chosen action is represented by at least one classifier. """
    	ret=0
    	while True:
    	    ret = int(random.random()*len(self.pa)) 
    	    if self.nr[ret]!=0:
    	        break
    	return ret
    

    def bestActionWinner(self):
        """ Selects the action in the prediction array with the best value.
         *MODIFIED so that in the case of a tie between actions - an action is selected randomly between the tied highest actions. """
        highVal = 0.0
        for i in self.pa:
            if i > highVal:
                highVal = i
        bestIndexList = []
        for i in range(len(self.pa)):
            if self.pa[i] == highVal:
                bestIndexList.append(i)
        return random.choice(bestIndexList)

        
    def rouletteActionWinner(self):
        """ Selects an action in the prediction array by roulette wheel selection. """
    	bidSum = sum(self.pa) * XCSConstants.random()
    	bidC=0.0
    	i = 0
    	while bidC<bidSum:
    	    bidC = bidC + self.pa[i]
            i = i + 1
        return i

