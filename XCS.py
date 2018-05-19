"""
Name: XCS.py
Author: Ryan Urbanowicz - written at Dartmouth College, Hanover, NH, USA 
Note: Code primarily based on python XCS authored by Jose Antonio Martin H. <jamartin@dia.fi.upm.es> tranlated from a version by Martin V. Butz (in Java 1.0) 
Contact: ryan.j.urbanowicz@darmouth.edu
Created: 3/20/2009
Updated: 10/15/2013
Description: XCS algorithm - Initializes the algorithm - Major purpose of modifications allow specification of parameters from command line, as well 
externally controlled cross validation.  This class is the XCS itself. It stores the population and the posed problem. The class provides methods for the 
main learning cycles in XCS distinguishing between single-step and multi-step problems as well as exploration vs. exploitation trials.  Moreover, it 
handles the performance evaluation.
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
import time
from XCS_Environment import *
from XCS_ClassifierSet import *
from XCS_Constants import *
from XCS_PredictionArray import *
#from pylab import * #Used for the graphing method
import copy
#from PyQt4 import QtCore, QtGui
    
class XCS:      
    def __init__(self, e, outFileString, outFileNewString, popOutFileString, bitLength, CVparts, graphPerform):
        """ Constructs the XCS system.  """
        self.env=e
        self.evaluationEnv = None
        #specify output file
        self.outFile = outFileString
        self.outFileNew = outFileNewString
        
        #specify population output file
        self.popFile = popOutFileString
        
        #initialize XCS
        self.pop=None
        self.bitLength = bitLength
        self.trainAccuracy  = 0
        self.trainTotalError  = 0 
        self.testAccuracy  = 0
        self.testTotalError  = 0    
             
        #Used for cross validation cycles
        self.CVpartitions = CVparts
        
        # Track learning time
        self.startLearningTime = 0
        self.endLearningTime = 0
        self.evalTime = 0
        
        self.performanceTrackList = [[0],[0],[0],[0],[0],[0]]
        self.graphPerform = graphPerform
        
        #Test output results
        self.test_output = []
        
        
    def setNumberOfTrials(self, trials, iterList):
        """ Resets the maximal number of learning iterations in an LCS run."""
        self.maxProblems = trials
        self.iterStops = iterList


    def setTrackingIterations(self, cycles):
        """ Resets the paramenters for how often progress tracking is reset and sent to the output file."""
        self.expCy = int(cycles)
        self.expCyMath = float(cycles)
            
            
    def setPopulationSize(self, popsize):
        """ Resets the max population size."""
        self.maxPopSize = int(popsize)
        
        
    def setSubsumption(self, subsumption):    
        """ Turns on or off, the subsumption mechanisms (in both GA and Action set)."""
        self.doGASubsumption = subsumption
        self.doActionSetSubsumption = subsumption
        
        
    def setSelection(self, selection): 
        """Resets the selection type to be used in the GA - either (0)roulette, or (1)tournament."""
        self.selectionType = selection
                
                
    def runXCS(self):
        """ Runs the posed problem with XCS.
        The function essentially initializes the output File and then runs the experiments.
        PT Update -- self.pop = XClassifierSet(self.env.getNrActions()) copied to this function instead of doSingleStepExperiment
        so that, with updateXCS, we can directly use the doSingleStepExperiment function"""
        
        try:
            pW = open(self.outFile+'.txt','w')     
        except IOError, (errno, strerror):
            print ("I/O error(%s): %s" % (errno, strerror))
            raise
        
        self.pop = XClassifierSet(self.env.getNrActions())
        
        self.doSingleStepExperiment(pW)
        print "LCS Training and Evaluation Complete!"
        
        try:
            pW.close()
        except IOError, (errno, strerror):
            print ("I/O error(%s): %s" % (errno, strerror))
            raise    

    def updateXCS(self, newData):
        """ Updates the posed problem with XCS.
        The function starts to run on the NewData 
        The function does not start with a new rule Population but leverages the existing population and builds on top of that
        """
        
        self.env.switchToNewData(newData)  
        
        self.popNew = copy.copy(self.pop)
        
        try:
            pWNew = open(self.outFileNew+'.txt','w')     
        except IOError, (errno, strerror):
            print ("I/O error(%s): %s" % (errno, strerror))
            raise

        self.doSingleStepExperiment(pWNew)
        print "LCS training on new data complete"
        
        try:
            pWNew.close()
        except IOError, (errno, strerror):
            print ("I/O error(%s): %s" % (errno, strerror))
            raise    
                        
            
    def doSingleStepExperiment(self,pW):
        """ Specifies the steps to run the XCS algorithm once through. The method name Experiment is a remnant of how it was originally implemented. """
        # Initialize Population
        #self.pop = XClassifierSet(self.env.getNrActions())
        
        # Initialize Objects 
        explore=0
        bestCorrectPos = 0
        correct  = [0.0 for i in range(self.expCy)] #tracks performance (accuracy of prediction) - collects findings in clusters of 50 data points (same for error)
        sysError = [0.0 for i in range(self.expCy)] #tracks error in reward prediction
        exploreProbC = 0  #Explore problem count - tracks the number of LCS cycles        
        
        pW.write("Explore_Iteration\tPerformance\tError\tGenerality\tWeightedGenerality\tMacroPopSize\n")
        self.startLearningTime = time.time()    #TIMER STARTS
        
        while exploreProbC < self.maxProblems:
            explore = (explore+1)%2
            state = self.env.resetState()    #refers to current input data from environment
            
            if explore != 0:
                self.doOneSingleStepProblemExplore(state, exploreProbC)
            else: # exploit
                self.doOneSingleStepProblemExploit(state, exploreProbC, correct, sysError)

            if (exploreProbC%self.expCy)==(self.expCy-1) and explore==0 and exploreProbC>0:  #evaluate performance every 50 explorations 
                self.pop.CSAnalysis(self.env) 
                self.writePerformance(pW, correct, sysError, exploreProbC+1, self.pop.getGenerality(), self.pop.getWeightGenerality()) 
                    
            exploreProbC = exploreProbC + explore   # only increments every other run(during explore phases)
            
            # MAJOR EVALUATIONS - has to be completely non-disruptive of learning cycles / environment
            # copy environment
            self.evaluationEnv = copy.copy(self.env)
            if self.evaluationEnv is self.env:
                print "Environment Object Error"
            tempTimeA = 0
            tempTimeB = 0
            
            if exploreProbC+1 in self.iterStops and explore == 0:
                self.endLearningTime = time.time()
                tempTimeA = time.time() 
                try:  
                    popW = open(self.popFile + '.'+ str(exploreProbC+1)+'.txt','w')   #New for pop output - now have to open one for each iteration setting
                except IOError, (errno, strerror):
                    print ("I/O error(%s): %s" % (errno, strerror))
                    raise
                
                #Run Evaluation
                trainEval = []
                testEval = []
                if self.CVpartitions > 1: #run CV partitions  
                    print 'Inside iterStops conditions'
                    # Run a complete classification evaluation and have the prediction accuracy saved where the popW is printed.
                    trainEval, trainResult = self.doPopEvaluation()  

                    self.evaluationEnv.switchToTesting()   
                    testEval, testResult = self.doPopEvaluation()  
                    
                    self.test_output.append([exploreProbC, testEval[0]]) 
                    
                else:
                    trainEval, trainResult = self.doPopEvaluation() 
                    testEval, testResult = [0.0,0.0,0.0]   
                    
#                    self.evaluationEnv.switchToNewData()   
#                    newDataEval, newDataResult = self.doPopEvaluation()   

                learnSec = self.endLearningTime - self.startLearningTime - self.evalTime
                self.pop.CSAnalysis(self.evaluationEnv)   # Measures some population characateristics - e.g Generality
                self.pop.printCSEvaluation(popW, trainEval, testEval, learnSec, self.evaluationEnv, self.CVpartitions)
                        
                try:
                    popW.close()  
                except IOError, (errno, strerror):
                    print ("I/O error(%s): %s" % (errno, strerror))
                    raise     
                #TIME TRACKER        
                tempTimeB = time.time() 
                self.evalTime += tempTimeB - tempTimeA      
                     
        
    def doOneSingleStepProblemExplore(self,state, counter):
        """ Executes one main learning loop for a single step problem.
        * @param state The actual problem instance.
        * @param counter The number of problems observed so far in exploration. """

        matchSet        = XClassifierSet(state, self.pop, counter, self.env.getNrActions(), self.maxPopSize)
        predictionArray = XCSPredictionArray(matchSet, self.env.getNrActions())
        actionWinner    = predictionArray.randomActionWinner()  #is this the best way to learn during explore phases? (maybe - this way we can begin to punish bad classifiers for guessing wrong( more exploration)
        actionSet       = XClassifierSet(matchSet, actionWinner)
        reward          = self.env.executeAction(actionWinner)
        actionSet.updateSet(0.0, reward, self.doActionSetSubsumption)
        actionSet.runGA(counter, state, self.env.getNrActions(), self.maxPopSize, self.doGASubsumption, self.selectionType)

        
    def doOneSingleStepProblemExploit(self, state, counter, correct, sysError):
        """ Executes one main performance evaluation loop for a single step problem.
        * @param state The actual problem instance.
        * @param counter The number of problems observed so far in exploration.
        * @param correct The array stores the last fifty correct/wrong exploitation classifications.
        * @param sysError The array stores the last fifty predicted-received reward differences. """
        #NOTE: action set not needed during exploit phase!!
        
        matchSet        = XClassifierSet(state, self.pop, counter, self.env.getNrActions(), self.maxPopSize)
        predictionArray = XCSPredictionArray(matchSet, self.env.getNrActions())
        actionWinner    = predictionArray.bestActionWinner()
        reward          = self.env.executeAction(actionWinner)
    
        if self.env.wasCorrect():
            correct[counter%self.expCy]=1
        else:
            correct[counter%self.expCy]=0
            
        sysError[counter%self.expCy] = abs(reward - predictionArray.getBestValue())


    def doPopEvaluation(self):
        """ Obtains a complete classification evaluation of the specified data set."""
        #Set up for the Evaluation
        dataPoints = self.evaluationEnv.getNrSamples()  #represents the number of iterations
        self.evaluationEnv.resetDataCount()
        correct  = [0.0 for i in range(dataPoints)] #tracks performance (accuracy of prediction) - collects findings in clusters of 50 data points (same for error)
        sysError = [0.0 for i in range(dataPoints)] #tracks error in reward prediction
        noMatch = [0.0 for i in range(dataPoints)]
        
        input_values = []
                
        for each in range(dataPoints):
            state = self.evaluationEnv.resetState()    #refers to current input data from environment
            # NOTE: the below will still allow covering to occur - in which case accurate classification with be 50/50 - and not bias either way.
            special = "EvalSet"
            matchSet = XClassifierSet(special, state, self.pop) #An alternative matchset object that does not implement covering - may return an empty match set or a set with only one action

            if matchSet.getSize() == 0:
                noMatch[each%dataPoints]=1
            else:
                noMatch[each%dataPoints]=0

            predictionArray = XCSPredictionArray(matchSet, self.evaluationEnv.getNrActions())
            actionWinner    =  predictionArray.bestActionWinner() #predictionArray.bestActionWinner()
            reward          = self.evaluationEnv.executeAction(actionWinner)
    
            if self.evaluationEnv.wasCorrect():
                correct[each%dataPoints]=1
            else:
                correct[each%dataPoints]=0
                        
            sysError[each%self.expCy] = abs(reward - predictionArray.getBestValue())   
            
            input_values.append([state, actionWinner])
                        
        print str(sum(correct)) + ' out of '+ str(dataPoints)+' correctly classified.'     #Debugging
        
        # A temporary list to store the accuracy and Total error calculated from the above evaluation
        resultList = [sum(correct)/float(dataPoints), sum(sysError)/float(dataPoints), sum(noMatch)/float(dataPoints)]   
        return resultList, input_values
        
 
    """##########---- Output ----##########"""
    def writePerformance(self, pW, performance, sysError, exploreProbC, generality, weightGenerality):
        """ Writes the performance of the XCS to the specified file.
        * The function writes time performance systemError actualPopulationSizeInMacroClassifiers.
        * Performance and system error are averaged over the last fifty trials.
        * @param pW The reference where to write the performance.
        * @param performance The performance in the last fifty exploration trials.
        * @param sysError The system error in the last fifty exploration trials.
        * @param exploreProbC The number of exploration trials executed so far. """

        perf  = sum(performance)/self.expCyMath
        serr  = sum(sysError)/self.expCyMath
        pop = self.pop.getSize()
        
        pW.write(str(exploreProbC) + "\t" + str(perf) + "\t" + str(serr) + "\t" + str(generality) + "\t" + str(weightGenerality) + "\t" + str(pop) + "\n")
        print ("Probe: " + str(exploreProbC) + "\t Performance: " + str(perf) + "\t Generality: " + str(generality) + "\t WeightedGenerality: " + str(weightGenerality) + "\t Error: " + str(serr) + "\t PopSize: " + str(self.pop.getSize()))

        if self.graphPerform:
            self.performanceTrackList[0].append(exploreProbC)
            self.performanceTrackList[1].append(perf)
            self.performanceTrackList[2].append(serr/float(self.env.maxPayoff))
            self.performanceTrackList[3].append(generality)  
            self.performanceTrackList[4].append(weightGenerality)          
            self.performanceTrackList[5].append(pop/float(self.maxPopSize))            
            self.graphPerformance()
            
            
    def graphPerformance(self):
        """ Graphs performance attributes in real time. """
        ion()   # Turn on interactive mode for interactive graphing
        line1 = plot(self.performanceTrackList[0], self.performanceTrackList[1],'g-')
        line2 = plot(self.performanceTrackList[0], self.performanceTrackList[2],'r-')
        line3 = plot(self.performanceTrackList[0], self.performanceTrackList[3],'b-')
        line4 = plot(self.performanceTrackList[0], self.performanceTrackList[4],'c-')
        line5 = plot(self.performanceTrackList[0], self.performanceTrackList[5],'y-')
        #axis([0, self.maxProblems, 0, 1])
        legend((line1,line2,line3,line4,line5),('Prediction Accuracy','Error(/'+str(self.env.maxPayoff)+')','Generality','WeightedGenerality','PopSize(/'+str(self.maxPopSize)+')'),loc=4)
        xlabel('Training Iterations')
        title('LCS Performance Tracking')
        grid(True)

