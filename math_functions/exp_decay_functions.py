#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 10:56:45 2024

@author: Joachim
"""

# Importing dependencies 
import numpy as np

# Exponential decay function
def ExpDecay (timedata,a,b,c):
        
    return (a-c)*np.exp(-b*timedata)+c

# Exponential decay with independent amplitude for testing
def ExpDecayTest (timedata,a,b,c):
        
    return a*np.exp(-b*timedata)+c

# Double exponential decay function
def DoubleExpDecay (timedata,Amp_1,R1_1,Amp_2,R1_2):
        
    # return a*np.exp(-b*timedata+c) + d*(1-np.exp(-e*timedata+f))
    # return Amp_1*np.exp(-R1_1*timedata) + Amp_2*np.exp(-R1_2*timedata)+Constant
    return Amp_1*np.exp(-R1_1*timedata) + Amp_2*np.exp(-(R1_1+R1_2)*timedata) #+Constant

# Double exponential decay function with additional constant term
def DoubleExpDecayAndConst (timedata,Amp_1,R1_1,Amp_2,R1_2,Constant):
        
    return Amp_1*np.exp(-R1_1*timedata) + Amp_2*np.exp(-(R1_1+R1_2)*timedata) + Constant

# Mono exponential abs function including noise
def ABSMonoExpDecay (timedata,a,b,c,noise):
        
    return np.sqrt(((a-c)*np.exp(-b*timedata)+c)**2 + 2*((a-c)*np.exp(-b*timedata)+c)*abs(noise) +2*noise**2)