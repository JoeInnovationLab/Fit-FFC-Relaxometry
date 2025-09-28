#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 14:26:00 2024

@author: Joachim
"""

class NMRDSeq_Data:

    def __init__(self):
        self._file_name = None
        self._file_path = None
        self._data_name = None
        self._SDF_parameter_summary = {}
        self._zone_parameters = {}
        self._zone_data = []
        self.block2zone_data = []
        self.zone2disp_data = []
        self.disp_fit = {}
        
        

    @property
    def file_name(self):
        return self._file_name
    
    @property
    def file_path(self):
        return self._file_path

    @property
    def data_name(self):
        return self._data_name

    @property
    def parameter_summary(self):
        return self._SDF_parameter_summary

    @property
    def zone_parameters(self):
        return self._zone_parameters

    @property
    def zone_data(self):
        return self._zone_data

    def get_data(self, data_name):
        return self._nmr_data.get(data_name)

    def set_data(self, data_name, data):
        self._nmr_data[data_name] = data
