"""
Name: XCS_Classifier.py
Author: Ryan Urbanowicz - written at Dartmouth College, Hanover, NH, USA 
Note: Code primarily based on python XCS authored by Jose Antonio Martin H. <jamartin@dia.fi.upm.es> tranlated from a version by Martin V. Butz (in Java 1.0) 
Contact: ryan.j.urbanowicz@darmouth.edu
Created: 3/20/2009
Updated: 10/15/2013
Description: Each instance of this class represents one classifier. The class provides different constructors for generating copies of existing classifiers, 
new matching classifiers with random action, new matching classifiers with specified action, and new completely random classifier.  It handles classifier 
mutation and crossover and provides, sets, and updates parameters.  Moreover, it handles all types of comparisons between different classifiers.
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
from random import *

class XClassifier:
    def __init__(self,a=None,b=None,c=None,d=None):
        """ Overloaded constructor see init1() init2() init3() init4()
        Constructs a classifier based on the type of the arguments. """
        
        self.condition          = []
        self.action             = 0
        self.prediction         = 0.0
        self.predictionError    = 0.0
        self.fitness            = 0.0
        self.numerosity         = 1.0
        self.experience         = 0.0
        self.actionSetSize      = 1.0
        self.timeStamp          = 0.0
        
        self.attCombList = []
        self.attCombos = cons.attributeCombos
        for i in range(self.attCombos):
            self.attCombList.append(str(i))
            
        if isinstance(c,list):
            self.init1(a,b,c,d)
        elif isinstance(d,list):
            self.init2(a,b,c,d)
        elif isinstance(b,int) and isinstance(c,int) and isinstance(d,int):
            self.init3(a,b,c,d)
        elif isinstance(a,XClassifier):
            self.init4(a)
        else:
            raise NameError('XClassifier unknown init params:')

        
    def init1(self, setSize,  time,  situation,  act):
        """ Constructs a classifier with matching condition and specified action.
        @param setSize The size of the current set which the new classifier matches.
        @param time  The actual number of instances the XCS learned from so far.
        @param situation The current problem instance/perception.
        @param act The action of the new classifier. """
        
    	self.createMatchingCondition(situation)
    	self.action = act
    	self.classifierSetVariables(setSize, time)

    
    def init2(self, setSize,  time,  numberOfActions,  situation):
        """ Construct matching classifier with random action.
        @param setSize The size of the current set which the new classifier matches.
        @param time The actual number of instances the XCS learned from so far.
        @param numberOfActions The number of different actions to chose from (This should be set to the number of actions possible in the problem).
        @param situation The current problem instance/perception.  
        NOT USED IN THE CURRENT IMPLEMENTATION """

    	self.createMatchingCondition(situation)
    	self.createRandomAction(numberOfActions)
    	self.classifierSetVariables(setSize, time)

        
    def init3(self, setSize, time, condLength, numberOfActions):
        """ Construct a classifier with random condition and random action.
        @param setSize The size of the current set which the new classifier matches.
        @param time  The actual number of instances the XCS learned from so far.
        @param condLength The length of the condition of the new classifier.
        @param numberOfActions The number of different actions to chose from. """
        
    	self.createRandomCondition(condLength)
    	self.createRandomAction(numberOfActions)
    	self.classifierSetVariables(setSize, time)

        
    def init4(self,clOld):
        """  Constructs an identical XClassifier.  However, the experience of the copy is set to 0 and the numerosity 
        is set to 1 since this is indeed a new individual in a population.
        @param clOld The to be copied classifier. """

    	self.condition       = clOld.condition[:] # a copy of the condition not the same reference
    	self.action          = clOld.action
    	self.prediction      = clOld.prediction
    	self.predictionError = clOld.predictionError

        #Here we should divide the fitness by the numerosity to get a accurate value for the new one!
    	self.fitness       = clOld.fitness / clOld.numerosity
    	self.numerosity    = 1
    	self.experience    = 0
    	self.actionSetSize = clOld.actionSetSize
    	self.timeStamp     = clOld.timeStamp

        
    def createRandomCondition(self,condLength):
        """ Creates a condition randomly considering the constant <code>P_dontcare<\code>. """
        
        condArray = []
    	for i in range(condLength):
    	    if random() < cons.P_dontcare:
    	        condArray.append(cons.dontCare)
    	    else:
                condArray.append(choice(self.attCombList))
    	self.condition = condArray

        
    def createMatchingCondition(self,cond):
        """ Creates a matching condition considering the constant <code>P_dontcare<\code>. """

    	condLength = len(cond)
    	condArray  = []
        for i in range(condLength):
            if random() < cons.P_dontcare:
                condArray.append(cons.dontCare)
    	    else:
    	        condArray.append(cond[i])
    	self.condition = condArray
  
        
    def createRandomAction(self, numberOfActions):
        """ Creates a random action.
        @param numberOfActions The number of actions to chose from. 
        NOT USED IN CURRENT IMPLEMENTAION """
    	action = int(random()*numberOfActions)

        
    def classifierSetVariables(self, setSize, time):
        """ Sets the initial variables of a new classifier.
        @param setSize The size of the set the classifier is created in.
        @param time The actual number of instances the XCS learned from so far. """

    	self.prediction      = cons.predictionIni
    	self.predictionError = cons.predictionErrorIni
    	self.fitness         = cons.fitnessIni

    	self.numerosity      = 1
    	self.experience      = 0
    	self.actionSetSize   = setSize
    	self.timeStamp       = time

        
    def match(self, state):
        """ Returns if the classifier matches in the current situation.
        @param state The current situation which can be the current state or problem instance. """
        
    	if len(self.condition) != len(state):
    	    return False
    	for i in range(len(self.condition)):
    	    if self.condition[i] != cons.dontCare and self.condition[i]!=state[i]:
    	        return False;
    	return True

	
    def twoPointCrossover(self,cl):
        """ Applies two point crossover and returns if the classifiers changed.
        @param cl The second classifier for the crossover application. """

    	changed = False;
    	if random() < cons.pX:
    	    length = len(self.condition)
    	    sep1   = int(random()*(length))
    	    sep2   = int(random()*(length)) + 1
    	    if sep1>sep2:
        		help1 = sep1
        		sep1 = sep2
        		sep2 = help1

    	    elif sep1==sep2:
    		  sep2= sep2+1

    	    cond1 = self.condition[:]
    	    cond2 = cl.condition
            for i in range(sep1,sep2):
        		if cond1[i] != cond2[i]:
        		    changed = True
        		    help2   = cond1[i]
        		    cond1[i]= cond2[i]
        		    cond2[i]= help2

    	    if changed:
        		self.condition = cond1
        		cl.condition   = cond2

    	return changed
  
        
    def applyMutation(self, state, numberOfActions):
        """ Applies a niche mutation to the classifier.
        This method calls mutateCondition(state) and mutateAction(numberOfActions) and returns
        if at least one bit or the action was mutated.
        @param state The current situation/problem instance
        @param numberOfActions The maximal number of actions possible in the environment. """
        
        # All changed references are currently not used in mutateCondition mutateAction or applyMutation
        changed = self.mutateCondition(state)
    	if self.mutateAction(numberOfActions):
    	    changed = True
    	return changed


        
    def mutateCondition(self, state):
        """ Mutates the condition of the classifier. If one allele is mutated depends on the constant pM.
        This mutation is a niche mutation. It assures that the resulting classifier
        still matches the current situation.
        @param state The current situation/problem instance.  """

    	changed    = False
    	condLength = len(self.condition)
        cond   = self.condition[:]
        
    	for i in range(condLength):
    	    if random() < cons.pM:
                changed= True
                if cond[i]==cons.dontCare:
        		    cond[i] = state[i]
                else:
        		    cond[i] = cons.dontCare

        self.condition = cond
    	return changed

	
    def mutateAction(self, numberOfActions):
        """ Mutates the action of the classifier.
        @param numberOfActions The number of actions/classifications possible in the environment. """

    	changed = False

    	if random() < cons.pM:
            act = int(random()*numberOfActions)
            while act==self.action:
                act = int(random()*numberOfActions)

            self.action = act
    	    changed= True
    	return changed


    def equals(self, cl):
        """ Returns if the two classifiers are identical in condition and action.
        @param cl The classifier to be compared. """

    	if cl.condition==self.condition:
    	    if cl.action == self.action:
    		  return True
        return False


    def subsumes(self, cl):
        """ Returns if the classifier subsumes cl.
        @param The new classifier that possibly is subsumed. """
        
    	if cl.action == self.action:
    	    if self.isSubsumer() and self.isMoreGeneral(cl):
    		    return True
    	return False


    def isSubsumer(self):
        """ Returns if the classifier is a possible subsumer. It is affirmed if the classifier
        has a sufficient experience and if its reward prediction error is sufficiently low.  """
        
    	if self.experience > cons.theta_sub  and self.predictionError < cons.epsilon_0:
    	    return True
    	return False

        
    def isMoreGeneral(self,cl):
        """ Returns if the classifier is more general than cl. It is made sure that the classifier is indeed more general and
        not equally general as well as that the more specific classifier is completely included in the more general one (do not specify overlapping regions)
        @param The classifier that is tested to be more specific. """

    	ret    = False
    	length = len(self.condition)
    	for i in range(length):
    	    if self.condition[i] != cons.dontCare and self.condition[i] != cl.condition[i]:
    	        return False
    	    elif self.condition[i] !=  cl.condition[i]:
    	        ret = True
    	return ret

        
    def getDelProp(self, meanFitness):
        """  Returns the vote for deletion of the classifier.
        @param meanFitness The mean fitness in the population. """
        
    	if self.fitness/self.numerosity >= cons.delta*meanFitness or self.experience < cons.theta_del:
    	    return self.actionSetSize*self.numerosity

        return self.actionSetSize * self.numerosity*meanFitness / ( self.fitness/self.numerosity)


    def updatePrediction(self, P):
        """  Updates the prediction of the classifier according to P.
        @param P The actual Q-payoff value (actual reward + max of predicted reward in the following situation). """

    	if self.experience < 1.0 / cons.beta:
    	    self.prediction = (self.prediction * (self.experience - 1) + P) / float(self.experience)
    	else:
    	    self.prediction = self.prediction + cons.beta * (P - self.prediction)

    	return self.prediction * self.numerosity

  
    def updatePreError(self, P):
        """ Updates the prediction error of the classifier according to P.
        @param P The actual Q-payoff value (actual reward + max of predicted reward in the following situation). """

    	if  self.experience < 1.0/cons.beta :
    	    self.predictionError = (self.predictionError*(self.experience - 1) + abs(P - self.prediction)) / float(self.experience)
    	else:
    	    self.predictionError = self.predictionError +  cons.beta * (abs(P - self.prediction) - self.predictionError)

    	return self.predictionError*self.numerosity
  
        
    def getAccuracy(self):
        """ Returns the accuracy of the classifier.
        The accuracy is determined from the prediction error of the classifier using Wilson's
        power function as published in 'Get Real! XCS with continuous-valued inputs' (1999) """
        
    	if self.predictionError <= cons.epsilon_0:
    	    accuracy = 1.0
    	else:
    	    accuracy = cons.alpha * ( (self.predictionError / cons.epsilon_0)**(-cons.nu) )

    	return accuracy

        
    def updateFitness(self, accSum, accuracy):
        """ Updates the fitness of the classifier according to the relative accuracy.
        @param accSum The sum of all the accuracies in the action set
        @param accuracy The accuracy of the classifier. """

    	self.fitness = self.fitness + cons.beta * ((accuracy * self.numerosity) / float(accSum) - self.fitness)
    	return self.fitness #fitness already considers numerosity

        
    def updateActionSetSize(self, numerositySum):
        """  Updates the action set size.
        @param numeriositySum The number of micro-classifiers in the population. """

    	if self.experience < 1.0/cons.beta:
    	    self.actionSetSize = (self.actionSetSize * (self.experience-1)+ numerositySum) / float(self.experience)
    	else:
    	    self.actionSetSize = self.actionSetSize + cons.beta * (numerositySum - self.actionSetSize)

    	return self.actionSetSize * self.numerosity

        
    def getAction(self):
        """  Returns the action of the classifier. """
    	return self.action
 
 
    def getCondition(self):
        """ Returns the condition of the classifier. """
        return self.condition
        
        
    def increaseExperience(self):
        """ Increases the Experience of the classifier by one. """
    	self.experience = self.experience + 1

  
    def getPrediction(self):
        """ Returns the prediction of the classifier. """
    	return self.prediction

    
    def setPrediction(self,new_predition):
        """ Sets the prediction of the classifier.
        @param new_predition The new prediction of the classifier. """
        
    	self.prediction=new_predition
    
        
    def getPredictionError(self):
        """ Returns the prediction error of the classifier. """
    	return self.predictionError

        
    def setPredictionError(self,preE):
        """ Sets the prediction error of the classifier.
        @param preE The new prediction error of the classifier. """
    	self.predictionError=preE

        
    def getFitness(self):
        """ Returns the fitness of the classifier. """
        return self.fitness

        
    def setFitness(self, fit):
        """  Sets the fitness of the classifier.
        @param fit The new fitness of the classifier. """
    	self.fitness=fit

    
    def getNumerosity(self):
        """ Returns the numerosity of the classifier. """
    	return self.numerosity

        
    def addNumerosity(self, num):
        """ Adds to the numerosity of the classifier.
        @param num The added numerosity (can be negative!). """
    	self.numerosity = self.numerosity + num


    def getClassifierGenerality(self):
        """ Calculates and returns the fraction of bits that infer generality (that have a wild card symbol) """
        
        genCount = 0
        condLength = len(self.condition)
        for x in self.condition:
            if str(x) == cons.dontCare:
                genCount += 1
        classifierGenerality = genCount/float(condLength)
        return classifierGenerality
           
    
    def getTimeStamp(self):
        """ Returns the time stamp of the classifier. """
        return self.timeStamp
    
    
    def setTimeStamp(self, ts):
        """ Sets the time stamp of the classifier.
        @param ts The new time stamp of the classifier. """
    	self.timeStamp = ts


    def __str__(self):
        """ the string represetation of the classifier
        used for printin purposed (usefull for debugin) """
        return str(self.condition)+"\t"+str(self.action)+"\t"+str(self.prediction)+"\t"+str(self.predictionError)+"\t"+str(self.fitness)+"\t"+str(self.numerosity)+"\t"+str(self.experience)+"\t"+str(self.actionSetSize)+"\t"+str(self.timeStamp)
        

    def printXClassifier(self, pW):
        """ Prints the classifier to the print writer (normally referencing a file).
        The method prints condition action prediction predictionError fitness numerosity experience actionSetSize timeStamp.
        @param pW The writer to which the classifier is written. """
        
        gen = self.getClassifierGenerality()
        for x in self.condition:
            pW.write(x)
        pW.write("\t"+str(self.action)+"\t"+str(self.prediction)+"\t"+str(self.predictionError)+"\t"+str(self.fitness)+"\t"+str(self.numerosity)+"\t"+str(self.experience)+"\t"+str(self.actionSetSize)+"\t"+str(self.timeStamp)+"\t"+str(gen)+"\n") 
