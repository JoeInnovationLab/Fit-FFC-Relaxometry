#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 10:56:45 2024

@author: Joachim
"""

# Importing dependencies 
import numpy as np

# Define the piecewise function with a smooth transition using a sigmoid
def piecewise_function(x, a1, b1, a2):
    
    return a1 / (1 + a2 * np.exp(-b1 * x))

# Stretched Lorentzian
def StrechedLorentzian(f,A,tau,n):
    
    return A/tau*(tau/(1+(2*np.pi*f*tau)**n) + 4*tau/(1+(2*2*np.pi*f*tau)**n))