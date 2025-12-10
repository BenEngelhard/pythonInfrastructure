import Data_analysis.FileUtilities as fUtile
from Data_analysis.LoggerABC import BaseLogger

class TrialLogger(BaseLogger):
    def __init__(self, oppid):
        super().__init__(1)
        self.csv_file_path = fUtile.get_file_path(oppid) + '_triallog.csv'

    def start_logging(self):
        header = ["Trial Number", "Trial Validity", "Self Decision", "Opponent Decision", "Reward",
                  "Center Reward", "Trial Start Time", "Time to Make Decision", "Time to Return to Center"]
        self._create_file(header)

    def log_data(self, trial_number, trial_validity, decision, opponent_decision, reward,
                 center_reward, start_time, time_to_make_decision, time_to_return_to_center):
        data = [trial_number, trial_validity, decision, opponent_decision, reward,
                center_reward, start_time, time_to_make_decision, time_to_return_to_center]
        self._log_data(data)

