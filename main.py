#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 22:39:49 2024

@author: Joachim
"""

# Import dependencies


# Import local dependencies
from UI.ffc_application import FFC_Application as App
import global_vars

global_vars.init()


app = App()
app.mainloop()

test = global_vars.DataStorage