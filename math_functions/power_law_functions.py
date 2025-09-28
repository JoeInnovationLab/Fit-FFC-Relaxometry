#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 10:56:45 2024

@author: Joachim
"""

# Importing dependencies 
import numpy as np

# OneSegPowerLaw
def OneSegPow (f,dl,vlow):
        
    return (dl*f**vlow)*f 


# TwoSegPowerLaw
def TwoSegPow (f,dl,vlow,vhigh,ftrans):
       
    return np.where(f<ftrans , (dl*f**vlow), ((dl*ftrans**(vlow-vhigh))*f**vhigh))

# ThreeSegPowerLaw
def ThreeSegPow (f,dl,vlow,vhigh,vhigh2,ftrans,ftrans2):
       
    return np.where(f<ftrans , (dl*f**vlow), np.where(f<ftrans2 , ((dl*ftrans**(vlow-vhigh))*f**vhigh), (((dl*ftrans**(vlow-vhigh))*ftrans2**(vhigh-vhigh2))*f**vhigh2)  ))
