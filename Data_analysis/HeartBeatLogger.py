import infrastructure.Data_analysis.FileUtilities as fUtile
from infrastructure.Data_analysis.LoggerABC import BaseLogger

class HeartBeatLogger(BaseLogger):
    def __init__(self):
        super().__init__(300)
        self.csv_file_path = fUtile.get_file_path(0) + '_heartbeat.csv'

    def start_logging(self):
        header = ['Time Stamp', 'Dropped Frame']
        self._create_file(header)

    def log_data(self, hb_time, dropped_frames):
        self._log_data([hb_time, dropped_frames])

