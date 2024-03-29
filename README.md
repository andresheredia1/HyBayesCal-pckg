

# "Advances" on a Python Package for Bayesian Calibration from Telemac Simulations

## Table of Contents

1. [Project's name](##Projects-name)
2. [Project purpose/description](#Project-purposedescription)
3. [Motivation](#Motivation)
4. [Goal](#Motivation)
5. [Package requirements](#Package-requirements)
6. [Code diagram UML](#Code-Diagram)
7. [Installation and run a project](#Installation-and-running-a-project)
8. [Package Folders and Files](#Package-Folders-and-Files)
9. [Steps to run the package ](#Steps-to-run-the-package )

***
# Authors 
Group name: AAA
* Andres Heredia Hidalgo
* Abhishek, Abhishek 
  
## Project's name
"Advances" on a Python package for Bayesian calibration from Telemac Simulations

## Project purpose/description
This projects aims to make significant development and contribution on creating a Bayesian Calibration package in Python using (this time) numerical simulations in Telemac 2D. Bayesian calibration techniques require a huge number of model simulations to perform statistical analysis in light of measured data. This is ,in fact, unfeasible when running numerical models may requiere several hours just for one realization. To make this possible, surrogate models (reduced models) are constructed as a first step with only __a few number of model realizations__. In this context, the main purpose relies on the creation of a package which could be able to run multiple simulations of Telemac as the basis of a subsequent surrogate model construction. 

## Motivation

* Extracting the required data such as user input parameters for calibration purposes from a unique Excel file .xlsx.
* Automating the process of running Telemac simulations the requiered times to construct a surrogate model.
* Extending the use of the package with other hydrodyamic numerical softwares. 
 

## Goal 
Create a package which is able to run multiple simulations of Telemac from a user input .xlsx sheet. A compiled matrix of desired model outputs will serve as the basis for a surrogate model construction to perform Bayesian calibration.

The project focuses on three main tasks:
* Running a Telemac model through Python several times as a baseline to construct a surrogate model for calibration purposes.
* Managing simulation output files .slf to extract relevant data for calibration purposes.
* Performing statistical analysis from the data obtained from the Telemac output files .slf

The full package is available from: **GitHub Repository URL**
```
https://github.com/andresheredia1/HyBayesCal-pckg.git
```

## Package requirements
To use this Python package, we have decided to use a Linux Mint operating system which is a popular and user-friendly Linux distribution. One of the main reasons why the package runs in Linux is because Telemac is primarily developed and tested on Linux-based systems. It gives us the flexibility for configuring the environment and optimizing settings for Telemac simulations while providing a powerful command-line interface, which is well-suited for running batch simulations and automating tasks which improves the productivity of the code when managing large data sets. The creation of a virtual machine with the following characteristics is required:

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

## Code Diagram

![UML Diagram](images/figure7.png)

## Brief Overview of the Package Components
* This package uses the python package [HyBayesCal-pckg](https://github.com/andresheredia1/HyBayesCal-pckg.git)
* ```main.py``` contains 2 methods and log action. This is a stand-alone python script.
* ```config.py``` contains basic and global libraries along with the desired file paths used in project.
* ```file_creator.py``` contains 2 functions to edit `.cas` files and export the simulations outputs Dataframe to `.xlsx`. 
* ```plot.py``` contains a class `PlotGraph` and 5 methods to read `.txt.`, `.xslx` and plot the graphs. 
* ```log_functions.py``` contains a method `log_action` and a submethod for wrapper function.
* ```package_launcher.py``` contains a custom class ```TelemacSimulations```. This class contains 2 methods and 4 magic methods


## Installation and running a project 
***
To use this package, ensure that the previously mentioned software and Python libraries are installed:
* Upon the initial launch of the VM, the first essential task is to update the system (which should be performed periodically):
  * Open Terminal.
  * Enter the command: `sudo apt update`
  * Execute: `sudo apt-get full-upgrade`.
  * Conclude with: `sudo apt autoremove` to remove outdated packages.
* If any required software is missing, install it using the command
  ```
  sudo apt-get install app_name
  ``` 
* Conversely, if you need to uninstall a software use the command, (make sure to change the `app_name` with software name)
  ```
  sudo apt-get remove app_name
  ```
Download the [package](https://github.com/andresheredia1/HyBayesCal-pckg.git) and copy it to a desired folder. The download version of the package has some folders and scripts  which are explained in detail in the following lines. 

Once you downloaded the package you will see these folders and files. 

![Package Folders](images/Figure1.png)

The package runs when a python virtual environment with all the requirements is already activated. Thus, the code requires the creation and activation of a Python virtual environment with all dependencies and Python libraries. The downloaded version of the package has already an environment folder called HBCenv, however you can also create a new one called HBCenv with all the necessary requirements shown in the file *requirementsHBCenv.txt*. 

### Creation of HBCenv  
To create HBCenv, navigate to the folder you have copied the package (i.e. HyBayesCal-pckg) using a Linux terminal and create the virtual environment as follows:
```
python3 -m venv HBCenv
```
After creating the environment, activate it by typing:
```
cd HBCenv/bin/activate
```
Once the environment has been activated, install all the requirements according to requirementsHBCenv.txt file. 
```
pip install package_name
```
## Package Folders and Files 
***

### env-scripts
This folder contains the bash `.sh` files to activate Telemac and HBCenv environments, which are necessary to run the package. It is important, that prior to running the package for the first time, to open each file and modify the directories based on your system. 
Within this folder you will find 2 bash .sh files:

* `activateHBCtelemac.sh`: Bash file that activates Telemac and Python environment for the first run. Change the paths according to the following recommendations.
* `TELEMAC_CONFIG_DIR` = /full/path/to/**configs**/folder/in/telemac
* `TELEMAC_CONFIG_NAME` = Name of Telemac compiler bash script `.sh` `pysource.template.sh` (i.e. pysource.gfortranHPC.sh).
* `HBCenv_DIR` = /full/path/to/HBCenv

**`activateTM.sh`**: Bash file that compiles Telemac.
* Modify `TELEMAC_CONFIG_DIR`= and `TELEMAC_CONFIG_NAME`= as mentioned above. 

**Tip:** Make sure to test a single Telemac simulation from telemac/examples/ so it runs properly. You can refer to the [Telemac Installation Guide](http://wiki.opentelemac.org/doku.php?id=installation_on_linux) if help needed on how to run and install Telemac. 

### HBCenv
Folder containing the Python virtual environment. As explained before, this folder holds the required python libraries to run the code.
 
### Simulationxxxx
Folder that should contain the necessary files to run Telemac and a subfolder called *auto-saved-results*. The folder *auto-saved-results* has an empty file that can be deleted once the package has been downloaded. To this point, the package only runs hydrodynamic simulations and one calibration parameter but it can also be implemented to run other Telemac modules and with other calibration parameters.  The folder must also have  the necessary Telemac files .cas, .cli , .slf and others. To test the package, the simulation folder has already a case study `2dsteady.cas`with the additional Tekemac files. (Hint: if the folder *auto-saved-results* is not present after download, create it before running the code).

* `.cas` - Telemac Steering file (2dsteady.cas for this case study),
* `.cli` - Boundary conditions file (boundaries.cli for this case)
* `.slf` - Mesh file (qgismesh.slf for this case) \

The folder should look like this:

![Simulationxxxx](images/Figure4.png)

### HyBayesCal
Bayesian Calibration Package. In this folder you will find the following python scripts:   
***
`config.py`: Python script that contains all the necessary file paths and variables. Change these according to the following comments before the first run:
* `input_worbook_name` = Name of `.xlsx` file containing user input parameters including the whole path (“home/… /… /HyBayesCal-pckg/use-case-xlsx/*.xlsx”)
* `activateTM_path` = Path to the Telemac activation/compiler file (“home/… /… /HyBayesCal-pckg/env-scripts/activateTM.sh”)
* `results_filename_base` = Write this according to how it is written in the `.cas` base file. Do not add the extension. 
* `output_excel_file_name`=` Choose a name for the `.xlsx` output file which is saved in auto-saved-results.
* `log_directory` = Desired path to save the LOGFILE.log
* `node_file_name`= Path to place the .txt file containing the number of nodes where measured data is available.
* `node_file_path`= Path to place the .txt file containing the number of nodes where measured data is available.
* `excel_file_path`= Path were the simulation_outputs.xlsx file is located. This path is the `auto-saved-results` folder path. 
***
`file_creator.py`: Python script that has two functions: 

* `cas_creator`: Creates the required number of `.cas` files based on a standard (base) `.cas` file located in the folder **Simulationxxxx**. The number of `.cas` files depends on the desired number of `Initial full-complexity model runs (init_runs)` retrieved from the input parameters excel file `.xlsx` from **Use-case-xlsx** folder. For this project,  `.cas` files are created for one calibration parameter (e.g.random friction coefficient) from a fixed range of values extracted from the input parameters excel file `.xlsx`. Since every `.cas` file and calibration parameter might be different, the code block denoted as : (## This code block should be changed according to the used `.cas` base file.)  in this python script should be modified according to the `.cas` base file that is currently used in case a different calibration parameter needs to be simulated. 

Additionally, the script returns a list of the random parameters that were used to create the `.cas` files and a list of the output `.slf` files’ paths. 

* `sim_output_df`: Creates a data frame of the model outputs and saves it as an excel file `output_excel_file_name` in the folder **auto-saved-results**. 
***
`plot.py`: Python script that extracts data (calibration quantity) from the model outputs `.xlsx` for specific nodes where measured data are available. Class `PlotGraph` and methods to plot graph for multiple simulation for specific node writen inside the `nodes_input.txt`. The script plots a line graph using method `plot_data` for velocity/Water depth vs Nodes and scatter plot for mean value using method `average`. 
***

`log_functions.py`: Python scripts that logs the actions to a logfile (LOGFILE.log). The logfile is saved in: *log_directory*  
***

`main.py`: Python script that should be called from Linux terminal. It executes two actions: 
* `import_input_parameters`: Imports the user input parameters from the input parameter excel file.  
* `multiple_run_simulation`: Runs Telemac simulations multiple times as the basis for surrogate model construction. 

This script works by executing subprocesses of the file called `package_launcher.py`.  
***

`package_launcher.py`: This python script owns a custom class called `TelemacSimulations`. The methods in this class are:
* `single_run_simulation`: Runs a single Telemac simulation and extracts the output values as a .txt file of the selected calibration parameter at the last time step of the simulation. 
* `import_excel_file`: Imports the necessary user input parameters for Bayesian calibration purposes from the user input parameters excel file `.xlsx`.
***

`bayesian_gpe.py`: Contains a class and methods for running a stochastic calibration of a deterministic model by using a Gaussian process emulator (GPE) - based surrogate model that is fitted through Bayesian active learning (BAL).
***

`active_learning.py`: Auxiliary functions for the stochastic calibration of model using Surrogate-Assisted Bayesian inversion
***

`nodes_input.txt`: File that contains the nodes where measured data are available.  
***

### use-case-xlsx
This folder contains the ***.xlsx file which holds the user input parameters for surrogate model construction and Bayesian Calibration. Before executing the code, ensure you have the correct user input data in this Excel (.xlsx) file. Modify this file according to the instructions provided in the HINT column. It should contain all the necessary parameters for running the simulation. At the end of the column, you will find hints for specific parameters (e.g., Simulation path - hint: Copy the path from the file explorer). The results of the simulation will be stored in a sub-folder named **auto-saved-results**. 

The `.xlsx` file has three main sections to insert data. 
* *TELEMAC*,
* *ACTIVE LEARNING*,
* *DEFINE PRIOR DISTRIBUTIONS*.

For now, the code runs the initial full-complexity model runs according to what is typed in the corresponding cell **Initial full-complexity model runs (init_runs)** and pulls out the model outputs for each run as text **.txt files according to what is chosen in **Calibration quantity 1 (calib_target1)** cell. The parameter BOTTOM is not available at this point because the GAIA module of Telemac is not used however it can be easily implemented to extract those values as well. 

In the following tables you will find the parameters that need to be modified to run this package. The rest of the parameters in the .xlsx file are not yet available. 

                                                              TELEMAC

|        PARAMETER                                |             VALUE                                         |     TYPE   |
|-------------------------------------------------|-----------------------------------------------------------|------------|
| Name of TELEMAC steering file (.cas)            | t2d-donau-const.cas                                       |     string |
| Simulation path                                 |/home/amintvm/modeling/hybayescalpycourse/examples/donau/  |     string |
| TELEMAC type (tm_xd)                            | Telemac2d                                                 |     string |
| Number of CPUs                                  | 2                                                         |        int |
| .....                                           | ....                                                      |        ... |
| ......                                          | ......                                                    |        ... |

                                                           ACTIVE LEARNING

|        PARAMETER                                |             VALUE                                         |     TYPE   |
|-------------------------------------------------|-----------------------------------------------------------|------------|
| ......                                          | ......                                                    |     .......|
| Initial full-complexity model runs (init_runs)  |      4                                                    |        int |
| Calibration quantity 1 (calib_target1)          |VELOCITY or DEPTH                                          |     string |
| .....                                           | ....                                                      |        ... |
| ......                                          | ......                                                    |        ... |

                                                      DEFINE PRIOR DISTRIBUTIONS

|        PARAMETER                                |             VALUE                                         |     TYPE   |
|-------------------------------------------------|-----------------------------------------------------------|------------|
| ......                                          | ......                                                    |     .......|
| FRICTION COEFFICIENT                            |   0.01,0.07                                               |     float  |
| .....                                           | ....                                                      |        ... |
| ......                                          | ......                                                    |        ... |

### images

This folder constains the figures (screen shots) that used to develop the README.md file.  

## Steps to run the package 
1. Since the package runs iteratively several Telemac simulations, you must ensure that Telemac is installed in your computer and properly running. For installation instructions, refer to [Telemac](https://opentelemac.org/index.php/installation). It is important to test one simulation from */home/......../......./telemac-mascaret/examples/telemac2d/* from your telemac folder. 
2. Once you have checked that Telemac runs properly in your system, set all the necessary user input parameters in the **input parameters excel file** located in the folder called: **use-case-xlsx**. Consider the comments in the HINT column. Remember that only the aboved mentioned parameters shown in [use-case-xlsx folder](#use-case-xlsx) are necessary to run the code at this point. Update the values of required parameters, editing only the cells highlighted in orange color. Save and close the .xlsl file 
   
3. Go into **env-scripts** folder and modify the paths of the bash .sh files **activateHBCtelemac.sh** and **activateTM.sh**  as mentioned above in [env-scripts](#env-scripts).
4. Go into HyBayesCal folder and open **config.py**. Modify the variables in this script considering the previously noted recommendations in [config.py](#HyBayesCal).
    
   4.1. Remember that since every `.cas` file and calibration parameter might be different in any simulation, the code block denoted as : (## This code block should be changed according to the used `.cas` base file.)  in this python script **file_creator.py** should be modified according to the `.cas` base file that is currently being used. This block of code replaces the desired calibration parameter by random values based on the range shown in the user input excel file.
   
5. Go into `nodes_input.txt` and mark the required or knows nodes on your grid where measured data is available. These nodes will be used for Bayesian Calibration purposes. 
6. Activating Environments: Open a Linux terminal, navigate to **env-scripts** folder and activate for the first time both the Python virtual environment *HBCenv* and Telemac compiler bash script *pysource.template.sh* by typing:
       ```
       source activateHBCtelemac.sh
       ```
   A message like this will show up:
    ```
   > Loading HBCenv...
    **Success**
   > Loading TELEMAC config...
    **Success**
   ```
7. Runing the code: In the same terminal navigate to the folder HyBayesCal where all the required python scripts are and run the **`main.py`** script.
   ```
    python main.py
    ```
 ![Running main.py](images/Figure3.png)
 
8. After completing to run the code, inside the simulation folder **simulationxxx** you will find the required number of **.cas files along with a run_launcher python script that can be deleted after completion. 

![simulationxxxx folder](images/Figure5.png)

9. Similarly, in the **auto-saved-results** folder you will find the `.slf`, `.txt` and `.xlsx`,  output files from the Telemac simulations and 2 graphs `data.jpg` and `average_plot.jpg`. An image of how it looks like is shown:
![auto-saved-results](images/Figure6.png)

An example of how the graphs look like (for one model run) are presented as follows: 

![data](images/figure8.jpg)  

![average_plot](images/figure9.jpg)  

An excel file with the model outputs at all nodes and at the last time step is saved in the folder **auto-saved-results**

![simulation_outputs.xlsx](images/Figure10.png) 


# References
* https://hydro-informatics.com/
* http://www.opentelemac.org/
* https://github.com/eduardoAcunaEspinoza/surrogated_assisted_bayesian_calibration.git

# License
This project is licensed under the GNU.
