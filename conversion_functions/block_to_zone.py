#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 11:32:48 2024

@author: Joachim
"""

# Import ecternal dependencies
import numpy as np
from scipy.optimize import curve_fit

# Import local dependencies
from math_functions.mapping_functions import all_Block_functions
from math_functions.exp_decay_functions import ExpDecayTest
from math_functions.exp_decay_functions import DoubleExpDecay


# Define FFC block to zone conversion functions and initialize them if necesarry
def Block2Zone(Algorithm,Magnitudes,Timedata,SubZone):
       
    if Algorithm == 'Average of Magnitudes':
        BlockValue,BlockValueDeviation = all_Block_functions(Algorithm)(Magnitudes)
            
            
    elif Algorithm == 'Average of Local Magnitudes':
        BlockValue,BlockValueDeviation = all_Block_functions(Algorithm)(Magnitudes,SubZone)
            
            

    elif Algorithm == 'Exponential Decay':
        ParamStartVals = np.array([Magnitudes[0], 2e-4 , Magnitudes[-1]])
        sol,covar = curve_fit(ExpDecayTest, Timedata-Timedata[0], Magnitudes, p0=ParamStartVals, method='lm', maxfev=int(1e6), gtol=1e-3)
        
        BlockValue = sol[0]+sol[2]
        # BlockValueDeviation = np.sqrt(np.diagonal(covar))
        BlockValueDeviation = np.std(Magnitudes-ExpDecayTest(Timedata-Timedata[0], *sol))
        BlockValueDeviation = [BlockValueDeviation , BlockValueDeviation]
            
            
    elif Algorithm == 'Double Exponential Decay':
          ParamStartVals = np.array([Magnitudes[0], -2e-4 , Magnitudes[0] , -2e-4 ])
          sol,covar = curve_fit(DoubleExpDecay, Timedata, Magnitudes, p0=ParamStartVals, method='lm', maxfev=int(1e6), gtol=1e-3)
            
          BlockValue = DoubleExpDecay(Timedata[0], *sol[0])
          BlockValueDeviation = np.sqrt(np.diagonal(covar))
         
    else:
        BlockValue,BlockValueDeviation = [],[]
          
    return BlockValue,BlockValueDeviation