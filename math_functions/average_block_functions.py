#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 10:56:45 2024

@author: Joachim
"""

# Importing dependencies 
import numpy as np

# Calculates the average of magnitudes in the given block data
def AverageOfMagnitude (BlockMagnitudes):
    
    return np.mean(BlockMagnitudes),[np.std(BlockMagnitudes) , np.std(BlockMagnitudes)]

# Calculates the average of magnitudes in a loclaized zone of the given block data
def AverageOfMagnitudeInAreas (BlockMagnitudes,SubZone):
    
    return AverageOfMagnitude(BlockMagnitudes[SubZone[0]:SubZone[1]])