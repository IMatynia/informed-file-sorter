class Addon:
    def __init__(self, context: "MainWindow"):
        self._addon_info = {}
        self._context: "MainWindow" = context


    @classmethod
    def init(self):
        pass

    @classmethod
    def unload(self):
        pass

    def get_info(self):
        return self._addon_info
