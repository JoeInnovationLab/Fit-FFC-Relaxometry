#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 14:48:35 2024

@author: Joachim
"""
# Import dependencies
import customtkinter as ctk


class SampleSelectFrameScroll(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.checkboxes = {}  # Dictionary to store checkboxes and their associated variables

        # Configure the frame to expand vertically
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Add widgets onto the frame
        self.label = ctk.CTkLabel(self, text="Sample Selection", font=("Arial", 10))
        self.label.pack(padx=10, pady=15, side=ctk.TOP)

    def addCheckBox(self, checkBoxName):
        # Use setdefault to avoid redundant existence check
        var = self.checkboxes.setdefault(checkBoxName, ctk.StringVar(value="on"))

        # Create and pack the checkbox only if it wasn't already in the dictionary
        if var.get() == "on" and not hasattr(var, 'checkbox'):
            c = ctk.CTkCheckBox(self, text=checkBoxName, variable=var, onvalue="on", offvalue="off")
            c.pack(side=ctk.TOP, fill=ctk.BOTH, padx=10, pady=1)
            var.checkbox = c  # Link the variable to the checkbox widget

    def getCheckboxValues(self):
        # Retrieve the values of all checkboxes using a dictionary comprehension
        return {name: var.get() for name, var in self.checkboxes.items()}
