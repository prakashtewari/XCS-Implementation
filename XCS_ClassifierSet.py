"""
Name: XCS_Classifier.py
Author: Ryan Urbanowicz - written at Dartmouth College, Hanover, NH, USA 
Note: Code primarily based on python XCS authored by Jose Antonio Martin H. <jamartin@dia.fi.upm.es> tranlated from a version by Martin V. Butz (in Java 1.0) 
Contact: ryan.j.urbanowicz@darmouth.edu
Created: 3/20/2009
Updated: 10/15/2013
Description: This class handles the different sets of classifiers. It stores each set in an array. The array is initialized to a sufficient large size so 
that no changes in the size of the array will be necessary. The class provides constructors for constructing the empty population, the match set, and the 
action set. It executes a GA in a set and updates classifier parameters of a set.  Moreover, it provides all necessary different sums and averages of 
parameters in the set.  Finally, it handles addition, deletion and subsumption of classifiers.
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
from XCS_Classifier import *
from XCS_Environment import *
import sys
from random import *

class XClassifierSet:
    def __init__(self,a=None,b=None,c=None,d=None, e=None):
        """ Creates a new classifier, see init1(), init2() , init3() for more details. """
        
        self.parentSet=None
        self.clSet=[]
        self.numerositySum = 0.0
        # Added for Evaluation Print-out
        self.attributeGenList = 0.0
        self.generality = 0.0
        self.weightedGenerality = 0.0
        
        if isinstance(a,int) and b==None and c==None and d==None and e==None:
            self.init1(a)
        elif isinstance(a,list) and isinstance(b,XClassifierSet):
            self.init2(a,b,c,d,e)
        elif isinstance(a,XClassifierSet):
            self.init3(a,b)
        elif isinstance(a,str) and isinstance(b,list) and isinstance(c,XClassifierSet):
            self.init4(a,b,c)


    def init1(self, numberOfActions):
        """ Creates a new, empty population initializing the population array to the maximal population size plus the number of possible actions.
        @param numberOfActions The number of actions possible in the problem. """
        
        self.numerositySum = 0
        self.parentSet     = None

        
    def init2(self,state, pop, time, numberOfActions, maxPopSize):
        """ Constructs a match set out of the population. After the creation, it is checked if the match set covers all possible actions
        in the environment. If one or more actions are not present, covering occurs, generating the missing action(s). If maximal
        population size is reached when covering, deletion occurs.
        @param state The current situation/problem instance.
        @param pop The current population of classifiers.
        @param time  The actual number of instances the XCS learned from so far.
        @param numberOfActions The number of actions possible in the environment. """
        
        self.parentSet     = pop
        self.numerositySum = 0
        
        actionCovered = [False for i in range(numberOfActions)]

        for i in range(len(pop.clSet)):
            cl = pop.clSet[i]
            if cl.match(state):
                self.addClassifier(cl)
                actionCovered[cl.getAction()] = True

        while True: #Check if each action is covered. If not -> generate covering XClassifier and delete if the population is too big
            again=False
            for i in range(len(actionCovered)):
                if not actionCovered[i]:
                    newCl = XClassifier(self.numerositySum+1, time, state, i)
                    self.addClassifier(newCl)
                    pop.addClassifier(newCl)

            while pop.numerositySum > maxPopSize:
                cdel = pop.deleteFromPopulation()
                # Update the current match set in case a classifier was deleted out of that and redo the loop if now another action is not covered in the match set anymore.
                pos = self.containsClassifier(cdel)
               
                if cdel != None and pos != -1:
        		    self.numerositySum = self.numerositySum - 1
        		    if cdel.getNumerosity()==0:
            			self.removeClassifier(pos)
            			if not self.isActionCovered(cdel.getAction()):
            			    again = True
            			    actionCovered[cdel.getAction()] = False
            if not again:
                break
       

    def init3(self, matchSet, action):
        """ Constructs an action set out of the given match set.
        @param matchSet The current match set
        @param action The chosen action for the action set. """
        
        self.parentSet     = matchSet
        self.numerositySum = 0
        for i in range(len(matchSet.clSet)):
            if matchSet.clSet[i].getAction() == action:
                self.addClassifier(matchSet.clSet[i])
        
        
    def init4(self, special, state, pop):
        """ Added to original XCS to allow for a non-destructive match set to be created for evaluation purposes. """
        
        self.parentSet = pop
        self.numerositySum = 0
               
        for i in range(len(pop.clSet)):
            cl = pop.clSet[i]
            if cl.match(state):
                self.addClassifier(cl)

        
    def containsClassifier(self,clP):
        """ Returns the position of the classifier in the set if it is present and -1 otherwise. Modified for python lists. """ 
           
        try:
            return self.clSet.index(clP)
        except ValueError:
            return -1

        
    def isActionCovered(self, action):
        """ Returns if the specified action is covered in this set. """
        
        for cl in self.clSet:
            if cl.getAction() == action:
                return True
        return False


    def updateSet(self,maxPrediction, reward, doActionSetSubsumption):
        """ Updates all parameters in the current set (should be the action set).
        Essentially, reinforcement Learning as well as the fitness evaluation takes place in this set.
        Moreover, the prediction error and the action set size estimate is updated. Also,
        action set subsumption takes place if selected. As in the algorithmic description, the fitness is updated
        after prediction and prediction error. However, in order to be more conservative the prediction error is
        updated before the prediction.
        @param maxPrediction The maximum prediction value in the successive prediction array (should be set to zero in single step environments).
        @param reward The actual resulting reward after the execution of an action. """
        
        P = reward + cons.gamma*maxPrediction
        for cl in self.clSet:
            cl.increaseExperience()
            cl.updatePreError(P)
            cl.updatePrediction(P)
            cl.updateActionSetSize(self.numerositySum)

        self.updateFitnessSet()
        if doActionSetSubsumption:
            self.doActionSetSubsumption()

        
    def updateFitnessSet(self):
        """ Special function for updating the fitness of the classifiers in the set. """

        accuracySum=0.0
        accuracies = []

        #First, calculate the accuracies of the classifier and the accuracy sums
        i = 0
        for cl in self.clSet:
            accuracies.append(cl.getAccuracy())
            accuracySum = accuracySum + accuracies[i]*cl.getNumerosity()
            i = i + 1

        #Next, update the fitness accordingly
        for i in range(self.getSize()):
            self.clSet[i].updateFitness(accuracySum, accuracies[i])

        
    def runGA(self, time, state, numberOfActions, maxPopSize, doGASubsumption, selection):
        """ The Genetic Discovery in XCS takes place here. If a GA takes place, two classifiers are selected
        by roulette wheel selection, possibly crossed and mutated and then inserted.
        @param time  The actual number of instances the XCS learned from so far.
        @param state  The current situation/problem instance.
        @param numberOfActions The number of actions possible in the environment. """
        
        # Don't do a GA if the theta_GA threshold is not reached, yet
        if self.getSize()==0 or (time-self.getTimeStampAverage()) < cons.theta_GA:
            return
    
        self.setTimeStamps(time)
        
        if selection == 0:
            fitSum =self.getFitnessSum()
            # Select two XClassifiers with roulette Wheel Selection
            cl1P = self.selectXClassifierRW(fitSum)
            cl2P = self.selectXClassifierRW(fitSum)
        else:
            cl1P = self.selectXClassifierT()
            cl2P = self.selectXClassifierT()
  
        cl1  = XClassifier(cl1P)
        cl2  = XClassifier(cl2P)
    
        changed = cl1.twoPointCrossover(cl2)
        if changed:
            cl1.setPrediction((cl1.getPrediction() + cl2.getPrediction())/2.0)
            cl1.setPredictionError(cons.predictionErrorReduction * (cl1.getPredictionError() + cl2.getPredictionError())/2.0)
            cl1.setFitness(cons.fitnessReduction * (cl1.getFitness() + cl2.getFitness())/2.0)
            cl2.setPrediction(cl1.getPrediction())
            cl2.setPredictionError(cl1.getPredictionError())
            cl2.setFitness(cl1.getFitness())
        else:   # ensure that the fitness discount is still applied for having run the GA at all
            cl1.setFitness(cons.fitnessReduction * cl1.getFitness())
            cl2.setFitness(cons.fitnessReduction * cl2.getFitness())
                        
        cl1.applyMutation(state, numberOfActions)
        cl2.applyMutation(state, numberOfActions)
   
        self.insertDiscoveredXClassifiers(cl1, cl2, cl1P, cl2P, maxPopSize, doGASubsumption)


    # ROULETTE WHEEL SELECTION    #this implementation has been tested to work correctly.
    def selectXClassifierRW(self,fitSum):
        """ Selects one classifier using roulette wheel selection according to the fitness of the classifiers. """
        
        choiceP = random()*fitSum
        i=0
        sum = self.clSet[i].getFitness()
        while choiceP>sum:
            i=i+1
            sum = sum + self.clSet[i].getFitness()
        return self.clSet[i]


    # TOURNAMENT SELECTION
    def selectXClassifierT(self):
        """  Selects one classifier using tournament selection according to the fitness of the classifiers. """
        
        actionSetSize = len(self.clSet) 
        tSize = int(actionSetSize*cons.theta_Select) # sets the number of items in the action set to be included in the tournament selection
        posList = []
        for i in range(tSize): #hold onto a list of random positions, then select the position with the highest fitness
            pos = randrange(actionSetSize)
            if pos in posList: # make sure that pos is a pos that has not yet been selected.
                pos = randrange(actionSetSize)
            else:
                posList.append(pos)
                
        bestF = 0
        bestC = 0
        for j in posList:
            if self.clSet[j].getFitness() > bestF:
                bestF = self.clSet[j].getFitness()
                bestC = j

        return self.clSet[bestC]

        
    def insertDiscoveredXClassifiers(self,cl1, cl2, cl1P, cl2P, maxPopSize, doGASubsumption):
        """ Inserts both discovered classifiers keeping the maximal size of the population and possibly doing GA subsumption.
        @param cl1 The first classifier generated by the GA.
        @param cl2 The second classifier generated by the GA.
        @param cl1P The first parent of the two new classifiers.
        @param cl2P The second classifier of the two new classifiers. """
        
        pop = self
        while pop.parentSet!=None: #This works in Python exactly as in Java
            pop = pop.parentSet;

        if doGASubsumption:
            self.subsumeXClassifier(cl1, cl1P, cl2P)
            self.subsumeXClassifier(cl2, cl1P, cl2P)
        else:
            pop.addXClassifierToPopulation(cl1)
            pop.addXClassifierToPopulation(cl2)

        while pop.numerositySum > maxPopSize:
            pop.deleteFromPopulation()

        
    def subsumeXClassifier(self, cl=None, cl1P=None, cl2P=None):
        """ Tries to subsume a classifier in the parents. If no subsumption is possible it tries to subsume it in the current set. """

        if cl1P!=None and cl1P.subsumes(cl):
            self.increaseNumerositySum(1)
            cl1P.addNumerosity(1)
        elif cl2P!=None and cl2P.subsumes(cl):
            self.increaseNumerositySum(1)
            cl2P.addNumerosity(1)
        else:
            self.subsumeXClassifier2(cl); #calls second subsumeXClassifier

        
    def subsumeXClassifier2(self, cl):
        """ Tries to subsume a classifier in the current set. This method is normally called in an action set.
        If no subsumption is possible the classifier is simply added to the population considering
        the possibility that there exists an identical classifier.
        @param cl The classifier that may be subsumed. """

        #Open up a new Vector in order to chose the subsumer candidates randomly
        choices = []
        for cls in self.clSet:
            if cls.subsumes(cl):
                choices.append(cls)

        if len(choices)>0:
            choice = int(random()*len(choices))
            choices[choice].addNumerosity(1)
            self.increaseNumerositySum(1)
            return

	    #If no subsumer was found, add the classifier to the population
        self.addXClassifierToPopulation(cl)

        
    def doActionSetSubsumption(self):
        """ Executes action set subsumption.  The action set subsumption looks for the most general subsumer classifier in the action set
        and subsumes all classifiers that are more specific than the selected one. """
        
        pop = self
        while pop.parentSet!=None:
            pop=pop.parentSet
        
        subsumer = None
        for cl in self.clSet:
            if cl.isSubsumer():
                if subsumer==None or cl.isMoreGeneral(subsumer):
                    subsumer=cl

        #If a subsumer was found, subsume all more specific classifiers in the action set
        if subsumer!=None:
            i=0
    	    while i<self.getSize():
                if subsumer.isMoreGeneral(self.clSet[i]):
        		    num = self.clSet[i].getNumerosity()
        		    subsumer.addNumerosity(num)
        		    self.clSet[i].addNumerosity((-1)*num)
        		    pop.removeClassifier(self.clSet[i])
        		    self.removeClassifier(i)
        		    i = i - 1
                i = i + 1

        
    def addXClassifierToPopulation(self,cl):
        """ Adds the classifier to the population and checks if an identical classifier exists.
        If an identical classifier exists, its numerosity is increased.
        @param cl The to be added classifier. """

        # set pop to the actual population
        pop=self
        while pop.parentSet!=None:
            pop = pop.parentSet
        oldcl=pop.getIdenticalClassifier(cl)
        
        if oldcl!=None:
            oldcl.addNumerosity(1)
            self.increaseNumerositySum(1)
        else:
            pop.addClassifier(cl)


    def getIdenticalClassifier(self, newCl):
        """ Looks for an identical classifier in the population.
        @param newCl The new classifier.
        @return Returns the identical classifier if found, null otherwise. """

        for cl in self.clSet:
            if newCl.equals(cl):
                return cl
        return None

        
    def deleteFromPopulation(self):
        """ Deletes one classifier in the population.  The classifier that will be deleted is chosen by roulette wheel selection
        considering the deletion vote. Returns the macro-classifier which got decreased by one micro-classifier. """

        meanFitness = self.getFitnessSum()/float(self.numerositySum)
        sum = 0.0
        for cl in self.clSet:
            sum = sum + cl.getDelProp(meanFitness)

        choicePoint = sum*random()
        sum=0.0
        i = 0
        for cl in self.clSet:
            sum = sum + cl.getDelProp(meanFitness)
            if sum > choicePoint:
                cl.addNumerosity(-1)
                self.numerositySum = self.numerositySum-1
                if cl.getNumerosity()==0:
		           self.removeClassifier(i)

                return cl
            i = i + 1

        return None

        
    def confirmClassifiersInSet(self):
        """ Updates the numerositySum of the set and deletes all classifiers with numerosity 0. """
        
        borrados = 0
    	for cl in self.clSet[:]:
    	    if cl.getNumerosity()==0:
    	        self.clSet.remove(cl)
    	        borrados = borrados  + 1
            else:
                self.numerositySum = self.numerositySum + cl.getNumerosity()

        
    def setTimeStamps(self, time):
        """ Sets the time stamp of all classifiers in the set to the current time. The current time
        is the number of exploration steps executed so far.
        @param time The actual number of instances the XCS learned from so far. """
        
        for cl in self.clSet:
            cl.setTimeStamp(time)

        
    def addClassifier(self, classifier):
        """ Adds a classifier to the set and increases the numerositySum value accordingly.
        @param classifier The to be added classifier. """

        self.clSet.append(classifier)
        self.addValues(classifier)
       
        
    def addValues(self,cl):
        """ Increases the numerositySum value with the numerosity of the classifier. """
        self.numerositySum = self.numerositySum + cl.getNumerosity()

        
    def increaseNumerositySum(self, nr):
        """ Increases recursively all numerositySum values in the set and all parent sets.
        This function should be called when the numerosity of a classifier in some set is increased in
        order to keep the numerosity sums of all sets and essentially the population up to date. """
        
        self.numerositySum = self.numerositySum + nr
        if self.parentSet != None:
            self.parentSet.increaseNumerositySum(nr)


    def removeClassifier(self,param=None):
        """ Overloaded method see removeClassifier1(classifier), removeClassifier2(pos)"""

        # This is -only one- of the various python ways of implementing overloaded methods.
        if isinstance(param,XClassifier):
            self.removeClassifier1(param)
        else:
            self.removeClassifier2(param)
        
        
    def removeClassifier1(self, classifier):
        """ Removes the specified (possible macro-) classifier from the population.
        The function returns true when the classifier was found and removed and false
        otherwise. It does not update the numerosity sum of the set, neither
        recursively remove classifiers in the parent set. This must be done manually where required.
        Hard modified for Pythonic way of doing things with lists. """
        
        try:
            self.clSet.remove(classifier)
            return True
        except ValueError:
            raise
            
        
    def removeClassifier2(self,pos):
        """ Removes the (possible macro-) classifier at the specified array position from the population.
        The function returns true when the classifier was found and removed and false
        otherwise. It does not update the numerosity of the set, neither
        recursively remove classifiers in the parent set. This must be done manually where required.
        Hard modified for Pythonic way of doing things with lists. """
        
        try:
            del self.clSet[pos]
        except IndexError:
            raise
        return True

        
    def getPredictionSum(self):
        """ Returns the sum of the prediction values of all classifiers in the set. """
        
        sum=0.0
        for cl in self.clSet:
            sum = sum + cl.getPrediction() * cl.getNumerosity()
        return sum


        
    def getFitnessSum(self):
        """ Returns the sum of the fitnesses of all classifiers in the set. """
        
        sum=0.0
        for cl in self.clSet:
            sum = sum + cl.getFitness()
        return sum


        
    def getTimeStampSum(self):
        """ Returns the sum of the time stamps of all classifiers in the set. """
        
        sum=0.0
        for cl in self.clSet:
            sum = sum + cl.getTimeStamp() * cl.getNumerosity()
        return sum


    def getNumerositySum(self):
        """ Returns the number of micro-classifiers in the set. """
        return self.numerositySum

        
    def getSize(self):
        """ Returns the number of macro-classifiers in the set. """
        return len(self.clSet)  # true size

        
    def getTimeStampAverage(self):
        """ Returns the average of the time stamps in the set. """
        return self.getTimeStampSum()/self.numerositySum
    
    
    def CSAnalysis(self,env): 
        """ Characterizes the current classifier set """
        # Creates the attribute Generality List
        bitLength = env.getAttributeLength()
        wildCount = self.characterizePop()
        self.attributeGenList = self.condenseToAttributes(wildCount,bitLength) 
        
        genSum = 0
        fitGenSum = 0
        fitSum = 0       
        for cl in self.clSet:
            genSum = genSum + cl.getClassifierGenerality() * cl.getNumerosity()
            fitGenSum = fitGenSum + cl.getClassifierGenerality() * cl.getNumerosity() * cl.getFitness()
            fitSum = fitSum + cl.getNumerosity() * cl.getFitness()
            
        self.generality = genSum / float(self.numerositySum)
        self.weightedGenerality = fitGenSum / float(fitSum)

        
    def getGenerality(self):
        """  Returns the generality of the rule-set. """
        return self.generality


    def getWeightGenerality(self):
        """ Returns the generality of the rule-set. """
        return self.weightedGenerality    
                     
                     
    def printCSEvaluation(self, pW, trainEval, testEval, learnSec, env, CVPartition):
        """ Prints all information on the Classifier Set evaluation to the designated output file object """
        #Segregate into two parts - Learning Characterisitcs and Pop Characteristics
        trainaccuracy = trainEval[0]
        traintotalError = trainEval[1]
        trainNoMatchFrq = trainEval[2]
        
        testaccuracy = testEval[0]
        testtotalError = testEval[1]
        testNoMatchFrq = testEval[2]
                
        pW.write("Performance Stats:\n")
        pW.write("Training_Accuracy\tTesting_Accuracy\tAverage_Training_Error\tAverage_Testing_Error\tNoMatchFreq_Train\tNoMatchFreq_Test\tLearningTime(min)\n")
        pW.write(str(trainaccuracy)+"\t")
        if CVPartition > 1:
            pW.write(str(testaccuracy)+"\t")
        else:
            pW.write("NA\t")
        pW.write(str(traintotalError) +"\t")
        if CVPartition > 1:
            pW.write(str(testtotalError)+"\t")
        else:
            pW.write("NA\t") 
        pW.write(str(trainNoMatchFrq) +"\t")            
        if CVPartition > 1:
            pW.write(str(testNoMatchFrq)+"\t")
        else:
            pW.write("NA\t")
        pW.write(str(learnSec/60)+"\n"+"\n")
        
        pW.write("Population Characterization:\n")   
        pW.write("MacroPopSize\tMicroPopSize\tGenerality\tWeightedGenerality\tAveragePrediction\tAverageFitness\n") 
        pW.write(str(len(self.clSet))+"\t"+ str(self.numerositySum)+"\t"+str(self.generality)+"\t"+str(self.weightedGenerality)+"\t"+str(self.getPredictionSum()/self.numerositySum)+"\t"+str(self.getFitnessSum()/self.numerositySum)+"\n")

        pW.write("WildSum\n")
        headList = env.getHeaderList()
        for i in range(len(headList)-1):    # Added the -1 to get rid of the Class Header
            if i < len(headList)-2:
                pW.write(str(headList[i])+"\t")
            else:
                pW.write(str(headList[i])+"\n")
                
        # Prints out the Gen Count for each attribute
        for i in range(len(self.attributeGenList)):
            if i < len(self.attributeGenList)-1:
                pW.write(str(self.attributeGenList[i])+"\t")
            else:
                pW.write(str(self.attributeGenList[i])+"\n")        
        
        pW.write("Ruleset Population: \n")
        pW.write("Condition\tAction\tPrediction\tPredictionError\tFitness\tNumerosity\tExperience\tActionSetSize\tTimeStamp\tGenerality\n")
        for cl in self.clSet:
            cl.printXClassifier(pW)
        

    def characterizePop(self):
        """ Sums up the #'s within all conditions. """
        condition = []
        countList = []
        for i in range(len(self.clSet[0].getCondition())):  #Over length of a binary code condition
            countList.append(int(0))   # makes an empty countList
            
        for cl in self.clSet:
            condition = cl.getCondition()
            for j in range(len(condition)):    #for each character string in the condition
                if condition[j] == '#':
                    countList[j] +=1
        
        return countList
    
    
    def condenseToAttributes(self, tempList, bitLength):
        """ Takes the results of the above method and condenses the values down to a "per attribute" value. """
        temp = 0
        newList = []
        for i in range(len(tempList)):
            if (i+1)%int(bitLength) != 0:  #first run it will be 1
                temp = temp + tempList[i]
            else:
                newList.append(temp + tempList[i])
                temp = 0
        return newList
                    
