#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 14:41:28 2024

@author: Joachim
"""

# Import dependencies
import customtkinter as ctk
import numpy as np

# Import local dependencies
from conversion_functions.block_to_zone import Block2Zone
from conversion_functions.zone_to_dispersion import Zone2Dispersion
import global_vars

class BlockFitSelectFrame(ctk.CTkFrame):
    def __init__(self, master, block_function_names, zone_function_names, sample_select_scroll_frame = None, dispersion_fit_select_frame = None, individual_plots = None , **kwargs):
        super().__init__(master, **kwargs)
        
        # Store reference to sample_select_scroll_frame
        self.sample_select_scroll_frame = sample_select_scroll_frame
        
        # Store reference to dispersion_fit_select_frame
        self.dispersion_fit_select_frame = dispersion_fit_select_frame
        
        # Store reference to individual_plots
        self.individual_plots = individual_plots
        
        self.block_function_names = block_function_names
        self.zone_function_names = zone_function_names

        # Add widgets onto the frame
        self.label = ctk.CTkLabel(self, text="Block to Zone Algorithm", font=("Arial", 10))
        self.label.grid(row=0, column=0)

        # Sample selection option box
        self.combobox_1 = ctk.CTkComboBox(self, values=self.block_function_names,
                                                    command=self.combobox_selection_changed, width=200)
        self.combobox_1.grid(row=1, column=0, padx=10, pady=(0, 10))

        self.label1 = ctk.CTkLabel(self, text="Zone to Dispersion Algorithm", font=("Arial", 10))
        self.label1.grid(row=2, column=0)

        self.combobox_2 = ctk.CTkComboBox(self, values=self.zone_function_names,
                                                    command=self.combobox_selection_changed, width=200)
        self.combobox_2.grid(row=3, column=0, padx=10, pady=(0, 10))

        self.button_2 = ctk.CTkButton(self, text="Start Fitting", command=self.start_fitting)
        self.button_2.grid_forget()

    def combobox_selection_changed(self, event=None):
        if self.combobox_1.get() != "Select Fitting" and self.combobox_2.get() != "Select Fitting":
            self.button_2.grid(row=4, column=0, padx=10, pady=(10, 10), sticky='nsew')
        else:
            self.button_2.grid_forget()

    def start_fitting(self):
        enabled_samples = [name for name, var in self.sample_select_scroll_frame.getCheckboxValues().items() if var == "on"]
        
        active_files = []
        for sample_name in enabled_samples:
            sample = global_vars.DataStorage[sample_name]
            self.fit_blocks(sample)
            self.fit_zones(sample)

            active_files.append(sample.file_name)
            if len(sample.zone2disp_data) == 6:
                active_files.append(f"{sample.file_name}_2nd")

            self.mask_negative_dispersion_values(sample)

        self.individual_plots.comboboxSamples.configure(values=active_files)
        self.individual_plots.comboboxSamplesDispersion.configure(values=["All"] + active_files)

    def fit_blocks(self, sample):
        block_size = int(float(sample.parameter_summary['BS']))
        zone_data = sample.zone_data

        blocked_zones_values = []
        blocked_zones_deviations = []

        for zone in zone_data:
            block_values, block_deviations = self.fit_zone_blocks(zone, block_size)
            blocked_zones_values.append(block_values)
            blocked_zones_deviations.append(block_deviations)

        sample.block2zone_data.clear()
        sample.block2zone_data.extend([blocked_zones_values, blocked_zones_deviations])

    def fit_zone_blocks(self, zone, block_size):
        block_values = []
        block_deviations = []

        for block_start in range(0, len(zone), block_size):
            block_data = zone[block_start:block_start + block_size]
            block_time_data = np.array([sublist[-1] for sublist in block_data])
            block_real = np.array([sublist[0] for sublist in block_data])
            block_img = np.array([sublist[1] for sublist in block_data])
            mag = np.sqrt(block_real ** 2 + block_img ** 2)

            block_value, block_deviation = Block2Zone(self.combobox_1.get(), mag, block_time_data,[1,20])
            block_values.append(block_value)
            block_deviations.append(block_deviation)

        return block_values, block_deviations

    def fit_zones(self, sample):
        if not sample.block2zone_data:
            print("No fitted blocks")
            return
    
        zone_params = sample.zone_parameters
        num_blocks = int(float(sample.parameter_summary['NBLK']))
    
        zone_value_summary, zone_deviation_summary, zone_fit_params_summary = [], [], []
        zone_value_summary_2, zone_deviation_summary_2 = [], []
        multi_disp = False
    
        blocked_zones_values, blocked_zones_deviations = sample.block2zone_data
    
        for count, blocked_zone in enumerate(blocked_zones_values):
            zone_times = self.get_zone_times(zone_params['T1Max'][count], zone_params['PrePolarization'][count], num_blocks)
            zone_value, zone_deviation, zone_fit_params = Zone2Dispersion(self.combobox_2.get(), np.array(blocked_zone), zone_times)
    
            if np.size(zone_value) == 1:
                zone_value_summary.append(zone_value)
                zone_deviation_summary.append(zone_deviation)
            else:
                multi_disp = True
                zone_value_summary.append(zone_value[1])
                zone_deviation_summary.append(zone_deviation[1])
                zone_value_summary_2.append(zone_value[0])
                zone_deviation_summary_2.append(zone_deviation[0])
    
            zone_fit_params_summary.append(zone_fit_params)
    
        sample.zone2disp_data.clear()
        sample.zone2disp_data.extend([zone_value_summary, zone_deviation_summary, self.combobox_2.get(), zone_fit_params_summary])
    
        if multi_disp:
            sample.zone2disp_data.extend([zone_value_summary_2, zone_deviation_summary_2, self.combobox_2.get(), zone_fit_params_summary])
    
        self.dispersion_fit_select_frame.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")


    def get_zone_times(self, block_t1_max, order, num_blocks):
        block_t1_max = float(block_t1_max)
        if order == "NP":
            return np.logspace(np.log10(4 * block_t1_max * 1e-6), np.log10(0.1 * block_t1_max * 1e-6), num=num_blocks)
        else:
            return np.logspace(np.log10(0.1 * block_t1_max * 1e-6), np.log10(4 * block_t1_max * 1e-6), num=num_blocks)

    def mask_negative_dispersion_values(self, sample):
        if not sample.zone2disp_data:  # Check if the dispersion data is empty
            return
        
        # Reinitialize the mask as an empty list
        sample.zone_parameters['DataMask'] = []
        mask = sample.zone_parameters['DataMask']
        
        # Create mask for the 1st dispersion
        mask_1st_dispersion = np.array(sample.zone2disp_data[0]) >= 0
        mask.append(mask_1st_dispersion)
        
        # Check for multi-dispersion case and create the second mask if needed
        if len(sample.zone2disp_data) == 8:
            mask_2nd_dispersion = np.array(sample.zone2disp_data[4]) >= 0
            mask.append(mask_2nd_dispersion)
