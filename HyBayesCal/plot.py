from config import *

class PlotGraph:
    """
    Author - Abhishek
    A class for plotting and analyzing data obtained from a text file and an Excel file.

    Attributes:
        file_path (str): The path where the files are located.
        file_name (str): The name of the Excel file containing the data.
        df_outputs (DataFrame): DataFrame to store the data read from the Excel file.
    """
    
    def __init__(self, file_path, file_name):
        self.file_path = file_path
        self.file_name = file_name
        self.df_outputs = None  # Initialize df_outputs attribute

    def read_txt(self):
        """
        Reads node values from a text file.

        Returns: list or None: A list of node values if the file is found, else None.
        """
        
        try:
            # Read node values from nodes_input.txt file
            with open(os.path.join(node_file_path, node_file_name), "r") as f:
                nodes = [int(line.strip()) for line in f if line.strip()]  # Skip empty lines
            return nodes
        except FileNotFoundError:
            print("Nodes input file not found.")
            return None

    def read_excel_file(self):
        """
        Reads data from an Excel file and stores it in a DataFrame.
        """
        
        try:
            # Read DataFrame from Excel file
            self.df_outputs = pd.read_excel(os.path.join(self.file_path, self.file_name))
        except Exception as e:
            print(f"An error occurred while reading the Excel file: {str(e)}")

    def plot_data(self):
        """
        Plots the data from the Excel file, with options for customizing the plot.
        """
       
        try:
            nodes = self.read_txt() # Read nodes from text file
            if nodes is None:
                return

            if self.df_outputs is None:
                self.read_excel_file()  # Read Excel file if DataFrame is not yet initialized
            is_velocity = (self.df_outputs < 0).any().any() # Check if any value in the DataFrame is less than 0
            filtered_df = self.df_outputs[self.df_outputs.iloc[:, 0].isin(nodes)] # Filter data based on nodes from nodes_input.txt          
            for i, column in enumerate(filtered_df.columns[1:], start=1): # Plotting each column as a separate line with legend labels
                y_values = filtered_df[column].values
                x_values = filtered_df.iloc[:, 0].values
                label = f'Run {i}'  # Update legend label
                plt.plot(x_values, y_values, label=label, marker='o')
            plt.xlabel('Nodes')  # Use the first column as x-axis label
            plt.ylabel('Velocity' if is_velocity else 'Water Depth')  # Determine y-axis label based on data
            plt.legend()
            plt.gcf().set_size_inches(10, 6)  # Set the size of the graph
            plt.savefig(os.path.join(self.file_path, "data.jpg"))  # Save the plot as a .jpg file
            #plt.show()
            plt.close()
            print("Plotting successful!")

        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def average(self):
        """
        Calculates the average of each column in the Excel data and plots it.
        """
        
        try:
            if self.df_outputs is None:
                self.read_excel_file()  # Read Excel file if DataFrame is not yet initialized
            is_velocity = (self.df_outputs < 0).any().any() # Check if any value in the DataFrame is less than 0
            df_array = self.df_outputs.to_numpy() # Convert DataFrame to NumPy array for indexing
            averages = np.mean(df_array[1:, 1:], axis=0) # Calculate the average of each column 
            num_columns = len(self.df_outputs.columns[1:]) # Determine the number of columns present          
            plt.scatter(np.arange(1, num_columns + 1), averages, marker='o',  # Plotting the averages as scatter plot
                        label=[f'Run {i}' for i in range(1, num_columns + 1)])  # Use scatter plot
            plt.xlabel('Runs')  # Use the first row as x-axis label
            plt.ylabel('Average Velocity' if is_velocity else 'Average Water Depth')  # Label for y-axis
            plt.title('Average Plot')
            plt.legend()  # Show legend with labels based on x-axis values
            plt.gcf().set_size_inches(10, 6)  # Set the size of the graph
            plt.savefig(os.path.join(self.file_path, "average_plot.jpg"))  # Save the plot as a .jpg file
            #plt.show()
            plt.close()
            print("Average plotting successful!")

        except Exception as e:
            print(f"An error occurred: {str(e)}")

