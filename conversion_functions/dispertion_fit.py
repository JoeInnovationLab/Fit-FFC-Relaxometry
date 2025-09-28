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
from math_functions.mapping_functions import all_Dispersion_functions

from math_functions.power_law_functions import OneSegPow, TwoSegPow, ThreeSegPow



# Define FFC Dispersion fit functions and initialize them if necesarry
def DispersionFit(Algorithm,FieldStrength,R1):

    if Algorithm == 'Piecewise':
        ParamStartVals = np.array([R1[0], 1e6 , R1[-1]])
        FittedParams,covar = curve_fit(all_Dispersion_functions(Algorithm), FieldStrength, R1, p0=ParamStartVals, method='lm', maxfev=int(1e6), gtol=1e-3)
        
        Deviation = np.sqrt(np.diagonal(covar))
    

    elif Algorithm == 'One Segment Powerlaw':

         ParamStartVals = np.array([R1[1], -5e-2])
         FittedParams,covar = curve_fit(OneSegPow,FieldStrength, R1 , p0=ParamStartVals, method='lm', maxfev=int(1e6), gtol=1e-6)
         
         
         Deviation = np.sqrt(np.diagonal(covar))        
            
    elif Algorithm == 'Two Segment Powerlaw':

         ParamStartVals = np.array([R1[0], -5e-2 , -3e-1 , 1e5])
         
         # Testing boundaries
         bound_test = [ [0, -np.inf, -np.inf, 1e3] , [np.inf, 0  , 0, np.inf] ]
         
         # FittedParams,covar = curve_fit(TwoSegPow,FieldStrength, R1 , p0=ParamStartVals, method='lm', maxfev=int(1e6), gtol=1e-6)
         FittedParams,covar = curve_fit(TwoSegPow,FieldStrength, R1 , p0=ParamStartVals, method='trf', maxfev=int(1e6), gtol=1e-6, bounds=bound_test)

         
         Deviation = np.sqrt(np.diagonal(covar))
     
    elif Algorithm == 'Three Segment Powerlaw':

         ParamStartVals = np.array([R1[0], -5e-2 , -3e-1 , -1e-1 , 2e5, 1e6])
         
         # Testing boundaries
         bound_test = [ [0, -np.inf, -np.inf, -np.inf , 1e3 , 1e5] , [np.inf, 0  , 0 , 0 , np.inf, np.inf] ]
         
         FittedParams,covar = curve_fit(ThreeSegPow,FieldStrength, R1 , p0=ParamStartVals, method='trf', maxfev=int(1e6), gtol=1e-6, bounds=bound_test)

         
         Deviation = np.sqrt(np.diagonal(covar))

     
    elif Algorithm == 'Stretched Lorentzian':

         ParamStartVals = np.array([10 , 1e-6 , 1])
         FittedParams,covar = curve_fit(all_Dispersion_functions(Algorithm),FieldStrength, R1 , p0=ParamStartVals, method='lm', maxfev=int(1e6), gtol=1e-6)
         
         
         Deviation = np.sqrt(np.diagonal(covar))     
         
         
    else:
        FittedParams,covar,Deviation = [],[],[]
          
    return FittedParams,covar,Deviation