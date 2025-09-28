#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 21:57:04 2024

@author: Joachim
"""

# Import dependencies
import customtkinter as ctk

# Import local dependencies
from UI.file_select_frame import FileSelectFrame
from UI.sample_select_frame import SampleSelectFrame  
from UI.block_fit_select_frame import BlockFitSelectFrame  
from UI.sample_select_frame_scroll import SampleSelectFrameScroll
from UI.dispersion_fit_select_frame import DispersionFitSelectFrame
from UI.individual_plot_tabs import IndividualPlotTabs
from UI.mask_zone_frame import MaskZonesFrame

from math_functions.mapping_functions import Block_Function_Mapper, Zone_Function_Mapper

class FFC_Application(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
        # Get screen resolution dynamically
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Set the window size based on a percentage of the screen resolution (e.g., 80%)
        window_width = int(screen_width * 0.7)
        window_height = int(screen_height * 0.9)
        
        # Configure window properties
        self.geometry(f"{window_width}x{window_height}")
        
        # Configure window properties
        # self.geometry("1000x800")
        self.title("FFC Analysis")
        self.DataStorage = {}

        # Configure grid layout (4x4)
        self._configure_grid_layout()
        
        # Create plotting frame
        self._create_plotting_frame()
        
        # Create sidebar with widgets
        self._create_sidebar()
        
        # Now that sidebar is initialized, pass sample_select_scroll_frame to individual_plots
        self.individual_plots.set_sample_select_scroll_frame(self.sample_select_scroll_frame)
        
        self.mask_zones_frame.set_dispersion_fit_select_frame(self.dispersion_fit_select_frame)
        self.mask_zones_frame.set_individual_plots(self.individual_plots)
        
        
        # Define app variables
        self.toplevel_window = None

    def _configure_grid_layout(self):
        """Configure the grid layout of the main window."""
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

    def _create_sidebar(self):
        """Create and configure the sidebar frame with its widgets."""
        self.sidebar_frame = ctk.CTkScrollableFrame(self, width=220, corner_radius=0, fg_color="transparent")
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(0, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="FFC Analysis", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=10, pady=(20, 10))
        
        # Insert Scrollable Frame for Sample Selection Checkboxes (initially hidden)
        self.sample_select_scroll_frame = SampleSelectFrameScroll(self.sidebar_frame, height=300)
        self.sample_select_scroll_frame.grid_forget()
        
        # Insert Dispersion Selection Frame (initially hidden)
        self.dispersion_fit_select_frame = DispersionFitSelectFrame(self.sidebar_frame, sample_select_scroll_frame=self.sample_select_scroll_frame, individual_plots = self.individual_plots)
        self.dispersion_fit_select_frame.grid_forget()
        
        # Insert Block Fit Selection frame (initially hidden)
        self.block_fit_selection_frame = BlockFitSelectFrame(self.sidebar_frame,list(Block_Function_Mapper.keys()), list(Zone_Function_Mapper.keys()), sample_select_scroll_frame=self.sample_select_scroll_frame, dispersion_fit_select_frame = self.dispersion_fit_select_frame, individual_plots = self.individual_plots)
        self.block_fit_selection_frame.grid_forget()
        
        # Insert File selection frame
        self.file_selection_frame = FileSelectFrame(self.sidebar_frame, block_fit_selection_frame=self.block_fit_selection_frame, sample_select_scroll_frame=self.sample_select_scroll_frame)
        self.file_selection_frame.grid(row=0, column=0, padx=10, pady=20, sticky="nsew")

        # Insert Sample selection frame (initially hidden)
        self.sample_selection_frame = SampleSelectFrame(self.sidebar_frame)
        self.sample_selection_frame.grid_forget()

    def _create_plotting_frame(self):
        """Create and configure the plotting frame."""
        self.plotting_frame = ctk.CTkScrollableFrame(self, width=600, corner_radius=0, fg_color="transparent")
        self.plotting_frame.grid(row=0, column=1, rowspan=4, columnspan=3, sticky="nsew")
        self.plotting_frame.grid_rowconfigure(0, weight=1)
        
        # Insert Mask Zones Frame (initially hidden)
        self.mask_zones_frame = MaskZonesFrame(self.plotting_frame)
        self.mask_zones_frame.pack_forget()
        
        # Insert individual plots tab
        self.individual_plots = IndividualPlotTabs(self.plotting_frame, mask_zones_frame = self.mask_zones_frame)
        self.individual_plots.pack(side=ctk.TOP, fill=ctk.BOTH, padx=5, pady=5, expand=True)

        

if __name__ == "__main__":
    import global_vars

    global_vars.init()
    
    app = FFC_Application()
    app.mainloop()