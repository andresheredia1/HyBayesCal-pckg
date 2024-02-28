try:
    import logging
    import os
except ModuleNotFoundError as basic:
    print(
        'ModuleNotFoundError: Missing basic libraries (required: logging, '
        'os)')
    print(basic)

try:
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import random
except ModuleNotFoundError as additional:
    print(
        'ModuleNotFoundError: Missing global packages (required: numpy, '
        'pandas, maptlotlib, random)')
    print(additional)

# Define file paths
input_worbook_name = "/home/amintvm/modeling/HyBayesCal-pckg-master/use-case-xlsx/tm-user-input_parameters.xlsx"
activateTM_path = "/home/amintvm/modeling/HyBayesCal-pckg-master/env-scripts/activateTM.sh"
results_filename_base = "r2dsteady"  # Choose this according to how it is written in the .cas base file. Do not add the extension.
output_excel_file_name="simulation_outputs.xlsx" # Choose a name for the **.xlsx output file.
log_directory = '/home/amintvm/modeling/HyBayesCal-pckg-master/simulationxxxx/auto-saved-results' #Choose a directory where you want to save the logfile.log. 
node_file_name='nodes_input.txt' # file to filter the required Nodes
node_file_path='/home/amintvm/modeling/HyBayesCal-pckg-master/HyBayesCal/' # Location to place the .txt file
# Absolute path of the current directory
this_dir = os.path.abspath(".")
logfile_path = os.path.join(log_directory, "logfile.log")
