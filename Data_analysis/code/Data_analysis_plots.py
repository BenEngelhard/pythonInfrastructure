
import matplotlib
matplotlib.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt
import os


class DataPlotter:
    def __init__(self, filepath, save_directory):
        self.data_file_path = filepath
        self.save_directory = save_directory  # Directly use this directory to save plots
        self.data = None

    def load_data(self):
        """Load data from the CSV file."""
        self.data = pd.read_csv(self.data_file_path, delimiter=',')
        print("Data loaded successfully.")

    def filter_completed_trials(self):
        """Filter the data to include only completed trials."""
        if self.data is not None:
            self.data = self.data[self.data['Trial Validity'] == 'Completed Trial']
            print("Filtered for completed trials.")
        else:
            print("Data is not loaded yet.")

    def save_plot_to_directory(self, filename):
        """Determine the save path for the plot."""
        # Use the specified save directory directly
        plots_directory_path = self.save_directory

        # Ensure the plots directory exists
        os.makedirs(plots_directory_path, exist_ok=True)

        # Define the full file path for the plot
        plot_file_path = os.path.join(plots_directory_path, filename)

        return plot_file_path

    def plot_data(self, column_name, title, ylabel, base_filename):
        """Generic method to plot data and save with a specific filename format."""
        if self.data is not None:
            plt.figure(figsize=(10, 6))
            plt.plot(self.data['Trial Number'], self.data[column_name], marker='o', linestyle='-', color='blue')
            plt.title(title)
            plt.xlabel('Trial Number')
            plt.ylabel(ylabel)
            plt.grid(True)

            # Use pandas to format the filename with the current date
            current_date_str = pd.Timestamp.now().strftime("%Y%m%d-%H%M%S")
            # Ensure base_filename does not include '.png' for proper formatting
            if base_filename.endswith('.png'):
                base_filename = base_filename[:-4]
            formatted_filename = f"{base_filename}_{current_date_str}.png"

            # Save the plot to the specified directory with the formatted filename
            save_path = self.save_plot_to_directory(formatted_filename)
            plt.savefig(save_path)
            plt.close()  # Close the plot figure
            print(f"Plot saved to {save_path}")
        else:
            print("Data is not filtered or loaded yet.")

    def plot_decision_time(self):
        """Plot the time to make decisions."""
        self.plot_data('Time to Make Decision', 'Time to Make Decision for Each Completed Trial',
                       'Time to Make Decision (seconds)', 'time_to_make_decision_plot.png')

    def plot_return_time(self):
        """Plot the time to return to center."""
        self.plot_data('Time to Return to Center', 'Time to Return to Center for Each Completed Trial',
                       'Time to Return to Center (seconds)', 'time_to_return_to_center_plot.png')

