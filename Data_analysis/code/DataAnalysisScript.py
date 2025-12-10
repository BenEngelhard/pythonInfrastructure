import pandas as pd
import os

class DataAnalyzer:
    def __init__(self, filepath):
        self.data_file_path = filepath

    def analyze_data(self):
        # Read the CSV file into a DataFrame
        df = pd.read_csv(self.data_file_path, delimiter=',')

        # Ensure numeric conversion for specified columns
        columns_to_convert = ['Reward', 'Center Reward', 'Opponent Reward', 'Opponent Center Reward']
        for col in columns_to_convert:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # Filter the DataFrame to include only rows where "Trial Validity" is "Completed Trial"
        df_completed_trials = df[df["Trial Validity"] == "Completed Trial"]

        # Calculate total_reward for completed trials
        total_reward = df_completed_trials[["Reward", "Center Reward"]].sum().sum()

        # Count the number of 'C' and 'D' choices within completed trials
        num_c_choices_completed = df_completed_trials[df_completed_trials['Mouse Choice'] == 'C'].shape[0]
        num_d_choices_completed = df_completed_trials[df_completed_trials['Mouse Choice'] == 'D'].shape[0]

        # The total number of completed trials for accurate percentage calculation
        total_completed_trials = df_completed_trials.shape[0]

        # Calculate the percentages and ratios of 'C' and 'D' choices based on completed trials
        percentage_c_completed = (num_c_choices_completed / total_completed_trials) * 100 if total_completed_trials > 0 else 0
        percentage_d_completed = (num_d_choices_completed / total_completed_trials) * 100 if total_completed_trials > 0 else 0
        ratio_c_to_d = num_c_choices_completed / num_d_choices_completed if num_d_choices_completed > 0 else float('inf')
        ratio_d_to_c = num_d_choices_completed / num_c_choices_completed if num_c_choices_completed > 0 else float('inf')

        # Calculate mean reward and other metrics
        reward_mean = total_reward / total_completed_trials if total_completed_trials > 0 else 0
        reward_to_be_delivered = 1.5 * total_completed_trials - total_reward
        mean_reward_by_opponent_choice = df_completed_trials.groupby('Opponent Choice')['Reward'].mean()
        average_time_to_make_decision = df_completed_trials['Time to Make Decision'].mean()
        average_time_to_return_to_center = df_completed_trials['Time to Return to Center'].mean()

        # Current date for the analysis results
        current_date = pd.Timestamp.now().strftime("%Y%m%d")

        # Return the analysis results as a dictionary
        analysis_results = {
            "Date": current_date,
            "Num trials": total_completed_trials,
            "Mean Reward": reward_mean,
            "Total Reward": total_reward,
            "Water to be given": reward_to_be_delivered,
            "Mean Reward by Opponent": mean_reward_by_opponent_choice.to_dict(),
            "Average Time to Make Decision": average_time_to_make_decision,
            "Average Time to Return to Center": average_time_to_return_to_center,
            "Number of C Choices": num_c_choices_completed,
            "Number of D Choices": num_d_choices_completed,
            "Percentage of C Choices": percentage_c_completed,
            "Percentage of D Choices": percentage_d_completed,
            "Ratio of C to D Choices": ratio_c_to_d,
            "Ratio of D to C Choices": ratio_d_to_c,
        }

        return analysis_results

    def save_results_to_file(self, results):
        current_datetime = pd.Timestamp.now()
        current_date = current_datetime.strftime("%Y%m%d")

        # Add the date to the results
        results_with_date = results.copy()
        results_with_date['Date'] = current_date

        # Extract the directory path from the current data file path and replace subdirectory
        directory_path = os.path.dirname(self.data_file_path)
        analysis_directory_path = directory_path.replace('data_from_trials', 'data_analysis_results')

        # Ensure the analysis directory exists
        os.makedirs(analysis_directory_path, exist_ok=True)

        # Define the file path for results
        result_file_path = os.path.join(analysis_directory_path, 'results.csv')
        #result_file_path=opfile
        # Check if the file exists
        if not os.path.isfile(result_file_path):
            # Create a new DataFrame with the results and write to a new CSV file
            pd.DataFrame([results_with_date]).to_csv(result_file_path, index=False)
        else:
            # If the file exists, append the new results as a new row
            pd.DataFrame([results_with_date]).to_csv(result_file_path, mode='a', header=False, index=False)

        return result_file_path