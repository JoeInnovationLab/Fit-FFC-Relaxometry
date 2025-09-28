#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 15:24:11 2024

@author: Joachim
"""

# Import dependencies
import customtkinter as ctk
import numpy as np

# Import local dependencies
import global_vars

class MaskingFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
       
class MaskZonesFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Store reference to dispersion_fit_select_frame
        self.dispersion_fit_select_frame = None
        
        # Store reference to individual_plots
        self.individual_plots = None
              
        self.checkboxes = {}  # Dictionary to store checkboxes and their associated variables

        # Configure the frame to expand vertically
        for i in range(1, 5):
            self.grid_columnconfigure(i, weight=1)

        # Add Mask Data label
        self.label = ctk.CTkLabel(self, text="Toggle Zones:")
        self.label.grid(row=0, column=0)
        
        # Create buttons to toggle zones and apply mask
        self._create_buttons()

        # Create the frame for checkboxes
        self.MaskFrame = MaskingFrame(master=self)
        self.MaskFrame.grid(row=1, column=0, padx=5, pady=5, columnspan=5, sticky="nsew")
        
    def set_dispersion_fit_select_frame(self, dispersion_fit_select_frame):
        """Set the SampleSelectFrameScroll after initialization."""
        self.dispersion_fit_select_frame = dispersion_fit_select_frame
        
    def set_individual_plots(self, individual_plots):
        """Set the SampleSelectFrameScroll after initialization."""
        self.individual_plots = individual_plots
        
    def _create_buttons(self):
        buttons = [
            ("Non-Polarized", self.toggle_NP_zones_event, None,'NP'),
            ("Polarized", self.toggle_PP_zones_event, None,'PP'),
            ("Activate All", self.activate_all_zones),
            ("Apply Mask", self.apply_mask, "DarkGreen")
        ]
        for idx, (text, command, *args) in enumerate(buttons):
            btn_color = args[0] if args else None
            if command in (self.toggle_NP_zones_event, self.toggle_PP_zones_event):
                button = ctk.CTkButton(self, text=text, command=lambda cmd=command, arg=args[0]: cmd(arg), fg_color=btn_color)
            else:
                button = ctk.CTkButton(self, text=text, command=command, fg_color=btn_color)
            button.grid(row=0, column=idx + 1, padx=5, pady=5, sticky="nsew")

    
    def toggle_NP_zones_event(self, *_):
        self._toggle_zones_for_current_selection('NP')

    def toggle_PP_zones_event(self, *_):
        self._toggle_zones_for_current_selection('PP')

    def _toggle_zones_for_current_selection(self, zone_type):
        if self._is_all_mode():
            # Use first sample as template for NP/PP zone membership
            template = next(iter(global_vars.DataStorage.values()), None)
            if not template:
                return
            for idx, zt in enumerate(template.zone_parameters['PrePolarization']):
                if zt == zone_type and idx in self.checkboxes:
                    self.checkboxes[idx].set(not self.checkboxes[idx].get())
        else:
            sample = self._get_selected_sample()
            if not sample:
                return
            for idx, zt in enumerate(sample.zone_parameters['PrePolarization']):
                if zt == zone_type and idx in self.checkboxes:
                    self.checkboxes[idx].set(not self.checkboxes[idx].get())

    def _toggle_zones(self, sample, zone_type):
        for index, ZoneType in enumerate(sample.zone_parameters['PrePolarization']):
            if ZoneType == zone_type:
                var = self.checkboxes.get(index)
                if var:
                    var.set(not var.get())
    
    def activate_all_zones(self):
        sel = self._current_selection()
    
        if sel == "All":
            # Just set all checkboxes True (UI update)
            for var in self.checkboxes.values():
                var.set(True)
            # Nothing else here — actual propagation to all samples
            # happens when "Apply Mask" is clicked.
    
        else:
            # Single sample
            if self._valid_sample_selected():
                sample = self._get_selected_sample()
                if sample:
                    for var in self.checkboxes.values():
                        var.set(True)
    
    def apply_mask(self):
        sel = self._current_selection()
    
        # -----------------------
        # GLOBAL MASKING (All)
        # -----------------------
        if sel == "All":
            # Step 1: Update masks for all samples
            for sample in global_vars.DataStorage.values():
                # primary dispersion mask
                n0 = len(sample.zone_parameters['DataMask'][0])
                for zone, var in self.checkboxes.items():
                    if zone < n0:
                        sample.zone_parameters['DataMask'][0][zone] = bool(var.get())
                # secondary dispersion mask, if present
                if len(sample.zone_parameters['DataMask']) > 1:
                    n1 = len(sample.zone_parameters['DataMask'][1])
                    for zone, var in self.checkboxes.items():
                        if zone < n1:
                            sample.zone_parameters['DataMask'][1][zone] = bool(var.get())
    
            # Step 2: Recalculate dispersion for all samples
            for sample_name, sample in global_vars.DataStorage.items():
                self.dispersion_fit_select_frame.recalculate_dispersion(sample_name)
    
            # Step 3: Refresh plots
            self.individual_plots.plot_all_dispersion_data()
            return
    
        # -----------------------
        # SINGLE SAMPLE MASKING
        # -----------------------
        sample = self._get_selected_sample()
        if not sample:
            return
    
        # Determine which dispersion mask to use (primary or secondary)
        target = 0
        if sel == sample.file_name + '_2nd':
            target = 1
    
        n = len(sample.zone_parameters['DataMask'][target])
        for zone, var in self.checkboxes.items():
            if zone < n:
                sample.zone_parameters['DataMask'][target][zone] = bool(var.get())
    
        # Recalculate dispersion for this single sample
        self.dispersion_fit_select_frame.recalculate_dispersion(sample.file_name)
    
        # Refresh plot for this sample
        self.individual_plots.DispersionSamplecombobox_callback(sel)
            

    def _valid_sample_selected(self):
        selected_sample = self.individual_plots.comboboxSamplesDispersion.get()
        return selected_sample != "All" and selected_sample != "Select Sample"

    def _get_selected_sample(self):
        selected_sample = self.individual_plots.comboboxSamplesDispersion.get()
        for sample_name in global_vars.DataStorage:
            if selected_sample == sample_name or selected_sample[:-4] == sample_name:
                return global_vars.DataStorage[sample_name]
        return None
    
    def addR1CheckBox(self, DataName):
        """Create checkboxes for the selected sample or for 'All' (global)."""
        # Clear old widgets and state
        for w in self.MaskFrame.winfo_children():
            w.destroy()
        self.checkboxes.clear()
    
        if DataName == "All":
            samples = list(global_vars.DataStorage.values())
            if not samples:
                return
            # Use the minimum zone count to stay consistent across datasets
            min_zones = min(len(s.zone_parameters['DataMask'][0]) for s in samples)
            # Global starting mask = intersection across samples (True only if all True)
            start_mask = [
                all(bool(s.zone_parameters['DataMask'][0][z]) for s in samples)
                for z in range(min_zones)
            ]
            self._create_checkboxes_from_mask(start_mask)
        else:
            sample = self._get_sample_by_name(DataName)
            if not sample:
                return
            start_mask = list(sample.zone_parameters['DataMask'][0])
            self._create_checkboxes_from_mask(start_mask)

    def _get_sample_by_name(self, name):
        for sample_name in global_vars.DataStorage:
            if name == sample_name or name[:-4] == sample_name:
                return global_vars.DataStorage[sample_name]
        return None

    def _create_checkboxes(self, sample):
        """Create checkboxes for the given sample’s zones."""
        data_mask = sample.zone_parameters['DataMask'][0]
        num_zones = len(data_mask)

        for zone in range(num_zones):
            var = ctk.BooleanVar(value=bool(data_mask[zone]))
            checkbox = ctk.CTkCheckBox(
                self.MaskFrame, text=str(zone + 1), variable=var, width=4
            )
            checkbox.grid(row=zone // 10, column=zone % 10, padx=1, pady=1, sticky="nsew")
            self.checkboxes[zone] = var

    def getR1CheckboxValues(self):
        return {name: var.get() for name, var in self.checkboxes.items()}

    
    def UpdateR1CheckBoxes(self):
        sel = self._current_selection()
        if sel == "All":
            samples = list(global_vars.DataStorage.values())
            if not samples:
                return
            min_z = min(len(s.zone_parameters['DataMask'][0]) for s in samples)
            for zone, var in self.checkboxes.items():
                if zone < min_z:
                    val = all(bool(s.zone_parameters['DataMask'][0][zone]) for s in samples)
                    var.set(val)
            return
    
        sample = self._get_selected_sample()
        if not sample:
            return
    
        data_mask = sample.zone_parameters['DataMask'][0]
        for zone, var in self.checkboxes.items():
            if zone < len(data_mask):
                var.set(bool(data_mask[zone]))
    
    def _current_selection(self):
        return self.individual_plots.comboboxSamplesDispersion.get()

    def _is_all_mode(self):
        return self._current_selection() == "All"
    
    def _create_checkboxes_from_mask(self, mask_list):
        num_zones = len(mask_list)
        for zone in range(num_zones):
            var = ctk.BooleanVar(value=bool(mask_list[zone]))
            cb = ctk.CTkCheckBox(self.MaskFrame, text=str(zone + 1), variable=var, width=4)
            cb.grid(row=zone // 10, column=zone % 10, padx=1, pady=1, sticky="nsew")
            self.checkboxes[zone] = var

