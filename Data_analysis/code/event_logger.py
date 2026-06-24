import Data_analysis.FileUtilities as fUtile
from Data_analysis.LoggerABC import BaseLogger

import pandas as pd


class EventLogger(BaseLogger):
    def __init__(self, oppid):
        super().__init__(5)
        self.event_number = 0  # Initialize event number
        self.csv_file_path = fUtile.get_file_path(oppid) + '_eventlog.csv'
        self.temp_data = []  # Temporary storage for events to calculate Time in State later

    def start_logging(self):
        header = ["Trigger", "Trial Number", "State", "Location", "Time"]
        self._create_file(header)

    def log_data(self, trigger, trial_number, state, location, time):
        data = [trigger, trial_number, state, location, time]
        self._log_data(data)


'''
        Anushka's old code
        ------------------
        
        # Assuming 'time' is in a format that can be converted to datetime directly
        time = pd.to_datetime(time)

        # Add data to temporary storage
        self.temp_data.append([trial_number, event, time, self.event_number, None])  # None for Time in State for now

    def finalize_logging(self):
        # Convert temp_data to DataFrame
        df = pd.DataFrame(self.temp_data, columns=["Trial Number", "Event", "Time", "Event Number", "Time in State"])

        # Calculate 'Time in State' now that we have all data
        df['Next Time'] = df.groupby('Event Number')['Time'].shift(-1)
        df['Time in State'] = (df['Next Time'] - df['Time']).dt.total_seconds()
        df = df.dropna(subset=['Time in State'])  # Drop rows where 'Time in State' cannot be calculated

        # Drop the 'Next Time' column as it's no longer needed
        df.drop(columns=['Next Time'], inplace=True)

        # Save the DataFrame to CSV
        df.to_csv(self.csv_file_path, index=False)

        print(f"Event logging finalized and saved to {self.csv_file_path}")
'''