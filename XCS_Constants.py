"""
Name: XCS_Constants.py
Author: Ryan Urbanowicz - written at Dartmouth College, Hanover, NH, USA 
Note: Code primarily based on python XCS authored by Jose Antonio Martin H. <jamartin@dia.fi.upm.es> tranlated from a version by Martin V. Butz (in Java 1.0) 
Contact: ryan.j.urbanowicz@darmouth.edu
Created: 3/20/2009
Updated: 10/15/2013
Description: Specifies default XCS run constants.  Most parameter-names are chosen similar to * the 'An Algorithmic Description of XCS' 
(Butz&Wilson, IlliGAL report 2000017)
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

class CXCSConstants:
    """ Specifies default XCS run constants. """
    
    alpha = 0.1   # The fall of rate in the fitness evaluation.
    beta = 0.2    # The learning rate for updating fitness, prediction, prediction error, and action set size estimate in XCS's classifiers.
    gamma = 0.95  # The discount rate in multi-step problems.
    delta = 0.1   # The fraction of the mean fitness of the population below which the fitness of a classifier may be considered in its vote for deletion.
    nu = 5.       # Specifies the exponent in the power function for the fitness evaluation.
    theta_GA = 25 # The threshold for the GA application in an action set.
    #theta_Select = 0.4   # Original Value as found in Butz 2002 Tournament Selection paper
    theta_Select = 0.5    # The fraction of the action set to be included in tournament selection.
    epsilon_0 = 10  # The error threshold under which the accuracy of a classifier is set to one.
    theta_del = 20  # Specified the threshold over which the fitness of a classifier may be considered in its deletion probability.
    pX = 0.8        # The probability of applying crossover in an offspring classifier.
    pM = 0.04       # The probability of mutating one allele and the action in an offspring classifier.
    P_dontcare = 0.5    # The probability of using a don't care symbol in an allele when covering.
    predictionErrorReduction = 0.25 # The reduction of the prediction error when generating an offspring classifier.
    fitnessReduction = 0.1  # The reduction of the fitness when generating an offspring classifier.
    theta_sub = 20  # The experience of a classifier required to be a subsumer.
    predictionIni = 10.0    # The initial prediction value when generating a new classifier (e.g in covering).
    predictionErrorIni = 0.0    # The initial prediction error value when generating a new classifier (e.g in covering).
    fitnessIni = 0.01   # The initial prediction value when generating a new classifier (e.g in covering).
    dontCare = '#'    # The don't care symbol (normally '#')

    def setEConstants(self,attributeCombos):
        self.attributeCombos = attributeCombos
        
XCSConstants = CXCSConstants()
cons = XCSConstants #To access one of the above constant values from another module, import XCS_Constants * and use "cons.Xconstant"
