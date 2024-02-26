import logging
import os
#from log_functions import *
#import logging
import random
import pandas as pd
"""
Creates .cas files according to the number in full complexity models
"""
def cas_creator(source_file, tm_model_dir, init_runs,results_filename_base,calib_param_range):
    results_filename_list=[]
    file_name = os.path.basename(source_file)
    prefix, extension = os.path.splitext(file_name)

    with open(source_file, 'r') as f:
        source_content = f.read()
    random_param = [random.uniform(calib_param_range[0], calib_param_range[1]) for _ in range(init_runs)]
    random_flowrate = [random.uniform(25, 45) for _ in range(init_runs)]

    for i in (range(1, init_runs + 1)):
        new_file_name = f"{prefix}-{i}{extension}"
        destination_file = os.path.join(tm_model_dir, new_file_name)

## This code block should be changed according to the used .cas base file.
##  -------------------------------------------------------------------------------------------------------
        new_content = (
            source_content
            .replace(f"RESULTS FILE : {results_filename_base}.slf",
                     f"RESULTS FILE : {results_filename_base}-{i}.slf")
            .replace("FRICTION COEFFICIENT : 0.03 / Roughness coefficient", f"FRICTION COEFFICIENT : {random_param[i-1]} / Roughness coefficient")
            .replace("PRESCRIBED FLOWRATES  : 35.; 0.",
                     f"PRESCRIBED FLOWRATES  : {random_flowrate[i-1]}; 0.")
        )
## ---------------------------------------------------------------------------------------------------------
        # random_value_roughness = round(random.uniform(0.01, 0.07), 3)
        # # print(random_value_roughness)
        # random_value_flowrate = round(random.uniform(150, 230), 1)
        # random_value_roughness = round(random.uniform(0.01, 0.07), 3)
        # #print(random_value_roughness)
        # random_value_flowrate = round(random.uniform(150, 230), 1)
        # new_content = (
        #     source_content
        #     .replace(f"RESULTS FILE                                 : {results_filename_base}.slf",
        #              f"RESULTS FILE                                 : {results_filename_base}-{i}.slf")
        #     .replace("ROUGHNESS COEFFICIENT OF BOUNDARIES = 0.01", f"ROUGHNESS COEFFICIENT OF BOUNDARIES = {random_value_roughness}")
        #     .replace("PRESCRIBED FLOWRATES                        : 218.0 ; 218.0",
        #              f"PRESCRIBED FLOWRATES                        : {random_value_flowrate} ; {random_value_flowrate}")
        # )

        results_filename_list.append(os.path.join(tm_model_dir,f"{results_filename_base}-{i}.slf"))
        with open(destination_file, 'w') as f:
            f.write(new_content)

        #logging.info(f"Copy {i}: {destination_file}")
    return results_filename_list,random_param,random_flowrate
def sim_output_df(tm_model_dir, init_runs,results_filename_base,output_excel_file_name,random_param,random_flowrate):
    # Initialize an empty DataFrame to store the data
    results_filename_list_txt = []
    auto_saved_results_path=os.path.join(tm_model_dir,"auto-saved-results")
    for index in range(1,init_runs+1):
        # Get the file name without the extension
        result_path_txt= auto_saved_results_path+f"/{results_filename_base}"+f"-{index}"+".txt"
        results_filename_list_txt.append(result_path_txt)
    df_outputs = pd.DataFrame()
    # Loop through each file path
    for file_path in results_filename_list_txt:
        # Read the text file into a DataFrame
        data = pd.read_csv(file_path, header=None, delimiter='\s+')

        # Extract the second column and append it to the DataFrame
        df_outputs = pd.concat([df_outputs, data.iloc[:, 1]], axis=1)

    # Set column names
    column_names = [f"File: {results_filename_base}-{i+1} - {random_param[i]} - {random_flowrate[i]}" for i in range(len(results_filename_list_txt))]
    df_outputs.columns = column_names
    df_outputs['TM Nodes'] = range(1, len(df_outputs) + 1)
    df_outputs.set_index('TM Nodes', inplace=True)
    df_outputs.to_excel(auto_saved_results_path + "/" + output_excel_file_name)
    print("DataFrame saved to Excel file:", output_excel_file_name)
    return df_outputs
