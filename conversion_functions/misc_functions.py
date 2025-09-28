#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 12:00:43 2024

@author: Joachim
"""

# Import dependencies
import numpy as np

# Import local dependencies
from math_functions.mapping_functions import all_Dispersion_functions, Dispersion_Function_Mapper

from conversion_functions.dispertion_fit import DispersionFit


# Define sorting function
def sort_and_format_values(values, deviations):
    sorting = np.argsort(values)
    values = np.take(values, sorting)
    deviations = np.take(deviations, sorting)
    return values, deviations


# Calculating the R2 values to evaluate the Dispersion fit
def CalculateR2(FieldStrengths, DataValues, FitType, FitParams):
    
    residuals = DataValues - all_Dispersion_functions(FitType)(FieldStrengths,*FitParams)
    sumsquares_residuals = np.sum(residuals**2)
    sumsquares_total = np.sum( (DataValues - np.mean(DataValues) )**2 )
    R2 = 1 - (sumsquares_residuals/sumsquares_total)   
    
    return R2


# Function to evaluate all the available dispersion fit functions
def FindBestDispersionFit(f,Dispersion,FieldStrengths):
    # return FittedParams,covar,ZoneValueDeviation
    #FieldStrengths = np.array(f[3][1],dtype=np.float64)*1e6
    
    # Mask the data according to selection
    # Mask = f[9][0]
    # FieldStrengths = FieldStrengths[Mask]
    # Dispersion = Dispersion[Mask]
    
    DispersionFunctionNames = list(Dispersion_Function_Mapper.keys())
    
    FitRes = []
    for DispFitType in DispersionFunctionNames:
        
        FittedParams,covar,ZoneValueDeviation = DispersionFit(DispFitType, FieldStrengths, Dispersion)
            
        R2 = CalculateR2(FieldStrengths, Dispersion, DispFitType, list(FittedParams))
        FitRes.append([DispFitType,R2])            
    return FitRes