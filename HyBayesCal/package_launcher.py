import sys
from bayesian_gpe import *
import json
import pdb
class TelemacSimulations:
    # def __init__(self,
                 # input_worbook_name="/home/amintvm/modeling/hybayescalpycourse/use-case-xlsx/tm-user-input_parameters_15_02_2024.xlsx",
                 # method_name='import_excel_file', *args, **kwargs):
    def __init__(self, input_worbook_name=str(sys.argv[2]),
                 method_name=str(sys.argv[1]),
                 *args,
                 **kwargs):
        self.input_worbook_name=input_worbook_name
        self.method_name=method_name
    def single_run_simulation(self,user_input_parameters):
        """
        Run a single Telemac simulation.S
        """
        #pdb.set_trace()
        if len(sys.argv) != 7:
            print(len(sys.argv))
            print("Incorrect number of command-line arguments passed to the script!!")
            sys.exit(1)
        self.i = int(sys.argv[2]) #2
        self.this_dir = str(sys.argv[3])#'/home/amintvm/modeling/hybayescalpycourse_md/HyBayesCal'
        self.case_file = str(sys.argv[4])#'2dsteady-1.cas'
        self.result_filename_path=str(sys.argv[5])
        self.results_filename_base=str(sys.argv[6])
        self.tm_model_dir = user_input_parameters['SIM_DIR']
        self.tm_xd = user_input_parameters['tm_xD']
        self.N_CPUS=user_input_parameters['N_CPUS']
        self.CALIB_TARGETS = str(user_input_parameters['CALIB_TARGETS'][0])
        #pdb.set_trace()
        replacement_map = {
            "VELOCITY": "VELOCITY U",
            "DEPTH": "WATER DEPTH"
        }
        for old_str, new_str in replacement_map.items():
            self.CALIB_TARGETS = self.CALIB_TARGETS.replace(old_str, new_str)
        #pdb.set_trace()
        # print(self.CALIB_TARGETS)
        # print(type(self.CALIB_TARGETS))
        tm_model = TelemacModel(
            model_dir=self.tm_model_dir,
            control_file=self.case_file,
            tm_xd=self.tm_xd,
            n_processors=self.N_CPUS,
        )
        tm_model.run_simulation()
        modelled_results=tm_model.get_variable_value(slf_file_name=self.result_filename_path,calibration_par=self.CALIB_TARGETS,specific_nodes=None,save_name=self.tm_model_dir+f"/auto-saved-results/{self.results_filename_base}-{self.i}.txt")
        # print(type(modelled_results))
    def import_excel_file(self):
        if len(sys.argv) != 3:
            print("Incorrect number of command-line arguments passed to the SUBPROCESS!!")
            sys.exit(1)
        xlsx_import = BalWithGPE(self.input_worbook_name,) #software_coupling="telemac"
        return {'init_runs': xlsx_import.init_runs,
            'CALIB_PTS': xlsx_import.CALIB_PTS,
            'AL_STRATEGY': xlsx_import.AL_STRATEGY,
            'score_method':xlsx_import.score_method,
            'IT_LIMIT': xlsx_import.IT_LIMIT,
            'AL_SAMPLES':xlsx_import.AL_SAMPLES,
            'MC_SAMPLES':xlsx_import.MC_SAMPLES,
            'MC_SAMPLES_AL':xlsx_import.MC_SAMPLES_AL,
            'TM_CAS': xlsx_import.TM_CAS,
            'SIM_DIR': xlsx_import.SIM_DIR,
            'tm_xD': xlsx_import.tm_xD,
            'N_CPUS': xlsx_import.N_CPUS,
            'init_run_sampling': xlsx_import.init_run_sampling,
            'calib_param_range': xlsx_import.CALIB_PAR_SET['FRICTION COEFFICIENT']['bounds'],
            'CALIB_TARGETS': xlsx_import.CALIB_TARGETS,
            # Add other parameters here as needed
            }
    def __call__(self):
        if self.method_name == 'import_excel_file':
            output = self.import_excel_file()
            with open('data.json', 'w') as file:
                json.dump(output, file)
        elif self.method_name == 'multiple_runs':
            with open('data.json', 'r') as file:
                user_input_parameters = json.load(file)
            self.single_run_simulation(user_input_parameters)
if __name__ == "__main__":

    simulation = TelemacSimulations()
    simulation() # This will call the __call__ method and execute the appropriate action based on the command-line arguments
