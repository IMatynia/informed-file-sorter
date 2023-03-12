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

    def reload_addons(self):
        addon_modules = os.listdir(self._addon_folder)

        for path in addon_modules:
            name, extension = os.path.splitext(path)
            name = os.path.basename(name)
            if extension == ".py" and name != "__init__":
                logging.info(f"Loaded addon {name}")
                module = importlib.import_module(f"addons.{name}")
                try:
                    self._all_addons[name] = getattr(module, "ADDON_CLASS")()
                    self._all_addons[name].init(self._context)
                except AttributeError:
                    logging.warning(f"Addon {name} is missing its addon class")

    def unload_addons(self):
        for addon_name in self._all_addons:
            self._all_addons[addon_name].unload(self._context)
