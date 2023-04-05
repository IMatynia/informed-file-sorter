import importlib
import logging
from typing import Any
from src.core.addon import Addon
import os

DEFAULT_ADDON_FOLDER = "addons"


class AddonLoader:
    def __init__(self, context: Any, addon_folder: str = DEFAULT_ADDON_FOLDER):
        self._all_addons: dict[str, Addon] = {}
        self._addon_folder = addon_folder
        self._context = context

    def load_addons(self):
        self.reload_addons()

    def reload_addons(self):
        addon_modules = os.listdir(self._addon_folder)

        for path in addon_modules:
            name, extension = os.path.splitext(path)
            name = os.path.basename(name)
            if extension == ".py" and name != "__init__":
                module = importlib.import_module(f"addons.{name}")
                try:
                    addon_class = getattr(module, "ADDON_CLASS")
                except AttributeError as e:
                    logging.warning(f"Addon {name} is missing its addon class")
                else:
                    self._all_addons[name] = addon_class(self._context)
                    self._all_addons[name].init()
                    logging.info(f"Loaded addon {self._all_addons[name].get_info()['name']}")


    def unload_addons(self):
        for addon_name in self._all_addons:
            self._all_addons[addon_name].unload()
