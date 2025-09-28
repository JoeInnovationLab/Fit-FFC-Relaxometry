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
from math_functions.exp_decay_functions import ExpDecay
from math_functions.exp_decay_functions import DoubleExpDecay
from math_functions.exp_decay_functions import ABSMonoExpDecay
from math_functions.exp_decay_functions import DoubleExpDecayAndConst

from conversion_functions.misc_functions import sort_and_format_values


# Define FFC Zones to Dispersion conversation functions and initialize them if necesarry
def Zone2Dispersion(Algorithm,Magnitudes,Timedata):

    if Algorithm == 'Exponential Decay':
        # ParamStartVals = np.array([Magnitudes[0], 2e-4 , Magnitudes[-1]])
        ParamStartVals = np.array([1, 1, 1])
        FittedParams,covar = curve_fit(ExpDecay, Timedata, Magnitudes, p0=ParamStartVals, method='lm', maxfev=int(1e6), gtol=1e-3)
        
        ZoneValue = FittedParams[1]
        ZoneValueDeviation = np.sqrt(np.diagonal(covar)[1])
            
    elif Algorithm == 'Double Exponential Decay':
         ParamStartVals = np.array([1, 1 , 0.2, 0.1])
         FittedParams,covar = curve_fit(DoubleExpDecay, Timedata, Magnitudes, p0=ParamStartVals, method='lm', maxfev=int(1e6), gtol=1e-3)
            
         # ZoneValue = FittedParams[1]
         # ZoneValueDeviation = np.sqrt(np.diagonal(covar)[1])
         
         ZoneValue = [ FittedParams[1], FittedParams[1]+FittedParams[3] ]
         ZoneValueDeviation = [ np.sqrt(np.diagonal(covar)[1]), np.sqrt(np.diagonal(covar)[3]) + np.sqrt(np.diagonal(covar)[1]) ]
         
         # sorting =np.argsort(ZoneValue)
         # ZoneValue = np.take(ZoneValue, sorting)
         # ZoneValueDeviation = np.take(ZoneValueDeviation, sorting)
         
         ZoneValue, ZoneValueDeviation = sort_and_format_values(ZoneValue, ZoneValueDeviation)
         
         
    elif Algorithm == 'Mono Exponential ABS':
         ParamStartVals = np.array([1, 1, 1, 1 ])
         FittedParams,covar = curve_fit(ABSMonoExpDecay, Timedata, Magnitudes, method='lm', maxfev=int(1e6), gtol=1e-3)
        
         ZoneValue = FittedParams[1]
         ZoneValueDeviation = np.sqrt(np.diagonal(covar)[1])
         
    elif Algorithm == 'DoubleExpDecayAndConst':
         # ParamStartVals = np.array([1, 1 , 1, 1, 1, 1, 1 ])
         ParamStartVals = np.array([1, 1 , 0.2, 0.1, 1])
         FittedParams,covar = curve_fit(DoubleExpDecayAndConst, Timedata, Magnitudes, p0=ParamStartVals, method='lm', maxfev=int(1e6), gtol=1e-3)
        
         # ZoneValue = FittedParams[1]
         # ZoneValueDeviation = np.sqrt(np.diagonal(covar)[1])
         ZoneValue = [ FittedParams[1], FittedParams[1]+FittedParams[3] ]
         ZoneValueDeviation = [ np.sqrt(np.diagonal(covar)[1]), np.sqrt(np.diagonal(covar)[3]) ]
         
         sorting =np.argsort(ZoneValue)
         ZoneValue = np.take(ZoneValue, sorting)
         ZoneValueDeviation = np.take(ZoneValueDeviation, sorting)
         
    else:
        ZoneValue,ZoneValueDeviation = [],[]
          
    return ZoneValue,ZoneValueDeviation,FittedParams