from typing import Any

class Addon:
    def __init__(self):
        self._addon_info = {}

    @classmethod
    def init(self, context: Any):
        pass

    @classmethod
    def unload(self, context: Any):
        pass

    def get_info(self):
        return self._addon_info
