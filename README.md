
# Python Package for Bayesian Calibration from Telemac Simulations
***
***Project's name***
"Advances" on a Python package for Bayesian calibration from Telemac Simulations

***Project purpose/description:***
This projects aims to make significant development and contribution on creating a Bayesian Calibration package in Python using (this time) numerical simulations in Telemac 2D. Bayesian calibration techniques require a huge number of model simulations to perform statistical analysis in light of measured data. This is ,in fact, unfeasible when running numerical models may requiere several hours just for one realization. To make this possible, surrogate models (reduced models) are constructed with only __a few number of model realizations__. In this context, the main purpose relies on the creation of a package which could be able to run multiple simulations of Telemac as the base of a surrogate model construction and proceeding with the subsequent Bayesian calibration. The original code is based on the work made by Mouris, K. et al (2023) applied to a reservoir model calibration. 

***Motivation:***

Extracting the required data such as user input parameters for calibration purposes from a unique Excel file .xlsx.
Automating the process of running Telemac simulations the requiered times to construct a surrogate model.
Extending the use of the package with other hydrodyamic numerical softwares. 
 

***Goal:***: Create a package which is able to run the multiple simulation of Telemac and along with the Bayesian calibration
The project focuses on three main tasks:
* Running a Telemac model through Python several times as a baseline to construct a surrogate model for calibration purposes.
* Managing simulation output files .slf to extract relevant data for calibration purposes.
* Performing statistical analysis from the data obtained from the Telemac output files .slf

GitHub Repository URL
```
[https://github.com](https://github.com/andresheredia1/hybayescalpycourse)
```

## Requirements
To use this Python package, we have decided to use a Linux Mint operating system which is a popular and user-friendly Linux distribution. One of the main reasons why the package runs in Linux is because Telemac is primarily developed and tested on Linux-based systems. It gives us the flexibility for configuring the environment and optimizing settings for Telemac simulations while providing a powerful command-line interface, which is well-suited for running batch simulations, automating tasks which improves the productivity of the code when managing large data sets. 

The creation of a virtual machine with the following characteristics is required:


