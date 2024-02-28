import subprocess
import json
import shutil
from log_functions import *
from file_creator import *
from plot import *

@log_actions
def import_input_parameters(input_worbook_name,method_name='import_excel_file'):
    python_instantiation_path = os.path.join(this_dir, "package_launcher.py")
    run_TMactivation_command = f"source {activateTM_path}"
    run_python_command = f"python {python_instantiation_path} {method_name} {input_worbook_name}"
    combined_command = f"/bin/bash -c '{run_TMactivation_command} && {run_python_command}'"
    logging.info(f"Importing data from Excel: {input_worbook_name}")
    print(f"Importing data from Excel: {input_worbook_name}")
    try:
        subprocess.run(combined_command, shell=True, check=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        with open('user_parameters.json', 'r') as file:
            user_input_parameters = json.load(file)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error occurred during subprocess execution: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    return user_input_parameters#subprocess_output
@log_actions
def multiple_run_simulation(results_filename_list,method_name='multiple_runs'):
    auto_saved_results_path = os.path.join(tm_model_dir,"auto-saved-results")
    logging.info("Starting multiple run simulation...")
    print("Starting multiple run simulations...")
    for i, result_filename_path in zip(range(1, init_runs + 1), results_filename_list):
        # Calls and runs the shell file .sh that activates Telemac environment and runs the python file .py which starts a Telemac simulation
        # The shell file has to be run (sourcing Telemac source pysource.xxxxx.sh) everytime a simulation starts within the loop.
        case_file = f"{case_file_base}"
        case_file = case_file.split('.')
        if len(case_file) == 2:
            case_file = f"{case_file[0]}-{i}.{case_file[1]}"
        else:
            logging.info("Invalid file name format")
        logging.info(f"RUNNING .cas FILE>>> {case_file}")
        print(f"RUNNING .cas FILE>>> {case_file}")
        run_TMactivation_command = f"source {activateTM_path}"  # Activates Telemac
        python_instantiation_path = os.path.join(this_dir, "package_launcher.py")
        run_python_command = (f"python {python_instantiation_path} {method_name} "
                              f"{i} {case_file} "
                              f"{result_filename_path} "
                              f"{results_filename_base}")
        combined_command = f"/bin/bash -c '{run_TMactivation_command} && {run_python_command}'"
        try:
            subprocess.run(combined_command, shell=True, check=True)
            shutil.copy2(result_filename_path, auto_saved_results_path)
            os.remove(result_filename_path)
            logging.info(f".slf and .txt files for: '{result_filename_path}' copied to >>>>>> auto-saved-results.")
            print(f".slf and .txt files for: '{result_filename_path}' copied to >>>>>> auto-saved-results.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error occurred during run {i}: {e}")
        except Exception as e:
            logging.error(f"An error occurred during run {i}: {e}")
# Call the main function if the script is executed directly
if __name__ == "__main__":
    user_input_parameters=import_input_parameters(input_worbook_name,method_name='import_excel_file')
    logging.info(f"The selected input parameters are >>>>> {user_input_parameters}")
    init_runs=user_input_parameters['init_runs']
    case_file_base=user_input_parameters['TM_CAS']
    tm_model_dir=user_input_parameters['SIM_DIR']
    init_run_sampling=user_input_parameters['init_run_sampling']
    calib_param_range=user_input_parameters['calib_param_range']
    source_file = tm_model_dir + case_file_base
    logging.info(f"Creating {init_runs} .cas files for surrogate model construction >>>>>> .....")
    print(f"Creating {init_runs} .cas files for surrogate model construction >>>>>> .....")
    results_filename_list,random_param=cas_creator(source_file, tm_model_dir, init_runs,results_filename_base,calib_param_range)
    multiple_run_simulation(results_filename_list)
    results_df=sim_output_df(tm_model_dir, init_runs,results_filename_base,output_excel_file_name,random_param)
    logging.info(f"Output *.xlsx file {output_excel_file_name} created in >>>>>> auto-saved-results.")
    print(f"Output *.xlsx file {output_excel_file_name} created in >>>>>> auto-saved-results.")
    plot_graph = PlotGraph(log_directory, output_excel_file_name)
    plot_graph.read_excel_file()
    plot_graph.plot_data()
    plot_graph.average()



