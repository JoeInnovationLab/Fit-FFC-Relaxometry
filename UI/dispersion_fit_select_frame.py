#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 14:54:38 2024

@author: Joachim
"""

# Import dependencies
import customtkinter as ctk
import numpy as np
import os 

# Import local denpendencies
from math_functions.mapping_functions import Dispersion_Function_Mapper
from conversion_functions.dispertion_fit import DispersionFit
from conversion_functions.misc_functions import CalculateR2
from data_export.export_ffc_fit_to_excel import ExportFFCFitToExcel
import global_vars

class DispersionFitSelectFrame(ctk.CTkFrame):
    def __init__(self, master, sample_select_scroll_frame = None, individual_plots = None, **kwargs):
        super().__init__(master, **kwargs)
        
        # Store reference to sample_select_scroll_frame
        self.sample_select_scroll_frame = sample_select_scroll_frame
        
        # Store reference to individual_plots
        self.individual_plots = individual_plots

        # Add widgets onto the frame
        self.label = ctk.CTkLabel(self, text="Dispersion Fit Type", font=("Arial", 10))
        self.label.grid(row=0, column=0)

        DispersionFunctionNames = list(Dispersion_Function_Mapper.keys())
        self.combobox = ctk.CTkComboBox(
            self, values=DispersionFunctionNames, command=self.combobox_selection_changed, width=200
        )
        self.combobox.set("Select Fitting")
        self.combobox.grid(row=1, column=0, padx=10, pady=(0, 10))

        self.button_FitDispersion = ctk.CTkButton(self, text="Fit to Dispersion", command=self.FitDispersion_event)
        self.button_FitDispersion.grid_forget()

        self.button_ExportExcel = ctk.CTkButton(self, text="Export Fit to Excel", command=self.ExportExcel_event)
        self.button_ExportExcel.grid_forget()

    def combobox_selection_changed(self, event=None):
        if self.combobox.get() != "Select Fitting":
            self.button_FitDispersion.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        else:
            self.button_FitDispersion.grid_forget()

    def FitDispersion_event(self):
        tmpActiveFiles = ["All"]

        for dataname in global_vars.DataStorage:
            if self.sample_select_scroll_frame.checkboxes[dataname].get() == 'on' and not ( global_vars.DataStorage[dataname] == []):
                FieldStrengths = np.array(global_vars.DataStorage[dataname].zone_parameters['BR'], dtype=np.float64) * 1e6
                Dispersion = np.array(global_vars.DataStorage[dataname].zone2disp_data[0])

                # Mask the data according to selection
                Mask = global_vars.DataStorage[dataname].zone_parameters['DataMask'][0]
                FieldStrengths, Dispersion = FieldStrengths[Mask], Dispersion[Mask]

                FittedParams, covar, ZoneValueDeviation = DispersionFit(self.combobox.get(), FieldStrengths, Dispersion)
                R2 = CalculateR2(FieldStrengths, Dispersion, self.combobox.get(), list(FittedParams))

                # Check for additional dispersion data
                if len(global_vars.DataStorage[dataname].zone2disp_data) == 8:
                    FieldStrengths = np.array(global_vars.DataStorage[dataname].zone_parameters['BR'], dtype=np.float64) * 1e6
                    Dispersion2 = np.array(global_vars.DataStorage[dataname].zone2disp_data[4])
                    Mask2 = global_vars.DataStorage[dataname].zone_parameters['DataMask'][1]
                    FieldStrengths2 = FieldStrengths[Mask2]
                    Dispersion2 = Dispersion2[Mask2]

                    FittedParams_2, covar_2, ZoneValueDeviation_2 = DispersionFit(
                        self.combobox.get(), FieldStrengths2, Dispersion2
                    )
                    R2_2 = CalculateR2(FieldStrengths2, Dispersion2, self.combobox.get(), list(FittedParams_2))
                else:
                    FittedParams_2 = covar_2 = ZoneValueDeviation_2 = R2_2 = None

                self._store_fit_results(global_vars.DataStorage[dataname], FittedParams, covar, ZoneValueDeviation, R2, 
                                        FittedParams_2, covar_2, ZoneValueDeviation_2, R2_2)

                tmpActiveFiles.extend(self._get_file_names(global_vars.DataStorage[dataname]))

        self.individual_plots.comboboxSamplesDispersion.configure(values=tmpActiveFiles)
        self.button_ExportExcel.grid(row=3, column=0, padx=10, pady=(10, 10), sticky="nsew")
        self.individual_plots.DispersionSamplecombobox_callback(self.individual_plots.comboboxSamplesDispersion.get())
    
    def UpdateDispersion_event(self):
        """
        Recalculate the dispersion for the currently selected sample in the combobox.
        """
        selected_sample_name = self.individual_plots.comboboxSamplesDispersion.get()
        self.recalculate_dispersion(selected_sample_name)
    
    def _store_fit_results(self, sample, FittedParams, covar, ZoneValueDeviation, R2,
                           FittedParams_2=None, covar_2=None, ZoneValueDeviation_2=None, R2_2=None):
        results = [self.combobox.get(), FittedParams, covar, ZoneValueDeviation, R2]
        if FittedParams_2 is not None:
            results.extend([self.combobox.get(), FittedParams_2, covar_2, ZoneValueDeviation_2, R2_2])

        sample.disp_fit = results

    def _get_file_names(self, sample):
        if len(sample.disp_fit) == 10:
            return [sample.file_name, sample.file_name + "_2nd"]
        return [sample.file_name]

    def ExportExcel_event(self):
        TMP_Exportfile = [global_vars.DataStorage[dataname] for dataname in global_vars.DataStorage if self.sample_select_scroll_frame.checkboxes[dataname].get() == 'on' and global_vars.DataStorage[dataname].disp_fit]
        ExportFFCFitToExcel(os.path.dirname(TMP_Exportfile[0].file_path), TMP_Exportfile)
    
    def recalculate_dispersion(self, sample_name):
        """
        Recalculate dispersion for a given sample_name without changing GUI selection.
        """
        sample = global_vars.DataStorage.get(sample_name)
        if not sample:
            print(f"No sample found for {sample_name}")
            return
    
        # Primary dispersion
        FieldStrengths = np.array(sample.zone_parameters['BR'], dtype=np.float64) * 1e6
        Dispersion = np.array(sample.zone2disp_data[0])
        Mask = sample.zone_parameters['DataMask'][0]
        FieldStrengths_masked, Dispersion_masked = FieldStrengths[Mask], Dispersion[Mask]
    
        FittedParams, covar, ZoneValueDeviation = DispersionFit(self.combobox.get(), FieldStrengths_masked, Dispersion_masked)
        R2 = CalculateR2(FieldStrengths_masked, Dispersion_masked, self.combobox.get(), list(FittedParams))
        
        # Store results
        sample.disp_fit[1:5] = [FittedParams, covar, ZoneValueDeviation, R2]
    
        # Secondary dispersion (if exists)
        if len(sample.zone2disp_data) >= 5:
            Dispersion2 = np.array(sample.zone2disp_data[4])
            Mask2 = sample.zone_parameters['DataMask'][1]
            FieldStrengths2, Dispersion2_masked = FieldStrengths[Mask2], Dispersion2[Mask2]
    
            FittedParams2, covar2, ZoneValueDeviation2 = DispersionFit(self.combobox.get(), FieldStrengths2, Dispersion2_masked)
            R2_2 = CalculateR2(FieldStrengths2, Dispersion2_masked, self.combobox.get(), list(FittedParams2))
            
            sample.disp_fit[6:10] = [FittedParams2, covar2, ZoneValueDeviation2, R2_2]

