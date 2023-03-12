class FileMovingManager:
    def __init__(self):
        self._current_source_folder_path = None
        self._source_files = []

        self._current_destination_folder_paths = []
        self._file_assignments = {}

    def add_assignment(self, file_path: str, new_folder_path: str):
        self._file_assignments[file_path] = new_folder_path

    def get_assignment(self, file_path: str) -> str:
        return self._file_assignments[file_path]

    def get_file_on_index(self, index) -> str:
        return self._source_files[index]
