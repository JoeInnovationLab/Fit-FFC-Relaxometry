#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 12:21:05 2024

@author: Joachim
"""

# Import dependencies
import os

# Import local dependencies
from data_import.read_sdf_file import read_sdf_file
from data_import.extract_ffc_zones import extract_ffc_zones
from data_import.NMRDSeq import NMRDSeq_Data


# Importing sdf data into file structure
def import_sdf_file(sdf_file_path):
    contents, data_name, variables = read_sdf_file(sdf_file_path)
    zone_parameters, zone_data = extract_ffc_zones(contents)

    data_name = os.path.basename(data_name).split('.')[0]
    file_name = os.path.basename(sdf_file_path).split('.')[0]

    # ZoneDataMasks = np.ones([2, len(zone_data)], dtype='bool')
    NMRD_file = NMRDSeq_Data()
    
    NMRD_file._file_name = file_name
    NMRD_file._file_path = sdf_file_path
    NMRD_file._data_name = data_name
    NMRD_file._SDF_parameter_summary = variables
    NMRD_file._zone_parameters = zone_parameters
    NMRD_file._zone_data = zone_data
    
    return NMRD_file
    