### Virtual Machine
The Virtual Machine configuration for this project is detailed below. For further information about the creation of a virtual machine, please visit the provided [Virtual Machine](https://hydro-informatics.com/get-started/vm.html)
* Operationg System: Linux Mint Xfce 21.2
* Storage: SATA 64 GB
* Software
  * QGIS
  * Telemac V8p4r0 (MPI distribution and Metis 5.1.0)
  * Python 3
  * PyCharm Community Edition
* Python Library
  * matplotlib
  * mpi4py
  * numpy
  * openpyxl
  * pandas
  * scikit-learn

## Installation and run a project 

To use this package, ensure the previously mentioned software and Python libraries are installed:
* Upon the initial launch of the VM, the first essential task is to update the system (which should be performed periodically):
  * Open Terminal.
  * Enter the command: `sudo apt update`
  * Execute: `sudo apt full-upgrade`.
  * Conclude with: `sudo apt autoremove` to remove outdated packages.
* If any required software is missing, install it using the command
  ```
  sudo apt install app_name
  ``` 
* Conversely, if you need to uninstall a software use the command, (make sure to change the `app_name` with software name)
  ```
  sudo apt install app_name
  ```
Download the package and copy it to a desired folder. The download version of the package has some folders and scripts  which are explained in detail in the following lines. 
Once you downloaded the package you will see these folders. 
[figure 1]

The creation of a virtual environment to run the package is required. The downloaded version of the package has already an environment folder called HBCenv, however you can also create a new one called HBCenv with all the necessary requirements shown in the file requirementsHBCenv.txt. 

To do so, navigate to the folder you have copied the package (i.e. HyBayesCal-pckg) using a Linux terminal and create the virtual environment as follows:
```bash
python3 -m venv HBCenv
```
After creating the environment, activate it by typing:
```bash
cd HBCenv/bin/activate
```
Once the environment has been activated, install all the requirements according to requirementsHBCenv.txt file. 
```bash
pip install package_name
```
## Folders and Files 

### env-scripts
This folder contains the .sh files to activate Telemac and HBCenv environments, which are necessary to run the package. It is important that prior to running the package, you open each file and modify the directories based on your system. 

This folder contains the bash .sh files to activate Telemac and HBCenv environments, which are necessary to run the package. It is important that prior to running the package, you open each file and modify the directories based on your system. 

**activateHBCtelemac.sh**: Bash file that activates Telemac and the Python environment for the first run. Change the paths according to the following recommendations. 

1. *TELEMAC_CONFIG_DIR=/full/path/to/**configs**/folder/in/telemac*

2. *TELEMAC_CONFIG_NAME= Name of Telemac compiler bash script .sh **pysource.template.sh** (i.e. pysource.gfortranHPC.sh).*

3. *HBCenv_DIR=/full/path/to/HBCenv*

**activateTM.sh**: Bash file that activates Telemac.
Modify *TELEMAC_CONFIG_DIR=* and *TELEMAC_CONFIG_NAME=* as mentioned above. 

**Tip:** Make sure to test a single Telemac simulation from telemac/examples/. You can refer to Telemac Installation Guide if help needed at: [OpenTelemac.org](http://wiki.opentelemac.org/doku.php?id=installation_on_linux)

### HBCenv
Folder containing the Python virtual environment. As explained before, this folder has the required python libraries to run the code. 

### HyBayesCal
Bayesian Calibration Package. In this folder you will find the following python scripts: 

#### **config.py**
Python script that contains all the necessary file paths and variables. Change these according to the following comments:

1. *input_worbook_name =* Name of *.xlsx file containing user input parameters including the whole path (“home/… /… /HyBayesCal-pckg/use-case-xlsx/*.xlsx”)
2. *activateTM_path =* Path to the Telemac activation file (“home/… /… /HyBayesCal-pckg/env-scripts/activateTM.sh”)
3. *results_filename_base =* Write this according to how it is written in the .cas base file. Do not add the extension. 
4. *output_excel_file_name=* Choose a name for the **.xlsx output file which is saved in auto-saved-results.

#### **file_creator.py**
Python script that has two functions: 

1.	**cas_creator:** Creates the required number .cas files based on a standard (base) .cas file. For this project,  .cas files are created based on random friction coefficients with a fixed range of values extracted from the input parameters excel file ***.xlsx from Use-case-xlsx folder. Since every .cas file and calibration parameter might be different, the code block denoted as : (## This code block should be changed according to the used .cas base file.)  in this python script should be modified according to the .cas base file.

Additionally, returns a list of the random parameters that were used to create the .cas files and a list of the output *.slf files’ paths. 

2.	**sim_output_df:** Creates a data frame of the model outputs and saves it as an excel file in the auto-saved-results. 

#### **filter_plot.py**

Python script that extracts data (calibration quantity) from the model outputs dataframe for specific nodes where measured data is available. 
Python script that plots the values of the calibration quantity for the calibration nodes.  

#### **log_functions.py**
Python scripts that logs the actions to a logfile (logfile.log). The logfile is saved in: *log_directory*  

#### **main.py**
Python script that should be called from Linux terminal. It executes two actions: 
1. **import_input_parameters:** Imports the user input parameters from the input parameter excel file.  
2. **multiple_run_simulation:** Runs Telemac simulations multiple times as the basis for surrogate model construction. 

This script works by executing subprocesses of the file called package_launcher.py.  

#### **package_launcher.py**
This python script owns a class called TelemacSimulations. The methods in this class are:
1. **single_run_simulation:** Runs a single Telemac simulation and extracts the output values as a .txt file of the selected calibration parameter at the last time step of the simulation. 
2.	**import_excel_file:** Imports the necessary user input parameters for Bayesian calibration purposes from the user input parameters excel file **.xlsx.

#### **bayesian_gpe.py**
Contains a class and methods for running a stochastic calibration of a deterministic model by using a Gaussian process emulator (GPE) - based surrogate model that is fitted through Bayesian active learning (BAL).

 
#### **active_learning.py**
Auxiliary functions for the stochastic calibration of model using Surrogate-Assisted Bayesian inversion


* Run Telemac 
  * To run Telemac simulations, ensure that Telemac is installed. For installation instructions, refer to [Telemac](https://opentelemac.org/index.php/installation).
  * To run multiple Telemac simulations, follow these steps:
    * Update (file_name.xlsl)
      1. Locate the .xlsl file at the specified location. 
      2. Choose the number of runs to simulate. 
      3. Update the values of required parameters, editing only the cells highlighted in orange color. ***Warning: Do not edit anything else.***
      4. Save and close the .xlsl file. 
    * Activating Environment: This package employs a virtual environment, with the activation script named `activateHBCtelemac.sh`. To activate this environment:
      1. Navigate to the directory containing the activation script:
       ```
       cd modeling/hybayescalpycourse/env-scripts
       ```
      2. Press Enter to execute the command.
      3. Activate the environment using:
       ```
       source activateHBCtelemac.sh
       ```

Text to be updated below this:-
*  python (filename) 
* Mesh file (`casename.slf`)
* Boundary conditions file (`casename.cli`)
* Output file (`case output.slf`)



## Data
### Input .xlsx file
Before executing the code, ensure you have the input data in an Excel (.xlsx) file. Modify this file according to the instructions provided. It should contain all the necessary parameters for running the simulation. At the end of the column, you'll find hints for specific parameters (e.g., Simulation path - hint: Copy the path from the file explorer). The results of the simulation will be stored in a sub-folder named "auto-results".


|PARAMETER                                        | VALUE                                                     | TYPE       |
|-------------------------------------------------|:----------------------------------------------------------|-----------:|
| Name of TELEMAC steering file (.cas)            | t2d-donau-const-1.cas                                     |     string |
| Name of Gaia steering file (.cas, optional)     |                                                           |     string |
| Simulation path                                 |/home/amintvm/modeling/hybayescalpycourse/examples/donau/  |     string |
| TELEMAC type (tm_xd)                            | Telemac2d                                                 |     string |
| Number of CPUs                                  | 2                                                         |        int |
| .....                                           | ....                                                      |        ... |
| ......                                          | ......                                                    |        ... |


***
## Code Diagram
![UML]
### Brief Overview of the Components
* This package uses the python package [link of HBC github]
* ```main.py```
* ```file_creator.py``` contain 2 methods 
* ```plot.py```
* ```log.py```
* ```package_launcher.py``` contain a custom class ```TelemacSimulations```. This class contains 2 methods and 4 magic methods

## Documentation of Functions and Classes

### main.py


---

### file_creator.py
* This file consists ```cas_creator()``` abcd ```sim_output()```

---

### plot.py
* This file consists 


---


### package_launcher.py
 This file consists 

---

### log.py
 This file consists 

---



# Author 
* Andres
* Abhishek 

# References
https://hydro-informatics.com/


# License
This project is licensed under the GNU - see the LICENSE.md file for details- TBC
