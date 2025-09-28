#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 10:56:45 2024

@author: Joachim
"""
# Import local dependencies
from math_functions.average_block_functions import AverageOfMagnitude,AverageOfMagnitudeInAreas

from math_functions.exp_decay_functions import ExpDecay,DoubleExpDecay, DoubleExpDecayAndConst, ABSMonoExpDecay

from math_functions.misc_dispersion_functions import piecewise_function, StrechedLorentzian

from math_functions.power_law_functions import OneSegPow, TwoSegPow, ThreeSegPow


## Block functionality
# Block function mapper to allocate block function names to functions
Block_Function_Mapper = {
    'Average of Magnitudes': AverageOfMagnitude,
    'Average of Local Magnitudes': AverageOfMagnitudeInAreas,
    'Exponential Decay': ExpDecay,
    # 'Double Exponential Decay': DoubleExpDecay,
    # 'Piecewise': piecewise_function,
    }

# Function to select block functions with inputs and recieve results
def all_Block_functions(selection):

    return Block_Function_Mapper.get(selection, 'None')


## Zone functionality
# Zone function mapper to allocate zone function names to functions
Zone_Function_Mapper = {
    'Exponential Decay': ExpDecay,
    'Double Exponential Decay': DoubleExpDecay,
    'DoubleExpDecayAndConst':DoubleExpDecayAndConst,
    'Mono Exponential ABS': ABSMonoExpDecay,
    }

# Function to select zone functions with inputs and recieve results
def all_Zone_functions(selection):

    return Zone_Function_Mapper.get(selection, 'None')


## Dispersion functionality
# Dispersion function mapper to allocate dispersion function names to functions
Dispersion_Function_Mapper = {

    'Piecewise': piecewise_function,
    'One Segment Powerlaw': OneSegPow,
    'Two Segment Powerlaw': TwoSegPow,
    'Three Segment Powerlaw': ThreeSegPow,
    'Stretched Lorentzian': StrechedLorentzian,
    }

# Function to select dispersion functions with inputs and recieve results
def all_Dispersion_functions(selection):

    return Dispersion_Function_Mapper.get(selection, 'None')
