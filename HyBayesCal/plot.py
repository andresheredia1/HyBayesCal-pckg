import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from config import log_directory, output_excel_file_name

class PlotGraph:
    def __init__(self, file_path, file_name):
        self.file_path = file_path
        self.file_name = file_name

    def read_txt(self):
        try:
            # Read node values from nodes_input.txt file
            with open("/home/amintvm/modeling/Simulation/HyBayesCal-pckg-master/HyBayesCal/nodes_input.txt", "r") as f:
                nodes = [int(line.strip()) for line in f if line.strip()]  # Skip empty lines
            return nodes
        except FileNotFoundError:
            print("Nodes input file not found.")
            return None

    def plot_data(self):
        try:
            # Read nodes from text file
            nodes = self.read_txt()
            if nodes is None:
                return

            # Read DataFrame from Excel file
            df_outputs = pd.read_excel(f"{self.file_path}/{self.file_name}")

            # Filter data based on nodes from nodes_input.txt
            filtered_df = df_outputs[df_outputs.iloc[:, 0].isin(nodes)]

            # Plotting each column as a separate line with legend labels from B1, C1, D1, ...
            for i, column in enumerate(filtered_df.columns[1:], start=1):
                y_values = filtered_df[column].values
                x_values = filtered_df.iloc[:, 0].values
                # Ignore values where yi is 0 or smaller
                mask = y_values > 0
                x_values_filtered = x_values[mask]
                y_values_filtered = y_values[mask]
                label = df_outputs.iloc[0, i]  # Get legend label from B1, C1, D1, ...
                plt.plot(x_values_filtered, y_values_filtered, label=label, marker='o')  # Use line plot

            plt.xlabel('Nodes')  # Use the first column as x-axis label
            plt.ylabel('Velocity') # 
            plt.title('Velocity Profile')
            plt.legend()
            plt.savefig(f"{self.file_path}/velocity_profile.jpg")  # Save the plot as a .jpg file
            plt.show()
            print("Plotting successful!")

        except Exception as e:
            print(f"An error occurred: {str(e)}")

# Example usage:
if __name__ == "__main__":
    plot_graph = PlotGraph(log_directory, output_excel_file_name)
    plot_graph.plot_data()
