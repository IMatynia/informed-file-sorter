import os.path
import pickle

DEFAULT_CONFIG_FOLDER = "./config"


class UserConfig:
    def __init__(self, config_folder_path: str = DEFAULT_CONFIG_FOLDER):
        self._config_folder_path = config_folder_path
        if os.path.exists(config_folder_path) and os.path.isdir(config_folder_path):
            pass
        elif os.path.exists(config_folder_path):
            raise Exception("Config folder must be a folder")
        else:
            os.mkdir(config_folder_path)

    def load_config(self, identifier: str):
        conf_file = f"{identifier}.cfg"
        unpickled = None
        with open(os.path.join(self._config_folder_path, conf_file), "rb") as conf_file_handle:
            unpickled = pickle.load(conf_file_handle)

        return unpickled

    def save_config(self, identifier: str, data):
        conf_file = f"{identifier}.cfg"
        with open(os.path.join(self._config_folder_path, conf_file), "wb") as conf_file_handle:
            pickle.dump(data, conf_file_handle)

    def check_for_changes(self, identifier: str, data):
        # TODO: check if config changed, return bool
        pass
