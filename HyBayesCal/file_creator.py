from config import *

"""
Creates .cas files according to the number in full complexity models
"""
def cas_creator(source_file, tm_model_dir, init_runs,results_filename_base,calib_param_range):
    """
    Author - Andres
    Creates .cas files for full complexity models.

    Parameters:
    - source_file: Path to source file.
    - tm_model_dir: Directory for .cas files.
    - init_runs: Number of runs.
    - results_filename_base: Base filename for results.
    - calib_param_range: Range for calibration parameter.

    Returns:
    - results_filename_list: List of generated results filenames.
    - random_param: List of random calibration parameters.
    - random_flowrate: List of random flow rates.

    """    
    results_filename_list=[]
    file_name = os.path.basename(source_file)
    prefix, extension = os.path.splitext(file_name)

    with open(source_file, 'r') as f:
        source_content = f.read()
    random_param = [random.uniform(calib_param_range[0], calib_param_range[1]) for _ in range(init_runs)]

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
        )
## ---------------------------------------------------------------------------------------------------------
        results_filename_list.append(os.path.join(tm_model_dir,f"{results_filename_base}-{i}.slf"))
        with open(destination_file, 'w') as f:
            f.write(new_content)
    return results_filename_list,random_param
def sim_output_df(tm_model_dir, init_runs,results_filename_base,output_excel_file_name,random_param):
    """
    Creates DataFrame from simulation outputs and saves to Excel.

    Parameters:
    - tm_model_dir: Directory for simulation results.
    - init_runs: Number of runs.
    - results_filename_base: Base filename for results.
    - output_excel_file_name: Filename for Excel file.
    - random_param: List of random calibration parameters.
    - random_flowrate: List of random flow rates.

    Returns:
    - df_outputs: DataFrame of simulation outputs.

    """ 
    # Initializes an empty DataFrame to store the data
    results_filename_list_txt = []
    auto_saved_results_path=os.path.join(tm_model_dir,"auto-saved-results")
    for index in range(1,init_runs+1):
        # Gets the file name without the extension
        result_path_txt= auto_saved_results_path+f"/{results_filename_base}"+f"-{index}"+".txt"
        results_filename_list_txt.append(result_path_txt)
    df_outputs = pd.DataFrame()
    # Loops through each file path
    for file_path in results_filename_list_txt:
        # Reads the text file into a DataFrame
        data = pd.read_csv(file_path, header=None, delimiter='\s+')
        # Extracts the second column and append it to the DataFrame
        df_outputs = pd.concat([df_outputs, data.iloc[:, 1]], axis=1)
    # Sets column names
    column_names = [f"File: {results_filename_base}-{i+1} - {random_param[i]:.3f}" for i in range(len(results_filename_list_txt))]
    df_outputs.columns = column_names
    df_outputs['TM Nodes'] = range(1, len(df_outputs) + 1)
    df_outputs.set_index('TM Nodes', inplace=True)
    df_outputs.to_excel(auto_saved_results_path + "/" + output_excel_file_name)
    print("DataFrame saved to Excel file:", output_excel_file_name)
    return df_outputs

