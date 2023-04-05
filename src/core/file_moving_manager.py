import logging
import os
import re
from typing import Optional


class FileMovingManager:
    def __init__(self, default_filter: str = ".*"):
        self._current_source_folder_path = None
        self._source_files = []
        self._regex_filter = default_filter

        self._destination_folder_paths = []
        self._file_assignments = {}

    def refresh_sources(self):
        self.set_current_source(self._current_source_folder_path)

    def get_regex_filter(self) -> str:
        return self._regex_filter

    def set_regex_filter(self, new_regex: str):
        self._regex_filter = new_regex

    def add_assignment(self, file_path: str, new_folder_path: str):
        self._file_assignments[file_path] = new_folder_path

    def get_assignment(self, file_path: str) -> Optional[str]:
        if file_path in self._file_assignments:
            return self._file_assignments[file_path]
        else:
            return None

    def get_file_on_index(self, index) -> str:
        return self._source_files[index]

    def set_file_on_index(self, index, file_path):
        self._source_files[index] = file_path

    def get_all_assignments(self) -> dict:
        return self._file_assignments

    def add_destination(self, folder_path: str):
        self._destination_folder_paths.append(folder_path)

    def remove_destination(self, folder_path_to_remove: str):
        # check if the folder is used
        for file_path in self._file_assignments:
            if self._file_assignments[file_path] == folder_path_to_remove:
                raise Exception(f"{file_path} is assigned to this folder!")
        self._destination_folder_paths.remove(folder_path_to_remove)

    def set_current_source(self, source_folder_path: Optional[str]):
        if not source_folder_path:
            self._source_files = []
            self._current_source_folder_path = None
        elif os.path.isdir(source_folder_path):
            self._source_files = [os.path.join(source_folder_path, file_path) for file_path in
                                  os.listdir(source_folder_path)]

            self._current_source_folder_path = source_folder_path
        else:
            raise Exception("Invalid source")

        def regex_filter(path):
            return bool(re.match(self._regex_filter, path))

        self._source_files = list(filter(regex_filter, self._source_files))

    def apply_assignments(self):
        for file_path in self._file_assignments:
            base_name = os.path.basename(file_path)
            new_file_path = os.path.join(self._file_assignments[file_path], base_name)
            try:
                os.rename(file_path, new_file_path)
            except FileExistsError:
                logging.error(f"Could not move {file_path} to {new_file_path}")
                raise

    def get_all_files_in_current_source(self) -> list:
        return self._source_files

    def get_n_of_source_files(self):
        return len(self._source_files)

    def get_all_destinations(self):
        return self._destination_folder_paths

    def remove_assignment(self, file_path: str):
        self._file_assignments.pop(file_path)

    def clear_assignments(self):
        self._file_assignments.clear()
