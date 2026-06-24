import csv
from abc import ABC, abstractmethod
import os


class BaseLogger(ABC):
    def __init__(self, buffer_size):
        self.csv_file = None
        self.csv_file_path = None
        self.csv_writer = None
        self.rows_buffer = []
        self.rows_buffer_size = buffer_size


    @abstractmethod
    def start_logging(self):
        pass

    def _log_data(self, data):
        self.rows_buffer.append(data)
        if len(self.rows_buffer) == self.rows_buffer_size:
            self._write_data()
            self.rows_buffer = []

    def _write_data(self):
        with open(self.csv_file_path, 'a', newline='') as csvfile:
            self.csv_writer = csv.writer(csvfile)
            self.csv_writer.writerows(self.rows_buffer)

    def _create_file(self, header):
        with open(self.csv_file_path, 'w', newline='') as csvfile:
            self.csv_writer = csv.writer(csvfile)
            self.csv_writer.writerow(header)
        print(f"Logging started, file created at: {self.csv_file_path}")

    def finalize_logging(self):
        if len(self.rows_buffer) != 0:
            self._write_data()

