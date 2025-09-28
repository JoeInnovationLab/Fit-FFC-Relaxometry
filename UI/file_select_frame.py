#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 22:20:14 2024

@author: Joachim
"""

# Import dependencies
import customtkinter as ctk
from tkinter.filedialog import askopenfilenames
import os

# Import local dependencies
from data_import.import_sdf_files import import_sdf_file
import global_vars

class FileSelectFrame(ctk.CTkFrame):
    def __init__(self, master, block_fit_selection_frame=None, sample_select_scroll_frame=None, **kwargs):
        super().__init__(master, **kwargs)
        
        # Store reference to BlockFitSelectFrame
        self.block_fit_selection_frame = block_fit_selection_frame
        
        # Store reference to sample_select_scroll_frame
        self.sample_select_scroll_frame = sample_select_scroll_frame
        
        # Configure the label
        self.label = ctk.CTkLabel(self, text="FFC File Selection", font=("Arial", 10), width=200)
        self.label.grid(row=0, column=0)

        # Configure the button
        self.select_file_button = ctk.CTkButton(self, text="Select SDF file", command=self.open_file_dialog)
        self.select_file_button.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    def open_file_dialog(self):
        # Ask user to select import files
        filetypes = [
            ('SDF files', '*.sdf'),
            ('SEF files', '*.sef'),
            ('Text files', '*.txt'),
            ('All files', '*.*')
        ]

        # Show dialog box and return the selected file paths
        selected_files = askopenfilenames(filetypes=filetypes)

        # Process selected files
        if selected_files:
            for file_path in selected_files:
                file_name, file_ext = os.path.splitext(os.path.basename(file_path))
                if file_ext == ".sdf":
                    global_vars.DataStorage[file_name] = import_sdf_file(file_path)

                        
            # Now access and set values in BlockFitSelectFrame comboboxes
            self.block_fit_selection_frame.combobox_1.set("Select Fitting")
            self.block_fit_selection_frame.combobox_2.set("Select Fitting")
            self.block_fit_selection_frame.grid(row=4, column=0, padx=10, pady=20, sticky="nsew")
            
            # Adding files to selection list
            for fname in list(global_vars.DataStorage.keys()):
                self.sample_select_scroll_frame.addCheckBox(str(fname))
               
            self.sample_select_scroll_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew", rowspan=3)