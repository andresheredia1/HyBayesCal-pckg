import os

# Define file paths
input_worbook_name = "/home/amintvm/modeling/simulation_test/use-case-xlsx/tm-user-input_parameters.xlsx"
activateTM_path = "/home/amintvm/modeling/simulation_test/env-scripts/activateTM.sh"
results_filename_base = "r2dsteady"  # Choose this according to how it is written in the .cas base file. Do not add the extension.
output_excel_file_name="simulation_outputs.xlsx" # Choose a name for the **.xlsx output file.
log_directory = '/home/amintvm/modeling/simulation_test/' #Choose a directory where you want to save the logfile.log. 
# Absolute path of the current directory
this_dir = os.path.abspath(".")
logfile_path = os.path.join(log_directory, "logfile.log")
