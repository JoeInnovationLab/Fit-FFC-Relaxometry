#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 12:21:05 2024

@author: Joachim
"""
# import dependencies
import re
import numpy as np

# Import local dependencies
from data_import.formatting_zone_data import convert_zone_data


def extract_ffc_zones(data_list):
    zone_parameters = {
        "ZoneName": [],
        "BR": [],
        "T1Max": [],
        "PrePolarization": [],
        "DataMask": None
    }
    zone_data = []

    block_data_logic = False
    np_pp_logic = ""

    # Pre-compile regex patterns for better performance
    name_pattern = re.compile(r"NAME:(.*)")
    zone_pattern = re.compile(r"ZONE")
    param_pattern = re.compile(r"=(.*)")
    data_start_pattern = re.compile(r"REAL\s+IMG\s+MOD\s+TIME\(us\)")

    for count, line in enumerate(data_list):
        line = line.strip()

        # Match NAME line and determine PP/NP logic
        name_match = name_pattern.search(line)
        if name_match:
            value = name_match.group(1).strip()
            np_pp_logic = "PP" if "PP-S" in value else "NP" if "NP-S" in value else np_pp_logic

        # Match ZONE line
        if zone_pattern.search(line):
            zone_parameters["ZoneName"].append(line)

            # Extract BR and T1Max parameters in subsequent lines
            zone_parameters["BR"].append(param_pattern.search(data_list[count + 1]).group(1).strip())
            zone_parameters["T1Max"].append(param_pattern.search(data_list[count + 2]).group(1).strip())

            # Append PrePolarization value (PP or NP)
            zone_parameters["PrePolarization"].append(np_pp_logic)

        # Match data block start
        if data_start_pattern.search(line):
            data_start = count + 1
            block_data_logic = True

        # Collect data block
        if block_data_logic and not line:
            zone_data.append(convert_zone_data(data_list[data_start:count]))
            block_data_logic = False

    # DataMask is simply a list of True values for each PrePolarization entry
    # zone_parameters["DataMask"] = [True] * len(zone_parameters["PrePolarization"])
    zone_parameters["DataMask"] = np.ones([2,len(zone_parameters["PrePolarization"])],dtype='bool')

    return zone_parameters, zone_data
