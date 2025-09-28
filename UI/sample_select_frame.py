#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 14:27:13 2024

@author: Joachim
"""

# Import dependencies
import customtkinter as ctk

class SampleSelectFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # add widgets onto the frame, for example:
        self.label = ctk.CTkLabel(self,text="Select Sample to be plotted",font=("Arial",10))
        self.label.grid(row=0, column=0)
        
        # Sample selection option box
        self.combobox_1 = ctk.CTkComboBox(self)
        self.combobox_1.grid(row=1, column=0, padx=10, pady=(0, 10),rowspan=2)        