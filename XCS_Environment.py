"""
Name: XCS_Environment.py
Author: Ryan Urbanowicz - written at Dartmouth College, Hanover, NH, USA 
Note: Code primarily based on python XCS authored by Jose Antonio Martin H. <jamartin@dia.fi.upm.es> tranlated from a version by Martin V. Butz (in Java 1.0) 
Contact: ryan.j.urbanowicz@darmouth.edu
Created: 3/20/2009
Updated: 10/15/2013
Description: This is the interface that must be implemented by all problems presented to the XCSPython implementation.
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
    
class Environment:
        
    def resetState(self):
        """  Resets the current state to a random instance of a problem.
          A random instance can be a next problem in a table, a randomly generated string, a random position in
          a maze ...  """
        raise Exception("Method 'resetState' must be implemented")
       
       
    def getCurrentState(self):
         """  Returns the current situation.
          A situation can be the current perceptual inputs, a random problem instance ...  """
         raise Exception("Method 'getCurrentState' must be implemented")

        
    def executeAction(self,action):
        """  Executes an action in the environment.
          @param action An action can be an active action like a movement, grip...
          or a simple classification (good/bad, correct/incorrect, class1/class2/class3, ...).  """
        raise Exception("Method 'executeAction' must be implemented")

    
    def wasCorrect(self):
        """ Returns if this action was a good/correct action.
          This function is essentially necessary in single-step (classification) problems in order
          to evaluate the performance. """
        raise Exception("Method 'wasCorrect' must be implemented")

    
    def doReset(self):
        """ Returns if the agent has reached the end of a problem.
          In a classification problem such as the Multiplexer Problem, this function should return true
          after a classification was executed. In a multi-step problem like the reward learning in maze environments
          this function should return true when the animat reached a food position. """
        raise Exception("Method 'doReset' must be implemented")

    
    def getConditionLength(self):
        """ Returns the length of the coded situations. """
        raise Exception("Method 'getConditionLength' must be implemented")

    
    def getMaxPayoff(self):
        """ Returns the maximal payoff receivable in an environment. """
        raise Exception("Method 'getMaxPayoff' must be implemented")

    
    def isMultiStepProblem(self):
        """ Returns true if the problem is a multi-step problem.  Although the doReset() function already distinguishes multi-step and single-step problems,
        this functions is used in order to get a better performance analysis! """
        raise Exception("Method 'isMultiStepProblem' must be implemented")

    
    def getNrActions(self):
        """ Returns the number of possible actions in the environment. """
        raise Exception("Method 'getNrActions' must be implemented")
    
    
    def getNrSamples(self):
        """ Returns the number of samples in the data set being examined. """        
        raise Exception("Method 'getNrSamples' must be implemented")
