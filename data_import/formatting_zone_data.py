#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 12:00:43 2024

@author: Joachim
"""

# Import dependencies
import numpy as np

def convert_zone_data(data):
    result = []

    for item in data:
        try:
            # Directly converting the first three values to int, and the last one to float
            parts = item.split('\t\t')
            if len(parts) == 4:  # Ensure there are exactly four parts to process
                values = [int(parts[0]), int(parts[1]), int(parts[2]), float(parts[3])]
                result.append(values)
            else:
                print(f"Skipping invalid data due to incorrect number of columns: {item}")
        except ValueError:
            print(f"Skipping invalid data due to conversion error: {item}")
    result_array = np.array(result)        
    return result_array