import logging
import threading
import os
from datetime import datetime
from time import sleep
import pathlib

from Tests.Utils.logging.LogNames import LogNames


# Singleton metaclass to ensure only one instance of Logger is created.
class SingletonType(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]



class Logger:
    def __init__(self, name=__name__, level=logging.DEBUG, log_file_name: LogNames =LogNames.TOKEN_LOGS):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.log_file_name =f"{log_file_name.value}.log"
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Avoid adding multiple handlers if already configured.
        if not self.logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

            today_report_folder=self.get_today_execution_report_folder()

            file_handler = logging.FileHandler(f"{today_report_folder}/{self.log_file_name}")
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)


    def get_last_folder_alphabetically(self, directory):
        """
        Get last folder of a directory by alphabetical order
        Args:
            directory: SO path to the folder
        Returns:
            The last folder of the list
        """
        # Get a list of all folders in the directory
        folders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]

        # Sort the folders alphabetically
        folders.sort()

        # Return the last folder in the sorted list, or None if no folders exist
        return folders[-1] if folders else None

    def get_today_execution_report_folder(self):
        """

        Returns:
            Scriptless report folder for the current day

        """
        current_time = datetime.now()
        current_time_str = current_time.strftime('%d-%m-%Y')
        folder_path =f"Tests/static/reports/{current_time_str}/"
        pathlib.Path(folder_path).mkdir(parents=True, exist_ok=True)
        return folder_path

    def get_logger(self):
        return self.logger