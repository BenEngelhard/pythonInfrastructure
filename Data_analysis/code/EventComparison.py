import os
import pandas as pd
import numpy as np

class EventComparator:
    def __init__(self, directory, latest_csv_path):
        self.directory = directory
        self.latest_csv_path = latest_csv_path

    @staticmethod
    def process_events(df):
        grouped = df.groupby('Trial Number')['Event'].apply(list)
        event_sets = grouped.apply(set)
        return event_sets

    @staticmethod
    def jaccard_similarity(set1, set2):
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union != 0 else 0

    @staticmethod
    def load_csv(file_path):
        return pd.read_csv(file_path)

    def compare_with_all(self):
        latest_df = self.load_csv(self.latest_csv_path)
        latest_event_sets = self.process_events(latest_df)

        # Get the current date
        current_date = pd.Timestamp.now().strftime("%Y%m%d")

        # Initialize a list for headers and a corresponding list for the scores
        headers = ['date']
        scores = [current_date]

        # Calculate Jaccard scores and populate the headers and scores lists
        for csv_file in os.listdir(self.directory):
            if csv_file.endswith('.csv') and os.path.join(self.directory, csv_file) != self.latest_csv_path:
                file_name = csv_file.replace('.csv', '')
                headers.append(file_name)
                df = self.load_csv(os.path.join(self.directory, csv_file))
                event_sets = self.process_events(df)
                min_trials = min(len(latest_event_sets), len(event_sets))
                jaccard_scores = [self.jaccard_similarity(latest_event_sets[i], event_sets[i]) for i in
                                  range(min_trials)]
                average_score = np.mean(jaccard_scores)
                scores.append(average_score)

        # Create a DataFrame with one row of scores, using the headers list
        scores_df = pd.DataFrame([scores], columns=headers)

        return scores_df

    def save_scores(self):
        scores_df = self.compare_with_all()



        # Extract the base directory path from the provided output_csv_path
        directory_path = os.path.dirname(self.latest_csv_path)

        # Define the new directory path for saving comparison scores
        comparison_directory_path = directory_path.replace('event_data_from_trials', 'comparison_event_data')

        # Ensure the comparison directory exists
        os.makedirs(comparison_directory_path, exist_ok=True)

        # Define the full path for the scores CSV file within the comparison directory
        scores_file_path = os.path.join(comparison_directory_path, f'comparison_scores.csv')

        # Save the DataFrame to the CSV file
        scores_df.to_csv(scores_file_path, index=False)

        print(f"Event analysis saved to {scores_file_path}")
        return scores_file_path