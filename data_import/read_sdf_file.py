#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 14:28:17 2024

@author: Joachim
"""

def read_sdf_file(sdf_file_path):
    variables = {}
    param_search = False
    data_name = ""

    with open(sdf_file_path) as f:
        contents = f.readlines()

        for line in contents:
            line = line.strip()

            if "NAME" in line and not param_search:
                _, value = line.split("NAME:", 1)
                data_name = value.strip()

            elif "PARAMETER SUMMARY" in line:
                param_search = True

            elif "=" in line:
                name, value = line.split("=", 1)
                variables[name.strip()] = value.strip()

            elif param_search and not line:
                param_search = False
                break

    return contents, data_name, variables
