from typing import Any
from src.core.addon import Addon


class WebpToPNG(Addon):
    def __init__(self):
        super().__init__()

    def init(self, context: Any):
        print("Hello world!", context)


ADDON_CLASS = WebpToPNG
