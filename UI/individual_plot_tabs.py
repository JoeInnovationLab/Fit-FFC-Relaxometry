#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 15:00:57 2024

@author: Joachim
"""

# Import dependencies
import customtkinter as ctk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import warnings

# import local dependencies
from math_functions.mapping_functions import all_Zone_functions,all_Dispersion_functions
import global_vars

class IndividualPlotTabs(ctk.CTkTabview):
    def __init__(self, master, mask_zones_frame = None, **kwargs):
        super().__init__(master, **kwargs)
        
        # Store reference to mask_zones_frame
        self.mask_zones_frame = mask_zones_frame
        self.sample_select_scroll_frame = None
        
        self.MaskToggle = False   
        self.create_tabs()
        self.create_widgets()
        
    def create_tabs(self):
        """Create and add tabs."""
        self.add("Blocks to Zone Plots")
        self.add("Dispersion Plots")
        
    def create_widgets(self):
        """Initialize and arrange widgets on the tabs."""
        self.create_dispersion_widgets()
        self.create_zone_widgets()
        self.MaskButton = ctk.CTkButton(self.tab("Dispersion Plots"), text="Open Masking", command=self.toggle_mask)
        self.MaskButton.grid_forget()

    def create_dispersion_widgets(self):
        """Create widgets for the Dispersion Plots tab."""
        self.label = ctk.CTkLabel(master=self.tab("Dispersion Plots"), text="Sample:")
        self.label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        self.combobox_SampleDispersion = ctk.StringVar()
        self.comboboxSamplesDispersion = ctk.CTkComboBox(
            self.tab("Dispersion Plots"),
            command=self.DispersionSamplecombobox_callback,
            variable=self.combobox_SampleDispersion
        )
        self.comboboxSamplesDispersion.set("Select Sample")
        self.comboboxSamplesDispersion.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

    def create_zone_widgets(self):
        """Create widgets for the Blocks to Zone Plots tab."""
        self.label1 = ctk.CTkLabel(master=self.tab("Blocks to Zone Plots"), text="Sample:")
        self.label1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        self.combobox_SampleNames = ctk.StringVar()
        self.comboboxSamples = ctk.CTkComboBox(
            self.tab("Blocks to Zone Plots"),
            command=self.Samplecombobox_callback,
            variable=self.combobox_SampleNames
        )
        self.comboboxSamples.set("Select Sample")
        self.comboboxSamples.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.combobox_Zonevar = ctk.StringVar()
        self.comboboxZones = ctk.CTkComboBox(
            self.tab("Blocks to Zone Plots"),
            command=self.Zonecombobox_callback,
            variable=self.combobox_Zonevar
        )
        self.comboboxZones.set("Select Zone")
        self.comboboxZones.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
    
    def toggle_mask(self):
        """Toggle the Mask Zones frame."""
        if self.MaskToggle:
            self.mask_zones_frame.pack_forget()
            # Update button text for the mode we're in
            if self.comboboxSamplesDispersion.get() == "All":
                self.MaskButton.configure(text="Open Global Masking")
            else:
                self.MaskButton.configure(text="Open Masking")
        else:
            self.mask_zones_frame.pack(side=ctk.TOP, fill=ctk.BOTH, padx=5, pady=5)
            # Build checkboxes for current selection
            self.mask_zones_frame.addR1CheckBox(self.comboboxSamplesDispersion.get())
            if self.comboboxSamplesDispersion.get() == "All":
                self.MaskButton.configure(text="Close Global Masking")
            else:
                self.MaskButton.configure(text="Close Masking")
        self.MaskToggle = not self.MaskToggle

        
    def set_sample_select_scroll_frame(self, sample_select_scroll_frame):
        """Set the SampleSelectFrameScroll after initialization."""
        self.sample_select_scroll_frame = sample_select_scroll_frame
        
    def Samplecombobox_callback(self, choice):
        """Handle sample selection and update zone options."""
        if self.comboboxSamples.get() != "Select Sample":
            NumberofZones = self.get_number_of_zones(self.comboboxSamples.get())
            self.update_zone_combobox(NumberofZones)
            if self.combobox_Zonevar.get() != "Select Zone":
                self.Zonecombobox_callback(self.combobox_Zonevar.get())
    
    def get_number_of_zones(self, sample_name):
        """Get the number of zones for the selected sample."""
        for dataname in global_vars.DataStorage:
            if dataname == sample_name:
                return len(global_vars.DataStorage[dataname].zone_data)
        return 0
    
    def update_zone_combobox(self, NumberofZones):
        """Update zone combobox with the appropriate number of zones."""
        if NumberofZones:
            tmpZonesinSample = [f"Zone: {s}" for s in range(1, NumberofZones + 1)]
            self.comboboxZones.configure(values=tmpZonesinSample)

    def Zonecombobox_callback(self, choice):
        """Callback function when a zone is selected from the combobox."""
        SelectedZone = int(choice.split(": ")[1]) - 1
        
        for dataname in global_vars.DataStorage:
            if dataname == self.comboboxSamples.get():
                
                BlockYData = global_vars.DataStorage[dataname].block2zone_data[0][SelectedZone]
                BlockYErr = np.transpose(global_vars.DataStorage[dataname].block2zone_data[1][SelectedZone])
                ZoneParameters = global_vars.DataStorage[dataname].zone_parameters
                Number_of_Blocks = int(global_vars.DataStorage[dataname].parameter_summary['NBLK'])
                BlockT1Max = float(ZoneParameters['T1Max'][SelectedZone])
                
                ZoneTimes = self.calculate_zone_times(BlockT1Max,ZoneParameters['PrePolarization'][SelectedZone],Number_of_Blocks)
                
                BlockFitFun = global_vars.DataStorage[dataname].zone2disp_data[2]
                BlockFitParams = list(global_vars.DataStorage[dataname].zone2disp_data[3][SelectedZone])
                
                fig = self.create_plot(ZoneTimes, BlockYData, BlockYErr, BlockFitFun, BlockFitParams)
                self.display_plot(fig, tab_name="Blocks to Zone Plots")

    def calculate_zone_times(self, BlockT1Max, TimeOrder, Number_of_Blocks):
        """Calculate the times for the zone based on the block T1 max and time order."""
        if TimeOrder == "NP":
            return np.logspace(np.log10(4 * BlockT1Max * 1e-6), np.log10(0.1 * BlockT1Max * 1e-6), num=Number_of_Blocks, base=10)
        elif TimeOrder == "PP":
            return np.logspace(np.log10(0.1 * BlockT1Max * 1e-6), np.log10(4 * BlockT1Max * 1e-6), num=Number_of_Blocks, base=10)

    def create_plot(self, x_data, y_data, y_err, BlockFitFun=None, BlockFitParams=None, x_label="Evolution Time (s)", y_label="Average of Magnitude"):
        """Create a plot with optional error bars and a fitted function."""
        fig = Figure(figsize=(6, 5), dpi=100)
        ax = fig.add_subplot(111)
        
        # Plotting the data with error bars
        ax.errorbar(x_data, y_data, yerr=y_err, linestyle='', marker='+', color="navy")
        
        # Plotting the fitted function if provided
        if BlockFitFun is not None and BlockFitParams is not None:
            ax.plot(x_data, all_Zone_functions(BlockFitFun)(x_data, *BlockFitParams), color="orangered")
        
        # Setting the scale and labels
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set(xlabel=x_label, ylabel=y_label)
        fig.tight_layout()
        
        return fig

    def display_plot(self, fig, tab_name):
        """Display the plot in the specified tab."""
        self.canvas = FigureCanvasTkAgg(fig, master=self.tab(tab_name))
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0, padx=5, pady=5, sticky="nsew", rowspan=3, columnspan=4)
    
    def DispersionSamplecombobox_callback(self, choice):
        SelDisp = self.comboboxSamplesDispersion.get()
    
        # Hide or show the mask button depending on selection
        if SelDisp == "Select Sample":
            # If the mask panel is open, close it when nothing is selected
            if self.MaskToggle:
                self.mask_zones_frame.pack_forget()
                self.MaskToggle = False
            self.MaskButton.grid_forget()
            return
    
        if SelDisp == "All":
            self.plot_all_dispersion_data()
            # If the mask panel is open, refresh its contents for global mode
            if self.MaskToggle:
                self.mask_zones_frame.addR1CheckBox("All")
                self.MaskButton.configure(text="Close Global Masking")
            else:
                self.MaskButton.configure(text="Open Global Masking")
            self.MaskButton.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
    
        else:
            self.plot_dispersion_data(SelDisp)
            # If the mask panel is open, refresh its contents for the selected sample
            if self.MaskToggle:
                self.mask_zones_frame.addR1CheckBox(SelDisp)
                self.MaskButton.configure(text="Close Masking")
            else:
                self.MaskButton.configure(text="Open Masking")
            self.MaskButton.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")


    def plot_dispersion_data(self, SelDisp):
        """Plot data for the selected dispersion sample."""
        for dataname in global_vars.DataStorage:
            if SelDisp == dataname:
                self.plot_dispersion_sample(global_vars.DataStorage[dataname], multi_disp = False)
            elif SelDisp[:-4] == dataname:
                self.plot_dispersion_sample(global_vars.DataStorage[dataname], multi_disp = True)

    def plot_all_dispersion_data(self):
        """Plot all dispersion data."""
        fig = self.create_combined_dispersion_plot()
        self.display_plot(fig, tab_name="Dispersion Plots")
        
    def create_combined_dispersion_plot(self):
        """Create and return a combined plot for all dispersion samples."""
        fig = Figure(figsize=(6, 5), dpi=100, layout='constrained')
        ax = fig.add_subplot(111)
        LegendLabels = []
        for dataname in global_vars.DataStorage:
            if self.sample_select_scroll_frame.checkboxes[dataname].get() == 'on':
                
                FieldStrengths = np.array(global_vars.DataStorage[dataname].zone_parameters['BR'], dtype=np.float64) * 1e6
                Dispersion = np.array(global_vars.DataStorage[dataname].zone2disp_data[0])
    
                # Mask the data according to selection
                Mask = global_vars.DataStorage[dataname].zone_parameters['DataMask'][0]
                FieldStrengths, Dispersion = FieldStrengths[Mask], Dispersion[Mask]
                
                # Get the next color in the cycle
                color = next(ax._get_lines.prop_cycler)['color']
                ax.plot(FieldStrengths, Dispersion, linestyle='', marker='o', color=color, label=dataname)
                ax.plot(FieldStrengths, all_Dispersion_functions(global_vars.DataStorage[dataname].disp_fit[0])(FieldStrengths, *global_vars.DataStorage[dataname].disp_fit[1]), color=color)
                
                # Append legend
                LegendLabels.append("_")
                LegendLabels.append(dataname + r' ($R^2$: %.2f)' % global_vars.DataStorage[dataname].disp_fit[4])
                
                if len(global_vars.DataStorage[dataname].disp_fit) == 10:
                    FieldStrengths = np.array(global_vars.DataStorage[dataname].zone_parameters['BR'], dtype=np.float64) * 1e6
                    Dispersion = np.array(global_vars.DataStorage[dataname].zone2disp_data[4])
    
                    # Mask the data according to selection
                    Mask = global_vars.DataStorage[dataname].zone_parameters['DataMask'][1]
                    FieldStrengths, Dispersion = FieldStrengths[Mask], Dispersion[Mask]
                    
                    # Get the next color in the cycle
                    # color = next(ax._get_lines.prop_cycler)['color']
                    ax.plot(FieldStrengths, Dispersion, linestyle='', marker='o', color=color, label=dataname)
                    ax.plot(FieldStrengths, all_Dispersion_functions(global_vars.DataStorage[dataname].disp_fit[5])(FieldStrengths, *global_vars.DataStorage[dataname].disp_fit[6]), color=color)
                    
                    # Append legend
                    LegendLabels.append("_")
                    LegendLabels.append(dataname +'_2nd' + " " + r' ($R^2$: %.2f)' % global_vars.DataStorage[dataname].disp_fit[9])
                    
                    
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set(xlabel="Evolution Field (Hz)",ylabel=str("$R_{1}$"  + r'$(\frac{1}{s})$'))
        # ax.set(xlabel="Evolution Time (s)", ylabel="Average of Magnitude")
        # fig.tight_layout()
        
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message="The label '_'")
            # fig.gca().legend(LegendLabels,loc='upper right')
            if len(LegendLabels) > 4:
                # fig.set_size_inches(5,5)
                fig.legend(LegendLabels,ncol=2,loc='outside lower right')
            else:
                fig.legend(LegendLabels,loc='outside lower right')
        
        return fig

    def plot_dispersion_sample(self, sample_data, multi_disp = False):
        """Plot a single dispersion sample."""
        fig = self.create_dispersion_sample_plot(sample_data,multi_disp)
        self.display_plot(fig, tab_name="Dispersion Plots")
        
    def create_dispersion_sample_plot(self, sample_data,multi_disp = False):
        """Create and return a plot for a single dispersion sample."""
        fig = Figure(figsize=(6, 5), dpi=100)
        ax = fig.add_subplot(111)
        
        FieldStrengths = np.array(sample_data.zone_parameters['BR'], dtype=np.float64) * 1e6
        
        if multi_disp == False:
            Dispersion = np.array(sample_data.zone2disp_data[0])

            # Mask the data according to selection
            Mask = sample_data.zone_parameters['DataMask'][0]
            FieldStrengths, Dispersion = FieldStrengths[Mask], Dispersion[Mask]
            ax.plot(FieldStrengths, Dispersion, linestyle='', marker='o', color="navy", label=sample_data.file_name)
            ax.plot(FieldStrengths, all_Dispersion_functions(sample_data.disp_fit[0])(FieldStrengths, *sample_data.disp_fit[1]), color="orangered")
            
        elif multi_disp == True:
            Dispersion = np.array(sample_data.zone2disp_data[4])

            # Mask the data according to selection
            Mask = sample_data.zone_parameters['DataMask'][1]
            FieldStrengths, Dispersion = FieldStrengths[Mask], Dispersion[Mask]
            ax.plot(FieldStrengths, Dispersion, linestyle='', marker='o', color="navy", label=sample_data.file_name + '_2nd')
            ax.plot(FieldStrengths, all_Dispersion_functions(sample_data.disp_fit[5])(FieldStrengths, *sample_data.disp_fit[6]), color="orangered")
        
        
        
        
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set(xlabel="Evolution Field (Hz)",ylabel=str("$R_{1}$"  + r'$(\frac{1}{s})$'))
        # ax.set(xlabel="Evolution Time (s)", ylabel="Average of Magnitude")
        fig.tight_layout()
        return fig

